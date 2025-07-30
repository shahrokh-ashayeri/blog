from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from .forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

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
