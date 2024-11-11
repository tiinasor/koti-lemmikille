from db import db
from sqlalchemy.sql import text

def get_all_categories():
    sql = text("SELECT id, name FROM categories ORDER BY name")
    return db.session.execute(sql).fetchall()
