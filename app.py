from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import click

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


import views
import models


@app.cli.command()
def initdb():
    db.drop_all()
    db.create_all()
    user = models.User(username='god', password='666', admin=True)
    user1 = models.User(username='god6', password='666')
    db.session.add(user)
    db.session.add(user1)
    db.session.commit()
    click.echo('Initialized database.')


@app.route('/')
def index():
    return render_template('index.html')


