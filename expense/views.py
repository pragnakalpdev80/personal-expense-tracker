from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404,redirect
from django.views import generic, View
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class RegistrationView(View):
    def get(self, request):
        # if request.user.is_authenticated:
        #     return redirect("/expense/dashboard")
        form = CustomUserCreationForm()
        return render(request, 'expense/register.html', { 'form': form})  
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/expense/login/')        
        # messages.info(request, "Account created Successfully!")
        
class LoginView(LoginView):
    template_name = 'expense/login.html'

class LogoutView(View):
    def post(self,request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('/expense/login/')

class DashboardView(View):
    template_name = 'expense/dashboard.html'
    def get(self, request):
        return render(request, self.template_name)
