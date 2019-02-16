from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import click
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)


import views
import models


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        if click.confirm('确定删除数据库吗？'):
            db.drop_all()
            click.echo('Drop tables.')
    db.create_all()
    # user = models.User(username='god', password='666', admin=True)
    # user1 = models.User(username='god6', password='666')
    # db.session.add(user)
    # db.session.add(user1)
    # db.session.commit()
    click.echo('Initialized database.')


@app.route('/')
def index():
    return render_template('index.html')


