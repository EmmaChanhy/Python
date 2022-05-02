import flask
import random
import json

quotes = open('top_10_billionairs_quotes.json')
data = json.load(quotes)

app = flask.Flask(__name__)
@app.route('/', methods=['GET'])
def home_page():
    num_of_quotes = len(data)
    random_quote = random.randint(0,num_of_quotes)
    select_quote = data[random_quote]

    return select_quote