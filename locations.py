from db import db
from sqlalchemy.sql import text

def get_all_locations():
    sql = text("SELECT id, name FROM locations ORDER BY name")
    return db.session.execute(sql).fetchall()
