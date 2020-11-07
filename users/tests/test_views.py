from PIL import Image
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from users.forms import *
from users.models import Profile


class LogInTest(TestCase):
    def setUp(self):
        self.credentials = {
            'username': 'test',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        c = Client()
        res = c.login(username='test', password='secret')
        self.assertTrue(res, 'Login fallito: credenziali non corrette\n')


class RegistrationTest(TestCase):
    def test_registration(self):
        c = Client()
        res = c.post(reverse('register'), data={
            'username': 'test',
            'email': 'test@gmail.it',
            'password': 'secret',
            'password2': 'secret'})
        self.assertTrue(res.status_code == 200, 'Registrazione fallita')


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="resu", password="TESTING321")
        self.user_vendor = User.objects.create_user(username="vendoruser", password="TESTING321")
        self.profile = Profile.objects.get(user=self.user)
        self.user_logged = Client()
        self.vendor_logged = Client()
        self.vendor_logged.login(username="vendoruser", password="TESTING321")
        self.user_logged.force_login(self.user)
        self.admin_user = User.objects.create_superuser(username="Super", password="TESTING321")
        self.admin_user_logged = Client()
        self.admin_user_logged.login(username="Super", password="TESTING321")
        self.vendor = Vendor.objects.create(user=self.user_vendor, address="indirizzo", mobile="123456789",
                                            description="ABCDEFGH", ranknum=0, ranksum=0)

    def test_update_money_get(self):
        response = self.user_logged.get(reverse("more-money"))
        self.assertEqual(response.status_code, 200)

    def test_update_money_post(self):
        response = self.user_logged.post((reverse("more-money")), data={"money": 5000})
        balance = int(Profile.objects.filter(user=self.user).first().money)
        self.assertEqual(balance, 5000)
        self.assertRedirects(response, '/users/profile/', status_code=302,
                             target_status_code=200, fetch_redirect_response=True)

    def test_update_profile(self):
        response = self.user_logged.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_upgrade_vendor_get(self):
        response = self.user_logged.get(reverse("upgrade"))
        self.assertEqual(response.status_code, 200)

    def test_upgrade_vendor_post(self):
        response = self.user_logged.post((reverse("upgrade")),
                                         data={'address': 'prova', 'mobile': '33301012', 'description': "test",
                                               "ranksum": 2, "ranknum": 1})
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200, fetch_redirect_response=False)

    def test_vendorlist(self):
        response = self.admin_user_logged.get(reverse("vendors_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/vendors_list.html')

    def test_newreview(self):
        response = self.user_logged.get(reverse("new-review", kwargs={"uid": 1, "vid": 1}))
        self.assertEqual(response.status_code, 200)

    def test_newreview_post(self):
        img = Image.open("./media/default.jpg")
        response = self.user_logged.post(reverse("new-review", kwargs={"uid": 1, "vid": 1}),
                                         data={'r_form': {"title": "titolo",
                                                          "text": "text",
                                                          "image": img, },
                                               "rank": {"ranksum": 3}})
        self.assertTrue(response.status_code, 200)
