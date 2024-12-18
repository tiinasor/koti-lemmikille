from app import app
from flask import render_template, request, redirect, session, url_for
import users
import categories
import locations
import listings
import messages

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

        errors = []
        if not username:
            errors.append("Käyttäjätunnus on täytettävä")
        if users.user_exist(username):
            errors.append("Käyttäjätunnus on jo käytössä")
        if len(username) > 20:
            errors.append("Käyttäjätunnus saa olla korkeintaan 20 merkkiä pitkä")
        if not password1:
            errors.append("Salasana on täytettävä")
        if len(password1) < 8:
            errors.append("Salasanan on oltava vähintään 8 merkkiä pitkä")
        if password1 != password2:
            errors.append("Salasanat eivät täsmää")
        if admin != "True" and admin != "False":
            errors.append("Roolin on oltava peruskäyttäjä tai ylläpitäjä")
        
        if len(errors) > 0:
            return render_template("register.html", errors=errors)
        elif users.register(username, password1, admin):
            users.login(username, password1)
            return redirect("/")
        else:
            return render_template("register.html", errors="Rekisteröityminen epäonnistui")
 
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
        users.check_csrf()
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
            return redirect("/user_listings")
        else:
            return render_template("add_listing.html", errors=["Ilmoituksen lisääminen epäonnistui"], categories=categories.get_all_categories(), locations=locations.get_all_locations())

@app.route("/listing/<int:listing_id>", methods=["GET"])
def listing(listing_id):
    listing = listings.get_listing(listing_id, session.get("user_id"))
    return render_template("listing.html", listing=listing)

@app.route("/category/<int:category_id>", methods=["GET"])
def listings_list(category_id):
    return render_template("listings.html", listings=listings.get_category_listings(category_id), category_name=categories.get_category_name(category_id))

@app.route("/user_listings", methods=["GET"])
def user_listings():
    if "user_id" not in session:
        return redirect("/")
    return render_template("user_listings.html", listings=listings.get_user_listings(session["user_id"]))

@app.route("/delete_listing/<int:listing_id>", methods=["POST"])
def delete_listing(listing_id):
    if "user_id" not in session:
        return redirect("/")
    users.check_csrf()
    if listings.delete_listing(listing_id, session["user_id"]):
        return render_template("user_listings.html", listings=listings.get_user_listings(session["user_id"]))
    else:
        return render_template("user_listings.html", listings=listings.get_user_listings(session["user_id"]), message="Ilmoituksen poistaminen epäonnistui")

@app.route("/admin_actions", methods=["GET"])
def admin_actions():
    if "user_id" not in session or not session.get("admin"):
        return redirect("/")
    return render_template("admin_actions.html")

@app.route("/manage_listings", methods=["GET"])
def manage_listings():
    if "user_id" not in session or not session.get("admin"):
        return redirect("/")
    all_listings = listings.get_all_listings()
    return render_template("manage_listings.html", listings=all_listings)

@app.route("/admin/delete_listing/<int:listing_id>", methods=["POST"])
def admin_delete_listing(listing_id):
    if "user_id" not in session or not session.get("admin"):
        return redirect("/")
    users.check_csrf()
    if listings.admin_delete_listing(listing_id):
        return render_template("manage_listings.html", listings=listings.get_all_listings())
    else:
        return render_template("manage_listings.html", listings=listings.get_all_listings(), message="Ilmoituksen poistaminen epäonnistui")
    
@app.route("/threads", methods=["GET"])
def threads():
    if "user_id" not in session:
        return redirect("/")
    return render_template("threads.html", threads=messages.get_threads(session["user_id"]))

@app.route("/thread_messages/<int:thread_id>", methods=["GET"])
def thread_messages(thread_id):
    if "user_id" not in session:
        return redirect("/")
    
    msgs, thread_subject, listing_id = messages.get_thread_messages(thread_id, session["user_id"])
    errors = request.args.getlist("errors")
    return render_template("thread_messages.html", messages=msgs, thread_subject=thread_subject, listing_id=listing_id, thread_id=thread_id, errors=errors)

@app.route("/create_thread", methods=["POST"])
def create_thread():
    if "user_id" not in session:
        return redirect("/")
    users.check_csrf()
    lister_id = int(request.form["lister_id"])
    listing_id = request.form["listing_id"]
    message = request.form["message"]

    listing = listings.get_listing(listing_id, session.get("user_id"))
    errors = []
    if not message:
        errors.append("Viesti ei saa olla tyhjä")
    if len(message) > 2000:
            errors.append("Viesti saa olla korkeintaan 2000 merkkiä pitkä")
    if listing["user_id"] == session["user_id"]:
        errors.append("Et voi lähettää viestiä itsellesi")
    if listing["user_id"] != lister_id:
        errors.append("Viestin vastaanottajan on oltava ilmoituksen tekijä")
    
    if len(errors) > 0:
        return render_template("listing.html", errors=errors, listing=listing)
    elif messages.initial_message(session["user_id"], lister_id, listing_id, message):
        listing = listings.get_listing(listing_id, session.get("user_id"))
        return render_template("listing.html", message="Viesti lähetetty", listing=listing)
    else:
        return render_template("listing.html", errors=["Viestin lähettäminen epäonnistui"], listing=listing)

@app.route("/send_message", methods=["POST"])
def send_message():
    if "user_id" not in session:
        return redirect("/")
    users.check_csrf()
    message = request.form["message"]
    thread_id = request.form["thread_id"]

    thread_exists = messages.thread_exists(thread_id, session["user_id"])

    errors = []
    if not message:
        errors.append("Viesti ei saa olla tyhjä")
    if len(message) > 2000:
            errors.append("Viesti saa olla korkeintaan 2000 merkkiä pitkä")
    if thread_exists == False:
        errors.append("Viestiketjua ei löydy")
    
    if len(errors) > 0:
        return redirect(url_for("thread_messages", errors=errors, thread_id=thread_id))
    elif messages.send_message(session["user_id"], thread_id, message):
        return redirect(url_for("thread_messages", thread_id=thread_id))
    else:
        return redirect(url_for("thread_messages", errors=["Viestin lähettäminen epäonnistui"], thread_id=thread_id))
    
@app.route("/delete_message/<int:message_id>", methods=["POST"])
def delete_message(message_id):
    if "user_id" not in session:
        return redirect("/")
    users.check_csrf()
    thread_id = request.form["thread_id"]

    if messages.delete_message(message_id, session["user_id"]):
        return redirect(url_for("thread_messages", thread_id=thread_id))
    else:
        return redirect(url_for("thread_messages", errors=["Viestin poistaminen epäonnistui"], thread_id=thread_id))
    