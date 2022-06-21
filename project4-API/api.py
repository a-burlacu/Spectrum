import flask  #import Flask library
from flask import request, jsonify


app = flask.Flask(__name__) # Creates Flask application object
app.config["DEBUG"] = True # Enables debugger

# @app.route('/', methods=["GET"]) #this maps the URL path to function 'home()' , methods states which HTTP requests are allowed
#
# def home():
#     return "<h1>Testing Flask API Creation</h1>"
#
# app.run()

# Create some test data for our catalog in the form of a list of dictionaries.
books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samuel R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'published': '1975'}
]
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/api/v1/resources/books/all', methods = ["GET"])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods = ["GET"])
def api_id():
    #Check if an ID was provided as part of the URL
    #If ID is provided, assign to variable
    #If ID not provided, display error in browser
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "<h1>Error: No ID field provided. Please specify an ID.</h1>"

    #Create empty list for our results
    results = []

    #Loop through the data and match results that fit requested ID
    #IDs are unique, but other fields may return many results
    for book in books:
        if book['id'] == id:
            results.append(book)

    #Use jsonify function from Flask to convert list of Python directories to JSON format
    return jsonify(results)

app.run()