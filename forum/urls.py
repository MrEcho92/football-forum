from django.urls import path
from forum.views import (PostListView, PostDetailView, CreatePostView,
                        PostUpdateView, PostDeleteView, CreateCommentView,
                        PostLikeToggle, PostLikeAPIToggle, ReportView, GuidelinesView, trending, mostcomment)


app_name='forum'

urlpatterns = [
    path('forum/', PostListView.as_view(), name='post_list'),
    path('trending/', trending, name='trending'),
    path('hot/', mostcomment, name='mostcomment'),
    path('forum/add/', CreatePostView.as_view(), name='post_new'),
    path('forum/<int:pk>/report/', ReportView.as_view(), name='report'),
    path('forum/<int:pk>/<slug:slug>/comment/', CreateCommentView.as_view(), name='add_comment_to_post'),
    path('forum/<int:pk>/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('forum/<int:pk>/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('forum/<int:pk>/<slug:slug>/remove/', PostDeleteView.as_view(), name='post_remove'),
    path('forum/<int:pk>/<slug:slug>/like/', PostLikeToggle.as_view(), name='like-toggle'),
    path('api/<int:pk>/<slug:slug>/like', PostLikeAPIToggle.as_view(), name='like-api-toggle'),
    path('forum/community_guidelines/', GuidelinesView.as_view(), name='guidelines'),

]
