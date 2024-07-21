from django.contrib import admin
from .models import Applicant, ApplicationStatus, Interviewer

# Register your models here.

class ApplicantAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email', 'phone', 'school', 'major', 'grade', 'first_choice', 'second_choice')
    list_display = ('id', 'name', 'email', 'school', 'major', 'grade', 'first_choice', 'second_choice')

    
class ApplicationStatusAdmin(admin.ModelAdmin):
    search_fields = ('applicant', 'handle_by', 'status')
    list_display = ('applicant', 'handle_by', 'status')
    
    
class InterviewerAdmin(admin.ModelAdmin):
    search_fields = ('name', 'department', "meeting_link")
    list_display = ('name', 'department', "meeting_link")
    
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(ApplicationStatus, ApplicationStatusAdmin)
admin.site.register(Interviewer, InterviewerAdmin)