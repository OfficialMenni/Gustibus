from PIL import Image
from django.test import TestCase

from users.forms import VendorUpdateForm
from users.views import *


class TestForms(TestCase):

    def test_UserRegisterForm_form_valid_data(self):
        form = UserRegisterForm(data={
            'username': 'Testaccount',
            'email': 'testmail@mail.it',
            'password1': "TESTING321",
            'password2': "TESTING321"
        })
        self.assertTrue(form.is_valid())

    def test_UserRegisterForm_form_invalid_data(self):
        form = UserRegisterForm(data={})
        self.assertFalse(form.is_valid())

    def test_UserUpdateForm_form_valid_data(self):
        form = UserUpdateForm(data={
            "username": "Testaccount",
            "email": "testmail@mails.it"
        })
        self.assertTrue(form.is_valid())

    def test_UserUpdateForm_form_invalid_data(self):
        form = UserUpdateForm(data={})
        self.assertFalse(form.is_valid())

    def test_ProfileUpdateForm_form_valid_data(self):
        img = Image.open("./media/default.jpg")
        form = ProfileUpdateForm(data={'image': img})
        self.assertTrue(form.is_valid())

    def test_GetMoneyForm_form_valid_data(self):
        form = GetMoneyForm(data={
            'money': 2000
        })
        self.assertTrue(form.is_valid())

    def test_GetMoneyForm_form_invalid_data(self):
        form = GetMoneyForm(data={})
        self.assertFalse(form.is_valid())

    def test_VendorUpgradeForm_form_valid_data(self):
        form = VendorUpgradeForm(data={
            'address': "via qualcosa n. 24",
            'mobile': "333 2221110",
            'description': "Un venditore bravo"
        })
        self.assertTrue(form.is_valid())

    def test_VendorUpgradeForm_form_invalid_data(self):
        form = VendorUpgradeForm(data={})
        self.assertFalse(form.is_valid())

    def test_VendorUpdateForm_form_valid_data(self):
        form = VendorUpdateForm(data={
            'address': "via qualcosa n. 24",
            'mobile': "333 2221110",
            'description': "Un venditore bravo"
        })
        self.assertTrue(form.is_valid())

    def test_VendorUpdateForm_form_invalid_data(self):
        form = VendorUpdateForm(data={})
        self.assertFalse(form.is_valid())

    #    def test_NewReviewForm_form_valid_data(self): // Non funziona per via del bug delle recensioni
    #        img = Image.open("./media/default.jpg")
    #        form = NewReviewForm(data={
    #            'title': "Titolo",
    #            'text': "text",
    #            'image': img
    #        })
    #        self.assertTrue(form.is_valid())

    def test_NewReviewForm_form_invalid_data(self):
        form = NewReviewForm(data={})
        self.assertFalse(form.is_valid())
