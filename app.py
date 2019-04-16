import click
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
# 启动任务调度
scheduler = BackgroundScheduler()
import views
views.start_scheduler()
import models


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        if click.confirm('确定删除数据库吗？'):
            db.drop_all()
            click.echo('Drop tables.')
    db.create_all()
    user = models.User(username='he', password='666', admin=True, sex='女', birthday='20001110')
    user1 = models.User(username='god6', password='666')
    db.session.add(user)
    db.session.add(user1)
    book_classify = models.BookClassify(name='文艺')
    db.session.add(book_classify)
    db.session.commit()
    click.echo('Initialized database.')



