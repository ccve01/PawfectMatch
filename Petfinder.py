import requests
import pandas as pd
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
import secrets
from flask_sqlalchemy import SQLAlchemy
from Forms import PrefernceForm

key = secrets.token_hex(16)
app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

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

AUTH_URL = 'https://api.petfinder.com/v2/oauth2/token'
token = get_token(API_key, API_secret)

def path_to_image_html(path):
    return '<img src="' + path + '" width="60" >'

def get_request(access_token, BASE_url):
    headers = {'Authorization': 'Bearer {token}'.format(token=access_token)}
    response = requests.get(BASE_url, headers=headers)
    return response


def convert_to_json(response):
    return response.json()

def parse_animals(animals_json):
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
    
    return animals_dict
 
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
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    type = db.Column(db.String(120), unique=False, nullable=False)
    breed_primary = db.Column(db.String(120), unique=False, nullable=False)
    color_primary = db.Column(db.String(120), unique=False, nullable=False)
    age = db.Column(db.String(120), unique=False, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=False)
    size = db.Column(db.String(120), unique=False, nullable=False)
    coat = db.Column(db.String(120), unique=False, nullable=False)
    status = db.Column(db.String(120), unique=False, nullable=False)

@app.route("/", methods=['GET', 'POST'])
@app.route("/index.html", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/preference.html", methods=['GET', 'POST'])
def preference():
    form = PrefernceForm()
    if form.validate_on_submit():
        output={'type': form.species.data, 'age':form.age.data, 'gender':form.gender.data, 'size':form.size.data}
        url = build_url(output)
        response = get_request(token, url)
        animalsdf = parse_animals(convert_to_json(response))
        print(animalsdf)
     
    return render_template('preference.html', form=form) 

@app.route("/match.html", methods=['GET', 'POST'])
def match():
    return render_template('matchpage.html')

@app.route("/login.html", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route("/signup.html", methods=['GET', 'POST'])
def register():
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8001)

    # output={'type': 'dog', 'age':'baby', 'gender':'male'}
    # url = build_url(output)
    # response = get_request(token, url)
    # animalsdf = parse_animals(convert_to_json(response))
    # print(animalsdf)

