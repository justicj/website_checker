#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import difflib
import json
import time
import sys
sys.path.append('D:\scripts\library')
import gmail

# variables
# url = "https://www.cityofvista.com/city-services/recreation-community-services/youth-basketball/girls-b"
url = "https://www.cremeofthecounty.com/2021-team-rosters"
# div_id = "widget_4_9319_5903"
div_id = "idqj4a7t_2"
# subject = "Girls B"
subject = "COTC"
body = "Something has changed on " + subject + " website, please check it out at " + url
ifttt_webhook = "https://maker.ifttt.com/trigger/GirlsB/with/key/dikq5osdJKlKCwvzbo9TFK"
interval = 1800
EMAIL_ADDRESS = 'jayjustice@gmail.com'
SUBJECT = f"{subject} Website changed"

def get_div(url):
    #requests module to get url content
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        #div = soup.find('div', id=div_id)
        div = soup.find('div', {'id':div_id})
        return div.text
    except requests.exceptions.RequestException as e:
        print("Exception is: ", e)
        return("failed")

def get_diff_ratio(base, compare):
    d = difflib.SequenceMatcher(None, base, compare)
    return d.ratio()


def webhook ():
    try:
        values = {"value1": subject, "value2": body}
        print(values)
        r = requests.post(url = ifttt_webhook, data = values)
        return(r.status_code, r.text)
    except requests.exceptions.RequestException as e:
        return("failed", "e")

def run_check(base):
    while True:
        print("Sleeping for", interval)
        time.sleep(interval)
        print("Getting Latest Content")
        compare = get_div(url)
        if compare != "failed":
            print("comparing base and latest content")
            print(compare)
            ratio = get_diff_ratio(base, compare)
            print(ratio)
            if ratio < 1.0:
                print ("Change : ", ratio, " ratio")
                gmail.send_email(EMAIL_ADDRESS, SUBJECT, [body])
                code, text = webhook()
                print(code, text)
                # send_push(subject, body, pushbullet_token)
                base = compare
            if ratio == 1.0:
                print ("Content matches")

#get initial div content, set to base
print("Getting Base Url Content")
base = get_div(url)
run_check(base)
