from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password',
                               max_length=30,
                               widget=forms.PasswordInput)


class SignUpForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=20)
    last_name = forms.CharField(label='Last Name', max_length=20)
    email_address = forms.EmailField(label='Email Address')
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password',
                               max_length=30,
                               widget=forms.PasswordInput)
