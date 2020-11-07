import unittest

from django.contrib.auth import views as auth_views
from django.urls import reverse, resolve

from users.views import *


class TestUrls(unittest.TestCase):

    def test_nuova_recensione_url(self):
        path = reverse('register')
        self.assertEquals(resolve(path).func, register)

    def test_profile_url(self):
        path = reverse('profile')
        self.assertEquals(resolve(path).func, profile)

    def test_login_url(self):
        path = reverse('login')
        self.assertEquals(resolve(path).func.view_class, auth_views.LoginView)

    def test_logout_url(self):
        path = reverse('logout')
        self.assertEquals(resolve(path).func.view_class, auth_views.LogoutView)

    def test_upgrade_url(self):
        path = reverse('upgrade')
        self.assertEquals(resolve(path).func, upgrade)

    def test_vendors_list_url(self):
        path = reverse('vendors_list')
        self.assertEquals(resolve(path).func, vendors_list)

    def test_vendor_profile_update_url(self):
        path = reverse('vendor-profile-update', kwargs={'pk': 1})
        self.assertEquals(resolve(path).func.view_class, VendorProfileUpdate)

    def test_money_update_url(self):
        path = reverse('more-money')
        self.assertEquals(resolve(path).func, get_money)

    def test_new_review_url(self):
        path = reverse("new-review", kwargs={"uid": 1, "vid": 2})
        self.assertEquals(resolve(path).func, new_review)
