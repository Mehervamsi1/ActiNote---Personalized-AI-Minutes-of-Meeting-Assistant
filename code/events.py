import json
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

tenant_id = os.getenv("AZURE_TENANT_ID")
client_id = os.getenv("AZURE_CLIENT_ID")
client_secret = os.getenv("AZURE_CLIENT_SECRET")
sender_email=os.getenv("SENDER_EMAIL")

def get_access_token():
    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    payload = {
        'grant_type': "client_credentials",
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(url, data=payload)
    response_data = response.json()
    return response_data['access_token']

def send_email():
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    #now = datetime.utcnow().isoformat() + "Z"

    url = f"https://graph.microsoft.com/v1.0/users/{sender_email}/events"

    with open('summary_json.json', 'r') as file:
        payload = json.load(file)


    response = requests.post(url, headers=headers, json=payload)
    print(response.status_code, response.text)

# Call the function
send_email()
