from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.core.paginator import Paginator

from main.forms import (
    blood_donor_search_form,
    user_profile_edit_form,
    user_username_edit_form,
    user_email_edit_form,
    user_email_config_form,
    user_userdetail_edit_form,
    user_location_edit_form,
    user_mobile_edit_form,
    user_mobile_config_form,
    user_social_edit_form,
    user_location_config_form,
    RegistrationForm,
    user_account_deactivate_form,
    user_profile_picture_edit_form,
    user_issue_form,
    user_message_form,
    user_complete_profile_info_form,
    certificate_search_form,
    blood_request_form, )

from main.models import (
    Certificate,
    DistrictCoordinator, )

from django.contrib.auth.forms import ( 
    AuthenticationForm,
    PasswordChangeForm )

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

from django.contrib.auth.hashers import check_password
from django.urls import reverse, reverse_lazy
from urllib.parse import urlencode, quote_plus

from main.utils import EmailThread, AccountActivationTokenGenerator

from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from django.core.mail import EmailMessage
from django.conf import settings as conf_settings

from django.db.models import Q
from sentry_sdk import capture_message


def index(request):
    form = blood_donor_search_form(request.GET or None)

    district = request.GET.get('district')
    blood_group = request.GET.get('blood_group')

    if district and blood_group:
        objects = User.objects.filter(userdetail__district__iexact=district).filter(userdetail__blood_group__iexact=blood_group).filter(userdetail__status__exact='Available').filter(is_active=True).order_by('-date_joined')

        paginator = Paginator(objects, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'page_obj': page_obj, 'district': district, 'blood_group': blood_group, 'search_path': urlencode({'district': district, 'blood_group': blood_group}, quote_via=quote_plus)}
        return render(request, 'main/blood_donor_search.html', context)
        
    district_coordinators = DistrictCoordinator.objects.values('district', 'name', 'mobile_number')[:25]

    context = {'form': form, 'district_coordinators': district_coordinators}
    return render(request, 'main/index.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.is_active = False
        instance.save()

        activation_link = 'http://' + get_current_site(request).domain + reverse('account_activation', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(instance.id)), 'token': AccountActivationTokenGenerator().make_token(instance)})

        account_activation_email = EmailMessage(
            '[FindREDD] Account activation link for @' + instance.username,
            'Hi @' + instance.username + ', Please click the link below to activate your account \n' + activation_link +'\n\nThe FindREDD System\n//This is an auto generated email "DO-NOT-REPLY-HERE"',
            conf_settings.EMAIL_HOST_USER,
            [instance.email],
        )

        EmailThread(account_activation_email).start()

        messages.success(request, 'Activation link has been sent to - %s' % instance.email )

        return redirect('signin')

    content = {'form': form}
    return render(request, 'main/signup.html', content)


def account_activation(request, uidb64, token):
    try:
        user = get_object_or_404(User, pk=force_str(urlsafe_base64_decode(uidb64)))

        if not AccountActivationTokenGenerator().check_token(user, token):
            return redirect('signin')

        if user.is_active:
            return redirect('signin')

        user.is_active = True
        user.save()

        login(request, user)

        request.session['acc_temp'] = 'account_activation'

        messages.add_message(request, messages.SUCCESS, 'Account for @%s has been activated successfully' % user.username, extra_tags='alert-success')

        return redirect('complete_profile', 'info')
    
    except Exception:
        return redirect('index')


def complete_profile(request, arg=None):
    if 'acc_temp' in request.session:

        if arg == 'info':
            form = user_complete_profile_info_form(request.POST or None, instance=request.user.userdetail)

            if form.is_valid():
                form.save()

                messages.add_message(request, messages.SUCCESS, 'Profile info has been saved', extra_tags='alert-success')

                return redirect('complete_profile', 'contact')

            if form.errors:
                messages.add_message(request, messages.ERROR, form.errors, extra_tags='alert-danger')

            context = {'form': form}
            return render(request, 'main/complete_profile_info.html', context)

        if arg == 'contact':
            form_MN = user_mobile_edit_form(request.POST or None, instance=request.user.userdetail)
            form_LN = user_location_edit_form(request.POST or None, instance=request.user.userdetail)

            if form_MN.is_valid() and form_LN.is_valid():
                form_MN.save()
                form_LN.save()

                messages.add_message(request, messages.SUCCESS, 'Profile contact has been saved, you can further customize your profile in', extra_tags='alert-success')

                return redirect('profile', request.user.username)

            if form_MN.errors:
                messages.add_message(request, messages.ERROR, form_MN.errors, extra_tags='alert-danger')

            if form_LN.errors:
                messages.add_message(request, messages.ERROR, form_LN.errors, extra_tags='alert-danger')

            context = {'form_MN': form_MN, 'form_LN': form_LN}
            return render(request, 'main/complete_profile_contact.html', context)

    return redirect('index')


def signin(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user)

    form = AuthenticationForm(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if request.GET:
                return HttpResponseRedirect(request.GET['next'])
                
            return redirect('profile', username)
            
    content = {'form': form}
    return render(request, 'main/signin.html', content)


def signout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('index')


def profile(request, username=None, arg=None):
    if request.user.username.lower() == username.lower():

        if arg == 'photo':
            return render(request, 'main/photo.html', {'object': request.user})

        elif arg and arg!= 'photo':
            return render(request, 'main/404.html')

        form = user_profile_edit_form(request.POST or None, instance=request.user.userdetail)

        if form.is_valid():
            form.save()
            
            messages.add_message(request, messages.SUCCESS, 'Profile has been updated successfully', extra_tags='alert-success')
            
            return redirect('profile', request.user)
        
        if form.errors:
            messages.add_message(request, messages.ERROR, form.errors, extra_tags='alert-danger')

        temp_acc_profile = False

        if 'acc_temp' in request.session:
            temp_acc_profile = True

            del request.session['acc_temp']        

        context = {'object': request.user, 'username': username, 'form': form, 'temp_acc_profile': temp_acc_profile}
        return render(request, 'main/profile.html', context)

    try:
        objects = User.objects.get(Q(username__iexact=username) & Q(is_active=True))

        if arg == 'photo':
            return render(request, 'main/photo.html', {'object': objects})

        elif arg and arg!= 'photo':
            return render(request, 'main/404.html')

    except ObjectDoesNotExist:
        context = {'username': username}
        return render(request, 'main/user_does_not_exit.html', context)

    context = {'object': objects}
    return render(request, 'main/profile.html', context)


def settings_redirect(request):
    return redirect('settings', 'profile')


@login_required
def settings(request, option=None):
    if option == 'profile':
        form = user_userdetail_edit_form(request.POST or None, instance=request.user.userdetail)
        form_PP = user_profile_picture_edit_form(request.POST or None, request.FILES or None, instance=request.user.userpicture)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile updated successfully', extra_tags='alert-success')
                
            return redirect('settings', 'profile')

        elif form_PP.is_valid():
            form_PP.save()
            
            messages.add_message(request, messages.SUCCESS, 'Profile updated successfully', extra_tags='alert-success')
                
            return redirect('settings', 'profile')

        if form.errors:
            messages.add_message(request, messages.ERROR, form.errors, extra_tags='alert-danger')

        context = {'object': request.user, 'form': form, 'form_PP': form_PP, 'temp': True}
        return render(request, 'main/settings_profile.html', context)

    if option == 'account':
        form = user_username_edit_form(request.POST or None, instance=request.user)
        form_AD = user_account_deactivate_form(request.POST or None)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Username has been changed successfully', extra_tags='alert-success')

            return redirect('settings', 'account')

        if form_AD.is_valid():
            password = form_AD.cleaned_data['password']

            if request.user.check_password(password):
                request.user.is_active = False
                request.user.save()

                messages.add_message(request, messages.SUCCESS, 'Account has been deactivated successfully', extra_tags='alert-success')
                logout(request)

                return redirect('index')

            messages.add_message(request, messages.ERROR, 'Password did not matched', extra_tags='alert-danger')

            return redirect('settings', 'account')


        if form.errors:
            messages.add_message(request, messages.ERROR, form.errors, extra_tags='alert-danger')
                  
        context = {'object': request.user, 'form': form, 'form_AD': form_AD}
        return render(request, 'main/settings_account.html', context)

    if option == 'mobile':
        form = user_mobile_edit_form(request.POST or None, instance=request.user.userdetail)
        form_MN = user_mobile_config_form(request.POST or None, instance=request.user.userconfig)

        if form.is_valid() and form_MN.is_valid():
            form.save()
            form_MN.save()

            messages.add_message(request, messages.SUCCESS, 'Mobile settings updated successfully', extra_tags='alert-success')

            return redirect('settings', 'mobile')

        if form.errors:
            messages.add_message(request, messages.ERROR, form.errors, extra_tags='alert-danger')

        context = {'object': request.user, 'form': form, 'form_MN': form_MN}
        return render(request, 'main/settings_mobile.html', context)

    if option == 'email':
        form = user_email_edit_form(request.POST or None, instance=request.user)
        form_EA = user_email_config_form(request.POST or None, instance=request.user.userconfig)

        if form.is_valid() and form_EA.is_valid():
            form.save()
            form_EA.save()

            messages.add_message(request, messages.SUCCESS, 'Email settings updated successfully', extra_tags='alert-success')

            return redirect('settings', 'email')

        if form.errors:
            messages.add_message(request, messages.ERROR, form.errors, extra_tags='alert-danger')

        context = {'object': request.user, 'form': form, 'form_EA': form_EA}
        return render(request, 'main/settings_email.html', context)

    if option == 'location':
        form = user_location_edit_form(request.POST or None, instance=request.user.userdetail)
        form_LN = user_location_config_form(request.POST or None, instance=request.user.userconfig)

        if form.is_valid() and form_LN.is_valid():
            form.save()
            form_LN.save()
            messages.add_message(request, messages.SUCCESS, 'Location settings updated successfully', extra_tags='alert-success')

            return redirect('settings', 'location')

        if form.errors:
            messages.add_message(request, messages.ERROR, form.errors, extra_tags='alert-danger')

        context = {'object': request.user, 'form': form, 'form_LN': form_LN}
        return render(request, 'main/settings_location.html', context)

    if option == 'social':
        form = user_social_edit_form(request.POST or None, instance=request.user.usersocialurl)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Social link has been updated successfully', extra_tags='alert-success')

            return redirect('settings', 'social')

        if form.errors:
            messages.add_message(request, messages.ERROR, form.errors, extra_tags='alert-danger')

        context = {'object': request.user, 'form': form}
        return render(request, 'main/settings_social.html', context)

    if option == 'security':
        form = PasswordChangeForm(data=request.POST or None, user=request.user)

        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Password has been changed successfully', extra_tags='alert-success')

            return redirect('settings', 'profile')

        if form.errors:
            messages.add_message(request, messages.ERROR, form.errors, extra_tags='alert-danger')

        context = {'object': request.user, 'form': form}
        return render(request, 'main/settings_security.html', context)

    context = {'object': request.user}
    return render(request, 'main/settings_profile.html', context)    


def password_reset_email_sent(request):
    if 'temp' in request.session:
        del request.session['temp']

        return render(request, 'main/password_reset_email_sent.html')

    return redirect('index')


def about_us(request):
    return render(request, 'main/about_us.html')


def contact_us(request):
    form = user_message_form(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)

        user_name = instance.name
        user_email = instance.email
        user_message = instance.message

        account_activation_email = EmailMessage(
            'New message from - %s' % user_name,
            'Hi admin, a new message is sent to FindREDD.\n\n<Sender Details>:\n\n<Name>: %s \n<Email>: %s \n<Message>: %s \n-------------------\n\nThe FindREDD System\n//This is an auto generated email "DO-NOT-REPLY-HERE"' % (user_name, user_email, user_message),
            conf_settings.EMAIL_HOST_USER,
            ['info.findredd@gmail.com'],
        )

        EmailThread(account_activation_email).start()

        instance.save()

        messages.success(request, "Thank you for messaging us, we'll reach you soon!")

        return redirect('contact_us')

    context = {'form': form}

    return render(request, 'main/contact_us.html', context)


def report_issue(request):
    form = user_issue_form(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.username = request.user

        reporter_name = request.user.userdetail.name
        reporter_username = request.user
        reporter_email = request.user.email
        issue_category = instance.category
        issue_heading = instance.heading
        issue_description = instance.description

        new_issue_email = EmailMessage(
            'New issue from - %s' %reporter_name,
            'Hi admin, a new issue is reported to FindREDD.\n\n<Reporter Details>:\n\n<Name>: %s \n<Username>: @(%s) \n<Email>: %s \n-------------------\n\n<Issue Details>: \n\n<Category>: %s \n<Heading>: %s \n<Discription>: %s \n\n====================\n\nThe FindREDD System\n//This is an auto generated email "DO-NOT-REPLY"' % (reporter_name, reporter_username, reporter_email, issue_category, issue_heading, issue_description),
            conf_settings.EMAIL_HOST_USER,
            ['developer.findredd@gmail.com', ],
        )

        if request.FILES:
            issue_attachment = request.FILES['attachment']
            account_activation_email.attach(issue_attachment.name, issue_attachment.read(), issue_attachment.content_type)

        EmailThread(new_issue_email).start()

        instance.save()

        messages.success(request, 'Issue has been reported successfully.')

        return redirect('report_issue')

    return render(request, 'main/report_issue.html', {'form': form})


def certificate(request):
    form = certificate_search_form(request.POST or None)
    if form.is_valid():
        certificate_number = form.cleaned_data['certificate_number']

        return redirect('certificate_details', certificate_number)

    return render(request, 'main/certificate.html', {'form': form})


def certificate_details(request, certificate_number=None):
    certificate = get_object_or_404(Certificate, certificate_number=certificate_number)
    return render(request, 'main/certificate_details.html', {'certificate': certificate, 'certificate_number': certificate_number})


def raise_a_request(request):
    form = blood_request_form(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)

        patient_name = instance.patient_name
        form_filler_name = instance.your_name
        district = instance.district
        hospital_address = instance.hospital_address
        mobile_number = instance.mobile_number
        alternate_mobile_number = instance.alternate_mobile_number
        blood_group_required = instance.blood_group_required
        units_required = instance.units_required

        blood_request_email = EmailMessage(
            'New blood request from - %s' %form_filler_name,
            'Hi admin, a new blood request is raised to FindREDD.\n\nRequest Details:\n================\n\nPatient name: %s \nFormfiller name: %s \nDistrict: %s \nBlood group required: %s \nUnits required: %s \nMobile number: %s \nAlternate mobile number: %s \nHospital address: %s \n\n====================\n\nThe FindREDD System\n//This is an auto generated email "DO-NOT-REPLY"' % (patient_name, form_filler_name, district, blood_group_required, units_required, mobile_number, alternate_mobile_number, hospital_address, ),
            conf_settings.EMAIL_HOST_USER,
            ['divam3003@gmail.com', ],
        )

        EmailThread(blood_request_email).start()

        instance.save()

        messages.success(request, 'Request has been submitted successfully.')

        return redirect('raise_a_request')

    context = {'form': form}
    return render(request, 'main/raise_a_request.html', context)


def terms_of_service(request):
    return render(request, 'main/terms_of_service.html')


def privacy_policy(request):
    return render(request, 'main/privacy_policy.html')


def team(request):
    return render(request, 'main/team.html')


# Error Handler View
def error_404(request, exception=None):
    capture_message("Page not found!", level="error")
    
    return render(request, 'main/404.html')
    
    
# Django Contrib Auth Views
class PasswordResetMainView(SuccessMessageMixin, PasswordResetView):
    success_url = reverse_lazy('password_reset_email_sent')

    def dispatch(self, request, *args, **kwargs):
        request.session['temp'] = 'password_reset_email_sent'
        return super().dispatch(request, *args, **kwargs)


class PasswordResetConfirmMainView(SuccessMessageMixin, PasswordResetConfirmView):
    success_url = reverse_lazy('signin')
    success_message = 'Your new password has been created successfully, you can now login with your new password.'
