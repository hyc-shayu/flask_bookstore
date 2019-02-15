from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(30), default=username)
    sex = db.Column(db.Enum('男', '女'), default='男')
    admin = db.Column(db.Boolean, default=False)
    birthday = db.Column(db.Date)


class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user 外键
    name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    address = db.Column(db.String(100), nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    # user
    # recipient
    payment_amount = db.Column(db.Float, nullable=False)
    state = db.Column(db.Enum('待付款', '已取消', '待发货', '待收货', '已完成', '已退货'), default='待付款')
    # 考虑创建索引
    create_time = db.Column(db.DateTime, default=datetime.now)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)
    # book
    # order


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float, nullable=False, default=0)
    # user


class CartItem(db.Column):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)
    # cart
    # book


class BookClassify(db.Model):
    __tablename__ = 'book_classify'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False)
    # classify 分类外键


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 考虑创建索引
    publish_time = db.Column(db.DateTime, default=datetime.now)
    content = db.Column(db.Text)
    # target_comment
    # user
    # book
