from flask import Flask, render_template, request, url_for, Response
from werkzeug.utils import secure_filename
import lang, os, db_utils
from snack import Snack
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__, static_url_path='')
port = int(os.getenv('PORT', 8000))
current_lang = lang.es_MX
current_path = os.path.abspath(os.getcwd())
uploads_path = os.path.join(str(current_path), 'static', 'images/')

@app.route('/')
def homepage():
    return render_template('homepage.html', content=current_lang['homepage'])

@app.route('/snacks/add', methods=['GET', 'POST'])
def add_snacks():
    if request.method == 'GET':
        return render_template('add_snacks.html', snack_data={})
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
    snack_data = db_utils.get_snack(id)
    styles = create_styles(snack_data['image'])
    return render_template('snack_details.html', snack_data=snack_data, styles=styles, url_info=request.url_root)

@app.route('/snacks/<id>/edit', methods=['GET', 'POST'])
def snack_edit(id):
    if request.method == 'GET':
        snack_data = db_utils.get_snack(id)
        return render_template('add_snacks.html', snack_data=snack_data)
    elif request.method == 'POST':
        new_data = Snack(request.form['name'])
        new_data.description = request.form['description']
        new_data.price = request.form['price']
        image_file = request.files['image']
        new_data.image = image_file.filename
        image_file.save(uploads_path + secure_filename(image_file.filename))
        db_utils.edit_snack(id, new_data.get_data())
        status = {'message': 'OK', 'action': 'Add snack', 'code': 200}
        return render_template('action_feedback.html', status=status)

@app.route('/sales/add')
def add_sales():
    return render_template('add_sales.html')

def create_styles(image_url):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('default.css')
    values = {
        "background_image_url": url_for('static', filename='images/' + image_url) ,
        "background_size": "cover"
    }
    return template.render(values=values)

@app.route('/test/styles/<image>')
def style_test(image):
    env = Environment(loader=FileSystemLoader('static'))
    template = env.get_template('test.css')
    values = {
        "background_image_url": url_for('static', filename='images/' + image) ,
        "background_size": "cover"
    }
    stylesheet = template.render(values=values)
    return Response(stylesheet, mimetype="text/css")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)