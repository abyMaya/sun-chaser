import pymysql

class DB:
    
    def getConnection():
        conn = None
        try:
            conn = pymysql.connect(
            host="db",
            db="SUN_Chaser",
            user="admin",
            password="chaser",
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
            )

            return conn
        
        except Exception as e:
            print(f"getConnectionDB接続エラー: {str(e)}")
            conn.close()

