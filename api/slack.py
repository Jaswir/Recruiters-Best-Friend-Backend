from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework import status
import requests
import json
from os import environ
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser

verification_token = environ.get("VERIFICATION_TOKEN")
@api_view(["POST"])
def slash(request):

    print("SLASH SLASH BABY")
    print(request)
    print(request.data)
    text = request.get('text', '')

 
    data = {
        "response_type": "in_channel",
        "text": "sending just text yes",
    }
    return Response(data, status=status.HTTP_200_OK)
