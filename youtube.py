from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

import os

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

creds = None


MAX_RESULTS=os.getenv("MAX_RESULTS")

def getComments(video_id):
    # Load saved token if it exists
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # If no valid token, login again
    if not creds or not creds.valid:

        # Refresh expired token automatically
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save token for future runs
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    youtube = build(
        "youtube",
        "v3",
        credentials=creds
    )

    response = youtube.commentThreads().list(
        part="snippet",
        order="time",
        # allThreadsRelatedToChannelId="UC0xAL-XyGo3lRspv9fTMl6w",
        videoId=video_id,
        maxResults=MAX_RESULTS
    ).execute()

    return response
