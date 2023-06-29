import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle
import re
from db import DB
import requests
import json

#  [
#     {
#       "id": "CHAT",
#       "name": "CHAT",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "system"
#     },
#     {
#       "id": "SENT",
#       "name": "SENT",
#       "type": "system"
#     },
#     {
#       "id": "INBOX",
#       "name": "INBOX",
#       "type": "system"
#     },
#     {
#       "id": "IMPORTANT",
#       "name": "IMPORTANT",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "system"
#     },
#     {
#       "id": "TRASH",
#       "name": "TRASH",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "system"
#     },
#     {
#       "id": "DRAFT",
#       "name": "DRAFT",
#       "type": "system"
#     },
#     {
#       "id": "SPAM",
#       "name": "SPAM",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelShow",
#       "type": "system"
#     },
#     {
#       "id": "CATEGORY_FORUMS",
#       "name": "CATEGORY_FORUMS",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "system"
#     },
#     {
#       "id": "CATEGORY_UPDATES",
#       "name": "CATEGORY_UPDATES",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "system"
#     },
#     {
#       "id": "CATEGORY_PERSONAL",
#       "name": "CATEGORY_PERSONAL",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "system"
#     },
#     {
#       "id": "CATEGORY_PROMOTIONS",
#       "name": "CATEGORY_PROMOTIONS",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "system"
#     },
#     {
#       "id": "CATEGORY_SOCIAL",
#       "name": "CATEGORY_SOCIAL",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "system"
#     },
#     {
#       "id": "STARRED",
#       "name": "STARRED",
#       "type": "system"
#     },
#     {
#       "id": "UNREAD",
#       "name": "UNREAD",
#       "type": "system"
#     },
#     {
#       "id": "Label_10",
#       "name": "✔",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "user"
#     },
#     {
#       "id": "Label_11",
#       "name": "✔✔",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "user"
#     },
#     {
#       "id": "Label_135950547395676116",
#       "name": "Being worked by broker",
#       "type": "user"
#     },
#     {
#       "id": "Label_1510598797269534228",
#       "name": "Previous funder decline",
#       "type": "user"
#     },
#     {
#       "id": "Label_1637791041414299557",
#       "name": "Bounce",
#       "type": "user"
#     },
#     {
#       "id": "Label_1742551274983280893",
#       "name": "DOA",
#       "type": "user"
#     },
#     {
#       "id": "Label_1843362026049333433",
#       "name": "Call Request",
#       "type": "user"
#     },
#     {
#       "id": "Label_1879111283402340759",
#       "name": "Block Email Attempt",
#       "type": "user"
#     },
#     {
#       "id": "Label_1895729505065856922",
#       "name": "Non MCA",
#       "type": "user"
#     },
#     {
#       "id": "Label_19",
#       "name": "GMass Scheduled",
#       "messageListVisibility": "show",
#       "labelListVisibility": "labelShow",
#       "type": "user"
#     },
#     {
#       "id": "Label_20",
#       "name": "GMass Auto Followup",
#       "messageListVisibility": "show",
#       "labelListVisibility": "labelShow",
#       "type": "user"
#     },
#     {
#       "id": "Label_21",
#       "name": "GMass Reports/Sent Copies",
#       "messageListVisibility": "show",
#       "labelListVisibility": "labelShow",
#       "type": "user"
#     },
#     {
#       "id": "Label_2141925096769309382",
#       "name": "One Slow Month",
#       "type": "user"
#     },
#     {
#       "id": "Label_22",
#       "name": "Gmelius",
#       "messageListVisibility": "show",
#       "labelListVisibility": "labelHide",
#       "type": "user"
#     },
#     {
#       "id": "Label_23",
#       "name": "Gmelius/Shared",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "user"
#     },
#     {
#       "id": "Label_231457674009520731",
#       "name": "Ramon",
#       "type": "user"
#     },
#     {
#       "id": "Label_2373951966064447668",
#       "name": "Modified Payments",
#       "type": "user"
#     },
#     {
#       "id": "Label_24",
#       "name": "Gmelius/Shared/Pending",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "user"
#     },
#     {
#       "id": "Label_25",
#       "name": "Gmelius/Shared/Closed",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "user"
#     },
#     {
#       "id": "Label_26",
#       "name": "Gmelius/Shared/Mine",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "user"
#     },
#     {
#       "id": "Label_27",
#       "name": "Gmelius/Shared/Assigned",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "user"
#     },
#     {
#       "id": "Label_28",
#       "name": "Gmelius/Shared/Unassigned",
#       "messageListVisibility": "hide",
#       "labelListVisibility": "labelHide",
#       "type": "user"
#     },
#     {
#       "id": "Label_2838120834246250661",
#       "name": "Offer email sent",
#       "type": "user"
#     },
#     {
#       "id": "Label_2878532336705858586",
#       "name": "Low rev",
#       "type": "user"
#     },
#     {
#       "id": "Label_290003399092844962",
#       "name": "Need app",
#       "type": "user"
#     },
#     {
#       "id": "Label_32",
#       "name": "CURRENTLY PENDING",
#       "messageListVisibility": "show",
#       "labelListVisibility": "labelShow",
#       "type": "user"
#     },
#     {
#       "id": "Label_33",
#       "name": "Currently pending deals",
#       "messageListVisibility": "show",
#       "labelListVisibility": "labelShow",
#       "type": "user"
#     },
#     {
#       "id": "Label_3323890249407164287",
#       "name": "No interest now",
#       "type": "user"
#     },
#     {
#       "id": "Label_34",
#       "name": "PENDING DEALS",
#       "messageListVisibility": "show",
#       "labelListVisibility": "labelShow",
#       "type": "user"
#     },
#     {
#       "id": "Label_3484552127175340835",
#       "name": "Sent Sheet",
#       "type": "user"
#     },
#     {
#       "id": "Label_3752065436905228422",
#       "name": "CC",
#       "type": "user"
#     },
#     {
#       "id": "Label_3791919917427550080",
#       "name": "Merchant Declined MP",
#       "type": "user"
#     },
#     {
#       "id": "Label_4303852885593834729",
#       "name": "Spreadsheets",
#       "type": "user"
#     },
#     {
#       "id": "Label_43148599282108030",
#       "name": "No contact yet",
#       "type": "user"
#     },
#     {
#       "id": "Label_443526723435511499",
#       "name": "Automatic Reply",
#       "type": "user"
#     },
#     {
#       "id": "Label_4860995266878354752",
#       "name": "ID & VC",
#       "type": "user"
#     },
#     {
#       "id": "Label_5033503290479590153",
#       "name": "SBA",
#       "type": "user"
#     },
#     {
#       "id": "Label_5306267516757792166",
#       "name": "AMA deal",
#       "type": "user"
#     },
#     {
#       "id": "Label_5404765621690589914",
#       "name": "DNC (REMOVE)",
#       "type": "user"
#     },
#     {
#       "id": "Label_5680414888159263713",
#       "name": "Funder Decline",
#       "type": "user"
#     },
#     {
#       "id": "Label_5771657951811349269",
#       "name": "Unrealistic expectations",
#       "type": "user"
#     },
#     {
#       "id": "Label_6333271555343619659",
#       "name": "SBA no interest",
#       "type": "user"
#     },
#     {
#       "id": "Label_657165392541380442",
#       "name": "Personal statements",
#       "type": "user"
#     },
#     {
#       "id": "Label_6572521976161552860",
#       "name": "CRM Updates",
#       "type": "user"
#     },
#     {
#       "id": "Label_6575202713555058085",
#       "name": "SBA UNSUB",
#       "type": "user"
#     },
#     {
#       "id": "Label_6582600068374059677",
#       "name": "Default",
#       "type": "user"
#     },
#     {
#       "id": "Label_66751476112208308",
#       "name": "Startup",
#       "type": "user"
#     },
#     {
#       "id": "Label_683100430529275591",
#       "name": "Waiting for status",
#       "messageListVisibility": "show",
#       "labelListVisibility": "labelShow",
#       "type": "user"
#     },
#     {
#       "id": "Label_7017013491743372130",
#       "name": "Followback over 1 month",
#       "type": "user"
#     },
#     {
#       "id": "Label_7138017054325680454",
#       "name": "Needs to be subbed",
#       "type": "user"
#     },
#     {
#       "id": "Label_7253584014487322543",
#       "name": "Diff Broker",
#       "type": "user"
#     },
#     {
#       "id": "Label_7396470736336707118",
#       "name": "Unsub",
#       "type": "user"
#     },
#     {
#       "id": "Label_7575830403551611024",
#       "name": "Needs monthly",
#       "type": "user"
#     },
#     {
#       "id": "Label_7606746542139638779",
#       "name": "Short form",
#       "type": "user"
#     },
#     {
#       "id": "Label_8031670026272969679",
#       "name": "Debt Collection",
#       "type": "user"
#     },
#     {
#       "id": "Label_820996828647876504",
#       "name": "Need statements",
#       "type": "user"
#     },
#     {
#       "id": "Label_8356025447856618997",
#       "name": "Floor File",
#       "type": "user"
#     },
#     {
#       "id": "Label_8557963143193082885",
#       "name": "Bitty Sub",
#       "type": "user"
#     },
#     {
#       "id": "Label_8759673964117114063",
#       "name": "Wrong info",
#       "type": "user"
#     },
#     {
#       "id": "Label_8804394129857385296",
#       "name": "Cannot connect",
#       "type": "user"
#     },
#     {
#       "id": "Label_8841708399193349449",
#       "name": "Lead forward",
#       "type": "user"
#     },
#     {
#       "id": "Label_8895583769018561835",
#       "name": "Have statement need app",
#       "type": "user"
#     },
#     {
#       "id": "Label_8970504453346432703",
#       "name": "Unanswered",
#       "type": "user"
#     }
#   ]


# Email is marketing@tribecagroupllc.com
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

unsubLabelId = 'Label_7396470736336707118'
abs_path = os.path.abspath(os.path.dirname(__file__))

def getCreds():
    creds = None    
        # the file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time
    if os.path.exists(abs_path + "/token.pickle"):
        with open(abs_path + "/token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(abs_path + '/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open(abs_path + "/token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds

def extractEmailFrom(fromStr):
    # fromStr = 'Smart Dev <smartdevello@gmail.com>'
    result = re.search(r".+<(.+@.+)>$", fromStr)
    if len(result.groups()) == 1: return result.group(1)
    else: return ""

db = DB()

creds = getCreds()
service = build('gmail', 'v1', credentials=creds)
totalSizeEstimate = 0
total = 0
pageToken = ''


for i in range(0, 100):
    results = service.users().messages().list(userId = 'me', labelIds=[unsubLabelId], pageToken=pageToken).execute()
    messages = results['messages']

    for message in messages:
        messageResponse = service.users().messages().get(userId = 'me', id = message['id']).execute()
        senderEmail = ''
        try:
            headers = messageResponse['payload']['headers']
            parts = messageResponse['payload']['parts']
            subject = next(filter(lambda obj : obj['name'] == 'Subject', headers  ))['value']
        except:
            pass
        try:
            fromName = next(filter(lambda obj : obj['name'] == 'From', headers  ))['value']
            senderEmail = extractEmailFrom(fromName)
        except:
            pass

        if senderEmail == '': continue
        row = db.findRowByEmail(senderEmail)
        if not row:
            db.insertRow(email=senderEmail, processed=0)


    total = total + len(messages)
    pageToken = results['nextPageToken'] if 'nextPageToken' in results else ''
    print(pageToken)
    if pageToken == '': break   

print(total)
x =0 

