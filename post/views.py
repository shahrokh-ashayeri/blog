import urllib.parse
from .models import Post, Category
from django.contrib import messages
from django.core.mail import send_mail
from .forms import CommentForm, ShareForm
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# def post_list(request):
#     posts_list = Post.objects.all()
#     paginator = Paginator(posts_list, 9)
#     page_number = request.GET.get("page", 1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)

#     categories = Category.objects.all()
#     # return render(request, "post/post_list.html", {"posts": posts, 'categories': categories})
#     return render(request, "post/post_list.html", {"posts": posts, 'categories': categories})


class PostListView(ListView):
    model = Post
    template_name = "post/post_list.html"
    context_object_name = "posts"
    paginate_by = 6
    #paginate variable is 'page_obj' by default

    def get_context_data(self, **kwargs):
        # Any data intended for the template should be included in the context variable, as follows
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

    def get_queryset(self):
        # This class sends this data to the template when no filter is specified
        if self.request.GET.get("category"):
            category_slug = self.request.GET.get("category")
            return Post.published.filter(category__slug=category_slug)
        else:
            return Post.published.all()


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        published_time__year=year,
        published_time__month=month,
        published_time__day=day,
        slug=slug,
    )
    categories = Category.objects.all()
    
    # retrieve active comments for the post
    comments = post.comments.filter(active=True)

    return render(
        request, "post/post_detail.html", {"categories": categories, "post": post, "comment_form": CommentForm(), "comments": comments}
    )


def post_share(request, post_slug, post_id):
    # post_id = request.GET.get("post_id")
    post = get_object_or_404(Post, id=post_id, slug=post_slug)
    post_url = request.build_absolute_uri(post.get_absolute_url())

    if request.method == "POST":
        form = ShareForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f"{cd['name']} ({cd['email']}) wants to share {cd['to']}"
            message = f"Message: {cd['text']}\n\nLink: {post_url}"
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            messages.add_message(
                request, messages.SUCCESS, "مقاله با موفقیت به اشتراک گذاشته شد"
            )
        # else:
        return render(request, "post/post_detail.html", {'post': post})

    form = ShareForm()
    telegram_share_url = (
        f"https://t.me/share/url?url={post_url}&text=لطفا این پست رو مشاهده کنید"
    )
    whatsapp_share_url = (
        f"https://api.whatsapp.com/send?text={urllib.parse.quote(post_url)}"
    )
    return render(
        request,
        "post/post_share.html",
        {
            "form": form,
            "post": post,
            "telegram_share_url": telegram_share_url,
            "whatsapp_share_url": whatsapp_share_url,
        },
    )


# Only allow POST requests for commenting
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.post = post
        comment.save()
        messages.add_message(
            request, messages.SUCCESS, "نظر شما با موفقیت ثبت شد"
        )
        return render(request, 'post/comment.html', {'form':comment_form, 'post': post, 'comment': comment})
        
    
    messages.add_message(
        request, messages.ERROR, "خطا در ثبت نظر. لطفا دوباره تلاش کنید."
    )
    
    return render(request, 'post/comment.html', {'form':comment_form, 'post': post, 'form': comment_form})