from flask_app import app, socketio
from flask_socketio import send, emit
from flask import render_template, request, redirect, session
import requests
import json
import math

from flask_app.models.user import User
from flask_app.models.yodel import Yodel

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash


# ================================================
# Render Index Template
# ================================================

@app.route("/")
def index():
    return render_template("index.html")


# ================================================
# Register User 
# ================================================
@app.route("/reg")
def reg():
    return render_template("register.html")




@app.route("/register", methods=["POST"])
def register():
    # checking the validation parameters
    if not User.validate_user(request.form):
        return redirect("/reg")
    # checking to see if the email exists
    data1 = {
        "username" : request.form["username"]
    }
    if User.get_by_username(data1):
        flash("Email already exists, need to register a differnt email")
        return redirect("/")

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "username" : request.form["username"],
        "password" : pw_hash
    }

    user_id = User.save(data)

    session["user_id"] = user_id
    return redirect("/dashboard")


# ================================================
# Login
# ================================================

@app.route("/login", methods=["POST"])
def login():
    data = {
        "username" : request.form["username"]
    }
    user_in_db = User.get_by_username(data)
    if not user_in_db:
        flash("Invalid Credentials")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Credentials")
        return redirect("/")

    session['user_id'] = user_in_db.id
    return redirect("/dashboard")

# ================================================
# Dashboard
# ================================================

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please register/login before you proceed to the website")
        return redirect("/")
    
    data = {
        "id" : session["user_id"]
    }
    logged_user = User.get_one(data)

    return render_template("/dashboard.html", user = logged_user)


# ================================================
# Logout
# ================================================

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================================================
# Pokemon
# ================================================

@socketio.on("msg")
def pokemon(id):
    print(id)

    pokemon_url = requests.get(f"https://pokeapi.co/api/v2/pokemon/{id}/")
    pokemon_data = pokemon_url.json()

    poke_name = pokemon_data['name']

    data = (poke_name)
    print(data)
    # send(data, broadcast=True)
    emit("msg", data)


# ================================================
# Weather
# ================================================

@socketio.on("message")
def weather(zip_code):
    api_key = "7f0ab817372d5166bb49752b9bf8573d"
    weather_url = requests.get(f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code},&appid={api_key}&units=imperial")
    weather_data = weather_url.json()

    temp = math.floor(weather_data['main']['temp'])
    weather = weather_data['weather'][0]['main']
    city = weather_data['name']

    data = (temp, weather, city)
    emit("message", {"message" : data})


