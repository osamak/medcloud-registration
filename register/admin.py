from django.contrib import admin
from register.models import Registration, Batch

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('email', 'group', 'is_successful', 'forgotten_password', 'submission_date')
    search_fields = ['email', 'unisersity_id']
    list_filter = ['batch', 'section', 'is_successful']

admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Batch)

