import re
import requests
from lxml import html
from bs4 import BeautifulSoup


def grades(self, Session, SchoolId, StudentId):
	SCHEDULE_URL = "https://www.lectio.dk/lectio/{}/grades/grade_report.aspx?elevid={}".format(SchoolId, StudentId)

	result = Session.get(SCHEDULE_URL)

	soup = BeautifulSoup(result.text, features="html.parser")
	gradeTable = soup.find('table', {"id": "s_m_Content_Content_karakterView_KarakterGV"})

	tableHeaders = gradeTable.findAll('th')

	grade = {}
	grades = []

	Id = 0
	for row in gradeTable.findAll('td'):
		grade.setdefault(tableHeaders[Id].text.replace("'", '"').replace(u"\n", "").replace(u"\r", "").replace(u"\t", ""), row.text.replace(u"\xa0", ' ').replace(u"\n", '').replace(u"\r", ''))
		Id += 1
		if Id == 4:
			Id = 0
			grades.append(grade)
			grade = {}


	return grades

