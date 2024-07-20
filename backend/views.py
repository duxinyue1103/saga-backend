from django.shortcuts import render
from .models import Applicant
from .serializers import UploadWritingTestApplicantSerializer, CreateApplicantSerializer, ApplicantSerializer, WritingTestFileSerializer
from .email import send_email, compose_email

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["POST"])
def applicant_create(request, format=None):
    if request.method == "POST":
        serializer = CreateApplicantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            res = send_email(serializer.data["email"],
                       "SAGA星光·第五期: 笔试邀请",
                       compose_email(serializer.data["id"], serializer.data["name"],
                                     serializer.data["first_choice"],
                                     serializer.data["created_at"])
                       )
            if res:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                serializer.delete()
                return Response("Failed to send email", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT"])
def applicant_submit(request, pk, format=None):
    try:
        applicant = Applicant.objects.get(pk=pk)
    except Applicant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = UploadWritingTestApplicantSerializer(applicant)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = UploadWritingTestApplicantSerializer(applicant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(["PUT", "DELETE"])
def file_detail(request, pk, format=None):
    try:
        applicant = Applicant.objects.get(pk=pk)
    except Applicant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        serializer = WritingTestFileSerializer(applicant, data=request.data)
        if request.data.get("writing_test_file").size > 1024 * 1024 * 10:
            return Response("File size too large", status=status.HTTP_400_BAD_REQUEST)
        elif request.data.get("writing_test_file").content_type != "application/pdf":
            return Response("File type not supported", status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response(request.data.get("writing_test_file").name, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        applicant.writing_test_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)