from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from flask import session

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

def login(username, password):
    sql = text("SELECT password, id, admin FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user and check_password_hash(user[0], password):
        session["user_id"] = user[1]
        session["username"] = username
        if user[2] == True:
            session["admin"] = True
        return True
    else:
        return False

def logout():
    session.pop("user_id", None)
    session.pop("admin", None)
    