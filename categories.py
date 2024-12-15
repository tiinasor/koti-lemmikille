from db import db
from sqlalchemy.sql import text

def get_all_categories():
    sql = text("""
        SELECT 
            categories.id, 
            categories.name, 
            COUNT(listings.id) AS listing_count
        FROM categories
        LEFT JOIN listings ON categories.id = listings.category AND listings.visible = TRUE
        GROUP BY categories.id
        ORDER BY categories.name
    """)
    return db.session.execute(sql).fetchall()

def category_exists(category_id):
    sql = text("SELECT 1 FROM categories WHERE id = :id")
    result = db.session.execute(sql, {"id": category_id}).fetchone()
    return result is not None

def get_category_name(category_id):
    sql = text("SELECT name FROM categories WHERE id = :id")
    return db.session.execute(sql, {"id": category_id}).fetchone()[0]
