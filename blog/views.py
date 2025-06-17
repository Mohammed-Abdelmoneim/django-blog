from django.shortcuts import get_object_or_404, render
from .models import Post, CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST


# Create your views here.
def post_list(request):
    post_list= Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
        
    return render(request, 'blog/post/list.html', {'posts': posts})

class PostListView(ListView):
    queryset = Post.published.all()
    
    context_object_name = 'posts'
    paginate_by = 3
    template_name= 'blog/post/list.html'
    
    
    
def post_detail(request, year, month, day, post): # post here means slug that's in the url.py file
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    # Retrive post by id
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    sent = False
    
    
    if request.method == 'POST':
        # From is submitted
        form  = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields are valid
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you read {post.title}"
            )
            
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
           
            send_mail(
               subject=subject,
               message=message,
               from_email=None, # DEFAULT_FROM_EMAIL setting will be used for the sender
               recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED
    )
    comment = None
    # a comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the databasa
        comment.save()
    return render('request', 'blog/post/comment,html', 
                  {'post': post, 'comment': comment, 'form': form})
