from Model import UserProfile
from Model import GlobalNamesOfActivityTypes
from Model import Activity
from Model import Task
from datetime import date
from datetime import datetime
from datetime import timedelta


class ActivityLogic:
    def __init__(self, userProfile):
        self.UserProfile = userProfile  # activityLogic = ActivityLogic(loggedUser)

    def GenerateActivity(self, userSelections):  # userSelections -> lista typów aktywnosci uzytkownika z Modelu typ aktywnosci
        self.UserProfile.ListOfActivity.clear()  # wyczyszcznie listy
        for oneChoice in userSelections:  # petla for gdzie oneChoice to wybor uzytkownika i jest on dodawany do aktywnosci (typeActivity)
            activitySelectedByUser = Activity(oneChoice)  # oneChoice wybór uzytkownika
            self.UserProfile.ListOfActivity.append(activitySelectedByUser)

        activityEndDate = datetime.combine(date.today(), datetime.min.time()) + timedelta(weeks=4)
        self.UserProfile.ActivityEndDate = activityEndDate  # przypisanie daty ogolnej zakonczenia aktywnosci

    def GenerateTasksForTheWeek(self, userSelections, activity):
        activity.ListOfTasks.clear()
        for oneChoice in userSelections:
            b1 = Task(oneChoice)
            activity.ListOfTasks.append(b1)

        activity.WeeklyTasksEndDate = datetime.combine(date.today(), datetime.min.time()) + timedelta(days=7)
