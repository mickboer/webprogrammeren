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
from helpers import api_request, game_data
from dataquery import quiz_maker, total_scores, in_use, create, select_opponent, finished_game

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///webprogrammeren.db")


@app.route("/index", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        # Creates random list of 10 animal with choosen level in dataquery.py
        level = request.form.get("level")
        quiz = quiz_maker(level)

        # Saves the current game data in a Session
        session["game_data"] = {"domain": level, "round_number": 1, "rounds": quiz, "score": []}

        return redirect("search")

    else:
        # First 3 levels with required score and level
        dict_level123 = {"pets": [0, 0], "farm": [100, 1], "wildlife": [200, 2]}

        # Last 3 levels with required score and level
        dict_level456 = {"sealife": [300, 3], "insects": [400, 4], "mix it up": [500, 5]}

        # Get current score and level from database via dataquery.py
        current_score, current_level = total_scores()


        # !?!?NAAR DATAQUERY.PY VERPLAATSEN!?!?!?!?!?!?!?!?
        # Select game data of all players
        one_person = db.execute("SELECT Username, score, level FROM Users")

        # Create top 10 sorted on level, than score
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
        try:
            if session["nickname"] != None:
                return redirect("index")

        except:
            return render_template("start.html")


# from nickname to index
@app.route("/nickname", methods=["GET", "POST"])
def nickname():
    """nickname"""
    if request.method == "POST":

        nickname = request.form.get("nickname")

        # Check if nickname is filled in
        if not nickname:
            return ("Nickname has to be at least 1 character long")

        # Check if nickname is in us
        if in_use(nickname) == False:

            return ("Nickname already in use")

        # Create a session for the user and save to database
        else:
            session["nickname"] = nickname
            create(nickname)

        return redirect("index")

    else:
        return render_template("nickname.html")



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

        # Gets session[game_data] from helpers.py
        animalname, unsplashanimal, round_number = game_data(3)

        # Get the API foto from from helpers.py
        photo, userlink, name, unsplashlink = api_request(unsplashanimal)

        #Selects opponent based on current level
        select_opponent()

        return render_template("question.html", photo=photo, userlink=userlink, name=name, unsplashlink=unsplashlink, word_len=len(animalname),
            round_number=round_number, opponent=session["opponent"]["nickname"],
            opponent_score=0, player=session["nickname"], score=0)

    if request.method == "POST":

        # Gets session[game_data] from helpers.py
        animalname, unsplashanimal = game_data(2)

        # Get the input from user
        user_input = ""
        for letter in range(len(animalname)):
            # breaks if field is empty
            if request.form.get("box" + str(letter)) == None:
                break
            else:
                user_input += request.form.get("box" + str(letter))

        # Validates the users input and add to score
        if animalname == user_input.lower():
            session["game_data"]["score"].append(1)
        elif animalname != user_input.lower():
            session["game_data"]["score"].append(0)


        # Check is game is finished, then redirects to winner/loser page
        if len(session["game_data"]["rounds"]) == 1:
           return redirect("winner")


        # Volgende vraag opzetten
        session["game_data"]["rounds"].remove(session["game_data"]["rounds"][0])
        session["game_data"]["round_number"] += 1

        # Haalt session[game_data] op uit helpers.py (4 variabelen)
        animalname, unsplashanimal, round_number, score = game_data(4)

        # Haalt de API foto informatie op uit helpers.py
        photo, userlink, name, unsplashlink = api_request(unsplashanimal)

        # Calculate the opponents current score
        opponent_score = session["opponent"]["status"][0:(round_number - 1)].count("1")

        return render_template("question.html", photo=photo, userlink=userlink, name=name, unsplashlink=unsplashlink,
            word_len=len(animalname), round_number=round_number, score=sum(score)*10, player=session["nickname"], opponent=session["opponent"]["nickname"],
            opponent_score = opponent_score)


@app.route("/winner", methods=["GET", "POST"])
def winner():
#  # telt hoeveel 1en in score

    if request.method == "GET":
        # opponent = session["opponent"]["status"]
        user = ""
        for number in session["game_data"]["score"]:
            user += str(number)

        total_opponent = session["opponent"]["status"].count("1")
        total_user = user.count("1")
        total_score = total_user * 10

        latest = "pets"
        if total_user > total_opponent or total_user == 10:
            latest = session["game_data"]["domain"]

        latest_level = 1
        level_dict = {"pets": 1, "farm": 2, "wildlife": 3, "sealife": 4, "insects": 5, "mix it up": 5}
        for key, value in level_dict.items():
            if latest == key:
                latest_level = value

        # Update database with new scores
        finished_game(user, total_score, latest_level)

        return render_template("winner.html", total_opponent=total_opponent, total_user=total_user)

    if request.method == "POST":
        return redirect("index")



