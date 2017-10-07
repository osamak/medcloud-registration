from django import forms
from .models import Registration, Batch, colleges 
from . import utils

class RegistrationForm(forms.ModelForm):
    college = forms.CharField(label=u'الكلية',
                              max_length=1,
                              widget=forms.Select(choices=colleges))
    number = forms.IntegerField(label=u"الدفعة", widget=forms.Select(choices=[(i, i) for i in range(1, 18)]))

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
