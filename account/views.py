from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView, DetailView, UpdateView
from django.views import View
from account.forms import UserCreateForm, UserProfileForm
from account.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin,  UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin

#sign off with email activation
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from account.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth import login

from forum.models import Post, Comment
from news.models import News


# Create your views here.
class SignUp(SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    #success_url = reverse_lazy("account:login")
    template_name = "account/signup.html"
    success_message = "Your account was created successfully and please confirm your email address to complete registration."

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  #set to false bcos user cannot login
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your ViewingSport account' #Remember to change if name is changed!
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message) #from user model
            return redirect('account:account_activation_sent')
        else:
            form = UserCreateForm()
        return render(request, 'account/signup.html', {'form': form})

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.userprofile.email_confirmed = True
            user.save()
            login(request, user)
            return redirect('account:login')
        else:
            #return HttpResponse('Activation link is invalid!')
            return render(request, 'account/invalid.html')

class Account_Activation_sent(TemplateView):
    template_name = 'account/account_activation_sent.html'


class UserProfileView(DetailView):
    model = User
    template_name = 'account/userprofile_detail.html'
    slug_field = 'username'


    #GET or Create user object
    def get_object(self, queryset=None):
        user = super(UserProfileView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user

    #Context for rendering in html
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userprofile'] = UserProfile
        username = self.kwargs.get('slug')
        user = get_object_or_404(User, username=username)
        context['posts'] = Post.objects.filter(author_id=user.pk) #User post list
        context['comments'] = Comment.objects.filter(user_id=user.pk) #User comment list
        context['draft_news'] = News.objects.filter(status=0).order_by('-created_date') #filter draft news
        return context


class UserProfileEditView(LoginRequiredMixin, UserPassesTestMixin,SuccessMessageMixin, UpdateView):
    model = UserProfile
    context_object_name = 'profile'
    form_class = UserProfileForm
    #form_class = UserCreateForm
    template_name = 'account/edit_profile.html'
    success_message = "Profile was updated successfully"

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_success_url(self):
        return reverse("account:dashboard", kwargs={'slug': self.request.user})

    # UserPassesTestMixin - prevent user accessing other users post
    def test_func(self):
        userprofile= self.get_object()
        if self.request.user == userprofile.user:
            return True
        return False

#function
