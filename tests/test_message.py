from tests.details import lectioUsername, lectioPassword, schoolId
from src.lectio import Lectio

lec = Lectio(lectioUsername, lectioPassword, schoolId)

print(lec.getMessage("12345678"))