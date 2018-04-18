from django import forms
from django.core.validators import EmailValidator


class LoginForm(forms.Form):
    username = forms.CharField(label='',
                               max_length=20,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='',
                               max_length=30,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


ACCOUNT_TYPES = (
    ('S', 'Seller'),
    ('B', 'Buyer'),
)


class SignUpForm(forms.Form):
    first_name = forms.CharField(label='',
                                 required=True,
                                 max_length=20,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))

    last_name = forms.CharField(label='',
                                required=True,
                                max_length=20,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    email_address = forms.CharField(label='',
                                    required=False,
                                    max_length=40,
                                    widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))

    username = forms.CharField(label='',
                               required=True,
                               max_length=20,
                               widget=forms.TextInput(attrs={'placeholder': 'Username'}))

    password = forms.CharField(label='',
                               required=True,
                               max_length=30,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    account_type = forms.MultipleChoiceField(label='',
                                             required=True,
                                             choices=ACCOUNT_TYPES,
                                             widget=forms.CheckboxSelectMultiple)


class EditProfileForm(forms.Form):
    first_name = forms.CharField(label='',
                                 required=True,
                                 max_length=20,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}))

    last_name = forms.CharField(label='',
                                required=True,
                                max_length=20,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))

    email_address = forms.EmailField(label='',
                                     required=False,
                                     validators=[EmailValidator],
                                     widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))

    password = forms.CharField(label='',
                               required=False,
                               max_length=30,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Reset Password'}))


class StoreEditForm(forms.Form):
    store_name = forms.CharField(label='',
                                 required=True,
                                 max_length=30,
                                 widget=forms.TextInput(attrs={'placeholder': 'Store Name'}))
