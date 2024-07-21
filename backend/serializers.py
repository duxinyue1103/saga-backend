from rest_framework import serializers
from .models import Applicant, ApplicationStatus

class CreateApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ["name", "email", "phone", "school",
                  "major", "grade", "sex", "wechat",
                  "first_choice", "second_choice", "third_choice",
                  "preferred_subject", "self_intro", "disposable_time",
                  "src",]        


class WritingTaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        read_only_fields = ["handle_by", "writing_task_ddl",]
        fields = ["handle_by", "writing_task_ddl", "writing_task_file", "writing_task_video_link"]
        
        
class WritingTaskSerializer(serializers.ModelSerializer):
    applications = serializers.SerializerMethodField()
    
    def get_applications(self, applicant):
        from django.db.models import Q
        
        queryset = applicant.applications.filter(Q(status="NEW_APPLICATION") | Q(status="WRTIING_TASK_EMAIL_SENT"))
        serializer = WritingTaskStatusSerializer(queryset, many=True)
        return serializer.data
    
    class Meta:
        model = Applicant
        fields = ["name", "applications"]


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = "__all__"
        # exclude = ("id", "created_at")
        