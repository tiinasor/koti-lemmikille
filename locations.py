from db import db
from sqlalchemy.sql import text

def get_all_locations():
    sql = text("SELECT id, name FROM locations ORDER BY name")
    return db.session.execute(sql).fetchall()

def location_exists(location_id):
    sql = text("SELECT 1 FROM locations WHERE id = :id")
    result = db.session.execute(sql, {"id": location_id}).fetchone()
    return result is not None
