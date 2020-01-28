import os
import requests as requests
import urllib.request as url

from flask import Flask, flash, jsonify, redirect, render_template, request, session

# ? wat is dit.
from functools import wraps

def api_request(animal):
    """Get's the image data from Unsplash API when animal name is given and returns individual variables"""

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
    """Returns given amount of game data variabele from current game played out of the session data"""

    # Append the animal name and image name for the next round
    game_data = [session["game_data"]["rounds"][0]["animal"], session["game_data"]["rounds"][0]["unsplash"]]

    # Append the round number for the next round
    game_data.append(session["game_data"]["round_number"])

    # Append players score of the current game
    game_data.append(session["game_data"]["score"])
    print(session["game_data"]["score"])

    # Return variable needed
    if aantal_var == 2:
        return game_data[0], game_data[1]
    elif aantal_var == 3:
        return game_data[0], game_data[1], game_data[2]
    elif aantal_var == 4:
        return game_data[0], game_data[1], game_data[2], game_data[3]
