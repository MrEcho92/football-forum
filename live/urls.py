from django.urls import path
from live.views import  FixtureView #subscriberView,

app_name='live'

urlpatterns = [
    #path('subscribe/', subscriberView, name='subscriber'),
    path('live-scores/', FixtureView.as_view(), name='live-scores'),

]
