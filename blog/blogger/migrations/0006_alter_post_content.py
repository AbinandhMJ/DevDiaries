# Generated by Django 5.0.1 on 2024-02-16 20:00

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("blogger", "0005_alter_tag_options_post_dislikes_post_shares_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="content",
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
