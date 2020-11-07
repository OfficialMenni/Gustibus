from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.functions import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView

from marketplace.forms import CartAddProductForm
from marketplace.models import Product
from users.models import Profile
from .extras import generate_order_id
from .models import OrderItem, Order, Transaction


# Create your views here.

def get_user_pending_order(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        return order[0]
    return 0


@login_required
def add_to_cart(request, **kwargs):
    user_profile = get_object_or_404(Profile, user=request.user)
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    n_product = 0
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        n_product = cd['quantity']
    if product.quantity <= 0:
        product.available = False
        product.save()
        messages.warning(request, "Errore! Il prodotto non è disponibile!")
        return render(request, 'marketplace/index.html')
    if product.quantity <= n_product:
        messages.warning(request, "Hai richiesto una quantità di prodotto non disponibile!")
        return redirect('home')
    else:
        product.quantity -= n_product
        if product.quantity <= 0:
            product.available = False
        product.save()
        order_item, status = OrderItem.objects.get_or_create(product=product, quantity=n_product)
        user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
        user_order.items.add(order_item)
        if status:
            user_order.ref_code = generate_order_id()
            user_order.save()
        messages.info(request, "Oggetto aggiunto al carrello.")
    return redirect('home')


@login_required()
def remove_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    n_item = item_to_delete[0].quantity
    if item_to_delete.exists():
        item = item_to_delete[0].product
        item.quantity += n_item
        item.save()
        item_to_delete[0].delete()
        messages.info(request, "Oggetto rimosso correttamente dal carrello.")
        return redirect('order-summary')


@login_required()
def order_details(request):
    existing_order = get_user_pending_order(request)
    context = {'order': existing_order}
    return render(request, 'shoppingcart/order_summary.html', context)


@login_required()
def update_transaction_records(request, order_id):
    order_p = Order.objects.filter(pk=order_id).first()
    order_p.is_ordered = True
    order_p.date_ordered = datetime.datetime.now()
    order_p.save()
    order_items = order_p.items.all()
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())
    messages.success(request, "Ordine completato!")


@login_required()
def update_transaction_records(request, order_id):
    order_to_purchase = get_user_pending_order(request)
    order_total = order_to_purchase.get_cart_total()
    user_profile = get_object_or_404(Profile, user=request.user)
    if user_profile.money < order_total:
        messages.warning(request, "Non hai abbastanza soldi per completare l'ordine. Ricarica il tuo conto!")
        return redirect('profile')
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = timezone.now()
    order_to_purchase.save()
    order_items = order_to_purchase.items.all()
    order_items.update(is_ordered=True, date_ordered=timezone.now())
    user_profile.money = user_profile.money - order_total
    user_profile.save()
    for item in order_items:
        vendor = item.product.vendor
        p_quantity = item.quantity
        p_cost = item.product.cost
        v_instance = Profile.objects.filter(user=vendor.user).first()
        v_instance.money += (p_cost * p_quantity)
        v_instance.save()

    # create a transaction
    transaction = Transaction(profile=request.user.profile,
                              order_id=order_to_purchase.id,
                              amount=order_to_purchase.get_cart_total(),
                              success=True)
    transaction.save()
    messages.info(request, "Grazie! Il tuo acquisto è stato completato correttamente")
    return redirect('home')


class OrdersListView(ListView, LoginRequiredMixin, UserPassesTestMixin):
    model = Order
    template_name = 'shoppingcart/orderlist.html'
    context_object_name = 'Orders'
    paginate_by = 5

    def get_queryset(self):
        user_profile = get_object_or_404(Profile, user=self.request.user)
        return Order.objects.filter(owner=user_profile).order_by('-date_ordered')
