from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views as API_views
from .views import CreateUserAPIView, LogoutUserAPIView, ProfileView, ItemDetailView, AddToCartView, \
    OrderDetailsView, RemoveFromCartView, ShopView, DeleteItemView, UpdateItemView, UpdateProfileView, OthersShop, \
    AddItemView, ReviewView, AddReviewView, SearchView, CategoryView, OrderListView, IsVendorView, VendorUpgradeView, \
    UpdateTransactionView

urlpatterns = [
    path('home/', API_views.Home.as_view(), name='API_home'),
    path('auth/login/', obtain_auth_token, name='API_auth_user_login'),
    path('auth/register/', CreateUserAPIView.as_view(), name='API_auth_user_create'),
    path('auth/logout/', LogoutUserAPIView.as_view(), name='API_auth_user_logout'),
    path('auth/isvendor/', IsVendorView.as_view(), name='API_auth_user_vendor'),
    path('auth/vendorupgrade/', VendorUpgradeView.as_view(), name='API_auth_vendor_upgrade'),
    path('profile/', ProfileView.as_view(), name='API_user_profile'),
    path('profile/edit/<int:pk>', UpdateProfileView.as_view(), name='API_update_profile'),
    path('item/<int:id>/', ItemDetailView.as_view(), name='API_item_detail'),
    path('add-to-cart/', AddToCartView.as_view(), name='API_add_to_cart'),
    path('remove-from-cart/', RemoveFromCartView.as_view(), name='API_remove_from_cart'),
    path('mycart/', OrderDetailsView.as_view(), name='API_my_cart'),
    path('shop/', ShopView.as_view(), name='API_shop'),
    path('shop/others/<int:vid>/', OthersShop.as_view(), name='API_others'),
    path('item_management/delete/', DeleteItemView.as_view(), name='API_delete_item'),
    path('item_management/edit/<int:pk>', UpdateItemView.as_view(), name='API_edit_item'),
    path('item_management/additem/', AddItemView.as_view(), name='API_add_item'),
    path('review/list/<int:vid>/', ReviewView.as_view(), name='API_review_list'),
    path('review/add_review/<int:vid>/', AddReviewView.as_view(), name='API_add_review'),
    path('search/<str:query>/', SearchView.as_view(), name='API_search'),
    path('search/category/<str:category>/', CategoryView.as_view(), name='API_search_category'),
    path('profile/orderlist/', OrderListView.as_view(), name='API_orderlist'),
    path('buy/', UpdateTransactionView.as_view(), name='API_buy'),

]
