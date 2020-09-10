from flask import Flask, render_template
import lang, os

app = Flask(__name__, static_url_path='')
port = int(os.getenv('PORT', 8000))

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/snacks/add')
def add_snacks():
    return render_template('add_snacks.html')

@app.route('/snacks/all')
def snacks_list():
    return render_template('snack_list.html', content=lang.es_MX['snack_list'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)