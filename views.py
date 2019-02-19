from app import app
from flask import request, render_template, redirect, url_for, session, flash, jsonify

from forms import *
from models import *

USER_ID = 'user_id'
PAGE_SIZE = 10


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            session[USER_ID] = user.id
            # 如果想在31天内不需要再登录
            # session.permanent = True
            if user.admin:
                return redirect(url_for('admin_view'))
            return redirect(url_for('index'))
        else:
            flash('用户名或密码错误')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
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


@app.route('/admin/logout/')
@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # session['user_id']
    session.clear()
    return redirect(url_for('login'))


# 个人中心
@app.route('/admin/personal_information/', methods=['GET', 'POST'])
@app.route('/personal_information/', methods=['GET', 'POST'])
def personal_information():
    form = PersonalForm()
    if form.validate_on_submit():
        user = User.query.get(session.get(USER_ID))
        user.username = form.username.data
        user.name = form.name.data
        user.birthday = form.birthday.data
        user.sex = form.sex.data
        db.session.commit()
        flash('修改成功')
        return redirect(url_for('personal_information'))
    user = get_user()
    form.username.data = user.username
    form.name.data = user.name
    form.birthday.data = user.birthday
    form.sex.data = user.sex
    return render_template('personal_information.html', form=form)


# 修改密码
@app.route('/update_password/', methods=['GET', 'POST'])
def update_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        user = User.query.get(session.get(USER_ID))
        old_password = form.oldPassword.data
        if old_password == user.password:
            new_password = form.newPassword1.data
            user.password = new_password
            db.session.commit()
            flash('修改密码成功')
            return redirect(url_for('index'))
        else:
            flash('旧密码错误，请核对后再重试！')
            return redirect(url_for('update_password'))
    return render_template('update_password.html', form=form)


@app.route('/admin/', methods=['GET', 'POST'])
def admin_view():
    if request.method == 'GET':
        orders_paid = OrderTable.query.filter(OrderTable.state == '待发货').all()
        orders_apply_return = OrderTable.query.filter(OrderTable.state == '申请退货').all()
        comments_new = Comment.query.filter(Comment.admin_check == False).order_by(Comment.publish_time.desc()).all()
        return render_template('admin.html', orders_paid=orders_paid, orders_apply_return=orders_apply_return,
                               comments_new=comments_new)
    else:
        return render_template('admin.html')


@app.route('/admin/dialog_modal/')
@app.route('/admin/test/')
def test():
    return render_template('admin_dialog_modal.html')


@app.route('/test1/<name>')
@app.route('/test1/')
def test1(name='1'):
    return name


@app.route('/admin/order_query-<order_id>/')
def order_query(order_id):
    order = OrderTable.query.filter(OrderTable.id == order_id).one()
    if order:
        return render_template('admin_order_detail.html', order=order)
    return redirect(url_for('admin_view'))


@app.route('/admin/update-order-<order_id>/', methods=['POST'])
def order_update(order_id):
    order = OrderTable.query.filter(OrderTable.id == order_id).one()
    if order:
        order.state = request.form.get('state')
        db.session.commit()
    else:
        flash('404')
    return jsonify()
    # return redirect(url_for(admin_view))


@app.route('/admin/reply_view_<book_id>_<page>')
@app.route('/admin/reply_view_<book_id>')
def admin_reply_view(book_id, page=1):
    book = Book.query.filter(Book.id == book_id).one()
    comments_list = Comment.query.filter(Comment.book_id == book_id).order_by(Comment.publish_time.desc()).paginate(
        page, PAGE_SIZE, False).items
    return render_template('admin_reply.html', book=book, comments=comments_list)


@app.route('/admin/comments_manage_<page>')
@app.route('/admin/comments_manage')
def admin_comments_view(page=1):
    total = Comment.query.all().count()
    total_page = total/PAGE_SIZE
    if total % PAGE_SIZE !=0:
        total_page += 1

    comments_list = Comment.query.order_by(Comment.publish_time.desc()).paginate(page, PAGE_SIZE, False).items
    return render_template('admin_comments_view.html', comments=comments_list, total_page=total_page)


@app.route('/admin/comments_manage_by_book_<page>')
@app.route('/admin/comments_manage_by_book')
def admin_comments_manage_by_book(page=1):
    books_list = Book.query.all().paginate(page, PAGE_SIZE, False).items
    render_template('admin_comments_book.html', books=books_list)


@app.route('/admin/reply/', methods=['POST'])
def admin_reply():
    book_id = request.form.get('book_id')
    target_id = request.form.get('target_id')
    author = get_user()
    content = request.form.get('content')
    comment = Comment(admin_check=True, from_user_id=author.id, to_user_id=target_id, book_id=book_id, content=content)
    db.session.add(comment)
    return jsonify()


def get_user():
    user_id = session.get(USER_ID)
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return user
    return None


@app.before_request
def validate_login():
    urls = request.full_path.split('/')
    user = get_user()
    if urls[1] != 'static':
        if urls[1] == 'admin':
            if not user or not user.admin:
                flash('你不是管理员')
                return redirect(url_for('index'))
        elif user and user.admin:
            flash('你不是用户')
            return redirect(url_for('admin_view'))


@app.context_processor
def my_context_processor():
    user = get_user()
    if user:
        return {'user': user}
    return {}
