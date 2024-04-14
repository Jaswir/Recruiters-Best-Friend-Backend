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



url = "https://api.vectara.io/v1/query"
api_key = environ.get("API_KEY")
customer_id = environ.get("CUSTOMER_ID")
corpus_id =8


@api_view(["POST"])
def slackQuery(request):
    return JsonResponse({"result": "Hello, World!"})

@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter('company', openapi.IN_QUERY, description="Company name", type=openapi.TYPE_STRING),
        openapi.Parameter('prompt', openapi.IN_QUERY, description="Prompt for the query", type=openapi.TYPE_STRING),
    ]
)
@api_view(["GET"])
@parser_classes((MultiPartParser, FormParser))
def query(request):
    # Extract prompt from query parameters
    prompt = request.GET.get("prompt", "")  # Example: /query/?prompt=your_prompt_here
    company = request.GET.get("company", "")

        
    if not company:
        return JsonResponse({"result": "Invalid Company Name"}, status=400)
    if prompt:
        try:
            result = get_response(prompt, company)
            return JsonResponse({"result": result})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    if not prompt:
        return JsonResponse({"result": "Please insert question"}, status=400)
    

@swagger_auto_schema(
    method="post",
    manual_parameters=[
        openapi.Parameter(
            name="uploaded_file",
            in_=openapi.IN_FORM,
            description="PDF File about Company FAQ",
            type="file",
            required=True,
        ),
         openapi.Parameter('company', openapi.IN_QUERY, description="Company name", type=openapi.TYPE_STRING),
    ],
    responses={200: openapi.Response("File successfully uploaded!")},
)
@api_view(["POST"])
@parser_classes((MultiPartParser, FormParser))
def uploadFile(request):

    upload_url = f"https://api.vectara.io/v1/upload?c={customer_id}&o={corpus_id}"

    if "uploaded_file" not in request.FILES:
        return JsonResponse({"error": "No pdf file provided"}, status=400, safe=False)

    if not request.GET.get("company", ""):
        return JsonResponse({"error": "Company name not provided"}, status=400, safe=False)
    
    uploaded_file = request.FILES["uploaded_file"]

    company = request.GET.get("company", "")
    filename = uploaded_file.name

    files = [("file", (f"{filename}", uploaded_file.read(), "application/pdf"))]
    payload = {"doc_metadata": json.dumps({"Company": company})}

    headers = {
        "Accept": "application/json",
        "x-api-key": api_key,
        "customer-id": customer_id,
    }

    response = requests.request("POST", upload_url, headers=headers, data=payload, files=files)

    print(response.text)

    return JsonResponse(response.text, safe=False)


def get_response(prompt, company):
    payload = {
        "query": [
            {
                "query": prompt,
                "queryContext": "",
                "start": 0,
                "numResults": 10,
                "contextConfig": {
                    "charsBefore": 0,
                    "charsAfter": 0,
                    "sentencesBefore": 2,
                    "sentencesAfter": 2,
                    "startTag": "%START_SNIPPET%",
                    "endTag": "%END_SNIPPET%",
                },
                "corpusKey": [
                    {
                        "customerId": customer_id,
                        "corpusId": 8,
                        "semantics": 0,
                        "metadataFilter": f"doc.Company='{company}'",
                        "lexicalInterpolationConfig": {"lambda": 0.98},
                        "dim": [],
                    }
                ],
                "summary": [
                    {
                        "debug": False,
                        "chat": {"store": True, "conversationId": ""},
                        "maxSummarizedResults": 5,
                        "responseLang": "eng",
                        "summarizerPromptName": "vectara-summary-ext-v1.2.0",
                        "factualConsistencyScore": True,
                    }
                ],
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": api_key,
        "customer-id": customer_id,
    }

    response = requests.post(url, headers=headers, json=payload)

    response_data = response.json()
    result = response_data["responseSet"][0]["summary"][0]["text"]
    return result
