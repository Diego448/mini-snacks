from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
import lang, os, db_utils
from snack import Snack

app = Flask(__name__, static_url_path='')
port = int(os.getenv('PORT', 8000))
current_lang = lang.es_MX
uploads_path = '/home/diego/Assets/'
#Uploads path for Windows
#uploads_path = 'C:\Users\'

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/snacks/add', methods=['GET', 'POST'])
def add_snacks():
    if request.method == 'GET':
        return render_template('add_snacks.html')
    elif request.method == 'POST':
        new_snack = Snack(request.form['name'])
        new_snack.description = request.form['description']
        new_snack.price = float(request.form['price'])
        new_snack.ingredients = request.form['ingredients'].split(',')
        image_file = request.files['image']
        new_snack.image = image_file.filename
        image_file.save(uploads_path + secure_filename(image_file.filename))
        db_utils.add_snack(new_snack.get_data())
        status = {'message': 'OK', 'action': 'Add snack', 'code': 200}
        return render_template('action_feedback.html', status=status)

@app.route('/snacks/all')
def snacks_list():
    snacks = db_utils.get_all_snacks()
    return render_template('snacks_list.html', content=current_lang['snacks_list'], snacks_list=snacks)

@app.route('/snacks/<id>')
def snack_details(id):
    snack = db_utils.get_snack(id)
    return render_template('snack_details.html', snack_data=snack)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)