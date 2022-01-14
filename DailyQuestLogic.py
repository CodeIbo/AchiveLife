from Model import Task
from Model import Activity
from Model import UserProfile
from datetime import date
from datetime import datetime
from datetime import timedelta

class DailyQuestLogic:
    def __init__(self, userProfile):
        self.UserProfile = userProfile



    def CompleteOfTaskAcceptanceStatuses(self, userAcceptanceList): # userAcceptanceList przyklad : [T,F,T,F,T ] 5 zadan z roznych aktywnosci nie ma znaczenia kolejnosc bo sprawdzamy po kolei
        counterInStatusTasks = 0
        for activity in self.UserProfile.ListOfActivity:
            for task in activity.ListOfTasks:
                task.IsAccepted = userAcceptanceList[counterInStatusTasks]
                counterInStatusTasks += 1



    def CompletionOfTaskCompletionStatus (self, userChoice, selectedTask): #wybor uzytkownika to bedzie pojedyncza wartosc TRUE /FALSE
        selectedTask.IsComplete = userChoice
        #punktacja
        self.UserProfile.PointCouter += selectedTask.PointValue


    def ResetOfDailyStatus(self, daysMissed): #overload sprawdzic
        dailyEndTask = datetime.combine(date.today(), datetime.min.time()) + timedelta( hours=24)  # podstawa do rozbudowy
        self.UserProfile.NextResetDate = dailyEndTask
        if daysMissed == None:
            for activity in self.UserProfile.ListOfActivity:
                for task in activity.ListOfTasks:
                    task.IsComplete = False
                    task.IsAccepted = True
        else:
            if daysMissed == 0 : # zero oznacza dzien pozniej
                for activity in self.UserProfile.ListOfActivity:
                    for task in activity.ListOfTasks:
                        if task.IsAccepted == True and task.IsComplete == False:
                            pointDown = task.PointValue/2
                            self.UserProfile.PointCouter -= pointDown
                        elif task.IsAccepted != True:
                            pointDown = task.PointValue
                            self.UserProfile.PointCouter -= pointDown
                        task.IsComplete = False
                        task.IsAccepted = True
            elif daysMissed > 0 : # wiecej dni
               for activity in self.UserProfile.ListOfActivity:
                   for task in activity.ListOfTasks:
                       pointDown = task.PointValue * daysMissed * 2
                       self.UserProfile.PointCouter -= pointDown
                       task.IsComplete = False
                       task.IsAccepted = True

