from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')

@app.route('/index')
def index():
    user = {'nickname': 'Phil'}  # fake user
    return render_template('index.html',
                           title='AutoDeploy',
                           user=user)
