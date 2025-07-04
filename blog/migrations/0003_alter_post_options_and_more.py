# Generated by Django 5.2.3 on 2025-06-12 16:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_slug_alter_post_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-publish']},
        ),
        migrations.RemoveIndex(
            model_name='post',
            name='blog_post_puplish_6a975f_idx',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='puplish',
            new_name='publish',
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-publish'], name='blog_post_publish_bb7600_idx'),
        ),
    ]
