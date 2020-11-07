import unittest

from django.urls import reverse, resolve

from marketplace.views import *


class TestUrls(unittest.TestCase):

    def test_product_form_url(self):
        path = reverse('product_form')
        self.assertEquals(resolve(path).func, newitem)

    def test_shop_url(self):
        path = reverse('shop')
        self.assertEquals(resolve(path).func, shop)

    def test_product_detail_view_url(self):
        path = reverse('product-detail', kwargs={'pk': "1"})
        self.assertEquals(resolve(path).func.view_class, ItemDetailView)

    def test_vendor_private_shop_url(self):
        path = reverse('myshop', kwargs={'username': "Menni"})
        self.assertEquals(resolve(path).func.view_class, VendorItemListView)

    def test_item_update_url(self):
        path = reverse('item-update', kwargs={'pk': "1"})
        self.assertEquals(resolve(path).func.view_class, ItemUpdateView)

    def test_item_delete_url(self):
        path = reverse('item-delete', kwargs={'pk': "1"})
        self.assertEquals(resolve(path).func.view_class, ItemDeleteView)

    def test_results_url(self):
        path = reverse('search')
        self.assertEquals(resolve(path).func.view_class, SearchView)

    def test_category_filter_url(self):
        path = reverse('category', kwargs={'category': "Drinks and Beverage"})
        self.assertEquals(resolve(path).func.view_class, CategoryView)
