from db import db
from sqlalchemy.sql import text

def add_listing(name, age_months, sex, location, category, species_breed, description, user_id):
    try:
        sql = text("INSERT INTO listings (name, age_months, sex, location, category, species_breed, description, user_id) VALUES (:name, :age_months, :sex, :location, :category, :species_breed, :description, :user_id)")
        db.session.execute(sql, {"name":name, "age_months":age_months, "sex":sex, "location":location, "category":category, "species_breed":species_breed, "description":description, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False
    