from django.shortcuts import render
from django.http import HttpResponse


from .forms import LoginForm, SignUpForm


def login(request):

    if request.method == 'POST':
        print("Here is the login Logic")
        return HttpResponse("Login Login")

    else:
        login_form = LoginForm()
        return render(request=request,
                      template_name='login.html',
                      context={'login_form': login_form})


def signup(request):

    if request.method == 'POST':
        return HttpResponse("Sign Up Logic")

    else:
        signup_form = SignUpForm()
        return render(request=request,
                      template_name='signup.html',
                      context={'signup_form': signup_form})
