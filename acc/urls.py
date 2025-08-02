"""
Account app URL file
"""

from django.urls import path
from .views import login_view, register_view, otp_view, logout_view

app_name = 'acc'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('otp/', otp_view, name='otp'),  # Assuming otp_view is similar to login_view
]
