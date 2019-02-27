from app import app
from flask import request, render_template, redirect, url_for, session, flash, jsonify
from sqlalchemy import or_

from forms import *
from models import *

USER_ID = 'user_id'
PAGE_SIZE = 12
BOOK_PAGE_SIZE = 20


@app.route('/')
def index():
    page = get_page()
    paginate = BookClassify.query.filter(BookClassify.books).paginate(page, PAGE_SIZE, False)
    return render_template('index.html', paginate=paginate)


# 新书
@app.route('/new_books')
def rank_new_book():
    page = get_page()
    paginate = Book.query.paginate(page, BOOK_PAGE_SIZE, False)
    return render_template('book.html', paginate=paginate, url=request.path)


# 图书分类页面
@app.route('/book_classify_<int:book_classify_id>')
def books_view_classify(book_classify_id):
    page = get_page()
    paginate = Book.query.filter(Book.book_classify_id == book_classify_id).paginate(page, BOOK_PAGE_SIZE, False)
    # 分页地址
    url = request.path
    return render_template('book.html', paginate=paginate, url=url)


# 用户搜索图书
@app.route('/books_query')
def books_query():
    page = get_page()
    query_str = request.args.get('search_str')
    paginate = Book.query.filter(Book.name.like('%' + query_str + '%')).paginate(page, BOOK_PAGE_SIZE, False)
    return render_template('book.html', paginate=paginate, url=request.path)


# 从url获取页数
def get_page():
    page = request.args.get('page')
    if not page:
        page = 1
    try:
        page = int(page)
    except ValueError or TypeError:
        page = 1
    return page


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
    pwd_form = UpdatePasswordForm()
    if form.validate_on_submit():
        user = User.query.get(session.get(USER_ID))
        user.username = form.username.data
        user.name = form.name.data
        user.birthday = form.birthday.data
        user.sex = form.sex.data
        db.session.commit()
        flash('修改成功')
        return redirect(request.path)
    # 提交修改密码
    if pwd_form.validate_on_submit():
        return update_password(pwd_form)
    user = get_user()
    form.username.data = user.username
    form.name.data = user.name
    form.birthday.data = user.birthday
    form.sex.data = user.sex
    return render_template('personal_information.html', form=form, pwd_form=pwd_form)


# 添加修改地址
@app.route('/admin/save_up_address', methods=['POST'])
@app.route('/save_up_address', methods=['POST'])
def save_up_address():
    re_id = request.form.get('id')
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')
    if re_id:
        recipient = Recipient.query.filter(Recipient.id == int(re_id)).one()
        recipient.name = name
        recipient.phone = phone
        recipient.address = address
    else:
        recipient = Recipient(user_id=get_user().id,name=name,phone=phone,address=address)
        db.session.add(recipient)
    db.session.commit()
    flash('修改完成')
    return redirect(url_for('personal_information'))


# 修改密码
def update_password(form):
    user = User.query.get(session.get(USER_ID))
    old_password = form.oldPassword.data
    if old_password == user.password:
        new_password = form.newPassword1.data
        user.password = new_password
        db.session.commit()
        flash('修改密码成功')
        return redirect(request.path)
    else:
        flash('密码错误，请核对后再重试！')
        return redirect(request.path)


# 添加到购物车
def add_


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
                               comments_new=comments_new, orders_apply_return_count=orders_apply_return_count,
                               orders_paid_count=orders_paid_count,
                               comments_new_count=comments_new_count)
    else:
        return '404'


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


# 查看图书分类-局部刷新
@app.route('/admin/book_classify_manage_<int:page>')
@app.route('/admin/book_classify_manage')
def book_classify_manage(page=1):
    paginate = BookClassify.query.paginate(page, PAGE_SIZE, False)
    return render_template('admin_book_classify_manage.html', paginate=paginate)


# 增加图书分类-模态框
@app.route('/admin/book_classify_add', methods=["POST"])
def book_classify_add():
    name = request.form.get('name')
    book_classify = BookClassify(name=name)
    db.session.add(book_classify)
    db.session.commit()
    return ''


# 删除图书分类
@app.route('/admin/book_classify_del_<book_classify_id>', methods=['POST'])
def book_classify_del(book_classify_id):
    book_classify = BookClassify.query.filter(BookClassify.id == book_classify_id).one()
    db.session.delete(book_classify)
    db.session.commit()
    return ''


# 修改图书分类-模态框
@app.route('/admin/book_classify_update_<int:book_classify_id>', methods=["POST"])
def book_classify_update(book_classify_id):
    book_classify = BookClassify.query.filter(BookClassify.id == book_classify_id).one()
    book_classify.name = request.form.get("name")
    db.session.commit()
    return ''


# 获取图书列表
@app.route('/admin/get_books_<int:book_classify_id>_<int:page>', methods=['GET', 'POST'])
@app.route('/admin/get_books_<int:book_classify_id>', methods=['GET', 'POST'])
def get_books_list(book_classify_id, page=1):
    paginate = Book.query.filter(Book.book_classify_id == book_classify_id).paginate(page, PAGE_SIZE, False)
    return render_template('admin_books_list.html', paginate=paginate)


# 查看 添加&修改图书页面
@app.route('/admin/opt_book_modal', methods=['POST'])
def opt_book_modal():
    book_classifies = BookClassify.query.all()
    book_id = request.form.get('book_id')
    book = Book.query.filter(Book.id == book_id).one_or_none() if book_id else None
    return render_template('opt_book_modal.html', book=book, book_classifies=book_classifies)


# 增加图书
@app.route('/admin/add_book', methods=['POST'])
def add_book():
    book_classify_id = request.form.get('book_classify_id')
    book_name = request.form.get('book_name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')
    book = Book(name=book_name, book_classify_id=book_classify_id, quantity=quantity, price=price)
    db.session.add(book)
    db.session.commit()
    return ''


# 修改图书
@app.route('/admin/update_book_<int:book_id>', methods=['POST'])
def update_book(book_id):
    book_classify_id = request.form.get('book_classify_id')
    book_name = request.form.get('book_name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')
    book = Book.query.filter(Book.id == book_id).one()
    book.book_classify_id = book_classify_id
    book.name = book_name
    book.quantity = quantity
    book.price = price
    db.session.commit()
    return ''


# 删除图书
@app.route('/admin/del_book_<int:book_id>', methods=['POST'])
def del_book(book_id):
    book = Book.query.filter(Book.id == book_id).one()
    db.session.delete(book)
    db.session.commit()
    return ''


# 评论查看页面——局部刷新
@app.route('/admin/comments_manage_<int:page>')
@app.route('/admin/comments_manage')
def admin_comments_view(page=1):
    paginate = Comment.query.order_by(Comment.publish_time.desc()).paginate(page, PAGE_SIZE, False)
    return render_template('admin_comments_view.html', paginate=paginate)


# 查看图书——局部刷新
@app.route('/admin/comments_manage_by_book_<int:page>', methods=['GET', 'POST'])
@app.route('/admin/comments_manage_by_book', methods=['GET', 'POST'])
def admin_comments_manage_by_book(page=1):
    paginate = Book.query.paginate(page, PAGE_SIZE, False)
    return render_template('admin_comments_book.html', paginate=paginate)


# 管理员 搜索  图书|图书分类|订单
@app.route('/admin/query_<query_type>_<query_str>')
@app.route('/admin/query')
def admin_query(query_type='', query_str=''):
    page = get_page()
    if query_str == '':
        query_type = request.args.get('search_type')
        query_str = request.args.get('search_str')
    try:
        str_to_int = int(query_str)
    except ValueError or TypeError:
        str_to_int = -1
    # 用来为分页拼接地址
    url = url_for('admin_query', query_type=query_type, query_str=query_str)
    if query_type == 'order':
        pass
    elif query_type == 'book':
        paginate = Book.query.filter(or_(Book.name.like('%' + query_str + '%'), Book.id == int(str_to_int))).paginate(
            page, PAGE_SIZE, False)
        return render_template('admin_query.html',
                               paginate=paginate, url=url)
    elif query_type == 'book_classify':
        paginate = BookClassify.query.filter(
            or_(BookClassify.name.like('%' + query_str + '%'), BookClassify.id == int(str_to_int))).paginate(page, PAGE_SIZE, False)
        return render_template('admin_query.html', paginate=paginate, url=url)
    else:
        flash('404')
        return '404'


# 图书详情-模态框ajax
@app.route('/admin/book_detail_<int:page>', methods=['POST'])
@app.route('/admin/book_detail', methods=['POST'])
def book_detail(page=1):
    comment_id = request.form.get('comment_id')
    g_page = request.form.get('page')
    book_id = request.form.get('book_id')
    if not book_id:
        book_id = request.args.get('book_id')
    page = g_page if g_page else page
    comment_query = Comment.query.filter(Comment.book_id == book_id)
    # 如果是查看具体某条评论
    if comment_id:
        comments = comment_query.order_by(Comment.publish_time.desc()).all()
        comment = comment_query.filter(Comment.id == comment_id).one()
        c_index = comments.index(comment)
        page = int(c_index / PAGE_SIZE) + 1

    paginate = comment_query.order_by(Comment.publish_time.desc()).paginate(int(page), PAGE_SIZE, False)
    comments_list = paginate.items
    if get_user() and get_user().admin:
        for comment in comments_list:
            comment.admin_check = True
        db.session.commit()
    book = Book.query.filter(Book.id == book_id).one()
    url = request.path
    return render_template('book_detail.html', book=book, paginate=paginate, url=url)


# 图书详情-模态框ajax
@app.route('/book_detail_<int:page>', methods=['POST'])
@app.route('/book_detail', methods=['POST'])
def book_detail_customer( page=1):
    return book_detail(page)


# 回复评论——模态框ajax
@app.route('/admin/reply/', methods=['POST'])
def comment_reply():
    book_id = request.form.get('book_id')
    target_id = request.form.get('target_id')
    author = get_user()
    content = request.form.get('content')
    comment = Comment(admin_check=author.admin, from_user_id=author.id, to_user_id=target_id, book_id=book_id,
                      content=content)
    db.session.add(comment)
    db.session.commit()
    return jsonify()


# 用户评论
@app.route('/replay', methods=['POST'])
def user_comment():
    return comment_reply()


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
    book_classifies = BookClassify.query.all()
    my_dict = {}
    user = get_user()
    if user:
        my_dict.update(user=user)
        if not user.admin:
            my_dict.update(book_classifies=book_classifies)
    else:
        my_dict.update(book_classifies=book_classifies)
    return my_dict
