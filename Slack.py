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


selected_channel = dev

def get_user_by_id(token, id):
    payload = {'token':token, 'user':id}
    r = requests.post('https://slack.com/api/users.info', params=payload)
    user_object = json.loads(r.text)
    name = user_object["user"]["name"]
    return name

def send_message(token, message, channel):
    payload = {'token':token,'channel':channel,'text':message}
    r = requests.post("https://slack.com/api/chat.postMessage", params=payload)
    return r.text

def read_chat(token, channel):
    payload = {'token':token, 'channel':channel}
    r = requests.post("https://slack.com/api/im.history", params=payload)
    return r.text

def list_channels(token):
    payload = {'token':token, 'pretty':1}
    r = requests.post("https://slack.com/api/channels.list", params=payload)
    return r.text

def open_RTS(token):
    payload={'token':token}
    r = requests.post("https://slack.com/api/rtm.start", params=payload)
    return r.text

def user_changed(user):
    print (user["id"])
    print (user["name"])

def fix_trevor(token):
    payload = {'token':token, 'channel':selected_channel}
    r = requests.post("https://slack.com/api/channels.unarchive", params=payload)

def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        ws.close()
        print "thread terminating..."
    thread.start_new_thread(run, ())


def get_stackoverflow(term):
    payload = {'site':'stackoverflow', 'order':'desc', 'sort':'votes', 'intitle':term}
    s_over = requests.get("http://api.stackexchange.com/2.2/search", params=payload)
    s_over = json.loads(s_over.text)
    top_5 = s_over["items"][0:4]
    compiled_string = ""
    for i in top_5:
        compiled_string += i["title"] + " - Score: " + str(i["score"]) + "\n" + i["link"] + "\n"
    print(compiled_string)
    compiled_string.replace('&#39', '\"')
    send_message(selected_token,compiled_string, selected_channel)

def on_message(text, text2):
    message_json = json.loads(text2)
    print "==" + message_json["type"] + "=="
    
    if message_json["type"] == "message":
        if "stackbot:" in message_json["text"] and message_json["channel"] == selected_channel:
            get_stackoverflow(message_json["text"].replace("stackbot:",""))
            
        if "subtype" in message_json:

            print message_json["subtype"]
            
        print message_json["type"] + " from " + get_user_by_id(selected_token, message_json["user"])  +" : '" + message_json["text"] + "' on channel " + message_json["channel"]
        
    if message_json["type"] == "user_typing":
        print get_user_by_id(selected_token, message_json["user"]) + " is typing" 
        
    if message_json["type"] == "channel_unarchive":
        send_message(selected_token, "It was probably Trevor's fault", selected_channel)
        
    if message_json["type"] == "channel_marked":
        print message_json["channel"]
    else:
        message_json["type"]

if __name__ == "__main__":
    logging.basicConfig()
    message = json.loads(open_RTS(selected_token))
    ws = websocket.WebSocketApp(message["url"], on_message=on_message)
    ws.on_open = on_open
    ws.run_forever()
