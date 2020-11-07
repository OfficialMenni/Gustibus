import unittest

from django.urls import reverse, resolve

from API.views import *


class TestUrls(unittest.TestCase):

    def test_API_home_url(self):
        path = reverse('API_home')
        self.assertEquals(resolve(path).func.view_class, Home)

    def test_API_auth_register_url(self):
        path = reverse('API_auth_user_create')
        self.assertEquals(resolve(path).func.view_class, CreateUserAPIView)

    def test_API_auth_logout_url(self):
        path = reverse('API_auth_user_logout')
        self.assertEquals(resolve(path).func.view_class, LogoutUserAPIView)

    def test_API_auth_user_vendor_url(self):
        path = reverse('API_auth_user_vendor')
        self.assertEquals(resolve(path).func.view_class, IsVendorView)

    def test_API_auth_vendor_upgrade(self):
        path = reverse('API_auth_vendor_upgrade')
        self.assertEquals(resolve(path).func.view_class, VendorUpgradeView)

    def test_API_user_profile_url(self):
        path = reverse('API_user_profile')
        self.assertEquals(resolve(path).func.view_class, ProfileView)

    def test_API_user_update_profile_url(self):
        path = reverse('API_update_profile', kwargs={'pk': 1})
        self.assertEquals(resolve(path).func.view_class, UpdateProfileView)

    def test_API_item_detail_url(self):
        path = reverse('API_item_detail', kwargs={'id': 1})
        self.assertEquals(resolve(path).func.view_class, ItemDetailView)

    def test_API_add_to_cart_url(self):
        path = reverse("API_add_to_cart")
        self.assertEquals(resolve(path).func.view_class, AddToCartView)

    def test_API_remove_from_cart_url(self):
        path = reverse("API_remove_from_cart")
        self.assertEquals(resolve(path).func.view_class, RemoveFromCartView)

    def test_API_order_details_url(self):
        path = reverse("API_my_cart")
        self.assertEquals(resolve(path).func.view_class, OrderDetailsView)

    def test_API_shop_url(self):
        path = reverse("API_shop")
        self.assertEquals(resolve(path).func.view_class, ShopView)

    def test_API_shop_others_url(self):
        path = reverse("API_others", kwargs={'vid': 1})
        self.assertEquals(resolve(path).func.view_class, OthersShop)

    def test_API_delete_item_url(self):
        path = reverse("API_delete_item")
        self.assertEquals(resolve(path).func.view_class, DeleteItemView)

    def test_API_edit_item_url(self):
        path = reverse("API_edit_item", kwargs={'pk': 1})
        self.assertEquals(resolve(path).func.view_class, UpdateItemView)

    def test_API_add_item_url(self):
        path = reverse("API_add_item")
        self.assertEquals(resolve(path).func.view_class, AddItemView)

    def test_API_review_list_url(self):
        path = reverse("API_review_list", kwargs={'vid': 1})
        self.assertEquals(resolve(path).func.view_class, ReviewView)

    def test_API_add_review_list_url(self):
        path = reverse("API_add_review", kwargs={'vid': 1})
        self.assertEquals(resolve(path).func.view_class, AddReviewView)

    def test_API_search_url(self):
        path = reverse("API_search", kwargs={'query': "random"})
        self.assertEquals(resolve(path).func.view_class, SearchView)

    def test_API_search_category_url(self):
        path = reverse("API_search_category", kwargs={'category': "random"})
        self.assertEquals(resolve(path).func.view_class, CategoryView)

    def test_API_order_list_url(self):
        path = reverse("API_orderlist")
        self.assertEquals(resolve(path).func.view_class, OrderListView)

    def test_API_buy_url(self):
        path = reverse("API_buy")
        self.assertEquals(resolve(path).func.view_class, UpdateTransactionView)
