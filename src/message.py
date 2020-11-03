import re
import requests
from lxml import html
from bs4 import BeautifulSoup

def message(self, Session, SchoolId, StudentId, MessageId):
	MESSAGE_URL = "https://www.lectio.dk/lectio/{}/beskeder2.aspx?type=showthread&elevid={}&selectedfolderid=-70&id={}".format(SchoolId, StudentId, MessageId)

	result = Session.get(MESSAGE_URL)

	soup = BeautifulSoup(result.text, features="html.parser")

	MessageOutput = {}

	#Example output
	"""
	{
		"Title": "Lorem Ipsum",
		"Forfatter": "John Doe",
		"Modtagere": "Alle 1. HTX elever, "
		"Oprettet": "11/03/2020 20:21"
		"Svar" [
			{
				"Forfatter": "Bo Jensen"
				"Besked": "Lorem Ipsum",
				"Tid": "11/03/2020 21:15"
			},
			{
				"Forfatter": "Bo Jensen"
				"Besked": "Lorem Ipsum",
				"Tid": "11/03/2020 21:15"
			},
		]
	}
	"""

	#Generel information about the message
	table = soup.find("table", {"class": "ShowMessageRecipients"})

	messageTitle = table.find("td", {"class": "textLeft"}).getText().strip()
	messageAuthor = table.find("span").getText()
	messageRecipients = soup.find("table", {"class": "maxWidth textTop"}).findAll("tr")[1].findAll("td")[2].getText().strip()
	messageCreatedAt = soup.find("table", {"class": "ShowMessage2Inner"}).find("td").getText().strip().split(", ")[1]


	#Loop through responses
	Messages = []
	OneMessage = {}
	messageTextTable = soup.find("ul", {"id": "s_m_Content_Content_ThreadList"})
	messageBricks = messageTextTable.findAll("li")
	for messageBrick in messageBricks:

		OneMessageAuthor = messageBrick.find("span").getText()
		OneMessageTime = messageBrick.find("td").getText().strip().split(", ")[1]
		OneMessageText = messageBrick.find("div").getText().strip().replace('\n', '')

		OneMessage["Forfatter"] = OneMessageAuthor
		OneMessage["Tid"] = OneMessageTime
		OneMessage["Besked"] = OneMessageText

		Messages.append(OneMessage)
		OneMessage = {}


	
	#messageText = messageTextTable.find("li").find("div").getText().strip().replace('\n', '')

	#Setting the final json up
	MessageOutput["Title"] = messageTitle
	MessageOutput["Forfatter"] = messageAuthor
	MessageOutput["Modtagere"] = messageRecipients
	MessageOutput["Oprettet"] = messageCreatedAt
	MessageOutput["Svar"] = Messages

	return MessageOutput