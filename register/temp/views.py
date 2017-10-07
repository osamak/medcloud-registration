# -*- coding: utf-8  -*-
import json
import os
import random
import requests
import re
import subprocess
import string

from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from constance import config

from register.models import Registration, Batch, colleges


new_message = u"""نشكرك على التسجيل في السحابة الطبية
اسم المستخدم: %s
كلمة السر: %s
رابط السحابة: https://ksauhs-med.com/
آملين أن تجد فيها ما يفيد!
"""

forgotten_message = u"""هذه معلوماتك الجديدة للدخول إلى السحابة الطبية:
اسم المستخدم: %s
كلمة السر: %s
رابط السحابة: https://ksauhs-med.com/
آملين أن تجد فيها ما يفيد!
"""

class RegistrationForm(forms.ModelForm):
    college = forms.CharField(label=u'الكلية',
                              max_length=1,
                              widget=forms.Select(choices=colleges))
    number = forms.IntegerField(label=u"الدفعة", widget=forms.Select(choices=[(i, i) for i in range(1, 17)]))

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        batch_msg = u"الدفعة التي اخترت غير موجودة."
        if 'college' in cleaned_data and 'number' in cleaned_data:
            try:
                Batch.objects.get(
                    college=cleaned_data['college'],
                    number=int(cleaned_data['number']))
            except Batch.DoesNotExist:
                self._errors['college'] = self.error_class([batch_msg])
                self._errors['number'] = self.error_class([batch_msg])
                del cleaned_data['college']
                del cleaned_data['number']

        return cleaned_data

    def save(self):
        new_registration = super(RegistrationForm, self).save()
        batch = Batch.objects.get(
            college=self.cleaned_data['college'],
            number=int(self.cleaned_data['number']),
            )
        new_registration.group = batch
        new_registration.save()
        return new_registration

    class Meta:
        model = Registration
        fields = ['email', 'college', 'number', 'unisersity_id']
        widgets = {
            'university_id': forms.TextInput(),
        }

class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label=u'بريدك الجامعي', max_length=100)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        password = generate_password()
        initial_registration = Registration(password=password)
        form = RegistrationForm(request.POST,
                                instance=initial_registration)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not email.endswith('ksau-hs.edu.sa'):
                context = {'form': form, 'error_message': 'university_email'}
            elif Registration.objects.filter(email__iexact=email, is_successful=True):
                context = {'form': form, 'error_message': u'already_registered'}
            else:
                user = email.split('@')[0].lower()
                registration = form.save()
                group = str(registration.group)
                if createuser(user, password, group):
                    registration.is_successful = True
                    registration.save()
                    send_mail(u'حسابك على السحابة الطبية', new_message %
                              (user, password), 'info@ksauhs-med.com',
                              [email], fail_silently=False)
                    return HttpResponseRedirect(reverse('register:thanks'))
                else:
                    context = {'form': form, 'error_message': 'unknown'}

        else:
            context = {'form': form}
    else:
        form = RegistrationForm()
        context = {'form': form}

    return render(request, 'register/register.html', context)

@csrf_exempt
def forgotten(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not email.endswith('ksau-hs.edu.sa'):
                context = {'form': form, 'error_message': 'university_email'}
            else:
                try: 
                    previous_registration = Registration.objects.get(email__iexact=email,
                                                                     is_successful=True)
                except ObjectDoesNotExist:
                    previous_registration = None
                    context = {'form': form, 'error_message': 'not_registered'}

                if previous_registration:
                    new_password = generate_password()
                    user = previous_registration.email.split('@')[0]
                    if reset_password(user, new_password):
                        previous_registration.password = new_password
                        previous_registration.forgotten_password = True
                        previous_registration.save()
                        send_mail(u'حسابك على السحابة الطبية', forgotten_message %
                                  (user, new_password), 'info@ksauhs-med.com',
                                  [email], fail_silently=False)
                        return HttpResponseRedirect(reverse('register:thanks'))
                    else:
                        context = {'form': form, 'error_message': 'unknown'}
        else:
            context = {'form': form}
    else:
        form = ResetPasswordForm()
        context = {'form': form}

    return render(request, 'register/reset.html', context)

def generate_password():
    return ''.join(random.choice(string.ascii_uppercase) for i in range(6))

def login():
    homepage_url = "https://www.ksauhs-med.com"

    homepage = requests.get(homepage_url)
    oc1d6beae686 = homepage.cookies['oc1d6beae686']
    cookies = {'oc1d6beae686': oc1d6beae686}
    login_requesttoken_regex = re.compile('data-requesttoken="(.+?)"', re.U)
    login_requesttoken = re.findall(login_requesttoken_regex, homepage.content)[0]
    login_data = {'user': config.OWNCLOUD_ADMIN_USERNAME,
                  'password': config.OWNCLOUD_ADMIN_PASSWORD,
                  'requesttoken': login_requesttoken,
                  'remember_login': '1',
                  'timezone-offset': 'Asia/Baghdad',
                  }
    login_page = requests.post(homepage_url, data=login_data, cookies=cookies)
    login_cookies = login_page.history[0].cookies
    cookies = {#'oc_username': login_cookies['oc_username'],
               #'oc_token': login_cookies['oc_token'],
               #'oc_remember_login': login_cookies['oc_remember_login'],
               'oc1d6beae686': login_cookies['oc1d6beae686'],
               }
    return cookies

def createuser(user, password, group):
    os.environ['OC_PASS'] = password
    command = "/usr/local/bin/php70 /home/medcloud/webapps/ownphp70/occ user:add {} --password-from-env -g {} -n".format(user, group)
    output = subprocess.call(command, shell=True)
    if output == 0:
        return True
    else:
        return False

    # createuser_url = "https://www.ksauhs-med.com/index.php/settings/users/users"
    # user_url = "https://www.ksauhs-med.com/index.php/settings/users"

    # login_cookies = login()
    # user_page = requests.post(user_url, cookies=login_cookies)
    # regex = re.findall("data-requesttoken=\"([^\"]+)\"", user_page.text)
    # requesttoken = regex[0]
    # user_data = {'username': user,
    #              'password': password,
    #              'groups[]': group}

    # headers = {'requesttoken': requesttoken}
    # createuser_page = requests.post(createuser_url, data=user_data, cookies=login_cookies, headers=headers)
    # json_object = json.loads(createuser_page.text)

    # if createuser_page.status_code == 201:
    #     return True
    # else:
    #     print json_object # REMOVE

def reset_password(user, password):
    os.environ['OC_PASS'] = password
    command = "/usr/local/bin/php70 /home/medcloud/webapps/ownphp70/occ user:resetpassword {} --password-from-env -n".format(user)
    output = subprocess.call(command, shell=True)
    if output == 0:
        return True
    else:
        return False

    # changepassword_url = "https://www.ksauhs-med.com/index.php/settings/users/changepassword"
    # user_url = "https://www.ksauhs-med.com/index.php/settings/users"

    # login_cookies = login()
    
    # user_page = requests.post(user_url, cookies=login_cookies)
    # regex = re.findall("data-requesttoken=\"([^\"]+)\"", user_page.text)
    # requesttoken = regex[0]
    # user_data = {'username': user,
    #              'password': password}
    # headers = {'requesttoken': requesttoken,
    #            'X-Requested-With': 'XMLHttpRequest',
    #            'Referer': user_url}
    # changepassword_page = requests.post(changepassword_url,
    #                                     data=user_data,
    #                                     cookies=login_cookies,
    #                                     headers=headers)
    # try:
    #     json_object = json.loads(changepassword_page.text)
    # except ValueError:
    #     json_object = {}

    # if json_object.get('status') == 'success':
    #     return True
