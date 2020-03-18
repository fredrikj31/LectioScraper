import re
import requests
from lxml import html
from bs4 import BeautifulSoup

def getMessage(self, Session, SchoolId, StudentId, MessageId):
	MESSAGE_URL = "https://www.lectio.dk/lectio/{}/beskeder2.aspx?type=showthread&elevid={}&selectedfolderid=-70&id={}".format(SchoolId, StudentId, MessageId)

	result = Session.get(MESSAGE_URL)

	soup = BeautifulSoup(result.text, features="html.parser")

	MessageOutput = {}

	#Example output
	"""
	{
		"MessageTitle": "Lorem Ipsum",
		"Author": "John Doe",
		"Recipients": "Alle 1. HTX elever, "
		"Created At": "11/03/2020 20:21"
		"Responses" [
			{
				"Author": "Bo Jensen"
				"Message": "Lorem Ipsum",
				"Time": "11/03/2020 21:15"
			},
			{
				"Author": "Bo Jensen"
				"Message": "Lorem Ipsum",
				"Time": "11/03/2020 21:15"
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

		OneMessage["Author"] = OneMessageAuthor
		OneMessage["Time"] = OneMessageTime
		OneMessage["Message"] = OneMessageText

		Messages.append(OneMessage)
		OneMessage = {}


	
	#messageText = messageTextTable.find("li").find("div").getText().strip().replace('\n', '')

	#Setting the final json up
	MessageOutput["MessageTitle"] = messageTitle
	MessageOutput["Author"] = messageAuthor
	MessageOutput["Recipients"] = messageRecipients
	MessageOutput["Created"] = messageCreatedAt
	MessageOutput["Responses"] = Messages

	return MessageOutput