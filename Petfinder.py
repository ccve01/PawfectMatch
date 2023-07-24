import requests
import pandas as pd
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_behind_proxy import FlaskBehindProxy
import secrets
from flask_sqlalchemy import SQLAlchemy
from Forms import PrefernceForm, ContactForm, NavigationForm

key = secrets.token_hex(16)
app = Flask(__name__)
proxied = FlaskBehindProxy(app)  ## add this line
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
spot = 0

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
    spot = 0

    for animal in animals_json["animals"]:
        animals_dict[spot] = {
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
            'contact(email)': animal["contact"]["email"],
            'contact(phone)': animal["contact"]["phone"]
        }
        
        address_text = ""
        for line in animal["contact"]["address"].values():
            if (line is not None):
                address_text += line + " "
        animals_dict[spot]['contact(address)'] = address_text

        try:
            photomedium = animal["primary_photo_cropped"]["medium"]
            animals_dict[spot]['photos'] = photomedium
            animals_dict[spot]['video'] = animal['videos'][0]["embed"]
        except TypeError:
            animals_dict[spot]['photos'] = None
        except IndexError:
            animals_dict[spot]['video'] = None
        if 'video' not in animals_dict[spot]:
            animals_dict[spot]['video'] = None

        spot += 1
    
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

def save_results(results):
    # print(results)
    for animal in results.values():
        # print(animal['video'])
        history = Data(id=animal['id'], name=animal['name'], type=animal['type'], breed_primary=animal['breed(primary)'], color_primary=animal['color(primary)'],
                       age=animal['age'], gender=animal['gender'], size=animal['size'], coat=animal['coat'], status=animal['status'], location=animal['contact(address)'],
                       photo=animal['photos'], video=animal['video'], email=animal['contact(email)'], phone=animal['contact(phone)'])
        db.session.add(history)
        db.session.commit()

    # print(results)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    type = db.Column(db.String(120), unique=False, nullable=True)
    breed_primary = db.Column(db.String(120), unique=False, nullable=True)
    color_primary = db.Column(db.String(120), unique=False, nullable=True)
    age = db.Column(db.String(120), unique=False, nullable=True)
    gender = db.Column(db.String(120), unique=False, nullable=True)
    size = db.Column(db.String(120), unique=False, nullable=True)
    coat = db.Column(db.String(120), unique=False, nullable=True)
    status = db.Column(db.String(120), unique=False, nullable=True)
    location = db.Column(db.String(120), unique=False, nullable=True)
    photo = db.Column(db.String(120), unique=False, nullable=True)
    video = db.Column(db.String(120), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=True)
    phone = db.Column(db.String(120), unique=False, nullable=True)

class Liked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=True)
    type = db.Column(db.String(120), unique=False, nullable=True)
    breed_primary = db.Column(db.String(120), unique=False, nullable=True)
    color_primary = db.Column(db.String(120), unique=False, nullable=True)
    age = db.Column(db.String(120), unique=False, nullable=True)
    gender = db.Column(db.String(120), unique=False, nullable=True)
    size = db.Column(db.String(120), unique=False, nullable=True)
    coat = db.Column(db.String(120), unique=False, nullable=True)
    status = db.Column(db.String(120), unique=False, nullable=True)
    location = db.Column(db.String(120), unique=False, nullable=True)
    photo = db.Column(db.String(120), unique=False, nullable=True)
    video = db.Column(db.String(120), unique=False, nullable=True)
    email = db.Column(db.String(120), unique=False, nullable=True)
    phone = db.Column(db.String(120), unique=False, nullable=True)

def save_matches(animal):
    # print(results)
    # print(animal['video'])
    history = Liked(id=animal.id, name=animal.name, type=animal.type, breed_primary=animal.breed_primary, color_primary=animal.color_primary,
                    age=animal.age, gender=animal.gender, size=animal.size, coat=animal.coat, status=animal.status, location=animal.location,
                    photo=animal.photo, video=animal.video, email=animal.email, phone=animal.phone)
    db.session.add(history)
    db.session.commit()
  
with app.app_context():
    # db.drop_all()
    db.create_all()

@app.route("/", methods=['GET', 'POST'])
@app.route("/index.html", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/preference.html", methods=['GET', 'POST'])
def preference():
    form = PrefernceForm()
    if form.validate_on_submit():
        output={'type': form.species.data, 'age':form.age.data, 'gender':form.gender.data, 'size':form.size.data, 'location':form.location.data, }
        url = build_url(output)
        # print(url)
        response = get_request(token, url)
        animalsdf = parse_animals(convert_to_json(response))
        save_results(animalsdf)
        return redirect(url_for('match'))
        # for Pet in Pets:
        #     print(Pet.id)
     
    return render_template('preference.html', form=form) 

@app.route("/match.html", methods=['GET', 'POST'])
def match():
    form=ContactForm()
    Pets = db.session.query(Data).first()
    print(Pets)
    if form.validate_on_submit():
        if form.submit.data:
            db.session.delete(Pets)
            db.session.commit()
            return redirect(url_for('match'))
        elif form.submit2.data:
            save_matches(Pets)
            db.session.delete(Pets)
            db.session.commit()
            print('Like')
            return redirect(url_for('match'))
    return render_template('matchpage.html', Pets=Pets, form=form)

@app.route("/login.html", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route("/signup.html", methods=['GET', 'POST'])
def register():
    return render_template('signup.html')

@app.route("/adopt.html", methods=['GET', 'POST'])
def adopt():
    form = PrefernceForm()
    if form.validate_on_submit():
        output={'type': form.species.data, 'age':form.age.data, 'gender':form.gender.data, 'size':form.size.data, 'location':form.location.data}
        url = build_url(output)
        response = get_request(token, url)
        animalsdf = parse_animals(convert_to_json(response))
        # print(animalsdf)
    
    return render_template('adopt.html')

@app.route("/likePage.html", methods=['GET', 'POST'])
def Like():
    global spot
    Cat = db.session.query(Liked).all()
    form = NavigationForm()
    if form.validate_on_submit():
        if form.submit.data:
            spot -= 1 
            if spot < 0:
                spot = len(Cat)-1
            return redirect(url_for('Like'))
        elif form.submit2.data:
            spot += 1 
            if spot > len(Cat)-1:
                spot = 0
            return redirect(url_for('Like'))
    print(Cat)
    return render_template('likePage.html', Pets=Cat[spot], form=form)

@app.route("/chatPage.html", methods=['GET', 'POST'])
def Chat():
    return render_template('chatPage.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8001)

    # output={'type': 'dog', 'age':'baby', 'gender':'male'}
    # url = build_url(output)
    # response = get_request(token, url)
    # animalsdf = parse_animals(convert_to_json(response))
    # print(animalsdf)

