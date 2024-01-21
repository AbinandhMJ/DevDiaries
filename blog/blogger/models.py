from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    author = models.CharField(max_length=60)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} on '{self.post}'"


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    status = models.CharField(max_length=10, choices=options, default="draft")

    class Meta:
        ordering = ("-created_at",) 

    def __str__(self):
        return self.title
