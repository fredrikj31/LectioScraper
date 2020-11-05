from tests.details import lectioUsername, lectioPassword, schoolId
from src.lectio import Lectio

lec = Lectio(lectioUsername, lectioPassword, schoolId)

print(lec.getExercise("12345678"))