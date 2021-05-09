from django.contrib import admin
from news.models import News
# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    list_display =('title', 'status', 'created_date', 'league')
    list_filter = ("status", "league",)
    search_fields =['title', 'message']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(News, NewsAdmin)
