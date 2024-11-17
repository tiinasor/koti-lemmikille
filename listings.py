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

def convert_age_months(age_months):
    years = int(age_months) // 12
    months = int(age_months) % 12
    return years, months

def get_all_listings(category_id):
    sql = text("""
        SELECT 
            listings.name, 
            listings.age_months, 
            listings.sex, 
            locations.name AS location_name,
            listings.species_breed, 
            listings.description,
            users.username AS username,
            listings.created_at
        FROM listings
        JOIN locations ON listings.location = locations.id
        JOIN categories ON listings.category = categories.id
        JOIN users ON listings.user_id = users.id
        WHERE listings.category = :category_id
    """)

    result = db.session.execute(sql, {"category_id":category_id})
    listings = result.fetchall()
    
    listings_dict = []
    for row in listings:
        sex = row[2]
        if sex == "male":
            sex = "Koiras"
        elif sex == "female":
            sex = "Naaras"
        else:
            sex = "Tuntematon"

        listing = {
            "name": row[0],
            "age_months": row[1],
            "sex": sex,
            "location_name": row[3],
            "species_breed": row[4],
            "description": row[5],
            "username": row[6],
            "created_at": row[7].strftime("%d.%m.%Y")
        }
        years, months = convert_age_months(listing["age_months"])
        listing["years"] = years
        listing["months"] = months
        listings_dict.append(listing)

    return listings_dict
