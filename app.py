import click

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import datetime, timedelta

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
    user = models.User(username='he', password='666', admin=True, sex='女', birthday='20001110')
    user1 = models.User(username='god6', password='666')
    recipient = models.Recipient(user_id=2, name='god6', phone='18998515319', address='天上人间')
    db.session.add(user)
    db.session.add(user1)
    db.session.add(recipient)
    book_classify = models.BookClassify(name='文艺')
    db.session.add(book_classify)
    book = models.Book(name='呵呵', quantity=300, price=30, book_classify_id=1)
    db.session.add(book)
    order = models.OrderTable(user_id=2, recipient_id=1, payment_amount=30, name=recipient.name, phone=recipient.phone, address=recipient.address, state='待发货')
    db.session.add(order)
    order_item = models.OrderItem(quantity=1, book_id=1, order_id=1, price=book.price)
    db.session.add(order_item)
    comment = models.Comment(from_user_id=2, book_id=1, content='极上佳作')
    comment1 = models.Comment(from_user_id=1, to_user_id=2, book_id=1, content='的确如此', publish_time=datetime.now()+timedelta(hours=1))
    db.session.add(comment)
    db.session.add(comment1)
    db.session.commit()
    click.echo('Initialized database.')

