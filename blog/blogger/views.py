from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Post, Category, Comment, Tag
from django.db.models import Count

class HomeView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['comments'] = Comment.objects.all()
        context['tags'] = Tag.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')[:15]
        context['post_titles'] = [post.title for post in context['posts']]
        context['recent_posts'] = Post.objects.order_by('-created_at')[:3]
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = self.object.tags.all()  # Retrieve tags associated with the post
        return context

def tag_detail(request, tag_name):
    # Retrieve the tag object based on the tag name
    tag = get_object_or_404(Tag, name=tag_name)

    # Assuming you have a template named 'tag_detail.html'
    return render(request, 'blog/tag_detail.html', {'tag': tag})

def category_detail(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    # Add any additional logic here if needed
    return render(request, 'blog/category_detail.html', {'category': category})
def view_all_categories(request):
    categories = Category.objects.all()
    return render(request, 'blog/all_categories.html', {'categories': categories})