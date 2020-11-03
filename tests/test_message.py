from tests.details import lectioUsername, lectioPassword
from src.lectio import Lectio

lec = Lectio(lectioUsername, lectioPassword, "680")

print(lec.getMessage("12345678"))