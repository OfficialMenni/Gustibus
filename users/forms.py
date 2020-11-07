from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Vendor, Review


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class GetMoneyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['money']


class VendorUpgradeForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['address', 'mobile', 'description']


class VendorUpdateForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['address', 'mobile', 'description']


class NewReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'text', 'image']


class NewRankForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewRankForm, self).__init__(*args, **kwargs)
        self.fields['ranksum'].widget.attrs['min'] = 1
        self.fields['ranksum'].widget.attrs['max'] = 5

    class Meta:
        model = Vendor
        fields = ['ranksum']
        labels = {'ranksum': 'Rank'}
