from db import db
from sqlalchemy.sql import text

def get_all_categories():
    sql = text("SELECT id, name FROM categories ORDER BY name")
    return db.session.execute(sql).fetchall()

def category_exists(category_id):
    sql = text("SELECT 1 FROM categories WHERE id = :id")
    result = db.session.execute(sql, {"id": category_id}).fetchone()
    return result is not None
