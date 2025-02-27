import hashlib
import re
import uuid
from datetime import datetime, timedelta

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
)
from models import dbConnect

app = Flask(__name__)

app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


# 新規登録ページ表示
@app.route("/signup")
def signup():
    return render_template("signup.html")


# 新規登録処理
@app.route("/signup", methods=["POST"])
def userSignup():
    username = request.form.get("username")
    email = request.form.get("email")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if username == "" or email == "" or password1 == "" or password2 == "":
        flash("全てのフォームに入力してください")
    elif password1 != password2:
        flash("２つのパスワードの値が違っています")
    elif re.match(pattern, email) is None:
        flash("正しいメールアドレスの形式ではありません")
    else:
        user_id = str(uuid.uuid4())
        password = hashlib.sha256(password1.encode("utf-8")).hexdigest()
        created_at = int(datetime.now().timestamp())
        DBuser = dbConnect.getUser(email)

        if DBuser is not None:
            flash("既に登録されています")
        else:
            dbConnect.createUser(
                user_id, username, email, password, created_at
                )
            session["user_id"] = user_id

            return redirect("/")

    return redirect("/signup")


# ログインページ表示
@app.route("/login")
def login():
    return render_template("login.html")


# ログイン処理
@app.route("/login", methods=["POST"])
def userLogin():
    email = request.form.get("email")
    password = request.form.get("password")

    if email == "" or password == "":
        flash("すべてのフォームに入力してください")
    else:
        user = dbConnect.getUser(email)
        if user is None:
            flash("このユーザーは登録されていません")
        else:
            hashPassword = hashlib.sha256(password.encode("utf-8")).hexdigest()
            if hashPassword != user["password"]:
                flash("パスワードが間違っています")
            else:
                session["user_id"] = user["user_id"]

                return redirect("/")

    return redirect("/login")


# メインページ表示
@app.route("/")
def main():
    user_id = session.get("user_id")

    if user_id is None:
        return redirect("/login")

    return render_template("serch.html", user_id=user_id)


# ログアウト処理
@app.route("/logout")
def logout():
    session.clear()

    return redirect("/login")


# ユーザー情報表示（セッティング画面）
@app.route("/profile")
def profile():
    user_id = session.get("user_id")

    if user_id is None:
        return redirect("/login")
    user = dbConnect.getUserById(user_id)
    if user is None:
        return redirect("/login")

    return render_template("setting.html", user=user)


# ユーザー名変更
@app.route("/update-username", methods=["POST"])
def update_username():
    data = request.get_json()
    new_username = data.get("username")
    user_id = session.get("user_id")
    updated_at = int(datetime.now().timestamp())

    if user_id is None:
        return redirect("/login")
    user = dbConnect.getUserById(user_id)
    if user:
        dbConnect.updateUser(user_id, new_username, updated_at)

    return jsonify(success=True)


# 観光地登録
# Regionsを取得
@app.route("/get-regions", methods=["GET"])
def fetch_regions():
    region = dbConnect.get_regions()

    if region is None:
        return jsonify({"error": "地域の取得に失敗しました"}), 500

    return jsonify(region)


# Stationsを取得
@app.route("/get-stations/<region_id>", methods=["GET"])
def get_stations(region_id):
    stations = dbConnect.get_stations(region_id)

    if stations is None:
        return jsonify({"error": "気象台の取得に失敗しました"}), 500

    return jsonify(stations)


# 観光地登録処理
@app.route("/spot-register", methods=["GET", "POST"])
def spotRegister():

    if request.method == "GET":
        return render_template("setting.html")
    spot = request.form.get("spot")
    location = request.form.get("location")
    station = request.form.get("station")

    if spot == "" or location == "" or station == "":
        flash("全てのフォームに入力してください")
        return redirect("/spot-register")

    created_at = int(datetime.now().timestamp())
    user_id = session.get("user_id")

    spot_id = dbConnect.createSpot(spot, location, station, created_at)
    dbConnect.createUserSpot(user_id, spot_id, created_at)

    return redirect("/")


# 観光地選択
@app.route("/get-spots", methods=["GET"])
def fetch_spots():
    spot = dbConnect.get_spots()

    if spot is None:
        return jsonify({"error": "観光地の取得に失敗しました"}), 500

    return jsonify(spot)


# 選択したスポットから気象台名IDを取得
@app.route("/get_station_id", methods=["GET"])
def get_station_id_api():
    spot_id = request.args.get("spot_id")

    if not spot_id:
        return jsonify({"get_station_id_apiでerror": "Invalid spot_id"}), 400
    if not spot_id.isdigit():
        return jsonify({"error": "spot_id must be an integer"}), 400
    spot_id = int(spot_id)
    try:
        station_id = dbConnect.get_station_id(spot_id)
    except Exception as e:
        print(f"Error in get_station_id_api: {str(e)}", flush=True)
        return jsonify({"error": "Internal server error"}), 500

    if not station_id:
        return jsonify(
            {"error": "No station found for the given spot_id"}
            ), 404

    return jsonify({"station_id": station_id})


# 天気データ結果取得
@app.route("/get_sunny_rate", methods=["GET"])
def get_sunny_rate_api():
    spot_id = request.args.get("spot_id")
    month = request.args.get("month")

    if not spot_id or not month:
        return jsonify({"error": "Invalid parameters"}), 400
    try:
        sunny_rate_data = dbConnect.get_sunny_rate(spot_id, month)
    except Exception as e:
        print(f"Error fetching sunny rate data: {str(e)}", flush=True)
        return jsonify(
            {"error": "Server error while fetching sunny rate data"}
            ), 500

    if not sunny_rate_data:
        return (jsonify(
            {"error": "No data found for the given parameters"}
            ),)

    return jsonify(sunny_rate_data)


# 結果ページ表示
@app.route("/result", methods=["GET"])
def result():
    spot_id = request.args.get("spot_id")
    station_id = request.args.get("station_id")
    year = request.args.get("year")
    month = request.args.get("month")

    if not spot_id:
        return jsonify({"error": "spot_id is missing"}), 400
    spot = dbConnect.get_spot_name_by_spot_id(spot_id)
    formatted_month = f"{year}/{month}" if year and month else ""

    return render_template(
        "result.html",
        spot=spot,
        station_id=station_id,
        year=year,
        month=formatted_month,
    )


# 検索ページ表示
@app.route("/serch")
def serch():
    return render_template("serch.html")


# 設定ページ表示
@app.route("/setting")
def setting():
    return render_template("setting.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
