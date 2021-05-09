from django.urls import path
from .views import AboutView, ContactView, TermsView, PrivacyView
#from .views import IndexView

app_name ='website'

urlpatterns = [
    path('about/', AboutView.as_view(), name='about-us'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('terms/', TermsView.as_view(), name='terms'),
    path('policy/', PrivacyView.as_view(), name='policy'),
]
