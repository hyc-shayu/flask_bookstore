from app import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(30), default=username)
    sex = db.Column(db.Enum('男', '女'), default='男')
    admin = db.Column(db.Boolean, default=False)
    birthday = db.Column(db.Date)
