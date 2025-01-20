"""
sentiment_analysis.py

This module provides a function to perform sentiment analysis on a given text 
using an external API (Watson NLP SentimentPredict). The function sends the 
text to the API and processes the returned sentiment label and score.

Functions:
- sentiment_analyzer(text_to_analyse): Sends text to the API and returns 
  the sentiment label and score.
"""

import requests

def sentiment_analyzer(text_to_analyse):
    """
    This function sends text to the API and returns 
    the sentiment label and score.
    """
    # Define the URL for the sentiment analysis API
    url = ('https://sn-watson-sentiment-bert.labs.skills.network/v1/watson.runtime.nlp.v1'
           '/NlpService/SentimentPredict')
    # Create the payload with the text to be analyzed
    myobj = { "raw_document": { "text": text_to_analyse } }
    # Set the headers with the required model ID for the API
    header = {"grpc-metadata-mm-model-id": "sentiment_aggregated-bert-workflow_lang_multi_stock"}
    # Initialize label and score as None before request
    label = None
    score = None

    try:
        # Make a POST request to the API with the payload and headers
        response = requests.post(url, json=myobj, headers=header, timeout=10)
        # Check if the response status code is 200 (OK)
        if response.status_code == 200:
            formatted_response = response.json()  # Parse JSON response
            # Safely access the 'label' and 'score' fields
            label = formatted_response.get('documentSentiment', {}).get('label', None)
            score = formatted_response.get('documentSentiment', {}).get('score', None)
        # Handle 500 status (server error)
        elif response.status_code == 500:
            print("Server error (500): Unable to process the request.")
        # Other status codes
        else:
            print(f"Error: Received unexpected status code {response.status_code}")

    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

    # Return the label and score in a dictionary
    return {'label': label, 'score': score}
