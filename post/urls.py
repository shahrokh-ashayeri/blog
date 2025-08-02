"""
Post app URL file
"""

from django.urls import path
from . import views


app_name = 'post'
urlpatterns = [
    # path('', view=views.post_list, name='post_list'),
    path('', view=views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<str:slug>', views.post_detail, name='post_detail'),
    path('share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]
