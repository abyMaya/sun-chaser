from flask import Flask, render_template
import uuid
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
# 新規登録機能

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


