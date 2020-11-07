from django.contrib import admin

from .models import Profile, Vendor, Review

# Register your models here.
admin.site.register(Profile)
admin.site.register(Vendor)
admin.site.register(Review)
