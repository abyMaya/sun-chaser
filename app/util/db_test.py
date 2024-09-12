from util.db import DB  # DB接続のファイルをインポート

def test_connection():
    try:
        connection = DB.getConnection()  # 接続を試みる
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE();")  # 現在接続中のデータベース名を取得
            db_name = cursor.fetchone()  # 取得したデータをフェッチ
            print(f"Connected to the database: {db_name['DATABASE()']}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    test_connection()  # 実行して接続をテスト
