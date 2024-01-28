from django.urls import path
from .views import HomeView, PostDetailView

urlpatterns = [
    path("", HomeView.as_view(), name="homepage"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),
]
