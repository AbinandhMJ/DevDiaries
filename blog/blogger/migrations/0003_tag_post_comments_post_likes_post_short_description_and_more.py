# Generated by Django 5.0.1 on 2024-02-05 11:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blogger", "0002_post_image_post_views"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="comments",
            field=models.ManyToManyField(
                blank=True, related_name="post_comments", to="blogger.comment"
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="likes",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="post",
            name="short_description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="post",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="posts", to="blogger.tag"
            ),
        ),
    ]
