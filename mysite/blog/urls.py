from django.urls import path
from blog.views import post_detail, post_share, post_list
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    # post views
    path('', post_list, name='post_list'),
    # path('', PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
]
