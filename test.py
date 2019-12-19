from details import lectioUsername, lectioPassword
from lectio import Lectio

lec = Lectio(lectioUsername, lectioPassword, "680")

#print(lec.getExercises()['Exercises'][0]['Hold'])

print(lec.getSchedule())