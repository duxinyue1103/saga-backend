from backend import views
from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns



urlpatterns = [
    path('applicants/', views.applicant_list),
    re_path(r'^applicants/(?P<pk>[0-9]+)$', views.applicant_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)