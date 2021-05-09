from django.shortcuts import render,redirect, get_object_or_404
from news.models import News
from django.views.generic import (ListView, DetailView, CreateView, UpdateView)
from news.filters import NewsFilter
from news.forms import NewsForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.contrib.auth.models import User

# Create your views here.

class Newslist(ListView):
    paginate_by = 20
    model = News
    template_name = 'news_list.html'

    #news = News.objects.filter(status=1).order_by('-published_date')
    #context_object_name = "news"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.filter(status=1).order_by('-published_date')
        context['newsfilter'] = NewsFilter(self.request.GET,queryset = News.objects.filter(status=1).order_by('-published_date'))
        context['news'] = NewsFilter(self.request.GET,queryset = News.objects.filter(status=1).order_by('-published_date')).qs #.qs to access filtered objs in view
        return context

'''
def listing(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 20) # Show 20 blogs per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news_list.html', {'page_obj': page_obj})
'''

class NewsDetail(DetailView):
    model = News
    template_name = 'news_detail.html'


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news_create.html'



class NewsUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'news_create.html'

    # UserPassesTestMixin - prevent user accessing other users post
    def test_func(self):
        news= self.get_object()
        if self.request.user.is_staff:
            return True
        return False
