from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from users.models import Vendor, User, Review
from .forms import ItemRegisterForm, CartAddProductForm
from .models import Product


# Create your views here.
def index(request):
    model = Product
    products = []
    for i in range(9):
        product = model.get_random(model)
        products.append(product)
    products_carousel = model.objects.all().order_by('-date_added')[:3][::-1]
    p1 = products_carousel[0]
    p2 = products_carousel[1]
    p3 = products_carousel[2]
    context = {'products_header': products, 'p1': p1, 'p2': p2, 'p3': p3}
    return render(request, 'marketplace/index.html', context)


@login_required()
def newitem(request):
    user = request.user
    vendor = Vendor.objects.filter(user=user).first()
    if vendor is None:
        messages.error(request, f'Non puoi vendere, non sei un venditore!')
        return redirect('home')
    else:
        if request.method == 'POST':
            form = ItemRegisterForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.vendor = vendor
                instance.save()
                messages.success(request, f'Nuovo oggetto aggiunto!')
                return redirect('product_form')
        else:
            form = ItemRegisterForm()
    return render(request, 'marketplace/product_form.html', {'form': form})


@login_required()
def shop(request):
    username = request.user.username
    return redirect(username + "/")


class VendorItemListView(ListView, LoginRequiredMixin, UserPassesTestMixin):
    model = Product
    template_name = 'marketplace/myshop.html'
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        vendor = Vendor.objects.filter(user=user).first()
        return Product.objects.filter(vendor=vendor).order_by('-date_added')

    def get_context_data(self, **kwargs):
        # Return custom data to the page
        rank = None
        isVendor = False
        context = super(VendorItemListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        vendor = Vendor.objects.filter(user=user).first()
        if vendor is not None:
            isVendor = True
            rank = vendor.get_rank()
        if not rank:
            rank = ""
        else:
            rank = str(rank) + "/5"
        reviews = Review.objects.filter(reviewed_vendor=vendor).order_by('-date')
        context['owner'] = user
        context['reviews'] = reviews
        context['rank'] = rank
        context['isVendor'] = isVendor
        return context


class ItemDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        # Return custom data to the page
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context['form'] = CartAddProductForm()
        return context


class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['item', 'description', 'category', 'image', 'cost', 'available', 'quantity']
    success_url = reverse_lazy("shop")

    def form_valid(self, form):
        vendor = Vendor.objects.filter(user=self.request.user).first()
        form.instance.vendor = vendor
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        vendor = Vendor.objects.filter(user=self.request.user).first()
        if vendor == item.vendor:
            return True
        return False


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("home")

    def test_func(self):
        item = self.get_object()
        vendor = Vendor.objects.filter(user=self.request.user).first()
        if vendor == item.vendor:
            return True
        return False


class SearchView(ListView):
    model = Product
    template_name = 'marketplace/search.html'
    context_object_name = 'all_search_results'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            postresult = Product.objects.filter(item__contains=query).order_by('-date_added')
            result = postresult
        else:
            result = ""
        return result


class CategoryView(ListView):
    model = Product
    template_name = 'marketplace/category.html'
    context_object_name = 'all_results'
    paginate_by = 5

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs.get("category")).order_by('-date_added')

    def get_context_data(self, **kwargs):
        # Return custom data to the page
        context = super(CategoryView, self).get_context_data(**kwargs)
        context['category'] = self.kwargs.get("category")
        return context
