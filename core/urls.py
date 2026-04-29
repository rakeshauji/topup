from django.urls import path, include
from . import views
from .views import chatbot_api
from django.contrib.auth import views as auth_views

urlpatterns = [

    # Home
    path('', views.home, name='home'),

    # Game & Package
    path('game/<int:game_id>/', views.game_detail, name='game_detail'),
    path('package/<int:id>/', views.package_detail, name='package_detail'),

    # Auth
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),

    # Topup
    path('topup/<int:game_id>/', views.topup, name='topup'),
    path('packages/', views.packages, name='packages'),

    # Allauth
    path('accounts/', include('allauth.urls')),

    # Chatbot
    path("chatbot/", chatbot_api, name='chatbot'),

    # OTP SYSTEM
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),

    # Django built-in password reset
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),

    path(
    'reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ),
    name='password_reset_confirm'
),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('create-order/', views.create_order, name='create_order'),

    # Logout
    path('logout/', views.logout_view, name='logout'),
]