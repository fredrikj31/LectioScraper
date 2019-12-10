import datetime
import re
import requests
from lxml import html
from bs4 import BeautifulSoup
from details import lectioUsername, lectioPassword


def login():

    ################################################
    # ENTER YOUR LECTIO USERNAME AND PASSWORD HERE #
    ################################################
    USERNAME = lectioUsername
    PASSWORD = lectioPassword
    ################################################

    URL_TEMPLATE = "https://www.lectio.dk/lectio/680/OpgaverElev.aspx?elevid=35886775656"

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

    soup = BeautifulSoup(r.text, features="html.parser")

    table = soup.find("table", {"id": "s_m_Content_Content_ExerciseGV"})

    rows = []
    columns = []

    for row in table.findAll("tr"):
        #rows.append(row.contents)
        for row1 in row.findAll('td'):
        	columns.append(row1.text)
        rows.append(columns)
        columns = []
    print((rows[1][5]).strip())


login()
