from app import db
from datetime import datetime

user_favorite_book_table = db.Table('user_favorite_book',db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                                db.Column('book_id', db.Integer, db.ForeignKey('book.id')))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(30), default=username)
    sex = db.Column(db.Enum('男', '女'), default='男')
    admin = db.Column(db.Boolean, default=False)
    birthday = db.Column(db.Date)
    # logout_time = db.Column(db.DateTime)

    recipients = db.relationship('Recipient')
    orders = db.relationship('OrderTable', back_populates='user')
    cart = db.relationship('Cart', uselist=False)
    comments = db.relationship('Comment', back_populates='from_user', foreign_keys='Comment.from_user_id')
    replies = db.relationship('Comment', back_populates='to_user', foreign_keys='Comment.to_user_id')
    favorite_books = db.relationship('Book', secondary=user_favorite_book_table, back_populates='liked_by_users')


class Recipient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user 外键
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 地址不需要知道用户信息
    # user = db.relationship('User', back_populates='recipients')
    name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    address = db.Column(db.String(100), nullable=False)


# 删除和修改地址 保持地址不变
# 地址id外键 冗余
class OrderTable(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    # user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='orders')
    # recipient
    recipient_id = db.Column(db.Integer, db.ForeignKey('recipient.id'))
    recipient = db.relationship('Recipient')

    # 设置默认值
    name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(11), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    payment_amount = db.Column(db.Float, nullable=False, default=0)
    # 是否还缺少状态 拒绝退货 同意退货
    state = db.Column(db.Enum('待付款', '已取消', '待发货', '待收货', '已完成', '申请退货', '同意退货', '拒绝退货', '已退货'), default='待付款')
    # 考虑创建索引
    create_time = db.Column(db.DateTime, default=datetime.now)

    order_items = db.relationship('OrderItem')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    # book
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship('Book')

    price = db.Column(db.Float, nullable=False)
    # order
    order_id = db.Column(db.Integer, db.ForeignKey('order_table.id'))


# 可以不需要购物车表
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float, nullable=False, default=0)
    # user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship('User', back_populates='cart')

    cart_items = db.relationship('CartItem', cascade='all, delete-orphan')


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)
    # cart
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    # book
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship('Book')


class BookClassify(db.Model):
    __tablename__ = 'book_classify'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    books = db.relationship('Book', cascade='all, delete-orphan')


# 买书才能评论？
class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False)

    introduction = db.Column(db.String(512))
    image_url = db.Column(db.String(255))
    author = db.Column(db.String(50))
    publish_time = db.Column(db.Date)
    press = db.Column(db.String(100)) # 出版社
    sales_volume = db.Column(db.Integer, default=0)
    # classify 分类外键
    book_classify_id = db.Column(db.Integer, db.ForeignKey('book_classify.id'))

    comments = db.relationship('Comment', cascade='all')
    favorite_user_count = db.Column(db.Integer,default=0)
    liked_by_users = db.relationship('User', secondary=user_favorite_book_table, back_populates='favorite_books')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 考虑创建索引
    publish_time = db.Column(db.DateTime, default=datetime.now)
    content = db.Column(db.Text)
    admin_check = db.Column(db.Boolean, default=False)
    # user
    from_user_id = db.Column('from_user_id', db.Integer, db.ForeignKey('user.id'))
    from_user = db.relationship('User', back_populates='comments', foreign_keys=[from_user_id])
    # to_user
    to_user_id = db.Column('to_user_id', db.Integer, db.ForeignKey('user.id'))
    to_user = db.relationship('User', back_populates='replies', foreign_keys=[to_user_id])

    # book
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    book = db.relationship('Book')
