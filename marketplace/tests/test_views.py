from PIL import Image
from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from shoppingcart.views import *
from users.models import Vendor


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="resu", password="TESTING321")
        self.user_vendor = User.objects.create_user(username="vendoruser", password="TESTING321")
        self.profile = Profile.objects.get(user=self.user)
        self.user_logged = Client()
        self.vendor_logged = Client()
        self.user_logged.force_login(self.user)
        self.admin_user = User.objects.create_superuser(username="Super", password="TESTING321")
        self.admin_user_logged = Client()
        self.admin_user_logged.force_login(self.admin_user)
        self.vendor = Vendor.objects.create(user=self.user_vendor, address="indirizzo", mobile="123456789",
                                            description="ABCDEFGH", ranknum=0, ranksum=0)
        self.product = Product.objects.create(item="test", description="testd", category="Desserts",
                                              cost=10, available=True,
                                              vendor=self.vendor)
        self.vendor_logged.force_login(self.user_vendor)
        self.order_item = OrderItem.objects.get_or_create(product=self.product, quantity=10)
        self.user_order = Order.objects.get_or_create(owner=self.profile, is_ordered=False)
        self.user_order_true = Order.objects.get_or_create(owner=self.profile, is_ordered=True)

    def test_shop_get(self):
        response = self.user_logged.get((reverse("shop")))
        self.assertRedirects(response, '/marketplace/shop/resu/', status_code=302,
                             target_status_code=200, fetch_redirect_response=False)

    def test_shop_username_get(self):
        response = self.user_logged.get((reverse("myshop", kwargs={"username": "vendoruser"})))
        self.assertEquals(response.status_code, 200)

    def test_item_detail_get(self):
        response = self.user_logged.get((reverse("product-detail", kwargs={"pk": 1})))
        self.assertEquals(response.status_code, 200)

    def test_item_delete_post(self):
        response = self.vendor_logged.post(
            (reverse("item-delete", kwargs={"pk": 1})))
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=False)

    def test_category_search_get(self):
        response = self.user_logged.get((reverse("category", kwargs={"category": "Desserts"})))
        self.assertEquals(response.status_code, 200)
