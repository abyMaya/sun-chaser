from flask import abort, app
import pymysql # type: ignore
from util.DB import DB
from app import app

class dbConnect:
    
    def createUser(user_id, user_name, email, password, created_at):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO Users (user_id, user_name, email, password, created_at) VALUES (%s, %s, %s, %s, %s);"
            cur.execute(sql, (user_id, user_name, email, password, created_at))
            conn.commit()
            
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            if cur:
                cur.close()  
            if conn:
                conn.close()


    def getUser(email):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM Users WHERE email=%s;"
            cur.execute(sql, (email,))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            if cur:
                cur.close()  
            if conn:
                conn.close()

    def getUserById(user_id):
        connection = DB.getConnection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Users WHERE user_id = %s"
                cursor.execute(sql, (user_id,))
                user = cursor.fetchone()
                return user
        except Exception as e:
            print(f"Error fetching user: {str(e)}")
            return None
        finally:
            connection.close()

    def updateUser(user_id, new_username):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE Users SET user_name = %s WHERE user_id = %s;"
            cur.execute(sql, (new_username, user_id))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    @staticmethod
    def get_regions():
        conn = None
        cursor = None
        regions = []  # 取得する地域を一つに設定
        try:
            print("Connecting to the database...", flush=True)  # 接続開始のログ
            conn = DB.getConnection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            sql = "SELECT region_id, region_name FROM Regions;"  # SQLクエリ
            print("Executing SQL:", sql, flush=True)  # SQL実行前のログ
            cursor.execute(sql)
            regions = cursor.fetchall()  # 単一の行を取得

            print("Fetched regions:", regions, flush=True)  # 取得した地域を表示

            if not regions:  # 取得したデータが空の場合
                print("No regions found in the database.", flush=True) 
                return []  # Noneを返す

        except pymysql.MySQLError as e:  # MySQL関連のエラーをキャッチ
            print(f"MySQL error: {str(e)}", flush=True)  # エラーメッセージを表示
            abort(500)  # エラーが発生した場合はHTTP 500エラーを返す
        except Exception as e:  # その他のエラーをキャッチ
            print(f"Error fetching regions: {str(e)}", flush=True)  # エラーメッセージを表示
            abort(500)  # エラーが発生した場合はHTTP 500エラーを返す
        finally:
            if cursor:
                cursor.close()  # カーソルを閉じる
            if conn:
                conn.close()  # 接続を閉じる
                
        return [{'region_id': region['region_id'], 'region_name': region['region_name']} for region in regions]  # 複数の地域を返すelse None  # 取得した地域を返す
        
    @staticmethod
    def get_stations(region_id):
        conn = None
        cursor = None
        stations = []
        try:
            print("Connecting to the database...", flush=True)  # 接続開始のログ
            conn = DB.getConnection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            sql = "SELECT station_id, station_name FROM WeatherStations WHERE region_id = %s;"
            cursor.execute(sql, (region_id,))  # region_idを正しく使用
            stations = cursor.fetchall()

        except pymysql.MySQLError as e:  # MySQL関連のエラーをキャッチ
            print(f"MySQL error: {str(e)}", flush=True)  # エラーメッセージを表示
            abort(500)  # エラーが発生した場合はHTTP 500エラーを返す      
                  
        except Exception as e:  # その他のエラーをキャッチ
            print(f"Error fetching regions: {str(e)}", flush=True)  # エラーメッセージを表示
            abort(500)  # エラーが発生した場合はHTTP 500エラーを返す
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return [{'station_id': station['station_id'], 'station_name': station['station_name']} for station in stations]

    def createSpot(spot_name, region_id, station_id, created_at):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO Spots (spot_name, region_id, station_id, created_at) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, (spot_name, region_id, station_id, created_at))
            conn.commit()
            print("データが挿入されました", flush=True)
            
        except Exception as e:
            print(e + 'が発生しています', flush=True)
            abort(500)
        finally:
            if cur:
                cur.close()  
            if conn:
                conn.close()
    
    @staticmethod
    def get_spots():
        conn = None
        cursor = None
        regions = []  # 取得する地域を一つに設定
        try:
            print("Connecting to the database...", flush=True)  # 接続開始のログ
            conn = DB.getConnection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            sql = "SELECT spot_id, spot_name FROM Spots;"  # SQLクエリ
            print("Executing SQL:", sql, flush=True)  # SQL実行前のログ
            cursor.execute(sql)
            spots = cursor.fetchall()  # 単一の行を取得

            print("Fetched spots:", spots, flush=True)  # 取得した地域を表示

            if not spots:  # 取得したデータが空の場合
                print("No spots found in the database.", flush=True) 
                return []  # Noneを返す

        except pymysql.MySQLError as e:  # MySQL関連のエラーをキャッチ
            print(f"MySQL error: {str(e)}", flush=True)  # エラーメッセージを表示
            abort(500)  # エラーが発生した場合はHTTP 500エラーを返す
        except Exception as e:  # その他のエラーをキャッチ
            print(f"Error fetching spots: {str(e)}", flush=True)  # エラーメッセージを表示
            abort(500)  # エラーが発生した場合はHTTP 500エラーを返す
        finally:
            if cursor:
                cursor.close()  # カーソルを閉じる
            if conn:
                conn.close()  # 接続を閉じる
                
        return [{'spot_id': spot['spot_id'], 'spot_name': spot['spot_name']} for spot in spots]  

    def get_sunny_rate(station_id, month):
        conn = None
        cursor = None
        sunny_rate_data = []

        try:
            print(f"Connecting to DB for sunny rate with station_id={station_id}, month={month}", flush=True)

            conn = DB.getConnection()
            cursor = conn.cursor()
            
            sql = """
            SELECT DATE_FORMAT(weather_date, '%%m') AS month, DATE_FORMAT(weather_date, '%%d') AS day, sunny_rate
            FROM WeatherData
            WHERE station_id = %s AND MONTH(weather_date) = %s;
            """

            month_number = month.split('-')[1] if '-' in month else month
            print(f"Executing SQL with parameters: station_id={station_id}, month={month_number}", flush=True)

            cursor.execute(sql, (station_id, month_number))

            sunny_rate_data = cursor.fetchall()

            print("Fetched sunny rate data:", sunny_rate_data, flush=True)

            return sunny_rate_data
        
        except pymysql.MySQLError as e:
            print(f"MySQL error: {str(e)}", flush=True)
            abort(500)
        except Exception as e:
            print(f"Error fetching sunny rate data: {str(e)}", flush=True)
            abort(500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        return sunny_rate_data

    def get_station_id(spot_id):
        conn = None
        cursor = None

        try:
            conn = DB.getConnection()
            cursor = conn.cursor()

            if not conn:
                print("Failed to establish a database connection", flush=True)

            # spot_idに基づいてstation_idを取得するSQL文
            sql = "SELECT station_id FROM Spots WHERE spot_id = %s;"
            print(f"Executing SQL: {sql} with spot_id={spot_id}", flush=True)

            cursor.execute(sql, int(spot_id,))
            result = cursor.fetchone()

            if result:
                print(f"Query Result: {result}", flush=True)
                print(f"Result Type: {type(result)}, Keys: {list(result.keys())}", flush=True)
                return result["station_id"]   # station_idを返す
            else:
                print("No result found for the given spot_id", flush=True)
                return None  # 見つからなかった場合はNoneを返す
        
        except Exception as e:
            print(f"Error getting station_id: {str(e)}", flush=True)
            raise
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_spot_name_by_spot_id(spot_id):
        conn = None
        cursor = None

        try:
            conn = DB.getConnection()
            cursor = conn.cursor()

            if not conn:
                print("Failed to establish a database connection", flush=True)

            # spot_idに基づいてstation_idを取得するSQL文
            sql = "SELECT spot_name FROM Spots WHERE spot_id = %s;"
            print(f"Executing SQL: {sql} with spot_id={spot_id}", flush=True)

            cursor.execute(sql, int(spot_id,))
            result = cursor.fetchone()

            if result:
                print(f"Query Result: {result}", flush=True)
                print(f"Result Type: {type(result)}, Keys: {list(result.keys())}", flush=True)
                return result["spot_name"] 
            else:
                print("No result found for the given spot_id", flush=True)
                return None  # 見つからなかった場合はNoneを返す
        
        except Exception as e:
            print(f"Error getting station_id: {str(e)}", flush=True)
            return None
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()    
    