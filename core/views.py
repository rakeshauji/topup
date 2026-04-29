from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from .models import ChatMessage
from .models import Slide, Game, Package, Order, SiteSetting, TopUpOrder
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
import random
from .models import EmailOTP
import requests

def home(request):
    slides = Slide.objects.all()
    games = Game.objects.all()
    packages = Package.objects.all()

    return render(request, 'home.html', {
        'slides': slides,
        'games': games,
        'packages': packages
    })

@login_required(login_url='login')   # enforce login here also
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    packages = Package.objects.filter(game=game)

    if request.method == "POST":
        package = get_object_or_404(Package, id=request.POST['package'])

        Order.objects.create(
    user=request.user,
    game=game,
    package=package,
    player_id=request.POST['player_id'],
    payment_method=request.POST['payment'],
    contact=request.POST['contact'],
    status='pending'   
)

        messages.success(request, "Order placed successfully!")
        return redirect('game_detail', game_id=game.id)

    return render(request, 'game_detail.html', {
        'game': game,
        'packages': packages
    })

def package_detail(request, id):
    package = get_object_or_404(Package, id=id)
    return render(request, 'package_detail.html', {'package': package})


def signup(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        username = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not all([first_name, last_name, email, username, password, confirm_password]):
            messages.error(request, "All fields are required!")
            return render(request, "signup.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, "signup.html")

        # user create POST
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    # GET request handle
    return render(request, "signup.html")


@csrf_protect
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password").lower()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")




def verify_hcaptcha(token):
    secret = "YOUR_SECRET_KEY"
    response = requests.post(
        "https://hcaptcha.com/siteverify",
        data={
            "secret": secret,
            "response": token
        }
    )
    return response.json()

@login_required(login_url='login')
def topup(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    packages = Package.objects.filter(game=game)
    setting = SiteSetting.objects.first()

    if request.method == "POST":
        player_id = request.POST.get('player_id')
        payment = request.POST.get('payment')
        contact = request.POST.get('contact')
        package_id = request.POST.get('package')

        # Validation
        if not all([player_id, payment, contact, package_id]):
            messages.error(request, "Please fill all fields!")
            return render(request, 'topup.html', {
                'game': game,
                'packages': packages
            })

        package = get_object_or_404(Package, id=package_id)

        # Save order
        Order.objects.create(
    user=request.user,
    game=game,
    package=package,
    player_id=request.POST['player_id'],
    payment_method=request.POST['payment'],
    contact=request.POST['contact'],
    status='pending'   
)

        messages.success(request, "TopUp order placed successfully!")
        return redirect('topup', game_id=game.id)

    return render(request, 'topup.html', {
        'game': game,
        'packages': packages,
        'setting': setting
    })

@login_required(login_url='login')
def packages(request):
    packages = Package.objects.all()
    return render(request, 'packages.html', {
        'packages': packages
    })

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("login")


def chatbot_api(request):
    if request.method == "POST":
        msg = request.POST.get("message")

        # simple reply logic
        if "hello" or "hii" in msg.lower():
            reply = "Hey gamer, Welcome to FeaHub! What do you want to do today?\n-Topup, Games, Payment"
        elif "topup" in msg.lower():
            reply = "🔥 TopUp Center 🔥\nWhich game do you want to topup?\n- Free Fire\n- PUBG\n- Valorant"
        elif "freefire" in msg.lower():
            reply = "💎 Free Fire Topup\nSelect package:\n- 100 Diamonds\n- 310 Diamonds\n- 520 Diamonds"
        elif "pubg" in msg.lower():
            reply = "🎯 PUBG UC Topup\nSelect package:\n- 60 UC\n- 325 UC\n- 660 UC"
        elif "payment" in msg.lower():
            reply = "💳 Payment Options:\nYou can pay using:\n- eSewa\n- Khalti\n👉 Which one do you prefer?"
        elif "esewa" in msg.lower():
            reply = "Great 👍 Send payment via eSewa and upload screenshot."
        elif "khalti" in msg.lower():
            reply =  "Nice 👍 Send payment via Khalti and upload screenshot."
        elif "how are you" in msg.lower():
            reply = "I'm awesome 😎 Ready to help you topup faster!"
        else:
            reply ="I didn't understand\n let me talk about payment, topup"
           
        # SAVE TO DATABASE
        ChatMessage.objects.create(
            user_message=msg,
            bot_reply=reply
        )

        return JsonResponse({"reply": reply})
    
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        
        user = User.objects.filter(email=email).first()

        if not user:
            messages.error(request, "Email is not registered. Please signup first.")
            return render(request, "forgot.html")

        otp = str(random.randint(100000, 999999))

        # save OTP using USER
        EmailOTP.objects.update_or_create(
            user=user,
            defaults={"otp": otp}
        )

        send_mail(
            "Your OTP Code",
            f"Your OTP is: {otp}",
            "hevannepal8@gmail.com",
            [email],
            fail_silently=False,
        )

        request.session["reset_user_id"] = user.id

        messages.success(request, "OTP sent to your email")
        return redirect("verify_otp")

    return render(request, "forgot.html")

def verify_otp(request):
    if request.method == "POST":
        user_id = request.session.get("reset_user_id")
        input_otp = request.POST.get("otp")

        try:
            otp_obj = EmailOTP.objects.get(user_id=user_id)

            if otp_obj.otp == input_otp:
                return redirect("reset_password")
            else:
                return render(request, "otp.html", {"error": "Invalid OTP"})

        except EmailOTP.DoesNotExist:
            return render(request, "otp.html", {"error": "OTP not found"})

    return render(request, "otp.html")



from django.contrib.auth.hashers import make_password

def reset_password(request):
    user_id = request.session.get("reset_user_id")

    if request.method == "POST":
        password = request.POST.get("password")

        user = User.objects.get(id=user_id)
        user.password = make_password(password)
        user.save()

        EmailOTP.objects.filter(user_id=user_id).delete()
        request.session.pop("reset_user_id", None)

        return redirect("login")

    return render(request, "reset_password.html")

def create_order(request):
    if request.method == "POST":

        Order.objects.create(
            user=request.user,
            player_id=request.POST.get('player_id'),
            package_name=request.POST.get('package_name'),
            price=request.POST.get('price'),
            payment_method=request.POST.get('payment'),
            contact=request.POST.get('contact'),
            status='pending'
        )

        return redirect('success_page')