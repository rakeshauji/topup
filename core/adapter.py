from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from .models import EmailOTP
import random

User = get_user_model()

class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        # THIS BLOCKS HELPS THIRD-PARTY SIGNUP FORM REMOVE
        return False

    def pre_social_login(self, request, sociallogin):

        email = sociallogin.user.email

        if not User.objects.filter(email=email).exists():
            request.session['error'] = "Email not registered. Please signup first."
            return redirect('/login/')