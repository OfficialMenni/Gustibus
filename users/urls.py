from django.contrib.auth import views as auth_views
from django.urls import path

from . import views as user_views

urlpatterns = [

    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('upgrade/', user_views.upgrade, name='upgrade'),
    path('vendors_list/', user_views.vendors_list, name='vendors_list'),
    path('vendor_profile_update/<int:pk>/', user_views.VendorProfileUpdate.as_view(),
         name='vendor-profile-update'),
    path('get_money/', user_views.get_money, name='more-money'),
    path('new_review/<int:uid>/<int:vid>/', user_views.new_review, name='new-review'), ]
