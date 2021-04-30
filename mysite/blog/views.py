from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count

# Create your views here.
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm
from taggit.models import Tag


# class PostListView(ListView,tag_slug=None):
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'

#     def get_context_data(self, **kwargs):
#         context = super(PostListView, self).get_context_data(**kwargs)
#         context['title'] = 'Мой блог'
#         return context


def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts,
               'page': page,
               'title': 'Мой блог',
               'tag': tag}
    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    # List active comment for this object
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # Пользователь отправил комментарий.
        form = CommentForm(data=request.POST)
        if form.is_valid():
            # created comments
            new_post = form.save(commit=False);
            # Bind comments in current object
            new_post.post = post
            new_post.save()
    else:
        form = CommentForm()
    context = {'post': post,
               'comments': comments,
               'new_comment': new_comment,
               'comment_form': form,
               'title': 'Публикация',
               'similar_posts': similar_posts}
    return render(request, 'blog/post/detail.html', context)


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':

        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # Отправка почты
            post_url = request.build_absolute_uri(post.get_absolute())
            subject = f'{cd["name"], settings.EMAIL_HOST_USER, post.title}'
            message = f'"Read"  {post.title} \n {post_url}  \n  {cd["name"]} \n {cd["comment"]} , "comments"'
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd["to"]], fail_silently=False)
            sent = True
    else:
        form = EmailPostForm()
    context = {
        'post': post,
        'form': form,
        'sent': sent
    }
    return render(request, 'blog/post/share.html', context)
