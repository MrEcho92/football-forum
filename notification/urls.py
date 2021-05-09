from django.urls import path
from notification.views import ( ShowNotifications, DeleteNotification, CountNotifications)


app_name='notification'

urlpatterns = [
    path('notifications/', ShowNotifications, name='show-notifications'),
    path('<int:pk>/delete/', DeleteNotification, name='delete-notification'),


]
