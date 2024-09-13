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
       
