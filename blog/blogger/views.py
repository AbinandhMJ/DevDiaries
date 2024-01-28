from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category, Comment

class HomeView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['comments'] = Comment.objects.all()
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/single-post.html" 
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.views += 1
        obj.save()
        return obj