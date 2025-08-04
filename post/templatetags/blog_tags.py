from post.models import Post
from django import template

register = template.Library()

@register.simple_tag
def total_count():
    return Post.published.count()
