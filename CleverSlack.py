import requests
import websocket
import thread
import json
import logging
import re as rex
from chatterbotapi import ChatterBotFactory, ChatterBotType

sassy_user = "U04V808C9"

dev = "C04SFFCKL"
random = "C02FPU1H9"
selected_channel = random

sassy_api_token = ""
user_api_token = ""
bot_api_token = ""
selected_token = sassy_api_token


factory = ChatterBotFactory()

ChatBot = factory.create(ChatterBotType.CLEVERBOT)
Session = ChatBot.create_session()

def on_message(text, text2):
    message_json = json.loads(text2)
    print message_json["text"].lower()
    if message_json["type"] == "message":
        if "<@u04v808c9>" in message_json["text"].lower():
            thread.start_new_thread(Compute_Sass, (message_json["user"],Session.think(message_json["text"])))
        else: 
            if "speedy" in message_json["text"].lower() and message_json["user"].lower() != sassy_user.lower():
                send_message(selected_token, "Speedy... *Shutters*", selected_channel)
            if "neptune" in message_json["text"].lower() and message_json["user"].lower() != sassy_user.lower():
                send_message(selected_token, "Neptune... FU *Stephan*", selected_channel)

def send_message(token, message, channel):
    payload = {'token':token,'channel':channel,'text':message, 'as_user':'true'}
    r = requests.post("https://slack.com/api/chat.postMessage", params=payload)
    print r.text

def open_RTS(token):
    payload={'token':token}
    r = requests.post("https://slack.com/api/rtm.start", params=payload)
    return r.text

def Compute_Sass(user, text):
    send_message(selected_token, "<@"+user+"|"+ get_user_by_id(selected_token, user) +">: " + text.replace("cleverbot","@sassybot"), selected_channel)

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print "thread terminating..."
    thread.start_new_thread(run, ())

def get_user_by_id(token, id):
    payload = {'token':token, 'user':id}
    r = requests.post('https://slack.com/api/users.info', params=payload)
    user_object = json.loads(r.text)
    name = user_object["user"]["name"]
    return name

if __name__ == "__main__":
    logging.basicConfig()
    message = json.loads(open_RTS(selected_token))
    ws = websocket.WebSocketApp(message["url"], on_message=on_message)
    ws.on_open = on_open
    ws.run_forever()
