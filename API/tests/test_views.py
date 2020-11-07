from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from shoppingcart.views import *
from users.models import Vendor, Profile


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="resu", password="TESTING321")
        self.user_vendor = User.objects.create_user(username="vendoruser", password="TESTING321")
        self.profile = Profile.objects.get(user=self.user)
        self.user_logged = APIClient()
        self.vendor_logged = APIClient()
        self.admin_user = User.objects.create_superuser(username="Super", password="TESTING321")
        self.admin_user_logged = APIClient()
        self.admin_user_logged.force_login(self.admin_user)
        self.vendor = Vendor.objects.create(user=self.user_vendor, address="indirizzo", mobile="123456789",
                                            description="ABCDEFGH", ranknum=0, ranksum=0)
        self.product = Product.objects.create(item="test", description="testd", category="Desserts",
                                              cost=10, available=True,
                                              vendor=self.vendor)
        self.user_logged.force_authenticate(user=self.user)
        self.vendor_logged.force_authenticate(self.user_vendor)
        self.order_item = OrderItem.objects.get_or_create(product=self.product, quantity=10)
        self.user_order = Order.objects.get_or_create(owner=self.profile, is_ordered=False)
        self.user_order_true = Order.objects.get_or_create(owner=self.profile, is_ordered=True)

    def test_profile_view_get(self):
        response = self.user_logged.get((reverse("API_user_profile")))
        self.assertTrue(response.status_code, 200)

    def test_profile_edit_post(self):
        response = self.user_logged.get((reverse("API_update_profile", kwargs={"pk": 1})))
        self.assertTrue(response.status_code, 200)

    def test_isVendor_false(self):
        response = self.user_logged.get((reverse("API_auth_user_vendor")))
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response, False)

    def test_isVendor_true(self):
        response = self.vendor_logged.get((reverse("API_auth_user_vendor")))
        self.assertTrue(response.status_code, 200)
        self.assertTrue(response, True)

    def test_vendor_upgrade_post(self):
        response = self.vendor_logged.post((reverse("API_auth_vendor_upgrade"), {
            "user": self.user,
            "address": "via di prova",
            "mobile": "9876543210",
            "description": "Descrizione di prova"
        }))
        self.assertTrue(response.status_code, 200)

    def test_vendor_upgrade_post_fail(self):
        response = self.vendor_logged.post((reverse("API_auth_vendor_upgrade"), {
            "user": self.user,
            "address": "via di prova",
            "description": "Descrizione di prova"
        }))
        self.assertTrue(response.status_code, 403)

    def test_item_detail_get(self):
        response = self.user_logged.get((reverse("API_item_detail", kwargs={'id': 1})))
        self.assertTrue(response.status_code, 200)

    def test_add_to_cart_post_success(self):
        response = self.user_logged.post((reverse("API_add_to_cart"), {"item_id": 1, "item_quantity": 5}))
        self.assertTrue(response.status_code, 200)

    def test_add_to_cart_post_fail_quantity_too_big(self):
        response = self.user_logged.post((reverse("API_add_to_cart"), {"item_id": 1, "item_quantity": 50000}))
        self.assertTrue(response.status_code, 412)

    def test_add_to_cart_post_fail_malformed(self):
        response = self.user_logged.post((reverse("API_add_to_cart"), {"item_quantity": 50000}))
        self.assertTrue(response.status_code, 406)

    def test_remove_item_from_cart_post_success(self):
        response = self.user_logged.post((reverse("API_remove_from_cart"), {"item_id": 1}))
        self.assertTrue(response.status_code, 200)

    def test_remove_item_from_cart_post_fail(self):
        response = self.user_logged.post((reverse("API_remove_from_cart"), {"item_id": 10}))
        self.assertTrue(response.status_code, 412)

    def test_mycart_get(self):
        response = self.user_logged.get((reverse("API_my_cart")))
        self.assertTrue(response.status_code, 200)

    def test_shop_get_noshop(self):
        response = self.user_logged.get((reverse("API_shop")))
        self.assertTrue(response.status_code, 404)

    def test_shop_get_isVendor(self):
        response = self.vendor_logged.get((reverse("API_shop")))
        self.assertTrue(response.status_code, 200)

    def test_others_shop_get(self):
        response = self.user_logged.get((reverse("API_others", kwargs={"vid": 1})))
        self.assertTrue(response.status_code, 200)

    def test_others_shop_get_invalid(self):
        response = self.user_logged.get((reverse("API_others", kwargs={"vid": 3223929})))
        self.assertTrue(response.status_code, 404)

    def test_delete_item_post_success(self):
        response = self.vendor_logged.post((reverse("API_delete_item"), {"id": 1}))
        self.assertTrue(response.status_code, 200)

    def test_delete_item_post_forbidden(self):
        response = self.user_logged.post((reverse("API_delete_item"), {"id": 1}))
        self.assertTrue(response.status_code, 403)

    def test_delete_item_post_malformed_id(self):
        response = self.user_logged.post((reverse("API_delete_item"), {"id": "sfj"}))
        self.assertTrue(response.status_code, 406)

    def test_edit_item_put_success(self):
        response = self.vendor_logged.put((reverse("API_edit_item", kwargs={"pk": 1}), {"item": "testuzzo",
                                                                                        "description": "testing321",
                                                                                        "cost": 5, "quantity": 100}))
        self.assertTrue(response.status_code, 200)

    def test_edit_item_put_forbidden(self):
        response = self.user_logged.put((reverse("API_edit_item", kwargs={"pk": 1}), {"item": "testuzzo",
                                                                                      "description": "testing321",
                                                                                      "cost": 5, "quantity": 100}))
        self.assertTrue(response.status_code, 403)

    def test_edit_item_put_malformed(self):
        response = self.user_logged.put((reverse("API_edit_item", kwargs={"pk": 1}), {"description": "testing321",
                                                                                      "cost": 5, "quantity": 100}))
        self.assertTrue(response.status_code, 406)

    def test_review_list_get(self):
        response = self.user_logged.get((reverse("API_review_list", kwargs={"vid": 1})))
        self.assertTrue(response.status_code, 200)

    def test_review_list_get_fail(self):
        response = self.user_logged.get((reverse("API_review_list", kwargs={"vid": 1445})))
        self.assertTrue(response.status_code, 404)

    def test_search_query_get(self):
        response = self.user_logged.get((reverse("API_search", kwargs={"query": "test"})))
        self.assertTrue(response.status_code, 200)

    def test_search_query_category_get(self):
        response = self.user_logged.get((reverse("API_search_category", kwargs={"category": "Desserts"})))
        self.assertTrue(response.status_code, 200)

    def test_order_list_get(self):
        response = self.user_logged.get((reverse("API_orderlist")))
        self.assertTrue(response.status_code, 200)

    def test_buy_get(self):
        response = self.user_logged.get((reverse("API_buy")))
        self.assertTrue(response.status_code, 200)
