from app import app
from flask import request, render_template, redirect, url_for, session, flash, jsonify, g, abort
from sqlalchemy import or_
from functools import wraps
import os
from datetime import timedelta

from forms import *
from models import *

USER_ID = 'user_id'
PAGE_SIZE = 12
BOOK_PAGE_SIZE = 20
CLASSIFY_PAGE_SIZE = 5

base_dir = os.path.abspath(os.path.dirname(__file__))

# 自定义检查登录错误类
class CheckLoginError(Exception):
    pass


# 装饰器 检查用户登录状态
def check_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not get_user():
            raise CheckLoginError
        return func(*args, **kwargs)
    return wrapper


# 装饰器 检查管理员登录状态
def check_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = get_user()
        if not user:
            raise CheckLoginError
        if not user.admin:
            raise  CheckLoginError
        return func(*args, **kwargs)
    return wrapper


@app.route('/')
def index():
    scroll_pos = request.args.get('scroll_pos')
    if scroll_pos:
        g.scroll_pos = scroll_pos
    page = get_page()
    paginate = BookClassify.query.join(Book, Book.book_classify_id == BookClassify.id).group_by(BookClassify.id)\
        .paginate(page, CLASSIFY_PAGE_SIZE, False)
    return render_template('index.html', paginate=paginate)


# 新书 & 销量 排行
@app.route('/rank_books_<rank_type>')
def rank_book(rank_type):
    scroll_pos = request.args.get('scroll_pos')
    if scroll_pos:
        g.scroll_pos = scroll_pos
    page = get_page()
    if rank_type == 'new':
        paginate = get_new_books_query().paginate(page, BOOK_PAGE_SIZE)
    else:
        paginate = get_sales_books_query().paginate(page, BOOK_PAGE_SIZE)
    return render_template('book.html', paginate=paginate, url=request.path)


# 图书分类页面
@app.route('/book_classify_<int:book_classify_id>')
def books_view_classify(book_classify_id):
    scroll_pos = request.args.get('scroll_pos')
    if scroll_pos:
        g.scroll_pos = scroll_pos
    page = get_page()
    classify = BookClassify.query.filter(BookClassify.id == book_classify_id).one()
    paginate = Book.query.filter(Book.book_classify_id == book_classify_id).paginate(page, BOOK_PAGE_SIZE, False)
    # 分页地址
    url = request.path
    return render_template('book.html', paginate=paginate, url=url, title=classify.name)


# 用户搜索图书
@app.route('/books_query_<query_str>')
@app.route('/books_query')
def books_query(query_str=None):
    scroll_pos = request.args.get('scroll_pos')
    if scroll_pos:
        g.scroll_pos = scroll_pos
    page = get_page()
    if not query_str:
        query_str = request.args.get('search_str')
    paginate = Book.query.filter(Book.name.like('%' + query_str + '%')).paginate(page, BOOK_PAGE_SIZE, False)
    return render_template('book.html', paginate=paginate, url=url_for('books_query', query_str=query_str))


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
        recipient = Recipient(user_id=get_user().id, name=name, phone=phone, address=address)
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


# 收藏 & 取消收藏 图书
@app.route('/like_change_<book_id>')
@check_login
def like_change(book_id):
    user = get_user()
    book = Book.query.filter(book_id == Book.id).one()
    if book in user.favorite_books:
        user.favorite_books.remove(book)
    else:
        user.favorite_books.append(book)
    db.session.commit()
    return ''


# 添加到购物车
@app.route('/add_to_cart')
def add_to_cart():
    book_id = request.args.get('book_id')
    scroll_pos = request.args.get('scrollPos')
    user = get_user()
    if not user:
        return redirect(url_for('login'))
    if user.cart:
        cart_item = CartItem.query.filter(CartItem.cart_id == user.cart.id).filter(CartItem.book_id == book_id).one_or_none()
    else:
        user.cart = Cart(user_id=user.id)
        cart_item = None
    if cart_item:
        cart_item.quantity += 1
        cart_item.price += cart_item.book.price
        user.cart.price += cart_item.book.price
    else:
        book = Book.query.filter(Book.id == book_id).one()
        cart_item = CartItem(quantity=1, price=book.price, cart_id=user.cart.id, book_id=book_id)
        db.session.add(cart_item)
        user.cart.price += book.price
    db.session.commit()
    flash('添加成功')
    url = request.referrer
    if scroll_pos:
        url = deal_url(url, scroll_pos)
    return redirect(url)


# 处理url 为url添加滚动条位置参数
def deal_url(url, scroll_pos):
    if '?' in url:
        if 'scroll_pos' in url:
            str1 = url.split('scroll_pos', 1)
            str_tmp = str1[1].split('&', 1)
            if len(str_tmp) > 1:
                str_tmp = '&' + str_tmp[1]
            else:
                str_tmp = ''
            url = str1[0] + 'scroll_pos=' + scroll_pos + str_tmp
        else:
            url += '&scroll_pos=' + scroll_pos
    else:
        url += '?scroll_pos=' + scroll_pos
    return url


# 删除购物车中的项
@app.route('/delete_cart_item')
def delete_cart_item():
    item_id = request.args.get('item_id')
    item = CartItem.query.filter(CartItem.id == item_id).one()
    db.session.delete(item)
    db.session.commit()
    return redirect(request.referrer)


# 查看购物车
@app.route('/query_cart')
def query_cart():
    return render_template('cart.html')


# 保存购物车信息
@app.route('/save_cart', methods=['POST'])
def save_cart():
    items = request.json
    cart_items = get_user().cart.cart_items
    for k, value in items.items():
        for item in cart_items:
            if item.id == int(k):
                item.quantity = int(value)
                item.price = item.book.price * item.quantity
                break
    db.session.commit()
    return ''


# 创建订单
@app.route("/create_order", methods=['POST'])
def create_order():
    item_id_list = request.json.get('item_list')
    # 地址
    recipient_id = request.json.get('recipient_id')
    recipient = Recipient.query.filter(Recipient.id == recipient_id).one()
    user = get_user()
    try:
        order = OrderTable(user_id=user.id, recipient_id=recipient_id, name=recipient.name, phone=recipient.phone, address=recipient.address)
        db.session.add(order)
        db.session.commit()
        for item_id in item_id_list:
            cart_item = CartItem.query.filter(CartItem.id == item_id).one()
            order_item = OrderItem(quantity=cart_item.quantity, book_id=cart_item.book_id, price=cart_item.price, order_id=order.id)
            db.session.add(order_item)
            order.payment_amount += cart_item.price
            db.session.delete(cart_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        if order:
            db.session.delete(order)
            db.session.commit()
    return render_template('pay.html',order=order)


# 支付
@app.route('/pay', methods=['POST'])
def pay():
    order_id = request.form.get('order_id')
    order = OrderTable.query.filter(order_id == OrderTable.id and OrderTable.user_id == get_user().id).one()
    if order.state == '待付款':
        order.state = '待发货'
        db.session.commit()
    else:
        flash('error')
    return redirect(url_for('index'))


# 查看订单页面
@app.route('/orders')
def orders_view():
    page = get_page()
    user = get_user()
    paginate = OrderTable.query.filter(OrderTable.user_id == user.id).paginate(page, BOOK_PAGE_SIZE, False)
    return render_template('orders.html', paginate=paginate)


# 订单详情页面
@app.route('/order_detail')
def order_detail():
    order_id = request.args.get('order_id')
    order = OrderTable.query.filter(OrderTable.id == order_id and OrderTable.user_id == get_user().id).one_or_none()
    return render_template('order_detail.html', order=order)


# 取消订单
@app.route('/order_cancel_<order_id>')
def order_cancel(order_id):
    order = OrderTable.query.filter(OrderTable.user_id == get_user().id and OrderTable.id == order_id).one_or_none()
    if order.state == '待付款' or order.state == '待发货':
        order.state = '已取消'
        db.session.commit()
    else:
        abort(404)
    return redirect(url_for(order_detail))


# 确认收货
@app.route('/order_complete_<order_id>')
def order_complete(order_id):
    order = OrderTable.query.filter(OrderTable.user_id == get_user().id and OrderTable.id == order_id).one_or_none()
    if order.state == '待收货':
        order.state = '已完成'
        for item in order.order_items:
            item.book.sales_volume += item.quantity
        db.session.commit()
    else:
        abort(404)
    return redirect(url_for(order_detail))


# 申请退货
@app.route('/order_apply_return_<order_id>')
def order_apply_return(order_id):
    order = OrderTable.query.filter(OrderTable.user_id == get_user().id and OrderTable.id == order_id).one_or_none()
    if order.state == '已完成':
        order.state = '申请退货'
        db.session.commit()
    else:
        abort(404)
    return redirect(url_for(order_detail))


# 管理员相关视图函数
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


# 查询订单——管理员首页 表格链接 模态框
@app.route('/admin/order_query-<order_id>/')
def order_query(order_id):
    order = OrderTable.query.filter(OrderTable.id == order_id).one()
    if order:
        return render_template('admin_order_detail.html', order=order)
    return redirect(url_for('admin_view'))


# 订单状态修改
@app.route('/admin/update-order-<order_id>/', methods=['POST'])
def order_update(order_id):
    order = OrderTable.query.filter(OrderTable.id == order_id).one()
    if order:
        order.state = request.form.get('state')
        db.session.commit()
    else:
        abort(404)
    return jsonify()
    # return redirect(url_for(admin_view))


# 管理员订单管理页面
@app.route('/admin/order_view')
@check_admin
def admin_order_manage():
    page = get_page()
    paginate = OrderTable.query.order_by(OrderTable.create_time.desc()).paginate(page, PAGE_SIZE)
    return render_template('admin_order_manage.html', paginate=paginate)


# 管理员订单详情页面
@app.route('/admin/order_detail_<order_id>')
@check_admin
def admin_order_detail(order_id):
    order = OrderTable.query.filter(OrderTable.id == order_id).one_or_none()
    return render_template('admin_order_detail_page.html', order=order)


# 管理员修改订单收货信息
@app.route('/admin/order_recipient_modify_<order_id>')
@check_admin
def admin_order_recipient_modify(order_id):
    order = OrderTable.query.filter(OrderTable.id == order_id).one_or_none()
    name = request.args.get('name')
    address = request.args.get('address')
    phone = request.args.get('phone')
    order.name = name
    order.address = address
    order.phone = phone
    db.session.commit()
    return redirect(request.referrer)


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
# @app.route('/admin/add_book', methods=['POST'])
# def add_book():
#     book_classify_id = request.form.get('book_classify_id')
#     book_name = request.form.get('book_name')
#     quantity = request.form.get('quantity')
#     price = request.form.get('price')
#     book = Book(name=book_name, book_classify_id=book_classify_id, quantity=quantity, price=price)
#     db.session.add(book)
#     db.session.commit()
#     return ''


# 修改图书 & 增加图书
@app.route('/admin/save_update_book', methods=['POST'])
def save_update_book():
    book_id = request.form.get('book_id')
    book_classify_id = request.form.get('book_classify_id')
    book_name = request.form.get('book_name')
    quantity = request.form.get('quantity')
    price = request.form.get('price')
    author = request.form.get('author')
    publish_time = request.form.get('publish_time')
    press = request.form.get('press')
    introduction = request.form.get('introduction')

    image = request.files.get('image')
    if image:
        now_time = datetime.now().strftime("%Y%m%d%H%M%S")
        path = base_dir + "/static/image/books/"
        random_filename = now_time + image.filename
        save_path = 'image/books/'+random_filename
        file_path = path + random_filename
        image.save(file_path)
    else:
        save_path = 'image/icon.png'
    if book_id:
        book = Book.query.filter(Book.id == book_id).one()
        book.book_classify_id = book_classify_id
        book.name = book_name
        book.quantity = quantity
        book.price = price
        book.author = author
        book.publish_time = publish_time
        book.press = press
        book.introduction = introduction
        if image:
            book.image_url = save_path
    else:
        book = Book(name=book_name, book_classify_id=book_classify_id, quantity=quantity, price=price, author=author,
                    publish_time=publish_time, press=press, introduction=introduction, image_url=save_path)
        db.session.add(book)
    db.session.commit()
    return redirect(request.referrer)


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
        paginate = OrderTable.query.join(User, OrderTable.user_id == User.id)\
            .filter(or_(User.username.like('%' + query_str + '%'), OrderTable.id == str_to_int))\
            .order_by(OrderTable.create_time.desc()).paginate(page, PAGE_SIZE)
        return render_template('admin_query.html', paginate=paginate, url=url)
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
        abort(404)


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
def book_detail_customer(page=1):
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


# 管理员检查
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


# 获取新书查询
def get_new_books_query():
    now = datetime.now()
    delta = timedelta(days=365)
    start_time = now - delta
    new_books_query = Book.query.filter(Book.publish_time > start_time).order_by(Book.publish_time.desc())
    return new_books_query


# 获取销量 查询
def get_sales_books_query():
    sales_books_query = Book.query.order_by(Book.sales_volume.desc())
    return sales_books_query


# 获取 收藏 查询
# def get_rank_like_books_query():
#     like_books_query = Book.query.order_by()


# 保存上下文变量
@app.context_processor
def my_context_processor():
    book_classifies = BookClassify.query.all()
    new_books = get_new_books_query().all()
    sales_books = get_sales_books_query().all()
    my_dict = {}
    user = get_user()
    if user:
        my_dict.update(user=user)
        if not user.admin:
            my_dict.update(book_classifies=book_classifies)
            my_dict.update(new_books=new_books)
            my_dict.update(sales_books=sales_books)
    else:
        my_dict.update(book_classifies=book_classifies)
        my_dict.update(new_books=new_books)
        my_dict.update(sales_books=sales_books)
    return my_dict


# 捕捉自定义 登录状态异常
@app.errorhandler(CheckLoginError)
def error_no_login(error):
    return redirect(url_for('login'))


@app.errorhandler(404)
def error_404(error):
    return '找不到页面'


@app.errorhandler(500)
def error_500(error):
    return '服务器去吃饭了，请稍后再试'
