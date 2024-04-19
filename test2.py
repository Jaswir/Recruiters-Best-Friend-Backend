import requests
import os

api_key = os.environ.get("API_KEY")
customer_id = "566695243"
corpus_id = 12

prompt = "Hi"

payload = {
    "query": [
        {
            "query": prompt,
            "queryContext": "",
            "start": 0,
            "numResults": 3,
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
                    "metadataFilter": "",
                    "lexicalInterpolationConfig": {"lambda": 1},
                    "dim": [],
                }
            ],
            "summary": [
                {
                    "debug": False,
                    "chat": {"store": True, "conversationId": ""},
                    "maxSummarizedResults": 3,
                    "responseLang": "eng",
                    "summarizerPromptName": "vectara-experimental-summary-ext-2023-12-11-large",
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
}
url = "https://api.vectara.io/v1/query"
response = requests.post(url, headers=headers, json=payload)

response_data = response.json()
result = response_data["responseSet"][0]["summary"][0]["text"]
factualConsistencyScore = response_data["responseSet"][0]["summary"][0][
    "factualConsistency"
]["score"]


print("This is the results we are getting ", response_data)
print("\nText: " + result)
print("Factual Consistency Score: ", factualConsistencyScore)

if factualConsistencyScore < 0.29:
    print("The response is not factually consistent")