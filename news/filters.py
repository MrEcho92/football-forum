import django_filters
from news.models import *


class NewsFilter(django_filters.FilterSet):
    class Meta:
        model = News
        fields = ['league', ]
