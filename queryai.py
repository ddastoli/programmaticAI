# queryai.py 

import os 
from openai import AzureOpenAI
import requests
import json
import base64


def getPassword(key, filename='pwdAPI'):
    try:
        with open(filename, 'r') as file:
            for line in file:
                # Split each line into key and value
                line_key, value = line.strip().split('=', 1)
                if line_key == key:
                    return value
        print(f"Password for key '{key}' not found.")
        return None
    except FileNotFoundError:
        print(f"The file '{filename}' was not found.")
        return None

clientID = getPassword("clientID")
clientSecret = getPassword("clientSecret")
appkey = getPassword("appkey")
client = str(clientID+":"+clientSecret)

# Encode the clientID and Secret into bytes, then base64 encode
encoded_bytes = base64.b64encode(client.encode('utf-8'))
client64 = encoded_bytes.decode('utf-8')

def getToken(client64AI):
    # Define the URL and headers
    url = "https://id.cisco.com/oauth2/default/v1/token"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic "+client64AI
    }
    # Define the data payload
    data = {
        "grant_type": "client_credentials"
    }
    # Send the POST request to get access token
    response = requests.post(url, headers=headers, data=data)
    # Parse the JSON response and get the token
    response_data = response.json()
    token = response_data.get("access_token")
    return token

def askAISimple(messageAI):
    token = getToken(client64)
    askAI(messageAI,token,appkey)


def askAI(messageToAI,tokenAI,appkeyAI):
    client = AzureOpenAI( 
        azure_endpoint = 'https://chat-ai.cisco.com', 
        api_key=tokenAI, 
        api_version="2024-07-01-preview" 
        ) 
    # Example message to send to the model
    message = [
        {"role": "user", "content": messageToAI}
    ]

    response = client.chat.completions.create( 
        model="gpt-4o-mini", # model = "deployment_name". 
        messages=message, 
        user=f'{{"appkey": "{appkeyAI}"}}' 
        ) 
    print(response.choices[0].message.content)

