from django.forms import ModelForm
from django.forms import Textarea
from .models import Comment
from django import forms


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        widgets = {
            "body": Textarea(
                attrs={"rows": 4, "placeholder": "نظر خود را اینجا بنویسید..."}
            ),
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "نام شما"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "ایمیل شما"}
            ),
        }
        labe0ls = {"name": "نام شما:", "email": "ایمیل:", "body": "نظر شما:"}


class ShareForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "نام شما"}
        ),
        label="نام شما",
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "ایمیل شما"}
        ),
        label="ایمیل شما",
    )
    to = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "ایمیل گیرنده"}
        ),
        label="ایمیل گیرنده",
    )
    text = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "متن پیام (اختیاری)",
                "rows": 4,
            }
        ),
        label="متن پیام (اختیاری)",
    )
