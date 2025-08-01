from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]  # Alphabetical order
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=200, unique_for_date="published_time", allow_unicode=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts", null=True, blank=True
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_time = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="posts"
    )
    objects = models.Manager()
    published = PublishedManager()
    status = models.CharField(
        max_length=10,
        choices=[
            ("draft", "Draft"),
            ("published", "Published"),
            ("archived", "Archived"),
        ],
        default="draft",
    )

    def get_absolute_url(self):
        return reverse(
            "post:post_detail",
            kwargs={
                "year": self.published_time.year,
                "month": self.published_time.month,
                "day": self.published_time.day,
                "slug": self.slug,
            },
        )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]  # Newest posts first
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        indexes = [
            models.Index(fields=["-published_time"]),
        ]


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField(null=True, blank=False)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"

    class Meta:
        ordering = ["-created"]  # Newest comments first
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        indexes = [
            models.Index(fields=["-created"]),
        ]
