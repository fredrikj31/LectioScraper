import re
import requests
from lxml import html
from bs4 import BeautifulSoup

def messages(self, Session, SchoolId, StudentId):
	MESSAGE_URL = "https://www.lectio.dk/lectio/{}/beskeder2.aspx?type=&elevid={}&selectedfolderid=-70".format(SchoolId, StudentId)

	result = Session.get(MESSAGE_URL)

	soup = BeautifulSoup(result.text, features="html.parser")

	table = soup.find("table", {"id": "s_m_Content_Content_threadGV"})

	Id = 0
	Messages = []
	Message = {}

	Informations = []

	for row in table.findAll('tr'):
		if Id == 0:
			Id += 1
			continue
		else:
			#print("THIS IS A TEST")
			for column in row:
				Informations.append(column)

			# Getting the message id
			MessageId = Informations[4].find('a')
			MessageIdStrip = MessageId['onclick'].split("$LB2$_MC_$_")[1]
			MessageIdReal = MessageIdStrip.split("');")[0]

			Message['Id'] = MessageIdReal
			Message['Title'] = Informations[4].getText().strip().replace("\r", "").replace("\n", " ")
			Message['Last Message'] = Informations[5].getText().strip().replace("\r", "").replace("\n", " ")
			Message['First Message'] = Informations[6].getText().strip().replace("\r", "").replace("\n", " ")
			for elem in Informations[7]:
				recipients = elem['title'].strip().replace("\r", "").replace("\n", " ")
			Message['Recipients'] = recipients
			Message['Last Update'] = Informations[8].getText().strip().replace("\r", "").replace("\n", " ")
					
			Messages.append(Message)
			Informations = []
			Message = {}
			

	return Messages