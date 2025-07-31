from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from .forms import CommentForm, ShareForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib import messages

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        if self.request.GET.get('category'):
            category_slug = self.request.GET.get('category')
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

    return render(request, "post/post_detail.html", {"post": post, 'form': CommentForm()})

def post_share(request):
    if request.method == "POST":
        form = ShareForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # send mail
            messages.add_message(request, messages.SUCCESS ,'مقاله با موفقیت به اشتراک گذاشته شد')
        # else:
        return render(request, "post/post_share.html", {"form": form})
    else:
        form = ShareForm()
        post_id = request.GET.get('post_id')
        
        post = Post.objects.get(id=post_id)
        post_url = request.build_absolute_uri(post.get_absolute_url())
        telegram_share_url = f"https://t.me/share/url?url={post_url}&text=Check this post!"
        return render(request, "post/post_share.html", {"form": form, "post": post, 'telegram_share_url': telegram_share_url})      