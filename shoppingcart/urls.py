from django.urls import path

from . import views as shoppingcart_views

urlpatterns = [
    path('add-to-cart/<int:item_id>/', shoppingcart_views.add_to_cart, name='add-to-cart'),
    path('order-summary', shoppingcart_views.order_details, name='order-summary'),
    path('update-transaction/<int:order_id>/', shoppingcart_views.update_transaction_records,
         name='update-records'),
    path('order-list', shoppingcart_views.OrdersListView.as_view(), name='order-list'),
    path('item/delete/<int:item_id>/', shoppingcart_views.remove_from_cart, name='remove-item'),
]
