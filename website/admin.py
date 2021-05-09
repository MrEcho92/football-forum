from django.contrib import admin
from website.models import subscriber
from import_export.admin import ImportExportModelAdmin
# Register your models here.

#admin.site.register(subscriber)

@admin.register(subscriber)
class subscribeAdmin(ImportExportModelAdmin):
    pass
