from flask import Flask, request
import requests
import json
from dotenv import load_dotenv, set_key
load_dotenv()
from os import environ

app = Flask(__name__)

def fetch_new_access_token():
    refresh_token = environ.get("REFRESH_TOKEN")
    client_id = environ.get("CLIENT_ID")
    client_secret = environ.get("CLIENT_SECRET")
    access_token_url = f"https://accounts.zoho.in/oauth/v2/token?refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}&grant_type=refresh_token"
    access_token_response = requests.post(access_token_url)
    access_token_response = json.loads(access_token_response.text)
    access_token = access_token_response["access_token"]
    return access_token

def create_phone_record_in_zoho(CallFrom,access_token):
    url = "https://creator.zoho.in/api/v2.1/strandls/spot/form/Missed_Call_Logs"
    headers = {
        "Content-Type":"application/json",
        "Authorization": "Zoho-oauthtoken " + access_token,
        "environment": environ.get("ENVIRONMENT")
    }
    CallFrom = request.args.get("CallFrom")
    data = {"data":[{"Phone_Number":f"{CallFrom}"}]}
    response = requests.post(f"{url}",headers=headers,json=data)
    return response.json()

def get_data(access_token):
    url = "https://creator.zoho.in/api/v2.1/strandls/spot/report/All_Phlebotomy_Results"
    headers = {
        "Content-Type":"application/json",
        "Authorization": "Zoho-oauthtoken " + access_token,
        "environment": environ.get("ENVIRONMENT")
    }
    response = requests.get(f"{url}",headers=headers)
    return response.json()

@app.route("/")
def home():
    access_token = environ.get("ACCESS_TOKEN")
    response = get_data(access_token)
    if response["code"]==1030:
        access_token = fetch_new_access_token()
        environ["ACCESS_TOKEN"] = f"{access_token}"
        set_key(".env", "ACCESS_TOKEN", environ["ACCESS_TOKEN"])
        response = get_data(access_token)
    return response

@app.route("/create",methods=["GET"])
def create():
    access_token = environ.get("ACCESS_TOKEN")
    CallFrom = request.args.get("CallFrom")
    response = create_phone_record_in_zoho(CallFrom,access_token)
    if(response["code"] == 1030):
        access_token = fetch_new_access_token()
        environ["ACCESS_TOKEN"] = f"{access_token}"
        set_key(".env", "ACCESS_TOKEN", environ["ACCESS_TOKEN"])
        response = create_phone_record_in_zoho(CallFrom,access_token)
    return response


if __name__ == "__main__":
    app.run(debug=True)

