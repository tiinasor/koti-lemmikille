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

def format_listing(row):
    sex = row[3]
    if sex == "male":
        sex = "Koiras"
    elif sex == "female":
        sex = "Naaras"
    else:
        sex = "Tuntematon"
    years, months = convert_age_months(row[2])
    return {
        "id": row[0],
        "name": row[1],
        "age_months": row[2],
        "sex": sex,
        "location_name": row[4],
        "species_breed": row[5],
        "description": row[6],
        "username": row[7],
        "created_at": row[8].strftime("%d.%m.%Y"),
        "years": years,
        "months": months
    }

def get_listings(query, parameters=None):
    if parameters is None:
        parameters = {}
    result = db.session.execute(query, parameters)
    listings = result.fetchall()
    listings_dict = [format_listing(row) for row in listings]
    return listings_dict

def get_listing(listing_id):
    sql = text("""
        SELECT 
            listings.id,
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
        WHERE listings.visible = TRUE
        AND listings.id = :listing_id
    """)
    return get_listings(sql, {"listing_id": listing_id})[0]

def get_category_listings(category_id):
    sql = text("""
        SELECT 
            listings.id,
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
        AND listings.visible = TRUE
        ORDER BY listings.created_at DESC
    """)
    return get_listings(sql, {"category_id": category_id})

def get_user_listings(user_id):
    sql = text("""
        SELECT 
            listings.id,
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
        WHERE users.id = :user_id 
        AND listings.visible = TRUE
        ORDER BY listings.created_at DESC
    """)
    return get_listings(sql, {"user_id": user_id})

def get_all_listings():
    sql = text("""
        SELECT 
            listings.id,
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
        WHERE listings.visible = TRUE
        ORDER BY listings.created_at DESC
    """)
    return get_listings(sql)

def delete_listing(listing_id, user_id):
    try:
        sql = text("""
            UPDATE listings
            SET visible = FALSE
            WHERE id = :listing_id AND user_id = :user_id
        """)
        db.session.execute(sql, {"listing_id":listing_id, "user_id":user_id})
        db.session.commit()
        return True
    except:
        return False

def admin_delete_listing(listing_id):
    try:
        sql = text("""
            UPDATE listings
            SET visible = FALSE
            WHERE id = :listing_id
        """)
        db.session.execute(sql, {"listing_id":listing_id})
        db.session.commit()
        return True
    except:
        return False
    