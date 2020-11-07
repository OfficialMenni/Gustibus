from PIL import Image
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    money = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        img = img.resize((300, 300), Image.ANTIALIAS)
        img.save(self.image.path)


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=30)
    mobile = models.CharField(max_length=30)
    description = models.TextField(default="")
    ranksum = models.IntegerField(default=0)
    ranknum = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} Vendor'

    def get_rank(self):
        if self.ranknum != 0:
            return round((self.ranksum / self.ranknum) * 2) / 2
        else:
            return 1


class Review(models.Model):
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewed_vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    title = models.CharField(default="", max_length=100)
    text = models.TextField(default="")
    rank = models.PositiveSmallIntegerField(default=1)
    image = models.ImageField(upload_to='reviews_pics', blank=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {}".format(self.posted_by.username, self.reviewed_vendor.user.username)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        img = img.resize((300, 300), Image.ANTIALIAS)
        img.save(self.image.path)
