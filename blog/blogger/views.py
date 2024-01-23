from django.shortcuts import render
from django.views.generic import ListView
from .models import Post, Category, Comment

class HomeView(ListView):
    model = Post
    model = Category
    model = Comment

    template_name = "blog/index.html"