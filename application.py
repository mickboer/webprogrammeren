# Imports copy van Finance
import os


from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Imports for API (via tutorial https://www.youtube.com/watch?v=wmosqwoVkrA)
import requests as requests
import urllib.request as url
import random

#from matplotlib import pyplot
from PIL import Image
from helpers import api_request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///webprogrammeren.db")
# TO DO: database juist koppelen
# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///finance.db")


@app.route("/index", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        return redirect("search")
    else:
        dict_level123 = {"pets": 0, "farm": 100, "wildlife": 200}
        dict_level456 = {"sealife": 300, "insects": 400, "mix it up": 500}
        current_score = 340
        return render_template("index.html", dict_level123=dict_level123, dict_level456=dict_level456, current_score=current_score)



@app.route("/", methods=["GET", "POST"])
def begin():

    return redirect("start")


# from start to nickname
@app.route("/start", methods=["GET", "POST"])
def start():
    """Startpagina"""
    if request.method == "POST":

        return redirect("nickname")

    else:

        return render_template("start.html")


# from nickname to index
@app.route("/nickname", methods=["GET", "POST"])
def nickname():
    """nickname"""
    if request.method == "POST":
        nickname = request.form.get("nickname")

        if not nickname:
            return ("Nickname has to be at least 1 character long")

        result = db.execute("INSERT INTO Users (username) VALUES (:name)", name=nickname)

        if not result:
            return ("Nickname already in use")

        return redirect("index")

    else:
        return render_template("nickname.html")
    #for any user_id
    session.clear()



# from index to search opponent
@app.route("/search", methods=["GET", "POST"])
def search():
    """search opponent"""

    if request.method == "POST":

        return redirect("question")

    else:

        return render_template("search.html")





@app.route("/question", methods=["GET", "POST"])
def question():
    if request.method == "GET":

        # Haalt alle dieren uit categorie op en selecteerd 10 voor spel
        animalrows = db.execute("SELECT animal, unsplash FROM animals WHERE domain = :domain", domain="pets")
        quiz = random.sample(animalrows, 3)
        print(quiz)
        # Slaat huidige game data op
        session["game_data"] = {"round_number": 1, "rounds": quiz}

        # Kiest eerste dier uit rij voor game display
        animalname = session["game_data"]["rounds"][0]["animal"]
        unsplashanimal = session["game_data"]["rounds"][0]["unsplash"]
        round_number = session["game_data"]["round_number"]

        # Haalt de foto informatie op
        # API FUNCTION
        photo, userlink, name, unsplashlink = api_request(unsplashanimal)


        return render_template("question.html", photo=photo, userlink=userlink, name=name, unsplashlink=unsplashlink, word_len=len(animalname), round_number=round_number)

    if request.method == "POST":

        if len(session["game_data"]["rounds"]) == 1:
            return render_template("test.html", answer="YOU WON THE GAME, or not")

        # Session data ophalen
        animalname = session["game_data"]["rounds"][0]["animal"]
        unsplashanimal = session["game_data"]["rounds"][0]["unsplash"]


        # Antwoord van gebruiker ophalen
        user_input = ""
        for letter in range(len(animalname)):
            user_input += request.form.get("box" + str(letter))

        # Valideert antwoord TOEVOEGEN STUK JUSTINE
        # En score toevoegen, TOEVOEGEN STUK JUSTINE
        if animalname == user_input.lower():
            answer = True
        else:
            answer = False

        # Volgende vraag opzetten
        session["game_data"]["rounds"].remove(session["game_data"]["rounds"][0])
        session["game_data"]["round_number"] += 1

        # Ronde data opslaan
        animalname = session["game_data"]["rounds"][0]["animal"]
        unsplashanimal = session["game_data"]["rounds"][0]["unsplash"]
        round_number = session["game_data"]["round_number"]

        photo, userlink, name, unsplashlink = api_request(unsplashanimal)


        return render_template("question.html", photo=photo, userlink=userlink, name=name, unsplashlink=unsplashlink, word_len=len(animalname), round_number=round_number)




        # return render_template("test.html", answer=answer)



#def check_score():
    #username = session["id"]
    #score = db.execute("SELECT Score FROM users WHERE username=:username", username=username)

    #dict_levels = {"pets": 0, "farm": 100, "wildlife": 200, "sealife": 300, "insects": 400, "all_levels": 500}
    #score = 340
    #latest_level = "pets"
    #for key, value in dict_levels.items():
        #if score >= value:
           # latest_level = key
    #print(latest_level)
    #return render_template("index.html", level=latest_level)


#app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form.get("username")

#         if not username:
#             return ("Nickname has to be at least 1 character long")

#         result = db.execute("INSERT INTO Users (username) VALUES (:name)", name=username)

#         if not result:
#             return ("Username already in use")
#         return redirect("/")

#     else:
#         return render_template("register.html")

# ############   END TESTING API    ###############
