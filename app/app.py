from flask import Flask, render_template, request, flash, redirect, session
import uuid, re, hashlib
from datetime import timedelta

from models import dbConnect

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


# ランディングページ表示
@app.route('/')
def sun_chaser():
    return render_template('login.html')

# 新規登録ページ表示
@app.route('/signup')
def signup():
    return render_template('signup.html')

# 新規登録処理
@app.route('/signup', method=['POST'])
def userSignup():
    user_name = request.form.get('user_name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if user_name == '' or email == '' or password1 == '' or password1 == '':
        flash('全てのフォームに入力してください')
    elif password1 != password2:
        flash('２つのパスワードの値が違っています')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        user_id = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        DBuser = dbConnect.getUser(email)

        if DBuser != None:
            flash('既に登録されています')
        else:
            dbConnect.createUser(user_id, username, email, password)
            UserId = str(user_id)
            session['user_id'] = UserId
            return redirect('/')
    return redirect('/signup')





    


# ログインページ表示
@app.route('/')
def sun_chaser():
    return render_template('login.html')

# ログイン機能

# ログアウト機能

# ユーザー名変更

# 観光地登録

# 日程選択

# 観光地選択

# 天気データ結果表示

# 検索条件保存


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


