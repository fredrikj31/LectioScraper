from details import lectioUsername, lectioPassword
from lectio import Lectio

lec = Lectio(lectioUsername, lectioPassword, "680")

# Besked
#print(lec.getMessage("40705529227"))

# Opgaver
#print(lec.getExercises())

# Opgave
#print(lec.getExercise("37663993333"))

# Beskeder
#print(lec.getMessages())

# Skoler
#print(lec.getSchools())

# Skema
#print(lec.getSchedule())

# Studieretning
#print(lec.getStudyProgramme())

# Unread Messages
#print(lec.getUnreadMessages())

# Grades
print(lec.getGrades())
