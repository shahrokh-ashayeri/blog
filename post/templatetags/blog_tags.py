from post.models import Post
from django import template

register = template.Library()

@register.simple_tag
def total_count():
    return Post.published.count()

@register.inclusion_tag('post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts =  Post.published.order_by("-published_time")[:count]
    return {'latest_posts': latest_posts}
