from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/snacks/add')
def add_snacks():
    return render_template('add_snacks.html')