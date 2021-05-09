from django.shortcuts import render
from django.views.generic.edit import  FormView
from website.forms import subscriberForm
from website.models import subscriber
from django.contrib import messages
# Create your views here.

class FixtureView(FormView):
    template_name = 'fixture.html'
    form_class = subscriberForm

    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST or None)

            if form.is_valid():
                f = form.save(commit=False)
                if subscriber.objects.filter(email=f.email).exists():
                    messages.warning(request, 'Email already exists in our database.')
                else:
                    f.save()
                    return render(request,self.template_name)
        else:
            form =subscriberForm()

        return render(request, self.template_name)


'''
def subscriberView(request):

    if request.method == 'POST':
        form = subscriberForm(request.POST or None)

        if form.is_valid():
            f = form.save(commit=False)
            if subscriber.objects.filter(email=f.email).exists():
                messages.warning(request, 'Email already exists in our database.')
            else:
                f.save()
                return render(request,'fixture.html')
    else:
        form =subscriberForm()

    context = {
    'form': form,
    }
    return render(request, 'fixture.html', context)
'''
