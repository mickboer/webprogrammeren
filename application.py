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
        quiz = random.sample(animalrows, 10)
        print(quiz)
        # Slaat huidige game data op
        session["game_data"] = {"domain": level, "round_number": 1, "rounds": quiz, "score": []}

        return redirect("search")

    else:
        dict_level123 = {"pets": [0, 0], "farm": [100, 1], "wildlife": [200, 2]}
        dict_level456 = {"sealife": [300, 3], "insects": [400, 4], "mix it up": [500, 5]}
        current_score = db.execute("SELECT score FROM Users WHERE Username = :Username", Username=session["nickname"])[0]["score"]
        current_level = db.execute("SELECT level FROM Users WHERE Username = :Username", Username=session["nickname"])[0]["level"]

        one_person = db.execute("SELECT Username, score, level FROM Users")
        level_and_score = sorted(one_person, key=lambda k: (k['level'], k["score"]), reverse=True)[0:10]

        leaderboard_list = [(player["Username"], player["level"], player["score"]) for player in level_and_score]

        return render_template("index.html", dict_level123=dict_level123, dict_level456=dict_level456, current_score=current_score,
        current_level=current_level, leaderboard_list=leaderboard_list)


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

        result = db.execute("SELECT Username from Users WHERE Username = :Username", Username=nickname)
        session["nickname"] = nickname

        if len(result) > 0:
            return ("Nickname already in use")

        else:
            db.execute("INSERT into Users (Username) VALUES(:Username)", Username=nickname)

        return redirect("index")

    else:
        return render_template("nickname.html")
    #for any user_id
    session.clear()



# from index to search opponent
@app.route("/search", methods=["GET", "POST"])
def search():
    """search opponent"""

    if request.method == "GET":

        return render_template("search.html")

    elif request.method == "POST":

        return redirect("question")



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
            # breaks als de gebruiker niks heeft ingevuld
            if request.form.get("box" + str(letter)) == None:
                break
            else:
                user_input += request.form.get("box" + str(letter))

        # Valideert antwoord en voegt score toe
        if animalname == user_input.lower():
            session["game_data"]["score"].append(1)
        elif animalname != user_input.lower():
            session["game_data"]["score"].append(0)


        # Als game klaar is wordt er doorverwezen naar winner/loser pagina
        if len(session["game_data"]["rounds"]) == 1:
           return redirect("winner")


        # Volgende vraag opzetten
        session["game_data"]["rounds"].remove(session["game_data"]["rounds"][0])
        session["game_data"]["round_number"] += 1

        # Haalt session[game_data] op uit helpers.py (4 variabelen)
        animalname, unsplashanimal, round_number, score = game_data(4)

        # Haalt de API foto informatie op uit helpers.py
        photo, userlink, name, unsplashlink = api_request(unsplashanimal)


        return render_template("question.html", photo=photo, userlink=userlink, name=name, unsplashlink=unsplashlink,
            word_len=len(animalname), round_number=round_number, score=score, opponent=session["opponent"]["nickname"])


@app.route("/winner", methods=["GET", "POST"])
def winner():
#  # telt hoeveel 1en in score

    if request.method == "GET":
        opponent = session["opponent"]["status"]
        user = ""
        for cijfer in session["game_data"]["score"]:
            user += str(cijfer)

        total_opponent = opponent.count("1")
        total_user = user.count("1")
        total_score = total_user * 10

        latest = "pets"
        if total_user > total_opponent:
            latest = session["game_data"]["domain"]

        latest_level = 1
        level_dict = {"pets": 1, "farm": 2, "wildlife": 3, "sealife": 4, "insects": 5, "mix it up": 5}
        for key, value in level_dict.items():
            if latest == key:
                latest_level = value


        db.execute("INSERT INTO game (nickname, status, level) VALUES (:nickname, :status, :level)",
        nickname=session["nickname"], status=user, level=session["game_data"]["domain"])

        db.execute("UPDATE Users SET score = score + :total_score, level = :level WHERE Username = :Username",
        Username=session["nickname"], total_score=int(total_score), level=latest_level)

        return render_template("winner.html", total_opponent=total_opponent, total_user=total_user)

    if request.method == "POST":
        return redirect("index")



