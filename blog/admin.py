from django.contrib import admin
from .models import Post, Comment
# Register your models here.


# admin.site.register(Post)
# Customizing how models are displayed in the admin site
@admin.register(Post) # edit the typo below!!!!
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author'] # filter the results on the sidebar
    search_fields = ['title', 'body'] # adding a search bar on the admin site
    prepopulated_fields = {'slug': ('title',)} # the slug field is filled in automatically using the title
    raw_id_fields = ['author'] # the author field is now displayed with a lookup widget,
    date_hierarchy = 'publish' # adding navigation links to navigate through
    ordering = ['status', 'publish'] # to order the posts by status and publish date
    # show_facets = admin.ShowFacets.ALWAYS # to show facets in the admin  
 
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
