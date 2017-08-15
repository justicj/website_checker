from bs4 import BeautifulSoup
import requests
import difflib
import json
import time

#variables
url = "http://www.cityofvista.com/services/city-departments/recreation-comm-services/programs-services/softball/monday-men-s-b-c"
div_id = "ColumnUserControl3"
#testing stuff
#url = "https://justicj.github.io/index.html"
#div_id = 'crapola'
pushbullet_token = "insertToken"
pushbullet_subject = "Men's Monday Softball Website Change"
pushbullet_body = "Something has changed on Vista Mens Monday Night Softball website, please check it out at http://www.cityofvista.com/services/city-departments/recreation-comm-services/programs-services/softball/monday-men-s-b-c"
interval = 1800

def get_div(url):
    #requests module to get url content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    #div = soup.find('div', id=div_id)
    div = soup.find('div', {'id':div_id})
    return div.text

def get_diff_ratio(base, compare):
    d = difflib.SequenceMatcher(None, base, compare)
    return d.ratio()

def send_push(title, body, token):
    data_send = {"type": "note", "title": title, "body": body}
    ACCESS_TOKEN = token
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print ("PushBullet Sent!")

def run_check(base):
    while True:
        print("Sleeping for ", interval)
        time.sleep(interval)
        print("Getting Latest Content")
        compare = get_div(url)
        print("comparing base and latest content")
        ratio = get_diff_ratio(base, compare)
        if ratio < 1.0:
            print ("Change : ", ratio, " ratio")
            send_push(pushbullet_subject, pushbullet_body, pushbullet_token)
            base = compare
        if ratio == 1.0:
            print ("Content matches")

#get initial div content, set to base
print("Getting Base Url Content")
base = get_div(url)
run_check(base)
