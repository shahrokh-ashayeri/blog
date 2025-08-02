"""
API app URL file
"""

from django.urls import path
from .views import posts_index

app_name = 'api'
urlpatterns = [
    path('posts/', posts_index, name='posts_index'),
]
