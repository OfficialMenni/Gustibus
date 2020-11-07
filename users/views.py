from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, VendorUpgradeForm, GetMoneyForm, \
    NewReviewForm, NewRankForm
from .models import Vendor


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Il tuo account è stato creato. Ora puoi effettuare il login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required()
def get_money(request):
    if request.method == 'POST':
        form = GetMoneyForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, f'Il tuo credito è stato correttamente modificato.')
            return redirect('profile')
    else:
        form = GetMoneyForm()
    return render(request, 'users/get_money.html', {'form': form})


@login_required
def profile(request):
    vendor = Vendor.objects.filter(user=request.user).first()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profilo aggiornato correttamente.')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'vendor': vendor
    }
    return render(request, 'users/profile.html', context)


@login_required
def upgrade(request):
    if request.method == 'POST':
        user = request.user
        sk = Vendor.objects.filter(user=user)
        if not sk:
            form = VendorUpgradeForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                messages.success(request,
                                 f'Procedura completata. Ora sei un venditore e puoi iniziare a vendere i tuoi oggetti. Visita il tuo shop per vendere il primo prodotto!')
        else:
            messages.error(request, f'Sei già un venditore!')
        return redirect('home')
    else:
        form = VendorUpgradeForm(instance=request.user)
    context = {'form': form}
    return render(request, 'users/upgrade.html', context)


@staff_member_required
def vendors_list(request):
    context = {'vendors': Vendor.objects.all()}
    return render(request, 'users/vendors_list.html', context)


class VendorProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Vendor
    fields = ['address', 'mobile', 'description']
    template_name = 'users/vendor_profile_update.html'
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        messages.success(self.request, 'Profilo venditore aggiornato.')
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        vendor = Vendor.objects.filter(user=self.request.user).first()
        if user == vendor:
            return True
        return False


@login_required()
def new_review(request, uid, vid):
    vendor = Vendor.objects.filter(id=vid).first()
    user = request.user
    if request.method == 'POST':
        r_form = NewReviewForm(request.POST, request.FILES)
        rank = NewRankForm(request.POST)
        if r_form.is_valid() and rank.is_valid():
            instance = r_form.save(commit=False)
            instance.reviewed_vendor = vendor
            instance.posted_by = user
            instance.rank = rank.cleaned_data.get("ranksum")
            vendor.ranksum = vendor.ranksum + rank.cleaned_data.get("ranksum")
            vendor.ranknum += 1
            vendor.save()
            instance.save()
            messages.success(request, f'La tua recensione è stata postata.')
            return redirect('home')
    else:
        r_form = NewReviewForm()
        rank = NewRankForm
    return render(request, 'users/new_review.html', {'form': r_form,
                                                     'rank_form': rank})
