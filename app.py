from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile('config.py')


@app.route('/')
def hello_world():
    return render_template('base.html')


import views
