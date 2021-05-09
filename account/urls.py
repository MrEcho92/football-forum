from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import views
from account.views import SignUp, UserProfileView, UserProfileEditView, Account_Activation_sent
from django.urls import reverse_lazy

app_name='account'

urlpatterns = [

    path('login/', views.LoginView.as_view(template_name="account/login.html"),name='login'),
    path('logout/', views.LogoutView.as_view(next_page='/'), name="logout"),
    path('signup/', SignUp.as_view(), name="signup"),
    #sign up email sent
    path('account_activation_sent/', Account_Activation_sent.as_view(), name='account_activation_sent'),

    path('change-password/',auth_views.PasswordChangeView.as_view(template_name="account/change_password.html", success_url=reverse_lazy('account:password_change_done')), name='password_change' ),

    path('password_change_done/',auth_views.PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"), name='password_change_done' ),

    #password reset urls
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="account/password_reset_form.html",
                                                                 success_url= reverse_lazy('account:password_reset_done'),
                                                                 subject_template_name='account/password_reset_subject.txt'), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"), name="password_reset_done"),

    # See top level URLS.PY === auth_views.PasswordResetConfirmView.as_view()
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"), name="password_reset_complete"),


    #path('menu/', MenuView.as_view(), name="menu"),
    path('user/<slug:slug>/', UserProfileView.as_view(), name="dashboard"),
    path('edit_profile/', UserProfileEditView.as_view(), name="edit_profile"),

]
