from program import app
from flask import render_template, request
from datetime import datetime
import requests


@app.route('/')
@app.route('/index')
def index():
    timenow = str(datetime.today())
    return render_template('index.html', time=timenow)


@app.route('/100days')
def p100days():
    return render_template('/100days.html')


def get_chuck_joke():
    r = requests.get('https://api.chucknorris.io/jokes/random')
    data = r.json()
    return data['value']


@app.route('/chuck')
def chuck():
    joke = get_chuck_joke()
    return render_template('chuck.html', joke=joke)


def get_j_questions():
    payload = {'count': 1}
    r = requests.get('http://jservice.io/api/random', params=payload)
    data = r.json()
    return data[0]


@app.route('/jeopardy')
def jeopardy():
    jitem = get_j_questions()
    difficulty = jitem['value']
    question = jitem['question']
    answer = jitem['answer']
    category = jitem['category']['title']
    return render_template('jeopardy.html',
                           difficulty=difficulty,
                           question=question,
                           answer=answer,
                           category=category)


def determine_valid_colors():
    r = requests.get('https://pokeapi.co/api/v2/pokemon-color')
    response = r.json()
    valid_colors = []
    results = response['results']
    for item in results:
        valid_colors.append(item['name'])
    return valid_colors


def get_poke_colors(color):
    r = requests.get('https://pokeapi.co/api/v2/pokemon-color/' + color.lower())
    pokedata = r.json()
    pokemon = []
    for i in pokedata['pokemon_species']:
        pokemon.append(i['name'])

    return pokemon


def get_poke_data(color):
    r = requests.get('https://pokeapi.co/api/v2/pokemon-color/' + color.lower())
    colordata = r.json()
    pokemon_links = []
    for i in colordata['pokemon_species']:
        pokemon_links.append(i['url'])

    pokemon_data = []
    for url in pokemon_links:
        r = requests.get(url)
        pokedata = r.json()
        flavor_text = ''
        while flavor_text == '':
            for item in pokedata['flavor_text_entries']:
                if item['language']['name'] != "en":
                    continue
                else:
                    flavor_text = item['flavor_text']
                    break

        if pokedata['habitat'] is None:
            habitat = ""
        else:
            habitat = pokedata['habitat']['name']

        poke = {'name': pokedata['name'],
                'habitat': habitat,
                'growth_rate': pokedata['growth_rate']['name'],
                'shape': pokedata['shape']['name'],
                'flavor': flavor_text}
        pokemon_data.append(poke)

    return pokemon_data


@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    pokemon = []
    VALID_COLORS = determine_valid_colors()
    error = ""
    if request.method == 'POST' and 'pokecolor' in request.form:
        color = request.form.get('pokecolor')
        if color in VALID_COLORS:
            pokemon = get_poke_data(color)
        else:
            error = "Please enter a valid Pokemon color"
    return render_template('pokemon.html',
                           pokemon=pokemon,
                           error=error)
