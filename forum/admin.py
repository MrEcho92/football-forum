from django.contrib import admin
from forum.models import Post, Comment, Report
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    #prepopulated_fields = {'slug': ('title',)}
    pass

admin.site.register(Post, PostAdmin)

admin.site.register(Comment)


admin.site.register(Report)
