from django.contrib import admin
from .models import Applicant

# Register your models here.

class ApplicantAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email', 'phone', 'school', 'major', 'grade', 'first_choice', 'second_choice', 'application_status')
    list_display = ('id', 'name', 'application_status', 'email', 'phone', 'school', 'major', 'grade', 'first_choice', 'second_choice')

    
admin.site.register(Applicant, ApplicantAdmin)