from django.forms import ModelForm
from django.forms import Textarea
from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={
                'rows': 4,
                'placeholder': 'نظر خود را اینجا بنویسید...'
            })
        }
        labels = {
            'content': 'نظر:'
        }