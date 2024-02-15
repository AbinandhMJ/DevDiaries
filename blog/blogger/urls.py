from django.urls import path
from .views import (
    HomeView,
    PostDetailView,
    tag_detail,
    category_detail,
    view_all_categories,
    register,
    user_login,
    dashboard,
    forgotpassword, logout_view, aboutus, contactus
)


urlpatterns = [
    path("", HomeView.as_view(), name="homepage"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path('tag/<str:tag_name>/', tag_detail, name='tag_detail'),
    path('category/<str:category_name>/', category_detail, name='category_detail'),
    path('categories/', view_all_categories, name='view_all_categories'),
    path('register', register, name="register"),
    path('login', user_login, name="login"),
    path('dashboard', dashboard, name="dashboard"),
    path('forgotpassword', forgotpassword, name="forgotpassword"),
    path('logout/', logout_view, name='logout'),
    path('aboutus/', aboutus, name='aboutus'),
    path('contactus/', contactus, name='contactus'),
]
