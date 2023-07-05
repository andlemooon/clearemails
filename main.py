import os
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def clear_old_emails():
    # Set the credentials and token file paths
    credentials_path = 'path/to/credentials.json'
    token_path = 'path/to/token.json'

    # Load or obtain credentials
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = google.auth.default(scopes=['https://www.googleapis.com/auth/gmail.modify'])
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    # Build the Gmail API service
    service = build('gmail', 'v1', credentials=creds)

    # Retrieve the list of old emails
    response = service.users().messages().list(userId='me', q='is:unread before:YYYY/MM/DD').execute()
    messages = response.get('messages', [])

    # Delete each old email
    for message in messages:
        service.users().messages().delete(userId='me', id=message['id']).execute()

# Usage: Call the function to clear old emails
clear_old_emails()
