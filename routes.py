from app import app
from flask import render_template, request, redirect
import users
import categories

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
