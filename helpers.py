import os
import requests as requests
import urllib.request as url

from flask import Flask, flash, jsonify, redirect, render_template, request, session

# ? wat is dit.
from functools import wraps

def api_request(animal):

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