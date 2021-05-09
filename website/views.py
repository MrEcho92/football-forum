from django.shortcuts import render
from django.views.generic import (TemplateView, )
#from website.forms import subscriberForm
#from website.models import subscriber


# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

class TermsView(TemplateView):
    template_name ='terms.html'

class PrivacyView(TemplateView):
    template_name ='privacy.html'

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request, exception=None):
    return render(request, '500.html', status=500)
