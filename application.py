# Imports copy van Finance
import os


from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import collections
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Imports for API (via tutorial https://www.youtube.com/watch?v=wmosqwoVkrA)
import requests as requests
import urllib.request as url
import random

#from matplotlib import pyplot
from PIL import Image
from helpers import api_request
from helpers import game_data

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

        level = request.form.get("level")
        print(level)

        # Haalt alle dieren uit categorie op en selecteerd 10 voor spel
        animalrows = db.execute("SELECT animal, unsplash FROM animals WHERE domain = :domain", domain=level)
        quiz = random.sample(animalrows, 3)
        print(quiz)
        # Slaat huidige game data op
        session["game_data"] = {"domain": level, "round_number": 1, "rounds": quiz, "score": []}


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
        session["nickname"] = nickname

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

    # if request.method == "POST":

    return redirect("question")

    # else:

    #     return render_template("search.html")





@app.route("/question", methods=["GET", "POST"])
def question():

    if request.method == "GET":

        # Haalt session[game_data] op uit helpers.py (3 variabelen)
        animalname, unsplashanimal, round_number = game_data(3)

        # Haalt de API foto informatie op uit helpers.py
        photo, userlink, name, unsplashlink = api_request(unsplashanimal)

        #selecteer een opponent op basis van game id
        session["opponent"] = random.choice(db.execute("SELECT * FROM game WHERE level= :domain", domain=session["game_data"]["domain"]))


        return render_template("question.html", photo=photo, userlink=userlink, name=name, unsplashlink=unsplashlink, word_len=len(animalname),
            round_number=round_number, opponent=session["opponent"]["nickname"])

    if request.method == "POST":

        # Haalt session[game_data] op uit helpers.py (twee variabelen)
        animalname, unsplashanimal = game_data(2)

        # Antwoord van gebruiker ophalen
        user_input = ""
        for letter in range(len(animalname)):
            user_input += request.form.get("box" + str(letter))


        # Valideert antwoord en voegt score toe
        if animalname == user_input.lower():
            session["game_data"]["score"].append(1)
        elif animalname != user_input.lower():
            session["game_data"]["score"].append(0)


        # Als game klaar is wordt er doorverwezen naar winner/loser pagina
        if len(session["game_data"]["rounds"]) == 1:

           return render_template("winner.html")


        # Volgende vraag opzetten
        session["game_data"]["rounds"].remove(session["game_data"]["rounds"][0])
        session["game_data"]["round_number"] += 1

        # Haalt session[game_data] op uit helpers.py (4 variabelen)
        animalname, unsplashanimal, round_number, score = game_data(4)

        # Haalt de API foto informatie op uit helpers.py
        photo, userlink, name, unsplashlink = api_request(unsplashanimal)


        return render_template("question.html", photo=photo, userlink=userlink, name=name, unsplashlink=unsplashlink,
            word_len=len(animalname), round_number=round_number, score=score, opponent=session["opponent"])


# @ WINNER PAGE.
#  # telt hoeveel 1en in score
#             opponent = opponentrow[0]["status"]
#             user = str(session["game_data"]["score"])
#             one = "1"

#             if opponent.count(one) > user.count(one):
#                 return render_template("winner.html", answer="YOU LOST THE GAME")

#             if opponent.count(one) < user.count(one):
#                 return render_template("winner.html", answer="YOU WON THE GAME")

#             else:
#                 return render_template("winner.html", answer="IT'S A TIE")


