from details import lectioUsername, lectioPassword
from lectio import Lectio

lec = Lectio(lectioUsername, lectioPassword, "680")

beskeder = lec.getMessages()

print(beskeder)
