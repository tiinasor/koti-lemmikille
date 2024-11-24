from app import app
from flask import render_template, request, redirect, session
import users
import categories
import locations
import listings

@app.route("/")
def index():
    return render_template("index.html", categories=categories.get_all_categories())

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        admin = request.form["admin"]
        if not username or not password1 or not password2:
            return render_template("register.html", message="Kaikki kentät on täytettävä")
        elif users.user_exist(username):
            return render_template("register.html", message="Käyttäjätunnus on jo käytössä")
        elif len(username) > 20:
            return render_template("register.html", message="Käyttäjätunnus saa olla korkeintaan 20 merkkiä pitkä")
        elif password1 != password2:
            return render_template("register.html", message="Salasanat eivät täsmää")
        elif admin != "True" and admin != "False":
            return render_template("register.html", message="Tuntematon käyttäjärooli")
        elif users.register(username, password1, admin):
            users.login(username, password1)
            return redirect("/")
        else:
            return render_template("register.html", message="Rekisteröityminen epäonnistui")
 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", message="Väärä käyttäjätunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/add_listing", methods=["GET", "POST"])
def add_listing():
    if request.method == "GET":
        if "user_id" not in session:
            return redirect("/")
        return render_template("add_listing.html", categories=categories.get_all_categories(), locations=locations.get_all_locations())
    if request.method == "POST":
        name = request.form["name"]
        age_years = request.form["age_years"]
        age_months = request.form["age_months"]
        age = 12 * int(age_years) + int(age_months)
        sex = request.form["sex"]
        location = request.form["location"]
        category = request.form["category"]
        species_breed = request.form["species_breed"]
        description = request.form["description"]
        age = 12 * int(age_years) + int(age_months)

        errors = []
        if not name:
            errors.append("Nimi on täytettävä")
        if len(name) > 30:
            errors.append("Nimi saa olla korkeintaan 30 merkkiä pitkä")                        
        if int(age_years) < 0 or int(age_years) > 200:
            errors.append("Ikä vuosina on oltava välillä 0-200")
        if int(age_months) < 0 or int(age_months) > 11:
            errors.append("Ikä kuukausina on oltava välillä 0-11")
        if sex != "male" and sex != "female" and sex != "unknown":
            errors.append("Sukupuolen on oltava koiras, naaras tai tuntematon")
        if not locations.location_exists(location):
            errors.append("Virheellinen sijainti")
        if not categories.category_exists(category):
            errors.append("Virheellinen kategoria")
        if len(species_breed) > 50:
            errors.append("Tarkempi laji/rotu saa olla korkeintaan 50 merkkiä pitkä")
        if len(description) > 2000:
            errors.append("Kuvaus saa olla korkeintaan 2000 merkkiä pitkä")

        if len(errors) > 0:
            return render_template("add_listing.html", errors=errors, categories=categories.get_all_categories(), locations=locations.get_all_locations())
        elif listings.add_listing(name, age, sex, location, category, species_breed, description, user_id=session["user_id"]):
            return redirect("/")
        else:
            return render_template("add_listing.html", errors=["Ilmoituksen lisääminen epäonnistui"], categories=categories.get_all_categories(), locations=locations.get_all_locations())

@app.route("/category/<int:category_id>", methods=["GET"])
def listings_list(category_id):
    return render_template("listings.html", listings=listings.get_all_listings(category_id))
