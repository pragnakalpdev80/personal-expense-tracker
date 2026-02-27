from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import generate_token
from django.shortcuts import render, get_object_or_404,redirect
from django.views import generic, View
from django.core.mail import EmailMessage
from .forms import CustomUserCreationForm
from .models import User
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
            print("Hello")
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Expense Tracker account.'
            message = render_to_string('active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':generate_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            form.save()
            return redirect('/expense/login/')    
        else:   
            print(" No Hello") 
            messages.error(request, "Email is wrong or Password not matched")
            return redirect('/expense/register/')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "User Verified")
        return redirect('/expense/login/')
    else:
        return HttpResponse('Activation link is invalid!')
            
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
        if not request.user.is_authenticated:
            return redirect("/expense/login")
        return render(request, self.template_name)
