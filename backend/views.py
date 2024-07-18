from django.shortcuts import render
from .models import Applicant
from .serializers import ApplicantSerializer, CreateApplicantSerializer

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(["GET", "POST"])
def applicant_list(request, format=None):
    if request.method == "GET":
        applicants = Applicant.objects.all()
        serializer = ApplicantSerializer(applicants, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = CreateApplicantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def applicant_detail(request, pk, format=None):
    try:
        applicant = Applicant.objects.get(pk=pk)
    except Applicant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = ApplicantSerializer(applicant)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = ApplicantSerializer(applicant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        applicant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

