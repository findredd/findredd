from django.urls import path
from django.contrib.auth import views as auth_views

from main import views as main_views


urlpatterns = [
    path('', main_views.index, name='index'),
    path('careers', main_views.careers, name='careers'),
    path('raise_a_request/', main_views.raise_a_request, name='raise_a_request'),
    path('plasma_donor_registration/', main_views.plasma_donor, name='plasma_donor'),
    path('report_issue/', main_views.report_issue, name='report_issue'),
    path('team/', main_views.team, name='team'),
    path('about_us/', main_views.about_us, name="about_us"),
    path('contact_us/', main_views.contact_us, name="contact_us"),
    path('certificate/', main_views.certificate, name='certificate'),
    path('certificate/<str:certificate_number>/', main_views.certificate_details, name='certificate_details'),
    path('terms_of_service/', main_views.terms_of_service, name='terms_of_service'),
    path('privacy_policy/', main_views.privacy_policy, name='privacy_policy'),
    path('signup/', main_views.signup, name='signup'),
    path('signin/', main_views.signin, name='signin'),
    path('signout/', main_views.signout, name='signout'),
    path('settings/', main_views.settings_redirect, name='settings_redirect'),
    path('settings/<str:option>/', main_views.settings, name='settings'),
    path('password_reset/', main_views.PasswordResetMainView.as_view(template_name='main/password_reset.html'), name='password_reset'),
    path('password_reset_email_sent/', main_views.password_reset_email_sent, name='password_reset_email_sent'),
    path('password_reset_confirm/<uidb64>/<token>/', main_views.PasswordResetConfirmMainView.as_view(template_name='main/password_reset_confirm.html'), name='password_reset_confirm'),
    path('account_activation/<str:uidb64>/<str:token>/', main_views.account_activation, name='account_activation'),
    path('complete_profile/<str:arg>/', main_views.complete_profile, name='complete_profile'),
    path('<str:username>/', main_views.profile, name='profile'),
    path('<str:username>/<str:arg>/', main_views.profile, name='profile'),
]
