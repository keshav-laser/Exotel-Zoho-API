from flask import Flask, request
from datetime import datetime
import requests
import json
from dotenv import load_dotenv, set_key
load_dotenv()
from os import environ
import fitz

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

def create_phone_record_in_zoho_success(access_token):
    url = "https://creator.zoho.in/api/v2.1/strandls/spot/form/Missed_Call_Logs"
    headers = {
        "Content-Type":"application/json",
        "Authorization": "Zoho-oauthtoken " + access_token,
        "environment": environ.get("ENVIRONMENT")
    }
    CallFrom = request.args.get("CallFrom")
    CallTo = request.args.get("CallTo")
    DialCallDuration = request.args.get("DialCallDuration")
    StartTime = request.args.get("StartTime")
    StartTime = datetime.strptime(StartTime,'%Y-%m-%d %H:%M:%S')
    StartTime = StartTime.strftime('%d-%b-%Y %H:%M:%S')
    DialCallStatus = request.args.get("DialCallStatus")
    Direction = request.args.get("Direction")
    data = {"data":[{"From":f"+91 {CallFrom}", "To":f"+91 {CallTo}","Call_Duration":f"{DialCallDuration}","Start_Time":f"{StartTime}","Call_Type":f"{DialCallStatus}","Direction":f"{Direction}"}]}
    response = requests.post(f"{url}",headers=headers,json=data)
    return response.json()

def create_phone_record_in_zoho(access_token):
    url = "https://creator.zoho.in/api/v2.1/strandls/spot/form/Missed_Call_Logs"
    headers = {
        "Content-Type":"application/json",
        "Authorization": "Zoho-oauthtoken " + access_token,
        "environment": environ.get("ENVIRONMENT")
    }
    CallFrom = request.args.get("CallFrom")
    CallTo = request.args.get("CallTo")
    DialCallDuration = request.args.get("DialCallDuration")
    StartTime = request.args.get("StartTime")
    StartTime = datetime.strptime(StartTime,'%Y-%m-%d %H:%M:%S')
    StartTime = StartTime.strftime('%d-%b-%Y %H:%M:%S')
    CallType = request.args.get("CallType")
    Direction = request.args.get("Direction")
    data = {"data":[{"From":f"+91 {CallFrom}", "To":f"+91 {CallTo}","Call_Duration":f"{DialCallDuration}","Start_Time":f"{StartTime}","Call_Type":f"{CallType}","Direction":f"{Direction}"}]}
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
        print(access_token)
        environ["ACCESS_TOKEN"] = f"{access_token}"
        # set_key(".env", "ACCESS_TOKEN", environ["ACCESS_TOKEN"])
        response = get_data(access_token)
    return response

@app.route("/create",methods=["GET"])
def create():
    access_token = environ.get("ACCESS_TOKEN")
    response = create_phone_record_in_zoho(access_token)
    if(response["code"] == 1030):
        access_token = fetch_new_access_token()
        environ["ACCESS_TOKEN"] = f"{access_token}"
        # set_key(".env", "ACCESS_TOKEN", environ["ACCESS_TOKEN"])
        response = create_phone_record_in_zoho(access_token)
    return response


@app.route("/create/success",methods=["GET"])
def create_success():
    access_token = environ.get("ACCESS_TOKEN")
    response = create_phone_record_in_zoho_success(access_token)
    if(response["code"] == 1030):
        access_token = fetch_new_access_token()
        environ["ACCESS_TOKEN"] = f"{access_token}"
        # set_key(".env", "ACCESS_TOKEN", environ["ACCESS_TOKEN"])
        response = create_phone_record_in_zoho_success(access_token)
    return response

@app.route("/convert/to/csv",methods=["GET"])
def convert_to_csv():
    urlToCall = request.args.get("url")
    print(urlToCall)
    response = requests.get(urlToCall)
    print(response.content)
    doc = fitz.open(stream=response.content, filetype="pdf")
    # with open('sample.pdf', 'wb') as f:
    #     f.write(response.content)
    # tables = camelot.read_pdf('sample.pdf', pages='all')
    resultList = list()
    for i in range(doc.page_count):
        page = doc.load_page(i)
        tables = page.find_tables()
        for table in tables:
            resultList.append(table.extract())
    # for table in tables:
    #     resultList.append(table.df.values.tolist())
    return resultList



if __name__ == "__main__":
    app.run(debug=False)

