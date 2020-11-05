from lxml import html
from bs4 import BeautifulSoup
import re

def dashboard(self, Session, SchoolId):
	DASHBOARD_URL = "https://www.lectio.dk/lectio/{}/forside.aspx".format(SchoolId)

	result = Session.get(DASHBOARD_URL)
	
	priority = ""
	content = ""
	rowObject = {}

	output = []


	soup = BeautifulSoup(result.text, features="html.parser")
	table = soup.find('table', {'id': "s_m_Content_Content_importantInfo"})

	for row in table.findAll('tr'):
		#Getting the priority
		firstSplit = re.split("/", row.find('img')['src'])[3]
		secondSplit = re.split("prio", firstSplit)[1]
		priority = secondSplit.split(".")[0]
		
		rowObject["Priority"] = priority
		rowObject["Text"] = row.findAll('td')[1].text.replace("\xa0", "").replace("\n", "")

		output.append(rowObject)
		rowObject = {}

	return output