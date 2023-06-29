import requests
import json

class Centrex:
    def __init__(self):
        self.client_id = '5015'
        self.client_secret = 'dbee13cc-8b41-8598-d5a2-045655754fc2'
        self.base_url  = 'https://api.centrexsoftware.com'     
        self.token = ''
        self.nuture_unsuscribed_id = '253578'


    def getAuthToken(self):
        url = self.base_url + "/v1/auth/token"
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        headers = {
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload) 
        response = json.loads(response.text)
        self.token = response['response']['api_key']
    def updateContactStatus(self, id, statusID):
        if self.token == '':
            self.getAuthToken()

        url = "https://api.debtpaypro.com/v1/contacts/{0}/workflow".format(id)

        payload = json.dumps({
            "statusID": statusID
        })
        headers = {
            'Accept': 'application/json',
            'Api-Key': self.token,
            'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        response = json.loads(response.text)
        return response['response']
    
    def searchContactsByEmail(self, email):

        if self.token == '':
            self.getAuthToken()

        url = self.base_url +  "/v1/contacts/search"

        payload = json.dumps({
            "field": "email",
            "term": email
        })
        headers = {
            'Accept': 'application/json',
            'Api-Key': self.token,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response = json.loads(response.text)
        return response['response']
    


   
