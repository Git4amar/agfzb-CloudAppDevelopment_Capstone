import requests
import json
import os
from .models import CarDealer, DealerReview
from dotenv import load_dotenv

# Load environement variables
load_dotenv()


def access_token(apikey):
    
    # get IAM access token
    iam_access = requests.post(
        url = "https://iam.cloud.ibm.com/identity/token",
        headers = {"Content-Type": "application/x-www-form-urlencoded"},
        data = {
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": apikey
        }
    )

    return json.loads(iam_access.text)["access_token"]


def request_to_functions(url, **kwargs):
    print(kwargs)
    print(f"POST request to {url}")

    fn_apikey = os.environ["FN_APIKEY"]

    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(f'{url}?blocking=true&result=true', headers={
            'accept': 'application/json',
            'Authorization': f"Bearer {access_token(fn_apikey)}",
            'content-type': 'application/json'
            }, data=json.dumps(kwargs))
    
    except:
        # If any error occurs
        print("Network exception occurred")
    
    else:
        status_code = response.status_code
        print(f"With Status {status_code}")
        json_data = response.json()
        return json_data


def get_dealers_from_cloudant(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = request_to_functions(url, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealers =  json_result["body"]["rows"] if len(kwargs.keys()) == 0 else json_result["body"]["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in 'doc' object
            dealer_doc = dealer["doc"] if len(kwargs.keys()) == 0 else dealer
            # Create a CarDealer instance with values from 'doc' object
            dealer_obj = CarDealer.from_dict(dealer_doc)
            
            results.append(dealer_obj)
    
    return results


def get_dealer_reviews_from_cloudant(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = request_to_functions(url, **kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealer_reviews =  json_result["body"]["rows"] if len(kwargs.keys()) == 0 else json_result["body"]["docs"]
        # For each dealer object
        for review in dealer_reviews:
            # Get its content in 'doc' object
            review_doc = review["doc"] if len(kwargs.keys()) == 0 else review
            review_obj = DealerReview.from_dict(review_doc)
            review_obj.sentiment=analyze_review_sentiment(review_obj.review)
            
            results.append(review_obj)

    return results


def analyze_review_sentiment(dealer_review):
    params = {
        "text": dealer_review,
        "version": "2022-04-07",
        "features": ["sentiment"],
        "return_analyzed_text": True,
        "language": "en"
    }

    nlu_apikey = os.environ["NLU_APIKEY"]

    response = requests.get(
        params = params,
        url = f'{os.environ["NLU_URL"]}/v1/analyze',
        headers = {
            'Authorization': f"Bearer {access_token(nlu_apikey)}",
            }
    )

    return response.json()["sentiment"]["document"]["label"]


def post_review(url, **kwargs):
    return request_to_functions(url, **kwargs)
