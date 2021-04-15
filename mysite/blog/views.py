from django.shortcuts import render, get_object_or_404

# Create your views here.
from blog.models import Post


def post_list(request):
    posts = Post.published.all()
    context = {'posts': posts,
               'title': 'My blog'}
    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    context = {'post': post,
               'title': 'My blog'}
    return render(request, 'blog/post/detail.html', context)
