import re
import requests
from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField

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

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name_plural = "tags"

    def __str__(self):
        return self.name

class Post(models.Model):
    options = (
        ("draft", "Draft"),
        ("published", "Published"),
    )

    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    # content = models.TextField()
    content = RichTextUploadingField()
    short_description = models.TextField(blank=True)
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category", related_name="posts")
    tags = models.ManyToManyField("Tag", related_name="posts", blank=True)
    status = models.CharField(max_length=10, choices=options, default="draft")
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    comments = models.ManyToManyField("Comment", related_name="post_comments", blank=True)
    reading_time = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=250, unique=True, blank=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Automatically generate the slug from the title if it's not provided
        if not self.slug:
            self.slug = slugify(self.title)[:250]  # Limit slug length to 250 characters

        # If no image is provided, fetch an image from Pexels API
        if not self.image:
            self.fetch_image_from_pexels()

        # Automatically generate short description from content
        if not self.short_description:
            self.short_description = self.generate_short_description()

        # Automatically generate reading time and tags
        if not self.reading_time:
            self.reading_time = self.calculate_reading_time()

        super().save(*args, **kwargs)  # Save the instance first

        if not self.tags.exists():  # Now you can safely access tags
            self.extract_tags_from_content()

    def fetch_image_from_pexels(self):
        # Fetch image from Pexels API based on keywords extracted from the post title
        if not self.image:
            keywords = self.extract_keywords_from_title()

            for keyword in keywords:
                headers = {"Authorization": "cfqed7d3TCjPaX70zHILKTtFad2T8or7lkEmx2A1NtxtylDrIYgt33AV"}
                params = {"query": keyword, "per_page": 1}
                response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)

                if response.status_code == 200:
                    image_url = self.extract_image_url(response.json())
                    if image_url:
                        response = requests.get(image_url)
                        self.image.save(f"{slugify(self.title)}.jpg", ContentFile(response.content), save=False)
                        break

    def extract_image_url(self, response_json):
        # Extract the first image URL from the Pexels API response
        photos = response_json.get("photos", [])
        if photos:
            return photos[0].get("src", {}).get("large", None)
        return None

    def increment_views(self):
        self.views += 1
        self.save()

    def generate_short_description(self):
        # Extract the first two sentences from the content as the short description
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', self.content)
        short_description = ' '.join(sentences[:2])
        return short_description

    def calculate_reading_time(self):
        # Assume an average reading speed of 200 words per minute
        words_per_minute = 200
        total_words = len(re.findall(r'\w+', self.content))
        return max(1, round(total_words / words_per_minute))

    def extract_tags_from_content(self):
        # Extract tags from the content based on certain criteria (e.g., hashtags)
        tags = re.findall(r'#(\w+)', self.content)
        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            self.tags.add(tag)

    def extract_keywords_from_title(self):
        # Implement your logic to extract and prioritize keywords from the post title
        # Example: Splitting the title into words and prioritizing longer words
        words = re.findall(r'\b\w+\b', self.title)
        sorted_keywords = sorted(words, key=len, reverse=True)
        return sorted_keywords

    def add_like(self):
        self.likes += 1
        self.save()

    def add_dislike(self):
        self.dislikes += 1
        self.save()

    def add_share(self):
        self.shares += 1
        self.save()

# Signal to update reading_time before saving
@receiver(pre_save, sender=Post)
def update_reading_time(sender, instance, **kwargs):
    instance.reading_time = instance.calculate_reading_time()
