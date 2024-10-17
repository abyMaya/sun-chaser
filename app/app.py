from flask import Flask, jsonify, render_template, request, flash, redirect, session, app, abort
import uuid, re, hashlib
from datetime import datetime, timedelta

from util.DB import DB
from models import dbConnect
import logging

app = Flask(__name__)

# # Logging configuration
# app.logger.setLevel(logging.DEBUG)

app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


# 新規登録ページ表示
@app.route('/signup')
def signup():
    return render_template('signup.html')

# 新規登録処理
@app.route('/signup', methods=['POST'])
def userSignup():

    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    # # POSTデータの確認
    # app.logger.debug(f"POSTデータ: user_name={user_name}, email={email}, password1={password1}, password2={password2}")


    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if user_name == '' or email == '' or password1 == '' or password2 == '':
        flash('全てのフォームに入力してください')
    elif password1 != password2:
        flash('２つのパスワードの値が違っています')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        user_id = str(uuid.uuid4())
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        created_at = datetime.now()
        DBuser = dbConnect.getUser(email)

        if DBuser != None:
            flash('既に登録されています')
        else:                
            dbConnect.createUser(user_id, user_name, email, password, created_at)
            session['user_id'] = user_id
            return redirect('/')
    return redirect('/signup')   


# ログインページ表示
@app.route('/login')
def login():
    return render_template('login.html')


# ログイン処理
@app.route('/login', methods=['POST'])
def userLogin():
    email = request.form.get('email')
    password = request.form.get('password')

    if email == '' or password == '':
        flash('すべてのフォームに入力してください')
    else:
        user = dbConnect.getUser(email)
        if user is None:
            flash('このユーザーは登録されていません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('パスワードが間違っています')
            else:
                session['user_id'] = user["user_id"] 
                return redirect('/')
    return redirect('/login')

# メインページ表示
@app.route('/')
def main():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    return render_template('serch.html', user_id=user_id)
        
# ログアウト処理
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ユーザー情報表示
@app.route('/profile')
def profile():
    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    
    user = dbConnect.getUserById(user_id)
    if user is None:
        return redirect('/login')
    
    return render_template('setting.html', user=user)

# ユーザー名変更
@app.route('/update-username', methods=['POST'])
def update_username():
    data = request.get_json()
    new_username = data.get('username')

    user_id = session.get("user_id")
    if user_id is None:
        return redirect('/login')
    
    user = dbConnect.getUserById(user_id)
    if user :
        dbConnect.updateUser(user_id, new_username)

    return jsonify(success=True)

# 観光地登録
# Regionsを取得
@app.route('/get-regions', methods=['GET'])
def fetch_regions():
    region = dbConnect.get_regions()  # get_regionsメソッドを呼び出す
    print("Region returned:", region, flush=True)  # 取得した地域のログ
    if region is None:
        return jsonify({'error': '地域の取得に失敗しました'}), 500
    return jsonify(region)  # 地域データをJSON形式で返す

# テスト用
@app.route('/test-get-stations', methods=['GET'])
def test_get_regions():
    print("Testing get_stations function...", flush=True)  # テスト呼び出しのログ
    station = dbConnect.get_stations()  # get_regionsメソッドを呼び出す
    print("Station returned:", station, flush=True)  # 取得した地域のログ
    if station is None:
        return jsonify({'error': '地域の取得に失敗しました'}), 500
    return jsonify(station)  # 地域データをJSON形式で返す

# Stationsを取得
@app.route('/get-stations/<region_id>', methods=['GET'])  # region_idをURLパラメータとして受け取る
def get_stations(region_id):
    stations = dbConnect.get_stations(region_id)  # 引数にregion_idを渡す
    print("Station returned:", stations, flush=True)  # 取得した地域のログ
    if stations is None:
        return jsonify({'error': '気象台の取得に失敗しました'}), 500
    return jsonify(stations)
    

if __name__ == '__main__':
    app.run(debug=True)

# 観光地登録処理
@app.route('/spot-register', methods=['GET', 'POST'])
def spotRegister():
    if request.method == 'GET':
        # フォームを表示するHTMLをレンダリング
        return render_template('setting.html')

    spot = request.form.get('spot')
    location = request.form.get('location')
    station = request.form.get('station')
    
    if spot == '' or location == '' or station == '' :
        flash('全てのフォームに入力してください')
        return redirect('/spot-register')
    
    else:
        created_at = datetime.now()
        dbConnect.createSpot(spot, location, station, created_at)
        return redirect('/')
   
# 日程選択

# 観光地選択
@app.route('/get-spots', methods=['GET'])
def fetch_spots():
    spot = dbConnect.get_spots()  

    print("Spots returned:", spot, flush=True)  

    if spot is None:
        return jsonify({'error': '観光地の取得に失敗しました'}), 500
    return jsonify(spot)  

# 天気データ結果取得
@app.route('/get_sunny_rate', methods=["GET"])
def get_sunny_rate_api():
    spot_id = request.args.get('spot_id')
    month = request.args.get('month')

    if not spot_id or not month:
        return jsonify({"error": "Invalid parameters"}), 400
    
    print(f"Received spot_id: {spot_id}, month: {month}", flush=True)

    sunny_rate_data = dbConnect.get_sunny_rate(spot_id, month)

    if not sunny_rate_data:
        return jsonify({"error": "No data found for the given parameters"}),
  
    print("Sunny rate data:", sunny_rate_data, flush=True) 
    return jsonify(sunny_rate_data)

# 結果ページ表示
@app.route('/result')
def result():
    spot = request.args.get('spot')
    year = request.args.get('year')
    month = request.args.get('month')

    return render_template('result.html', spot=spot, year=year, month=month)




 
# 検索条件保存

# DB接続確認エンドポイント
@app.route('/db-test')
def db_test():
    try:
        connection = DB.getConnection()
        if connection:
            return "DB接続成功"
        else:
            return "DB接続失敗"
    except Exception as e:
        print(e + 'が発生しています')
        return "Error during DB test", 500
    
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


