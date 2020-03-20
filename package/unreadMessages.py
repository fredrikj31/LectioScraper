import re
import requests
from lxml import html
from bs4 import BeautifulSoup

def unreadMessages(self, Session, SchoolId):
	UNREAD_URL = "https://www.lectio.dk/lectio/{}/forside.aspx".format(SchoolId)

	result = Session.get(UNREAD_URL)

	output = {}

	soup = BeautifulSoup(result.text, features="html.parser")
	table = soup.find('table', {'id': "s_m_Content_Content_BeskederInfo"})

	rows = table.findAll('tr')
	if len(rows) == 1:
		if rows[0].find('td').getText() == "Ingen nye beskeder":
			output['Ulæste beskeder'] = " "
	else:
		messages = []
		message = {}
		for row in rows:
			lines = row.findAll('td')
			message['Title'] = lines[1].find('span').getText().strip()
			message['Fra'] = lines[2].find('span').getText().strip()
			message['Dato'] = lines[3].getText().strip()
			messages.append(message)
			message = {}

		output['Ulæste beskeder'] = messages

	return output