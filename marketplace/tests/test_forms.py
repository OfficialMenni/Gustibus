from PIL import Image
from django.test import TestCase

from marketplace.forms import *


class TestForms(TestCase):

    def test_ItemRegisterForm_form_valid_data(self):
        img = Image.open("./media/default.jpg")
        form = ItemRegisterForm(data={
            'item': 'TestItem',
            'description': 'item test',
            'category': "Desserts",
            'image': img,
            'cost': 50,
            'available': True,
            'quantity': 10
        })
        self.assertTrue(form.is_valid())

    def test_CartAddProductForm_form_valid_data(self):
        form = CartAddProductForm(data={
            'quantity': 5,
        })
        self.assertTrue(form.is_valid())

    def test_ItemRegisterForm_form_invalid_data(self):
        form = ItemRegisterForm(data={})
        self.assertFalse(form.is_valid())

    def test_CartAddProductForm_form_invalid_data(self):
        form = CartAddProductForm(data={})
        self.assertFalse(form.is_valid())
