import datetime
import re
import requests
from lxml import html
from details import lectioUsername, lectioPassword


def login():

    ################################################
    # ENTER YOUR LECTIO USERNAME AND PASSWORD HERE #
    ################################################
    USERNAME = lectioUsername
    PASSWORD = lectioPassword
    ################################################

    URL_TEMPLATE = "https://www.lectio.dk/lectio/680/" \
                   "SkemaNy.aspx?type=elev&elevid=35886775656"

    LOGIN_URL = "https://www.lectio.dk/lectio/680/login.aspx"

    # Start requests session and get eventvalidation key
    s = requests.Session()
    result = s.get(LOGIN_URL)
    # print(result.text)
    tree = html.fromstring(result.text)
    authenticity_token = list(
        set(tree.xpath("//input[@name='__EVENTVALIDATION']/@value")))[0]

    # Create payload
    payload = {
        "m$Content$username2": USERNAME,
        "m$Content$password2": PASSWORD,
        "m$Content$passwordHidden": PASSWORD,
        "__EVENTVALIDATION": authenticity_token,
        "__EVENTTARGET": "m$Content$submitbtn2",
        "__EVENTARGUMENT": "",
        "LectioPostbackId": ""
    }

    # Perform login
    result = s.post(LOGIN_URL, data=payload, headers=dict(referer=LOGIN_URL))

    # Scrape url
    r = s.get(URL_TEMPLATE)

    print(r.text)

    return r


print(login())
