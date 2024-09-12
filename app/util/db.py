import pymysql

class DB:
    @staticmethod
    def get_connection():
        connection = None
        try:
            connection = pymysql.connect(
                host="db",
                db="SUN_Chaser",
                user="admin",
                password="chaser",
                charset="utf8",
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")
            return connection