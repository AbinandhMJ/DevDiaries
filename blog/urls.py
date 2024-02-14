from django.contrib import admin
from django.urls import path, include

handler404 = 'blog.blogger.views.custom_404_view'


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.blogger.urls")),
]
