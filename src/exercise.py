import re
import requests
from lxml import html
from bs4 import BeautifulSoup



def exercise(self, Session, SchoolId, StudentId, ExerciseId):
	EXERCISE_URL = "https://www.lectio.dk/lectio/{}/ElevAflevering.aspx?elevid={}&exerciseid={}".format(SchoolId, StudentId, ExerciseId)

	result = Session.get(EXERCISE_URL)

	exerciseOutput = {}

	soup = BeautifulSoup(result.text, features="html.parser")
	

	#Grabbing generel information
	exerciseGenerel = soup.find('div', {'id': 'm_Content_registerAfl_pa'})
	rows = exerciseGenerel.findAll('td')

	titles = ['Title', 'Note', 'Hold', 'Karakterskala', 'Ansvarlig', 'Elevtid']

	n = 0
	for row in rows:
		if n <= 5:
			try:
				exerciseOutput[titles[n]] = rows[n].find('span').getText()
				n += 1
			except:
				exerciseOutput[titles[n]] = " "
				n += 1
		else:
			break

	#Grabbing the afleveringsfrist and undervisningsbeskrivelse
	exerciseOutput['Afleveringsfrist'] = rows[6].getText()
	if rows[7].getText() == "Ja":
		exerciseOutput['I undervisningsbeskrivelse'] = True
	else:
		exerciseOutput['I undervisningsbeskrivelse'] = False
	


	sections = soup.findAll('section', {'class': 'island'})
	if len(sections) == 4:
		exerciseOutput['Gruppeaflevering'] = True

		groupMembers = []

		groupTable = soup.find('table', {'id': 'm_Content_groupMembersGV'})
		groupMembersTable = groupTable.findAll('td')
		n = 0
		for member in groupMembersTable:
			if (n % 2) == 0:
				groupMembers.append(member.find('span').getText())
				n += 1
			else:
				n += 1

		exerciseOutput['Members'] = groupMembers

	else:
		exerciseOutput['Gruppeaflevering'] = False

	


	return exerciseOutput