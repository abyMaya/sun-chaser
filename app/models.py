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


            
