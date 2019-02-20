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


# 管理员界面 显示最新记录10条
@app.route('/admin/', methods=['GET', 'POST'])
def admin_view():
    if request.method == 'GET':
        orders_paid = OrderTable.query.filter(OrderTable.state == '待发货').all()
        orders_paid_count = len(orders_paid)
        orders_paid = orders_paid[0:PAGE_SIZE]
        orders_apply_return = OrderTable.query.filter(OrderTable.state == '申请退货').all()
        orders_apply_return_count = len(orders_apply_return)
        orders_apply_return = orders_apply_return[0:PAGE_SIZE]
        comments_new = Comment.query.filter(Comment.admin_check == False).order_by(Comment.publish_time.desc()).all()
        comments_new_count = len(comments_new)
        comments_new = comments_new[0:PAGE_SIZE]
        return render_template('admin.html', orders_paid=orders_paid, orders_apply_return=orders_apply_return,
                               comments_new=comments_new, orders_apply_return_count=orders_apply_return_count, orders_paid_count=orders_paid_count,
                               comments_new_count=comments_new_count)
    else:
        return render_template('admin.html')


# 查询订单——管理员首页 表格链接
@app.route('/admin/order_query-<order_id>/')
def order_query(order_id):
    order = OrderTable.query.filter(OrderTable.id == order_id).one()
    if order:
        return render_template('admin_order_detail.html', order=order)
    return redirect(url_for('admin_view'))


# 订单详情——模态框
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


# 评论查看页面——局部刷新
@app.route('/admin/comments_manage_<int:page>')
@app.route('/admin/comments_manage')
def admin_comments_view(page=1):
    total = len(Comment.query.all())
    total_page = int(total/PAGE_SIZE)
    if total % PAGE_SIZE != 0:
        total_page += 1
    comments_list = Comment.query.order_by(Comment.publish_time.desc()).paginate(page, PAGE_SIZE, False).items
    return render_template('admin_comments_view.html', comments=comments_list, total_page=total_page, current_page=page)


# 图书评论-按书分类显示评论——局部刷新
@app.route('/admin/comments_manage_by_book_<int:page>')
@app.route('/admin/comments_manage_by_book')
def admin_comments_manage_by_book(page=1):
    total = len(Book.query.all())
    total_page = int(total / PAGE_SIZE)
    if total % PAGE_SIZE != 0:
        total_page += 1
    books_list = Book.query.paginate(page, PAGE_SIZE, False).items
    return render_template('admin_comments_book.html', books=books_list, total_page=total_page)


# 图书详情-模态框ajax
@app.route('/admin/book_detail_<int:page>', methods=['POST'])
@app.route('/admin/book_detail', methods=['POST'])
def book_detail(page=1):
    comment_id = request.form.get('comment_id')
    book_id = request.form.get('book_id')
    comment_query = Comment.query.filter(Comment.book_id == book_id)
    # 如果是查看具体某条评论
    if comment_id:
        comments = comment_query.order_by(Comment.publish_time.desc()).all()
        comment = comment_query.filter(Comment.id == comment_id).one()
        index = comments.index(comment)
        page = int(index/PAGE_SIZE)+1

    comments_list = comment_query.order_by(Comment.publish_time.desc()).paginate(page, PAGE_SIZE, False).items
    total = len(comment_query.all())
    total_page = int(total / PAGE_SIZE)
    if total % PAGE_SIZE != 0:
        total_page += 1
    book = Book.query.filter(Book.id == book_id).one()
    return render_template('book_detail.html', book=book, comments=comments_list, total_page=total_page, current_page=page)


# 回复评论——模态框ajax
@app.route('/admin/reply/', methods=['POST'])
def comment_reply():
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
