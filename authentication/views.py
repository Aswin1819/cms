from django.shortcuts import render,redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import set_jwt_cookies
import logging

logger = logging.getLogger(__name__)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("User registered successfully..")
            return redirect('login')
        else:
            logger.error(f"form is not valid:{form.errors}")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form':form})



def login_view(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                
                response = redirect('admin_posts' if user.is_superuser else 'user_home')
                response = set_jwt_cookies(response,access_token, str(refresh) )
                logger.info('user login successfully')
                return response
            else:
                logger.warning("Invalid login attempt")
                return render(request,'login.html', {'form':form,'error':'Invalid Credentials'})
        else:
            logger.info('Invalid form ')
            return render(request, 'login.html', {'form':form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})

                
            
