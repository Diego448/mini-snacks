from flask import Flask, render_template
import lang

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/snacks/add')
def add_snacks():
    return render_template('add_snacks.html')

@app.route('/snacks/all')
def snacks_list():
    return render_template('snack_list.html', content=lang.es_MX['snack_list'])