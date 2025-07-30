from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.
def login_view(request):
    """
    Render the login page.
    """
    return render(request, "account/login.html")


def register_view(request):
    """
    Render the registration page.
    """
    return render(request, "account/register.html")


def otp_view(request):
    """
    Render the OTP page.
    """
    return render(request, "account/otp.html")


def logout_view(request):
    logout(request)
    return redirect("post:post_list")
