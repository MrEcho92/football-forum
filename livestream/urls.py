"""livestream URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from forum.views import PostListView
from account.views import  ActivateAccountView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostListView.as_view(), name='post_list'),
    path('', include('website.urls', namespace='website')),
    path('', include('forum.urls', namespace='forum')),
    path('', include('account.urls', namespace='account')),

    #To aviod No reversematch for below path, django password_reset_email is saved at ../opt/miniconda3/envs/myDjangoEnv/lib/python3.8/site-packages/django/contrib/admin/templates/registration
    #This have {% url 'password_reset_confirm' uidb64=uid token=token'%} which do link to account app_name
    #So to make it match with this file, I moved passwordresetconfirmview path here, and moved template_name to overall templates
    #Easier to put password here!
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html", success_url= reverse_lazy('account:password_reset_complete')), name="password_reset_confirm"),

    #sign up email sent
    path('activate/<uidb64>/<token>/',ActivateAccountView.as_view(), name='activate'),

    path('', include('news.urls', namespace='news')),
    path('', include('live.urls', namespace='live')),
    path('', include('notification.urls', namespace='notification')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'website.views.handler404'
handler500 = 'website.views.handler500'
