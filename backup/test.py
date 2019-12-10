import datetime
import requests
from bs4 import BeautifulSoup

s = requests.Session()
result = s.get("http://localhost:8080/Testing/index.php")

soup = BeautifulSoup(result.text, features="html.parser")

table = soup.find("table")

rows = []

for row in table.findAll("tr"):
	for row1 in row.findAll('td'):
		print(row1.contents)
		rows.append(row1.contents)
		print(" ")

print(rows[0])