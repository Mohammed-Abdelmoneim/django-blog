<div align="center">
  <br />
   
  <h1>Django Blog Application</h1> 
  <div>
    <img src="https://img.shields.io/badge/Django-green?logo=django" alt="django" />
    <img src="https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql&logoColor=white" alt="postgres" />
  </div>

</div>

## <a name="introduction">🤖 Introduction</a>

A Django-powered blog application that supports post publishing, tagging, and user comments. It features a simple and clean interface for reading blog posts, as well as a search system, pagination and share a post via email. Posts are stored in a PostgreSQL database, and the app includes an admin panel for content management.

## <a name="tech-stack">⚙️ Tech Stack</a>

- **[Django](https://djangoproject.com/)** is a free and open-source, high-level Python web framework that facilitates the rapid development of secure and maintainable websites. It is maintained by the Django Software Foundation. 

- **[PostgreSQL](https://www.postgresql.org/)** is a powerful, open source object-relational database system with over 35 years of active development that has earned it a strong reputation for reliability, feature robustness, and performance.

- **[Docker](https://www.docker.com/)** (for PostgreSQL) is used to containerize the PostgreSQL database, ensuring easy setup, portability, and consistency across development environments.

- **[Django Taggit](https://django-taggit.readthedocs.io/en/latest/)** is a simple and flexible tagging library for Django. It allows users to associate tags with blog posts and supports tag-based filtering and suggestions.

- **[PostgreSQL Full-Text Search](https://django-taggit.readthedocs.io/en/latest/)** This feature enables powerful search functionality using PostgreSQL’s built-in indexing and ranking system. It's integrated into the blog to provide fast and accurate search results based on post content.


## <a name="features">🔋 Features</a>

👉 **Post Publishing System**: Create, edit, and publish blog posts with a built-in admin interface. Posts can be scheduled and filtered by publish date.

👉 **Tag-Based Navigation**: Posts can be tagged with multiple keywords using django-taggit, allowing users to explore related content easily.

👉 **Commenting System**: Readers can leave comments on blog posts. Only approved (active) comments are displayed to maintain quality discussions.

👉 **Post Recommendations**: Each post page displays a list of similar posts based on shared tags to keep readers engaged.

👉 **Pagination**: Posts are paginated on the list view for improved performance and a cleaner browsing experience.

👉 **Post Sharing via Email**: Users can share blog posts with others by entering an email address and an optional message. The system sends a nicely formatted email with the post link.

and many more, including code architecture and reusability

## <a name="quick-start">🤸 Quick Start</a>

Follow these steps to set up the project locally on your machine.

**Prerequisites**

Make sure you have the following installed on your machine:

- [Git](https://git-scm.com/)
- [Django](https://www.djangoproject.com/)
- [Docker](https://www.docker.com/)

**Cloning the Repository**

```bash
git clone https://github.com/Mohammed-Abdelmoneim/django-blog

```

**Set Up a Virtual Environment**


```bash
python3 -m venv env
source env/bin/activate # On Windows use `env\Scripts\activate`
```

**Install Python Dependencies**

```bash
pip install -r requirements.txt
```

**Start PostgreSQL with Docker**

Make sure you have Docker installed and running. Then run:

```bash
docker run --name blog-postgres -e POSTGRES_USER=bloguser -e POSTGRES_PASSWORD=blogpass -e POSTGRES_DB=blogdb -p 5432:5432 -d postgres
```
**Configure Environment Variables**

Create a <code>.env</code> file in the project root (or set variables directly) with:

```ini
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=PASSWORD
DEFAULT_FROM_EMAIL=My Blog <your-email@gmail.com>
DB_NAME=blog
DB_USER=blog
DB_PASSWORD=PASSWORD
DB_HOST=localhost

```
Update <code>settings.py</code> to read from .env (optional but recommended).

**Apply Migrations**
```bash
python manage.py migrate
```

**Create a Superuser (Admin)**
```bash
python manage.py createsuperuser
```

**Run the Development Server**
```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to view the project.

Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## <a name="snippets">🕸️ Snippets</a>

<details>
<summary><code>views.py</code></summary>

```py
def post_detail(request, year, month, day, post): # post here means slug that's in the url.py file
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment 
    form = CommentForm() 
    
    # List of similar posts 
    post_tags_ids = post.tags.values_list('id', flat=True) # retrieve a list if IDs 
    similar_posts = Post.published.filter(
        tags__in =post_tags_ids # get all posts contain any of these tags
    ).exclude(id=post.id) # exclude current post id to not sugg the same post
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]
    
    
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form,
            'similar_posts': similar_posts
        }
    )

```

</details>

<details>
<summary><code>models.py</code></summary>

```py
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
    tags = TaggableManager()
    
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
```
</details>

