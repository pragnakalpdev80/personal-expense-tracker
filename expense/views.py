import datetime
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum    
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView, PasswordChangeView
from django.views.generic.edit import FormView
from django.views.generic import CreateView,UpdateView,DeleteView
from django.contrib.messages.views import SuccessMessageMixin
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
from .forms import CustomUserCreationForm, ProfileForm, CategoryForm, ExpenseForm
from .models import User, Profile, Category, Expense
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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            Profile.objects.create(user=user)
            current_site = get_current_site(request)
            mail_subject = 'Activate your Expense Tracker account'
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
        login(request, user)
        return redirect('/expense/dashboard/')
    else:
        return HttpResponse('Activation link is invalid!')
            
class LoginView(LoginView):
    template_name = 'expense/login.html'

class LogoutView(View):
    def post(self,request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('/expense/login/')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'expense/password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('expense:login')

class ResetPasswordDoneView(PasswordResetDoneView):
    template_name='password_reset_done.html'

class ResetPasswordConfirmView(PasswordResetConfirmView):
    template_name='password_reset_confirm.html'

class ResetPasswordCompleteView(PasswordResetCompleteView):
    template_name='password_reset_complete.html'

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'expense/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('expense:dashboard')

class DashboardView(View):
    model = Profile
    template_name = 'expense/dashboard.html'
    context_object_name = 'profile'
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/expense/login")
        
        today = datetime.date.today()
        
        monthly_expenses = Expense.objects.filter(
            user=request.user,
            date__month=today.month,
            date__year=today.year
        )

        total_monthly = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        category_totals = monthly_expenses.values('category__name').annotate(total=Sum('amount')).order_by('-total')
        recent_transactions = Expense.objects.filter(user=request.user).order_by('-date')[:5]

        context = {
            'total_monthly': total_monthly,
            'category_totals': category_totals,
            'recent_transactions': recent_transactions,
            'current_month_name': today.strftime("%B"),
        }
        return render(request, self.template_name, context)

    def get_object(self):
        return Profile.objects.get(id=self.kwargs.get("id"))

class ProfileView(View):
    profile = Profile.objects.all()

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'expense/profile.html', { 'form': form, 'profile': request.user.profile})  
    
    def post(self, request):
        form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('expense:dashboard')
        
class CategoryView(View):
    template_name = 'expense/category.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/expense/login/')
            
        categories = Category.objects.filter(user=request.user)
        
        return render(request, self.template_name, {'categories': categories})

    def post(self, request):
        action = request.POST.get('action')
        confirm = request.POST.get('confirm')

        if confirm:
            user = get_object_or_404(Profile, user_id=request.user.id)
            user.category_confirmed = True
            user.save()

        if action == 'create':
            category_name = request.POST.get('name') 
            
            if category_name:
                Category.objects.create(
                    user=request.user, 
                    name=category_name, 
                    is_default=False
                )
                messages.success(request, "New category added!")

        elif action == 'update':
            category_id = request.POST.get('category_id')
            new_name = request.POST.get('name')
            
            category = get_object_or_404(Category, id=category_id, user=request.user)
            
            if new_name:
                category.name = new_name
                category.save()
                messages.success(request, "Category updated successfully!")

        elif action == 'delete':
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, id=category_id, user=request.user)
            expense_exist = Expense.objects.filter(category_id=category_id)
            if expense_exist:
                print("Hello")
                messages.error(request, f"Cannot Delete {category} category because expense with this category already exists.")
            else:
                print("Bye")
                category.delete()
                messages.success(request, "Category deleted.")

        return redirect('expense:category')

class AddExpenseView(View):
    template_name = 'expense/add_expense.html'

    def get_daily_context(self, user):
        today = datetime.date.today()
        todays_expenses = Expense.objects.filter(user=user, date=today)
        
        total_today = todays_expenses.aggregate(Sum('amount'))['amount__sum']
        
        if total_today is None:
            total_today = 0
            
        category_totals = todays_expenses.values('category__name').annotate(total=Sum('amount'))

        return {
            'todays_expenses': todays_expenses,
            'total_today': total_today,
            'category_totals': category_totals,
        }

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/expense/login/')
            
        if not request.user.profile.category_confirmed:
            messages.error(request, "Please confirm your categories before adding expenses.")
            return redirect('expense:category')
        form = ExpenseForm(user=request.user)
        context = self.get_daily_context(request.user)
        context['form'] = form
        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/expense/login/')
        
        form = ExpenseForm(request.user, request.POST)
        
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            
            messages.success(request, "Expense added successfully!")
            return redirect('expense:add_expense') 
            
        context = self.get_daily_context(request.user)
        context['form'] = form
        
        return render(request, self.template_name, context)