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
        if not name:
            return render_template("add_listing.html", message="Nimi on täytettävä")
        elif len(name) > 30:
            return render_template("add_listing.html", message="Nimi saa olla korkeintaan 30 merkkiä pitkä")                          
        elif int(age_years) < 0 or int(age_years) > 200:
            return render_template("add_listing.html", message="Ikä vuosina on oltava välillä 0-200")
        elif int(age_months) < 0 or int(age_months) > 11:
            return render_template("add_listing.html", message="Ikä kuukausina on oltava välillä 0-11")
        elif sex != "male" and sex != "female" and sex != "unknown":
            return render_template("add_listing.html", message="Sukupuolen on oltava koiras, naaras tai tuntematon")
        elif len(species_breed) > 50:
            return render_template("add_listing.html", message="Tarkempi laji/rotu saa olla korkeintaan 50 merkkiä pitkä") 
        elif len(description) > 2000:
            return render_template("add_listing.html", message="Kuvaus saa olla korkeintaan 2000 merkkiä pitkä")
        elif listings.add_listing(name, age, sex, location, category, species_breed, description, user_id=session["user_id"]):
            return redirect("/")
        else:
            return render_template("add_listing.html", message="Ilmoituksen lisääminen epäonnistui")

@app.route("/category/<int:category_id>", methods=["GET"])
def listings_list(category_id):
    return render_template("listings.html", listings=listings.get_all_listings(category_id))
