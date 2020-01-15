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

from helpers import api_request

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# TO DO: database juist koppelen
# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///finance.db")


##########################   TESTING API  #########
# TEST API
@app.route("/")
def index():
    """Test voor de Unsplash API"""

    return redirect("test_api")



@app.route("/test_api", methods=["GET", "POST"])
def test_api():
    """Test voor de Unsplash API"""
    animals = ['cat', 'dog', 'lion', 'meerkat', 'dolphin', 'ant', 'jaguar', 'pig', 'spider', 'snake', 'shark', 'whale']
    animal = random.choice(animals)

    # input = 'https://api.unsplash.com/search/photos?query=' + animal + '&page=1&per_page=1&orientation=landscape&client_id=5246d76723858160b0f3fc3d254a89d4a27144e528dda80235c28c6874cdc014'
    # r = requests.get(input)
    # data = r.json()
    # photo = data['results'][0]['user']

    photo, userlink, name, unsplashlink = api_request(animal)


    return render_template("test_api.html", photo=photo, userlink=userlink, name=name, unsplashlink=unsplashlink)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")


        return redirect("/")
    else:
        return render_template("register.html")

############   END TESTING API    ###############
