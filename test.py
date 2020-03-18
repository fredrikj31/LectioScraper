from details import lectioUsername, lectioPassword
from lectio import Lectio
import pprint

pp = pprint.PrettyPrinter(indent=4)

lec = Lectio(lectioUsername, lectioPassword, "680")

# Get specified message
#pp.pprint(lec.getMessage("40705529227"))

# Get Exercises
#pp.pprint(lec.getExercises())

# Get all messages
#pp.pprint(lec.getMessages())

# Get all schools
#pp.pprint(lec.getSchools())

# Get Schedule
pp.pprint(lec.getSchedule())