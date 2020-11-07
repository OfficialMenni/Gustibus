import random

from PIL import Image
from django.db import models
from django.db.models import Max

from users.models import Vendor


# Create your models here.

class Product(models.Model):
    PRIMO = 'Main courses'
    SECONDO = 'Steaks'
    DOLCE = 'Desserts'
    BEVANDA = 'Drinks and Beverage'
    DISH_CHOICES = [
        (PRIMO, 'Main courses'),
        (SECONDO, 'Steaks'),
        (DOLCE, 'Desserts'),
        (BEVANDA, 'Drinks and Beverage'),
    ]
    item = models.CharField(max_length=30)
    description = models.TextField()
    category = models.CharField(max_length=30, choices=DISH_CHOICES)
    image = models.ImageField(default='default.jpg', upload_to='item_pics')
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    available = models.BooleanField(default=True)
    quantity = models.IntegerField(default=1)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.item}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        img = img.resize((300, 300), Image.ANTIALIAS)
        img.save(self.image.path)

    def get_random(self):
        max_id = self.objects.all().aggregate(max_id=Max("id"))['max_id']
        if max_id is None:
            max_id = 1
        while True:
            pk = random.randint(1, max_id)
            objj = self.objects.filter(pk=pk, available=True).first()
            if objj:
                return objj
