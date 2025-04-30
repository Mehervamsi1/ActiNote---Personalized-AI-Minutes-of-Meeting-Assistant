import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

tenant_id = os.getenv("TENANT_ID_2")
client_id = os.getenv("CLIENT_ID_2")
client_secret = os.getenv("CLIENT_SECRET_2")
sender_email=os.getenv("SENDER_EMAIL")

# Step 1: Get Access Token
def get_access_token():
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    access_token = response.json().get("access_token")
    return access_token

# Step 2: Fetch Recent Chats (Meeting chats)
def get_meeting_chats(token):
    print(token)
    url = "https://graph.microsoft.com/v1.0/chats"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(response)
    response.raise_for_status()
    print("Error response:", response.status_code, response.text)

    return response.json()

# Step 3: Fetch Messages from a Chat (to find transcript)
def get_chat_messages(chat_id, token):
    url = f"https://graph.microsoft.com/v1.0/chats/{chat_id}/messages"
    # url = f"https://graph.microsoft.com/v1.0/chats/19:meeting_YjFlMjc5MmEtNTVhOC00MmQ2LWFlNmYtMDEzMGY4OThlMTAw@thread.v2/messages"
    print(url)
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Main Execution
if __name__ == "__main__":
    token = get_access_token()
    chats = get_meeting_chats(token)
    print(chats)

    for chat in chats.get('value', []):
        chat_id = chat.get('id')
        print(f"Fetching messages for Chat ID: {chat_id}")
    
    # chat_id ="19:meeting_YjFlMjc5MmEtNTVhOC00MmQ2LWFlNmYtMDEzMGY4OThlMTAw@thread.v2"
        
    messages = get_chat_messages(chat_id, token)
        
    for message in messages.get('value', []):
        if "transcript" in (message.get('body', {}).get('content', '')).lower():
            print(f"\nTranscript Message:\n{message['body']['content']}\n")
