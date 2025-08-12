from django.shortcuts import render
from core.decorators import jwt_required

# Create your views here.

@jwt_required
def user_home(request):
    return render(request, 'user_home.html')