from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import click

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


@app.cli.command()
def initdb():
    db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


@app.route('/')
def hello_world():
    return render_template('base.html')


import views
import models
