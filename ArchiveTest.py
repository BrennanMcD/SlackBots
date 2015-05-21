import requests
import websocket
import thread
import json
import logging
import re as rex

sassy_user = "U04V808C9"

dev = "C04SFFCKL"
random = "C02FPU1H9"
selected_channel = dev

bot_api_token = ""
sassy_api_token = ""
user_api_token = ""
selected_token = sassy_api_token

def archive(token, channel):
    payload = {'token': token, 'channel':channel}
    return requests.post("https://slack.com/api/channels.archive", params=payload).text

def un_archive(token, channel):
    payload = {'token': token, 'channel':channel}
    return requests.post("https://slack.com/api/channels.unarchive", params=payload).text

def list_channels(token):
    payload = {'token':token}
    r = requests.post("https://slack.com/api/channels.list", params=payload)
    request_json = json.loads(r.text)
    if request_json["ok"]:
        for channel in request_json["channels"]:
            print channel["id"]
            print channel["name"]
            print channel["topic"]
            print channel["is_archived"]


print archive(selected_token, dev)

print un_archive(selected_token, dev)

