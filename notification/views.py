from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from notification.models import Notification

# Create your views here.
def ShowNotifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user).order_by('-date')
    Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)
    context ={
        'notifications': notifications,
    }
    return render(request,'notifications.html',context)

def DeleteNotification(request, pk):
	user = request.user
	Notification.objects.filter(pk=pk, user=user).delete()
	return redirect('notification:show-notifications')


def CountNotifications(request):
	count_notifications = 0
	if request.user.is_authenticated:
		count_notifications = Notification.objects.filter(user=request.user, is_seen=False).count()

	return {'count_notifications':count_notifications}
