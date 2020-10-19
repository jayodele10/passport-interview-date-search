import requests
import json

#code adopted from: https://medium.com/@javiergalvis/mobile-and-laptop-push-notifications-over-python-916e78795060
def pushbullet_message(title, body):
    msg = {"type": "note", "title": title, "body": body}
    TOKEN = MY_TOKEN
    resp = requests.post('https://api.pushbullet.com/v2/pushes', 
                         data=json.dumps(msg),
                         headers={'Authorization': 'Bearer ' + TOKEN,
                                  'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Error',resp.status_code)
    else:
        print ('Message sent') 