from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Registration, Batch, colleges
from . import utils, forms


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


@csrf_exempt
def register(request):
    if request.method == 'POST':
        password = utils.generate_password()
        initial_registration = Registration(password=password)
        form = forms.RegistrationForm(request.POST,
                                instance=initial_registration)
        if form.is_valid():
            email = form.cleaned_data['email']
            college = form.cleaned_data['college']
            if Registration.objects.filter(email__iexact=email, is_successful=True):
                context = {'form': form, 'error_message': u'already_registered'}
            else:
                registration = form.save()
                if college == 'FMRTP':
                    user = 'user%d' % registration.pk
                else:
                    user = email.split('@')[0].lower()
                group = str(registration.group)
                if utils.createuser(user, password, group):
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
        form = forms.RegistrationForm()
        context = {'form': form}

    return render(request, 'register/register.html', context)

@csrf_exempt
def forgotten(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try: 
                previous_registration = Registration.objects.get(email__iexact=email,
                                                                 is_successful=True)
            except ObjectDoesNotExist:
                previous_registration = None
                context = {'form': form, 'error_message': 'not_registered'}

            if previous_registration:
                new_password = utils.generate_password()
                user = previous_registration.email.split('@')[0]
                if utils.reset_password(user, new_password):
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
        form = forms.ResetPasswordForm()
        context = {'form': form}

    return render(request, 'register/reset.html', context)

