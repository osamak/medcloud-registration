from django.db import models

colleges = [
    ('', 'الكلية'),
    ('M', 'كلية الطب'),
    ('D', 'كلية الأسنان'),
    ('P', 'كلية الصيدلة'),
    ('N', 'كلية التمريض'),
    ('FMRTP', 'Family Medicine Residency Training Program')
]

class Batch(models.Model):
    number = models.PositiveSmallIntegerField(verbose_name=u"رقم الدفعة")
    college = models.CharField(max_length=10, choices=colleges,
                               verbose_name=u"الكلية")

    def __unicode__(self):
        return "%s%s" % (self.college, self.number)

class Registration(models.Model):
    email = models.EmailField(max_length=200,
                              verbose_name=u"البريد الجامعي")
    batch = models.CharField(max_length=3,
                             verbose_name=u"الدفعة")
    section = models.CharField(max_length=2,
                               verbose_name=u"القسم")
    group = models.ForeignKey(Batch, verbose_name=u"الدفعة",
                              null=True,
                              on_delete=models.SET_NULL)
    unisersity_id = models.PositiveIntegerField(null=True, blank=True,
                                       verbose_name=u"الرقم الجامعي")
    password = models.CharField(max_length=6)
    date = models.DateTimeField('date', auto_now=True)
    is_successful = models.BooleanField(default=False)
    forgotten_password = models.BooleanField(default=False)
    submission_date = models.DateTimeField(u'تاريخ الإرسال',
                                           auto_now_add=True, null=True)
    edit_date = models.DateTimeField(u'تاريخ التعديل', auto_now=True, null=True)

    def __unicode__(self):
        return self.email
