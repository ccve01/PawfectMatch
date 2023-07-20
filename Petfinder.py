import requests
import pandas as pd
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy

ANIMAL_TYPES_LIST = [None, 'Dog', 'Cat', 'Rabbit', 'Small-Furry', 'Horse',
                     'Bird', 'Scales-Fins-Other', 'Barnyard']
ANIMAL_GENDERS_LIST = [None, 'Male', 'Female']
ANIMAL_AGE_LIST = [None, 'Baby', 'Young', 'Adult', 'Senior']
ANIMAL_SIZE_LIST = [None, 'Small', 'Medium', 'Large', 'Xlarge']

API_key = 'OXmcV0LKuvPuDmXXVJFb7nsl5O0djD5SbPbWk0yU4yMbIsxRHH'
API_secret = 'TxgjuRnIIKKzn7tbVrtMw3PkObM4S7ESYNUJak0i'

def get_token(API_key, API_secret):
    response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': API_key,
        'client_secret': API_secret,
    })  
    return response.json()['access_token']

def path_to_image_html(path):
    return '<img src="' + path + '" width="60" >'

def get_request(access_token, BASE_url):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    response = requests.get(BASE_url, headers=headers)
    return response


def convert_to_json(response):
    return response.json()

def parse_animals(animals_json):
    animalsdf = pd.DataFrame()
    animals_dict = {}
    count = 0

    for animal in animals_json["animals"]:
        animals_dict[count] = {
            'id': animal["id"],
            'type': animal["type"],
            'breed(primary)': animal["breeds"]["primary"],
            'color(primary)': animal["colors"]["primary"],
            'age': animal["age"],
            'gender': animal["gender"],
            'size': animal["size"],
            'coat': animal["coat"],
            'name': animal["name"],
            'description': animal["description"],
            'status': animal["status"],
            'published_at': animal["published_at"],
        }
        
        try:
            photomedium = animal["primary_photo_cropped"]["medium"]
            animals_dict[count]['photos'] = photomedium
            animals_dict[count]['video'] = animal['videos'][0]["embed"]
        except TypeError:
            animals_dict[count]['photos'] = None
        except IndexError:
            animals_dict[count]['video'] = None

        count += 1

    animalsdf = pd.DataFrame.from_dict(animals_dict,
                                       orient='index')
    return animalsdf
 
def get_request(access_token, BASE_url):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    response = requests.get(BASE_url, headers=headers)
    return response

def build_url(dict_inputs):
    url = "https://api.petfinder.com/v2/animals?"
    no_preference = True
    for key, value in dict_inputs.items():
        if value is not None:
            no_preference = False
            url += f'{key}={value}&'
    url = url[:-1]

    if no_preference:
        return 'https://api.petfinder.com/v2/animals'
    else:
        return url

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8001)
    AUTH_URL = 'https://api.petfinder.com/v2/oauth2/token'
    token = get_token(API_key, API_secret)

    output={'type': 'dog', 'age':'baby', 'gender':'male'}
    url = build_url(output)
    response = get_request(token, url)
    animalsdf = parse_animals(convert_to_json(response))
    print(animalsdf)

