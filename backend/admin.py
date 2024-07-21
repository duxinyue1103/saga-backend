from django.contrib import admin
from .models import Applicant, ApplicationStatus, Interviewer
from django.contrib import messages


# Register your models here.

class ApplicantAdmin(admin.ModelAdmin):
    search_fields = ('name', 'school', 'major')
    list_display = ('id', 'name', 'email', 'school', 'major', 'grade', 'first_choice', 'second_choice')
    list_filter = ('grade', 'first_choice', 'second_choice', 'src')
    
class ApplicationStatusAdmin(admin.ModelAdmin):
    search_fields = ('applicant', )
    list_display = ('applicant', 'handle_by', 'status')
    list_filter = ('handle_by', 'status')
    autocomplete_fields = ('applicant', 'interviewer')
    actions = ['send_writing_task_email', 'send_interview_email', 'send_decision_email']
    
    def send_writing_task_email(self, request, queryset):
        all_success = True
        self.message_user(request, "处理中...", level=messages.INFO)
        for application in queryset:
           all_success = all_success and application.send_writing_task_email()
        if all_success:
            self.message_user(request, "全部笔试邮件发送成功")
        else:
            self.message_user(request, "某些笔试邮件发送失败", level=messages.WARNING)
    send_writing_task_email.short_description = "向选择的申请发送笔试邮件"
    
    def send_interview_email(self, request, queryset):
        all_success = True
        self.message_user(request, "处理中...", level=messages.INFO)

        for application in queryset:
            all_success = all_success and application.send_interview_email()
        if all_success:
            self.message_user(request, "全部面试邮件发送成功")
        else:
            self.message_user(request, "某些面试邮件发送失败", level=messages.WARNING)
    send_interview_email.short_description = "向选择的申请发送面试邮件"
    
    def send_decision_email(self, request, queryset):
        all_success = True
        self.message_user(request, "处理中...", level=messages.INFO)

        for application in queryset:
            all_success = all_success and application.send_decision_email()
        if all_success:
            self.message_user(request, "全部录取邮件发送成功")
        else:
            self.message_user(request, "某些录取邮件发送失败", level=messages.WARNING)
    send_decision_email.short_description = "向选择的申请发送录取/拒绝邮件"
    
    
class InterviewerAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ('name', 'department', "meeting_link")
    
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(ApplicationStatus, ApplicationStatusAdmin)
admin.site.register(Interviewer, InterviewerAdmin)

admin.site.disable_action('delete_selected')
