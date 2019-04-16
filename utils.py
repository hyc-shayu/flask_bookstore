from flask import redirect, url_for, request, session, flash, abort
from app import app
from models import *
from setting import USER_ID
from errors import UnknownError


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


# 排序查询类
class BookSort:
    @staticmethod
    def sort_sale(query):
        return query.order_by(Book.sales_volume.desc())

    @staticmethod
    def sort_sale_up(query):
        return query.order_by(Book.sales_volume)

    @staticmethod
    def sort_time(query):
        return query.order_by(Book.publish_time.desc())

    @staticmethod
    def sort_time_up(query):
        return query.order_by(Book.publish_time)

    @staticmethod
    def sort_like(query):
        return query.order_by(Book.favorite_user_count.desc())

    @staticmethod
    def sort_like_up(query):
        return query.order_by(Book.favorite_user_count)

    @staticmethod
    def sort_price(query):
        return query.order_by(Book.price.desc())

    @staticmethod
    def sort_price_up(query):
        return query.order_by(Book.price)

    @staticmethod
    def get_sort(query, sort_type):
        sort_func = eval('BookSort.sort_{sort_type}'.format(sort_type=sort_type))
        return sort_func(query)


def book_sort_query(query, sort_type):
    try:
        return BookSort.get_sort(query, sort_type)
    except Exception:
        raise UnknownError
