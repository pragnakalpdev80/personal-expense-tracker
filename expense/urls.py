from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static

app_name = "expense"
urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path("login/",views.LoginView.as_view(),name="login"),
    path("logout/",views.LogoutView.as_view(),name="logout"),
    path("dashboard/",views.DashboardView.as_view(),name="dashboard"),
    path("category/",views.CategoryView.as_view(),name="category"),
    path("profile/",views.ProfileView.as_view(),name="profile"),
    path("add/",views.AddExpenseView.as_view(),name="add_expense"),
    path("view/",views.ExpenseView.as_view(),name="all_expense"),
    path('update/<int:pk>/', views.UpdateExpenseView.as_view(), name='update_expense'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset/done/', views.ResetPasswordDoneView.as_view(),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.ResetPasswordConfirmView.as_view(),name='password_reset_confirm'),
    path('password-reset-complete/',views.ResetPasswordCompleteView.as_view(),name='password_reset_complete'),
    path('password-change/',views.ChangePasswordView.as_view(),name='password_change'),
]