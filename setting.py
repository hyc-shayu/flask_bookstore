from datetime import timedelta
import os
from enum import Enum, unique

USER_ID = 'user_id'
PAGE_SIZE = 12
BOOK_PAGE_SIZE = 20
CLASSIFY_PAGE_SIZE = 5
Single = 60
TEST_AUTO_CANCEL_TIME = timedelta(minutes=10)
TEST_AUTO_CONFIRM_TIME = timedelta(minutes=10)
TEST_AUTO_FINISH_TIME = timedelta(minutes=10)

base_dir = os.path.abspath(os.path.dirname(__file__))
BOOK_PATH = "/static/image/books/"
ICON_PATH = "/static/image/icon.png"
CAROUSEL_PATH = '/static/image/carousel/'


@unique
class OrderState(Enum):
    WaitPay = '待付款'
    Cancel = '已取消'
    WaitDelivery = '待发货'
    WaitReceive = '待收货'
    Received = '已收货'
    Completed = '已完成'
    ApplyReturn = '申请退货'
    AgreedReturn = '同意退货'
    RefuseReturn = '拒绝退货'
    Returned = '已退货'
