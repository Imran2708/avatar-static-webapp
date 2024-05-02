import logging
import requests
import os
import azure.functions as func

# Configure logging
logging.basicConfig(level=logging.INFO)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Get request method
    req_method = req.method
    logging.info(f'Request method: {req_method}')

    # Check if request method is POST
    if req_method != 'POST':
        logging.error('Invalid request method. Only POST requests are allowed.')
        return func.HttpResponse(
            body='Invalid request method. Only POST requests are allowed.',
            status_code=405,
            headers={
                "Content-Type": "text/plain"
            }
        )

    # Define subscription key and region
    subscription_key = os.environ.get("AZURE_SPEECH_API_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")

    if not subscription_key or not region:
        logging.error('AZURE_SPEECH_API_KEY or AZURE_SPEECH_REGION environment variable is missing.')
        return func.HttpResponse(
            body='AZURE_SPEECH_API_KEY or AZURE_SPEECH_REGION environment variable is missing.',
            status_code=500,
            headers={
                "Content-Type": "text/plain"
            }
        )

    # Define token endpoint
    token_endpoint = f"https://{region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"

    # Make HTTP request with subscription key as header
    try:
        response = requests.post(token_endpoint, headers={"Ocp-Apim-Subscription-Key": subscription_key})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f'Error fetching access token: {e}')
        return func.HttpResponse(
            body=f'Error fetching access token: {e}',
            status_code=500,
            headers={
                "Content-Type": "text/plain"
            }
        )

    if response.status_code == 200:
        access_token = response.text
        logging.info('Access token retrieved successfully.')

        cors_response = func.HttpResponse(
            access_token,
            status_code=200,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                "Content-Type": "text/plain"
            }
        )
        return cors_response
    else:
        logging.error(f'Error fetching access token. Status code: {response.status_code}')
        return func.HttpResponse(
            body=f'Error fetching access token. Status code: {response.status_code}',
            status_code=response.status_code,
            headers={
                "Content-Type": "text/plain"
            }
        )
