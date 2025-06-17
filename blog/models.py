from django.conf import settings
from django.db import models 
from django.urls import reverse
from django.utils import timezone


class PublishedManager(models.Manager):
    def get_queryset(self):

        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
      settings.AUTH_USER_MODEL, # Use the user model defined in settings.py, which is usually the default User model
      on_delete=models.CASCADE, # If the user is deleted, all their posts will be deleted as well
      related_name='blog_posts', # Allows reverse access to posts from the user (user.blog_posts.all() to get all posts by a user
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now) # Date when the post is published
    created = models.DateTimeField(auto_now_add=True) # auto add the field on creation
    updated = models.DateTimeField(auto_now=True) # auto update the field on every save
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    
    objects = models.Manager() # the default manager
    published = PublishedManager() # our custom manager
    
    class Meta:
        ordering = ['-publish'] # Reverse Posts order as the latest post should be first  
        indexes = [ # Index for puplish field to speed up queries performance 
            models.Index(fields=['-publish'])
        ]
    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        # the revese function get the URL path of a view by its name
        return reverse("blog:post_detail", args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ])


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]
        
    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
