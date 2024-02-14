from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView
from .models import Post, Category, Comment, Tag
from django.db.models import Count, Q
from django.http import HttpResponse, Http404
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def logout_view(request):
    logout(request)
    return redirect('login') 

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful!', extra_tags='toast-success')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('homepage') 
        else:
             for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error in {field}: {error}", extra_tags='toast-error') 
    else:
        form = CustomUserCreationForm() 
    return render(request, 'authentication/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Invalid form submission. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})  
      
def dashboard(request):
    return render(request, 'dashboard/index.html')

def forgotpassword(request):
    return render(request, 'authentication/forgot-password.html')

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
    template_name = "blog/post-details.html" 
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
    return render(request, 'blog/tags&cat.html', {'tag': tag})

def category_detail(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    # Add any additional logic here if needed
    return render(request, 'blog/tags&cat.html', {'category': category})
def view_all_categories(request):
    categories = Category.objects.all()
    return render(request, 'blog/tags&cat.html', {'categories': categories})