import os
import requests as requests
import urllib.request as url

from flask import Flask, flash, jsonify, redirect, render_template, request, session

# ? wat is dit.
from functools import wraps

def api_request(animal):
    """Haalt de gevraagde foto data op uit Unsplash API"""

    # Get image data from unsplash API
    input = 'https://api.unsplash.com/search/photos?query=' + animal + '&page=1&per_page=1&orientation=landscape&client_id=5246d76723858160b0f3fc3d254a89d4a27144e528dda80235c28c6874cdc014'
    r = requests.get(input)
    data = r.json()

    # Filter image data
    photo = data['results'][0]['urls']['small']
    username = data['results'][0]['user']['username']
    name = data['results'][0]['user']['name']

    # Create reference links to sources
    userlink = 'https://unsplash.com/@' + username + '?utm_source=Animal_Kingdom_Quiz&utm_medium=referral'
    unsplashlink = 'https://unsplash.com/?utm_source=Animal_Kingdom_Quiz&utm_medium=referral'

    return photo, userlink, name, unsplashlink


def game_data(aantal_var):
    """Vraagt huidige data game data uit in de session op basis van opgegeven aantal variabelen"""

    if aantal_var == 4:
        animalname = session["game_data"]["rounds"][0]["animal"]
        unsplashanimal = session["game_data"]["rounds"][0]["unsplash"]
        round_number = session["game_data"]["round_number"]
        score = sum(session["game_data"]["score"])*10

        return animalname, unsplashanimal, round_number, score

    elif aantal_var == 3:
        animalname = session["game_data"]["rounds"][0]["animal"]
        unsplashanimal = session["game_data"]["rounds"][0]["unsplash"]
        round_number = session["game_data"]["round_number"]

        return animalname, unsplashanimal, round_number

    elif aantal_var == 2:
        animalname = session["game_data"]["rounds"][0]["animal"]
        unsplashanimal = session["game_data"]["rounds"][0]["unsplash"]

        return animalname, unsplashanimal