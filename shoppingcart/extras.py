import random
import string

from .models import OrderItem


def saveOrderItem(order):
    order_item = OrderItem.objects.get_or_create(order=order)
    order_item.save()
    return order_item


def generate_order_id():
    length = 15
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
