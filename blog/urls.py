"""
Base URL file
"""

from django.contrib import admin
from django.urls import path, include
from post.views import PostListView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('posts/', include('post.urls', namespace='post')),
    path('acc/', include('acc.urls', namespace='acc')),
    path('api/', include('api.urls', namespace='api')),
    path('', PostListView.as_view(), name="homepage")
]
