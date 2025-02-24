import pymysql

from flask import abort

from util.DB import DB

class dbConnect:
    
    def createUser(user_id, username, email, password, created_at):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO Users (user_id, username, email, password, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s);"
            cur.execute(sql, (user_id, username, email, password, created_at, None))
            conn.commit()            
        except Exception as e:
            print(f"Error in createUser: {str(e)}")
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
            print(f"Error in getUser: {str(e)}")
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

    def updateUser(user_id, new_username, updated_at):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()            
            sql = "UPDATE Users SET username = %s, updated_at = %s WHERE user_id = %s;"
            cur.execute(sql, (new_username, updated_at, user_id))
            conn.commit()
        except Exception as e:
            print(f"Error in updateUser: {str(e)}")
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
        regions = [] 
        try:
            conn = DB.getConnection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)            
            sql = "SELECT region_id, region_name FROM Regions;"
            cursor.execute(sql)
            regions = cursor.fetchall()

            if not regions:
                print("No regions found in the database.") 
                return []             
        except pymysql.MySQLError as e:
            print(f"MySQLError: {str(e)}")
            abort(500)
        except Exception as e:
            print(f"Error in get_regions: {str(e)}")
            abort(500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
        return [{'region_id': region['region_id'], 'region_name': region['region_name']} for region in regions]
        
    @staticmethod
    def get_stations(region_id):
        conn = None
        cursor = None
        stations = []
        try:
            conn = DB.getConnection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT station_id, station_name FROM WeatherStations WHERE region_id = %s;"
            cursor.execute(sql, (region_id,))
            stations = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"MySQLError: {str(e)}")
            abort(500)                  
        except Exception as e:
            print(f"Error in get_stations: {str(e)}")
            abort(500)
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
            sql = "INSERT INTO Spots (spot_name, region_id, station_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s);"
            cur.execute(sql, (spot_name, region_id, station_id, created_at, None))
            conn.commit()

            spot_id = cur.lastrowid
            return spot_id
        
        except Exception as e:
            print(f"Error in createSpot: {str(e)}")
            abort(500)
        finally:
            if cur:
                cur.close()  
            if conn:
                conn.close()
    
    def createUserSpot(user_id, spot_id, created_at):
        conn = None
        cur = None
        try:
            conn = DB.getConnection()
            cur = conn.cursor()

            sql = "INSERT INTO UsersSpots (user_id, spot_id, created_at, updated_at) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, (user_id, spot_id, created_at, None))
            conn.commit()
        except Exception as e:
            print(f"Error in createUserSpot: {str(e)}")
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
        spots = []
        try:
            conn = DB.getConnection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)            
            sql = "SELECT spot_id, spot_name FROM Spots;"
            cursor.execute(sql)
            spots = cursor.fetchall()

            if not spots:
                return [] 
        except pymysql.MySQLError as e:
            print(f"MySQL error: {str(e)}") 
            abort(500)
        except Exception as e:
            print(f"Error in get_spots: {str(e)}")
            abort(500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
                
        return [{'spot_id': spot['spot_id'], 'spot_name': spot['spot_name']} for spot in spots]  

    def get_sunny_rate(station_id, month):
        conn = None
        cursor = None
        sunny_rate_data = []
        try:
            conn = DB.getConnection()
            cursor = conn.cursor()            
            sql = """
            SELECT DATE_FORMAT(weather_date, '%%m') AS month, DATE_FORMAT(weather_date, '%%d') AS day, sunny_rate
            FROM WeatherData
            WHERE station_id = %s AND MONTH(weather_date) = %s;
            """
            month_number = month.split('-')[1] if '-' in month else month
            cursor.execute(sql, (station_id, month_number))
            sunny_rate_data = cursor.fetchall()

            return sunny_rate_data                
        except pymysql.MySQLError as e:
            print(f"MySQL error: {str(e)}")
            abort(500)
        except Exception as e:
            print(f"Error in get_sunny_rate: {str(e)}")
            abort(500)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_station_id(spot_id):
        conn = None
        cursor = None
        try:
            conn = DB.getConnection()
            cursor = conn.cursor()
            sql = "SELECT station_id FROM Spots WHERE spot_id = %s;"
            cursor.execute(sql, int(spot_id,))
            result = cursor.fetchone()

            if result:
                return result["station_id"]
                         
            return None             
        except Exception as e:
            print(f"Error in get_station_id: {str(e)}")
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
            sql = "SELECT spot_name FROM Spots WHERE spot_id = %s;"
            cursor.execute(sql, int(spot_id,))
            result = cursor.fetchone()

            if result:
                return result["spot_name"]
             
            return None              
        except Exception as e:
            print(f"Error in get_spot_name_by_spot_id: {str(e)}")
            return None        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()    
    