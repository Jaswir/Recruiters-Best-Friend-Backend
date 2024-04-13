from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import requests
import json
import streamlit as st


url = "https://api.vectara.io/v1/query"
api_key = "zut_IccVS9aWrgH6-s9K--BKSt9pVfYKgClXR8j3cg" 

@require_http_methods(["GET"])
def query(request):
    # Extract prompt from query parameters
    prompt = request.GET.get('prompt', '')  # Example: /cat/?prompt=your_prompt_here

    if prompt:
        try:
            result = get_response(prompt)
            return JsonResponse({'result': result})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Missing prompt parameter'}, status=400)

def get_response(prompt):
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
                        "customerId": 566695243,
                        "corpusId": 7,
                        "semantics": 0,
                        "metadataFilter": "",
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
        "customer-id": "566695243",
    }

    response = requests.post(url, headers=headers, json=payload)

    response_data = response.json()
    result = response_data["responseSet"][0]["summary"][0]["text"]
    return result