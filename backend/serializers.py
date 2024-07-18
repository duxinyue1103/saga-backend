from rest_framework import serializers
from .models import Applicant

class CreateApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = ["name", "email", "phone", "school",
                  "major", "grade", "sex", "wechat",
                  "first_choice", "second_choice", "third_choice",
                  "preferred_subject", "self_intro", "disposable_time",
                  "src"]


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = "__all__"
        # exclude = ("id", "created_at")
        