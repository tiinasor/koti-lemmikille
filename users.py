from db import db
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import text

def register(username, password, admin):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username,password,admin) VALUES (:username,:password,:admin)")
        db.session.execute(sql, {"username":username, "password":hash_value, "admin":admin})
        db.session.commit()
        return True
    except:
        return False

def user_exist(username):
    sql = text("SELECT username FROM users WHERE username=:username")
    return db.session.execute(sql, {"username":username}).fetchone()
