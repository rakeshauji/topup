from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import random

#  SLIDER
class Slide(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    button_text = models.CharField(max_length=50)
    button_link = models.CharField(max_length=200)
    background = models.ImageField(upload_to='slides/')

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin_user = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

# GAME
class Game(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to='games/', null=True, blank=True)

    def __str__(self):
        return self.name


# PACKAGE
class Package(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.ImageField(upload_to='packages/', null=True, blank=True)

    def __str__(self):
        return f"{self.game.name} - {self.name}"


# SITE SETTINGS (ONLY ONE - FIXED)
class SiteSetting(models.Model):
    logo = models.ImageField(upload_to='logo/', null=True, blank=True)
    site_name = models.CharField(max_length=100, default="TopUp Center")
    allow_guest_checkout = models.BooleanField(default=False)

    def __str__(self):
        return self.site_name


# PROFILE (role system)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, default="user")  # admin / user

    def __str__(self):
        return self.user.username


# ORDER
class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)   # ADD
    package = models.ForeignKey(Package, on_delete=models.CASCADE)  # ADD
    player_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return self.player_id
    
created_at = models.DateTimeField(auto_now_add=True)


# TOPUP ORDER
class TopUpOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)

    player_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)

    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.game.name}"
    
class ChatMessage(models.Model):
    user_message = models.TextField()
    bot_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
        return self.user_message
    
class EmailOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)