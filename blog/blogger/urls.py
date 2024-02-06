from django.urls import path
from .views import HomeView, PostDetailView, tag_detail, category_detail, view_all_categories


urlpatterns = [
    path("", HomeView.as_view(), name="homepage"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
    path('tag/<str:tag_name>/', tag_detail, name='tag_detail'),
    path('category/<str:category_name>/', category_detail, name='category_detail'),
    path('categories/', view_all_categories, name='view_all_categories'),
]
