from flask import Flask, jsonify, render_template, request, flash, redirect, session, app, flash, abort
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

        
# ログアウト機能

# ユーザー名変更

# 観光地登録

# 日程選択

# 観光地選択

# 天気データ結果表示

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


