from django.urls import path

from . import views as marketplace_views

urlpatterns = [
    path('product_form/', marketplace_views.newitem, name='product_form'),
    path('shop/', marketplace_views.shop, name='shop'),
    path('shop/<str:username>/', marketplace_views.VendorItemListView.as_view(), name='myshop'),
    path('product/<int:pk>/', marketplace_views.ItemDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update/', marketplace_views.ItemUpdateView.as_view(), name='item-update'),
    path('product/<int:pk>/delete/', marketplace_views.ItemDeleteView.as_view(), name='item-delete'),
    path('results/', marketplace_views.SearchView.as_view(), name='search'),
    path('category/<str:category>/', marketplace_views.CategoryView.as_view(), name='category'),
]
