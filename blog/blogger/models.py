import requests
from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils.text import slugify

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
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    status = models.CharField(max_length=10, choices=options, default="draft")
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # If no image is provided, fetch an image from Pexels API
        if not self.image:
            self.fetch_image_from_pexels()
        super().save(*args, **kwargs)

    def fetch_image_from_pexels(self):
        # Fetch image from Pexels API based on the post title
        query = slugify(self.title)
        headers = {"Authorization": "cfqed7d3TCjPaX70zHILKTtFad2T8or7lkEmx2A1NtxtylDrIYgt33AV"}
        params = {"query": query, "per_page": 1}
        response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)

        if response.status_code == 200:
            image_url = self.extract_image_url(response.json())
            if image_url:
                response = requests.get(image_url)
                self.image.save(f"{slugify(self.title)}.jpg", ContentFile(response.content), save=False)

    def extract_image_url(self, response_json):
        # Extract the first image URL from the Pexels API response
        photos = response_json.get("photos", [])
        if photos:
            return photos[0].get("src", {}).get("large", None)
        return None
