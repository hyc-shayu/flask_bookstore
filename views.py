from app import app
from flask import request, render_template, redirect, url_for, session, flash

from forms import *
from models import *


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 如果想在31天内不需要再登录
            # session.permanent = True
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.username == username).first()
        if user:
            flash('用户名已存在')
            return redirect(url_for('register'))
        else:
            if password1 != password2:
                flash('两次密码不一致')
                return redirect(url_for('register'))
            else:
                user = User(username=username, password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # session.pop('user_id')
    # session['user_id']
    session.clear()
    return redirect(url_for('login'))


# 个人中心
@app.route('/personal_information', methods=['GET', 'POST'])
def personal_information():
    form = PersonalForm()
    user = get_user()
    form.username.data = user.username
    form.name.data = user.name
    form.birthday.data = user.birthday
    form.sex.data = user.sex
    if form.validate_on_submit():
        user = User.query.get(user.id)
        user.username = form.username.data
        user.name = form.name.data
        user.birthday = form.birthday.data
        user.sex = form.sex.data
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('personal_information'))
    return render_template('personal_information.html', form=form)



def get_user():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return user
    return None


@app.context_processor
def my_context_processor():
    user = get_user()
    if user:
        return {'user': user}
    return {}
