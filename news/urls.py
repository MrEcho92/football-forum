from django.urls import path
from news.views import Newslist, NewsDetail,CreateNews,  NewsUpdateView


app_name='news'

urlpatterns = [
    path('news/', Newslist.as_view(), name='news_list'),
    path('news/create/', CreateNews.as_view(), name='add_news'),
    path('news/<slug:slug>/', NewsDetail.as_view(), name='news_detail'),
    path('news/<slug:slug>/edit/',  NewsUpdateView.as_view(), name='news_edit'),
]
