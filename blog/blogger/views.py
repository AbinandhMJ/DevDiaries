from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView
from .models import Post, Category, Comment, Tag
from django.db.models import Count, Q, F
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .forms import CustomUserCreationForm, LoginForm, ContactForm, CreateBlogForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.utils.timezone import now

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Generate a unique slug
            base_slug = slugify(post.title)
            timestamp = now().strftime("%Y%m%d%H%M%S")
            post.slug = f"{base_slug}-{timestamp}"

            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = CreateBlogForm()
        
    return render(request, 'blog/createblog.html', {'form': form})

def aboutus(request):
    return render(request, 'general/aboutus.html')

def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Get form data
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            reason = form.cleaned_data.get('reason', '')  # Assuming 'reason' is an optional field
            message = form.cleaned_data.get('message')

            # Construct email message
            subject = f"New message from {name}"
            body = f"From: {name}\nEmail: {email}\nReason: {reason}\n\nMessage: {message}"
            from_email = 'courtfinder277@gmail.com'  # Replace with your email address
            to_email = 'abinandhmurukesan@gmail.com'  # Recipient email address

            # Send email
            send_mail(subject, body, from_email, [to_email])

            # Redirect with success message
            return HttpResponseRedirect(request.path_info + '?submitted=True')
    else:
        form = ContactForm()

    form_submitted = request.GET.get('submitted', False)
    return render(request, 'general/contactus.html', {'form': form, 'form_submitted': form_submitted})

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
    paginate_by = 10  # Number of posts per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['comments'] = Comment.objects.all()
        context['tags'] = Tag.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')[:15]
        context['post_titles'] = [post.title for post in context['posts']]
        context['recent_posts'] = Post.objects.order_by('-created_at')[:3]
        context['trending_posts'] = Post.objects.order_by('-views')[:3] 
        context['popular_post'] = Post.objects.order_by('-views', '-likes',).first()

        # Retrieve the latest post
        latest_post = Post.objects.first()

        # Retrieve a post related to cybersecurity or AI
        cybersecurity_posts = Post.objects.filter(tags__name__in=['cybersecurity', 'AI']).order_by('?').first()

        # Check if the latest post is the same as the cybersecurity or AI post
        if cybersecurity_posts and latest_post == cybersecurity_posts:
            cybersecurity_posts = None

        # Determine the post to display as the "Editors Pick"
        editors_pick = latest_post if latest_post else cybersecurity_posts

        context['editors_pick'] = editors_pick

        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return posts

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
    if tag_name == 'default_tag':
        # Handle default_tag separately
        # Add your logic here for handling default_tag
        return render(request, 'blog/tags&cat.html')
    
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
