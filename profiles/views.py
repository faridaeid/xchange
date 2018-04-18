from django.shortcuts import render, redirect
from django.db import connection
from django.views import View

from .forms import LoginForm, SignUpForm, EditProfileForm, StoreEditForm
from .models import User
import datetime

from Encryption import Encryption

class StartPageView(View):
    template_name = 'start_page.html'
    loginForm = LoginForm
    signupForm = SignUpForm
    encryption = Encryption()

    def get(self, request):
        if request.session.get('user_id') is not None:
            return redirect('homepage_view')

        login_form = self.loginForm()
        signup_form = self.signupForm()
        return render(request=request,
                      template_name=self.template_name,
                      context={'login_form': login_form,
                               'signup_form': signup_form})


class LoginView(StartPageView):
    def post(self, request):

        form = self.loginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            enc_username = self.encryption.encrypt(username)
            enc_password = self.encryption.encrypt(password)

            users = User.objects.raw('''SELECT * 
                                        FROM user
                                        WHERE username = "{}" '''.format(enc_username))

            if not len(list(users)) or str(enc_password) != str(list(users)[0].password):

                if not len(list(users)):
                    error_mess = "Username doesn't exists"
                else:
                    error_mess = "Incorrect password"

                return render(request=request,
                              template_name=self.template_name,
                              context={'login_form': form,
                                       'signup_form': self.signupForm(),
                                       'error_mess': error_mess})

            else:
                user_id = list(users)[0].user_id
                request.session['username'] = username
                request.session['user_id'] = user_id
                return redirect('homepage_view')


class SignupView(StartPageView):
    def post(self, request):

        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            enc_username = self.encryption.encrypt(username)
            users = User.objects.raw('''SELECT * 
                                        FROM user 
                                        WHERE username = "{}" '''.format(enc_username))

            if len(list(users)):
                error_mess = "Username already exists"
                return render(request=request,
                              template_name=self.template_name,
                              context={'login_form': self.loginForm(),
                                       'signup_form': form,
                                       'error_mess': error_mess,
                                       'signup_error': True})
            else:

                with connection.cursor() as cursor:

                    enc_password = self.encryption.encrypt(data['password'])

                    cursor.execute('''INSERT INTO user 
                              (first_name, last_name, username, password, email_address)
                              VALUES ("{}", "{}", "{}", "{}", "{}")'''
                                   .format(data['first_name'], data['last_name'], enc_username, enc_password,
                                           data['email_address']))

                    user_id = cursor.lastrowid

                    for account_type in list(data['account_type']):
                        if account_type[0] == 'S':
                            date = datetime.date.today().strftime('%Y-%m-%d')
                            cursor.execute('''INSERT INTO store
                                       (store_name, create_date, owner_id) VALUES ("{}", "{}", "{}")'''
                                           .format('{} Store'.format(username), date, user_id))
                        else:
                            cursor.execute('''INSERT INTO cart (owner_id) VALUES ("{}")'''
                                           .format(user_id))

                # request.session['username'] = username
                request.session['user_id'] = user_id
                return redirect('homepage_view')


class EditProfileView(View):
    form = EditProfileForm
    store_form = StoreEditForm
    template_name = 'edit_profile.html'

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute('''SELECT S.store_name FROM store S, user U 
                              WHERE S.owner_id = U.user_id AND U.user_id = "{}"'''.format(request.session['user_id']))

            (store_name,) = cursor.fetchone()
            print(store_name)
            user_info = list(User.objects.raw('''SELECT * FROM user WHERE user_id = "{}"'''
                                              .format(request.session['user_id'])))[0]

            edit_profile_form = self.form(initial={'first_name': user_info.first_name,
                                                   'last_name': user_info.last_name,
                                                   'email_address': user_info.email_address})
            store_form = self.store_form(initial={'store_name': store_name})
            return render(request,
                          template_name=self.template_name,
                          context={'form': edit_profile_form,
                                   'store_form': store_form})

    def post(self, request):
        with connection.cursor() as cursor:
            if 'update_btn' in request.POST:

                form = self.form(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    cursor.execute('''UPDATE user SET first_name = "{}", last_name = "{}", email_address = "{}"
                                              WHERE user_id = "{}"'''
                                   .format(data['first_name'], data['last_name'], data['email_address'],
                                           request.session['user_id']))
                    if data['password'] != '':
                        cursor.execute('''UPDATE user SET password = "{}" WHERE user_id = "{}"'''
                                       .format(data['password'], request.session['user_id']))
            else:
                form = self.store_form(request.POST)
                if form.is_valid():
                    data = form.cleaned_data
                    request.session['store_name'] = data['store_name']
                    cursor.execute('''SELECT S.store_id FROM store S, user U 
                                      WHERE S.owner_id = U.user_id AND U.user_id = "{}"'''
                                   .format(request.session['user_id']))
                    (store_id,) = cursor.fetchone()
                    cursor.execute('''UPDATE store SET store_name = "{}" WHERE store_id = "{}"'''
                                   .format(data['store_name'], store_id))

            return redirect('homepage_view')
