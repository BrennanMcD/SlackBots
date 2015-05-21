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


def send_message(token, message, channel):
    payload = {'token':token,'channel':channel,'text':message, 'as_user':'true', 'username':'God'}
    r = requests.post("https://slack.com/api/chat.postMessage", params=payload)
    return r.text

def on_message(text, text2):
    message_json = json.loads(text2)
    if message_json["type"] == "message":
        if "speedy" in message_json["text"].lower() and message_json["user"] != "U04V808C9":
            send_message(api_token, "Speedy... *Shutters*", random)
        if "neptune" in message_json["text"].lower() and message_json["user"] != "U04V808C9":
            send_message(api_token, "Neptune... FU *Stephan*", random)

def open_RTS(token):
    payload={'token':token}
    r = requests.post("https://slack.com/api/rtm.start", params=payload)
    return r.text

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print "thread terminating..."
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    logging.basicConfig()
    message = json.loads(open_RTS(api_token))
    ws = websocket.WebSocketApp(message["url"], on_message=on_message)
    ws.on_open = on_open
    ws.run_forever()