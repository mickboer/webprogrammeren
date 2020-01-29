import os
import requests as requests
import urllib.request as url
import random

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///webprogrammeren.db")

# DATABASE SELECTS

def quiz_maker(level):
    """Creates a ten question quiz on input level from animal quize database"""

    if level == "mix it up":
        animalrows = db.execute("SELECT animal, unsplash FROM animals")
        return random.sample(animalrows, 10)


    else:
        # Imports all animals from the database in selected 'level'
        animalrows = db.execute("SELECT animal, unsplash FROM animals WHERE domain = :domain", domain=level)

        # Returns a random selection of 10 animals
        return random.sample(animalrows, 10)


def total_scores():
    """Get the current score and level of the player from the users database"""

    current_score = db.execute("SELECT score FROM Users WHERE Username = :Username", Username=session["nickname"])[0]["score"]
    current_level = db.execute("SELECT level FROM Users WHERE Username = :Username", Username=session["nickname"])[0]["level"]

    return current_score, current_level

def game_data():
    """ Get all Usernames, Scores and Levels"""

    data = db.execute("SELECT Username, score, level FROM Users")

    return data

def in_use(nickname):
    """Searches in the database if the given username exists"""

    for username in db.execute("SELECT Username from Users"):

        if username["Username"].lower() == nickname.lower():
            return False

    return True


def select_opponent():
    """Random select an opponent from the database within given level and create session"""

    opponent = random.choice(db.execute("SELECT * FROM game WHERE level= :domain", domain=session["game_data"]["domain"]))
    if opponent == session["nickname"]:
        select_opponent()
    else:
        session["opponent"] = opponent

# DATABASE INSERTS
def create(nickname):
    """Creates an user in the database with given nickname"""

    db.execute("INSERT into Users (Username) VALUES(:Username)", Username=nickname)


def finished_game(user, total_user, latest_level):
    """Updates the database with the played game information"""

    db.execute("INSERT INTO game (nickname, status, level) VALUES (:nickname, :status, :level)",
    nickname=session["nickname"], status=user, level=session["game_data"]["domain"])

    db.execute("UPDATE Users SET score = score + :total_user, level = :level WHERE Username = :Username",
    Username=session["nickname"], total_user=int(total_user), level=latest_level)
