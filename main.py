from Login_logic import LoginLogic
from ActivityLogic import ActivityLogic
from Model import GlobalNamesOfActivityTypes
from datetime import date
from datetime import datetime
from Model import GlobalNamesOfTasksTypes
from DailyQuestLogic import DailyQuestLogic


# FUNKCJE
def ShowTasks(user):
    CounterInTasks = 0
    for oneActivity in user.ListOfActivity:
        for oneTask in oneActivity.ListOfTasks:
            CounterInTasks += 1
            print(f"{CounterInTasks}.{oneTask.ContentOfTheTasks}")

def ShowActiveTasks(user):
    counterTask = 0
    for task in user.GetListActiveTasks():
        counterTask += 1
        print(f"{counterTask}.{task.ContentOfTheTasks}")

# deklaracje

loginLogic = LoginLogic()
loggedUser = None
activityLogic = None

# Logowanie uzytkownika
print("=====================")
print("Witaj w programie G-Life.")
print("=============================")
print("Jeśli nie posiadasz konta wpisz -new by utworzyć profil")
print(":)")
while True:
    loginInputUser = input("Login: ").strip()
    passwordInputUser = ""  # none w przypadku klasy, lub zmienna bedzie obslugiwala warotsc none
    # sprawdzenie czy uzytkownik chce sie zarejestrowac

    if loginInputUser == "-new":
        print("Zarejestruj sie")
        while True:  # rejestracja uzytkownika wykorzystanie NONE z Login_logic
            loginInput = input("Podaj login: ")
            passwordInput = input("Podaj haslo: ")
            loggedUser = loginLogic.AddUser(loginInput, passwordInput)

            if loggedUser == None:
                print("Niepoprawne dane")
                continue
            else:
                print("Zarejestrowano")
                print("")
                print(f"Dzień dobry {loginInput.title()}.") #do zmiany logged user
                loginLogic.Save()
                break

    # koniec sprawdzenia rejestracji
    else:
        passwordInputUser = input("Password: ").strip()

    if loggedUser == None:
        loggedUser = loginLogic.Login(loginInputUser,passwordInputUser)  # proba zalogowania dopiero po sprawdzeniu czy uzytkownik nie chcial sie zarejestrowac -new

    if loggedUser == None:
        print("Niepoprawne dane")
    else:

        if loginInputUser != "-new":
            print("")
            print(f"Dzień dobry {loginInputUser.title()}.")
            print("")
            print("Zalogowano")
            print("")
        break

# koniec logowania

# Wybor aktywnosci przez uzytkownika

activityLogic = ActivityLogic(loggedUser)  # odwołanie do SELF.PROFILU_UZYTKOWNIKA !!!!
if len(loggedUser.ListOfActivity) < 1 or (loggedUser.ActivityEndDate - datetime.combine(date.today(),  datetime.min.time())).days < 0:  # dwa warunki : pierwszy to porownanie do listy aktywnosci a drugi to sprawdzenie daty zakonczenia . Jesli obydwa warunki są poprawne nie zostaje dodana nowa aktywnosc
    print("================================================================================================================================================================")
    print( "<Pamietaj by wpisac numer oraz przecinek jeśli chcesz wybrać więcej niż jedną opcję. Przykladowo: 1,2 (wybralem 1 - czyli aktywnosc fizyczna oraz 2 - Finanse)>")
    print("================================================================================================================================================================")
    print("")
    print("Wybierz aktywnosci dostepne z listy")

    for idxOneActivityForUser, oneActivityForUser in enumerate(GlobalNamesOfActivityTypes.ListOfAcitvityForUser()):
        print(f"{idxOneActivityForUser + 1}.{oneActivityForUser}")

    listOfValidActivityFromUser = []
    while True:
        isTrue = True
        activityInput = input().strip()
        if activityInput == "":
            continue
        listOfActivityFromUser = activityInput.split(",")
        ListOfFilteredActivityFromUser = []
        for oneActivityForUser in listOfActivityFromUser:
            oneActivityForUser = oneActivityForUser.strip()  # usuwanie spacji z pojedynczego stringa w liscie wyborow
            if oneActivityForUser.isdigit() == False or int(oneActivityForUser) > len(GlobalNamesOfActivityTypes.ListOfAcitvityForUser()):  # numer dla uzytkownika po prawej stronie
                isTrue = False
                break
            ListOfFilteredActivityFromUser.append(int(oneActivityForUser))
        if isTrue == False:
            continue

        UniqueChoices = list(dict.fromkeys(ListOfFilteredActivityFromUser))

        for oneActivityForUser in UniqueChoices:
            oneActivityForUser = oneActivityForUser - 1
            validTypeActivity = GlobalNamesOfActivityTypes.ListOfAcitvityForUser()[oneActivityForUser]
            listOfValidActivityFromUser.append(validTypeActivity)
        break

    activityLogic.GenerateActivity(listOfValidActivityFromUser)

# koniec Wyboru aktywnosci przez uzytkownika

# generowanie zadan

for activity in loggedUser.ListOfActivity:
    if len(activity.ListOfTasks) < 1 or (activity.WeeklyTasksEndDate - datetime.combine(date.today(), datetime.min.time())).days < 0: # TU ZMIENIIONE ListOfTasks[0].TaskEndDate

        print("")
        print(f"Wybierz zadania z aktywnosci {activity.TypeActivity} ktore podejmiesz sie realizowac w tym tygodniu:")
        listOfPossibleTasks = GlobalNamesOfTasksTypes.ReturnListOfTasksForTheTypeOfActivity(activity.TypeActivity)
        for idxOneActivityForUser, oneActivityForUser in enumerate(listOfPossibleTasks):
            print(f"{idxOneActivityForUser + 1}-{oneActivityForUser}")

        listOfTaskTypesForActivity = []
        while True:
            isTrue = True
            activityInput = input().strip().lower()
            if activityInput == "":
                continue
            listOfActivityFromUser = activityInput.split(",")
            ListOfFilteredActivityFromUser = []
            for oneActivityForUser in listOfActivityFromUser:
                oneActivityForUser = oneActivityForUser.strip()  # usuwanie spacji z pojedynczego stringa w liscie wyborow
                if oneActivityForUser.isdigit() == False or int(oneActivityForUser) > len(listOfPossibleTasks):  # numer dla uzytkownika po prawej stronie
                    isTrue = False
                    break
                ListOfFilteredActivityFromUser.append(int(oneActivityForUser))
            if isTrue == False:
                continue

            UniqueChoices = list(dict.fromkeys(ListOfFilteredActivityFromUser))

            for oneActivityForUser in UniqueChoices:
                oneActivityForUser = oneActivityForUser - 1
                typeTask = listOfPossibleTasks[oneActivityForUser]
                listOfTaskTypesForActivity.append(typeTask)
            break
        activityLogic.GenerateTasksForTheWeek(listOfTaskTypesForActivity, activity)

# KONIEC generowania zadan

print("")
print("Wybrane zadania na tydzień to:")
ShowTasks(loggedUser)
loginLogic.Save()

# PROCESOWANIE ZADAN PRZEZ UZYTKOWNIKA

dailyQuest = DailyQuestLogic(loggedUser)

# reset statusow
ifIsResetOk = False

if loggedUser.NextResetDate == None:
    dailyQuest.ResetOfDailyStatus(None) # ujemna liczba dni oznacza ze "zostal czas"
    ifIsResetOk = True
else:
    daysLeft = (datetime.combine(date.today(), datetime.min.time()) - loggedUser.NextResetDate ).days
    if daysLeft >= 0 :
        dailyQuest.ResetOfDailyStatus(daysLeft)
        ifIsResetOk = True


    # akceptacja zadan
if ifIsResetOk == True:
    print("")
    print("Wybierz zadania do akceptacji w dniu dzisiejszym: ")

    listOfTruesAndFalseToAcceptableTasks = []
    for oneActivity in loggedUser.ListOfActivity:
        for oneTask in oneActivity.ListOfTasks:
                print(f"Czy akceptujesz {oneTask.ContentOfTheTasks}?")
                print("Wpisz tak/nie:")
                while True:
                    taskAcceptInput = input().strip().lower()
                    if taskAcceptInput == "tak":
                        listOfTruesAndFalseToAcceptableTasks.append(True)
                        break
                    elif taskAcceptInput == "nie":
                        listOfTruesAndFalseToAcceptableTasks.append(False)
                        break
                    else:
                        print("Wpisano niepoprawną wartość")
                        continue

    dailyQuest.CompleteOfTaskAcceptanceStatuses(listOfTruesAndFalseToAcceptableTasks)
    loginLogic.Save()
print("")
print("Lista zaakceptowanych zadań na dziś: ")
ShowActiveTasks(loggedUser)


print("")

# ZAMKNIECIE ZADAN

print("")
print("Wybierz ktore zadania chcesz zakonczyc, jesli nie chcesz wpisz koniec by zamknac program :")

activeListTasks = list(loggedUser.GetListActiveTasks())
isEnd = False

while True:
    userInputToEndTask = input().lower().strip()
    if userInputToEndTask == "koniec":
        break
    listUserChoicesToEndTask = userInputToEndTask.split(",")
    for userChoice in listUserChoicesToEndTask:
        if userChoice.isdigit() == True and int(userChoice) in range(1,len(activeListTasks)+1):
           dailyQuest.CompletionOfTaskCompletionStatus(True,activeListTasks[int(userChoice)-1])
           isEnd = True
        else:
            print("niepoprawna wartosc")
            break
    if isEnd == True:
        break
print("")
print(f"Licznik punktów: {loggedUser.PointCouter}")
activeListTasks = list(loggedUser.GetListActiveTasks()) # drugi raz by zrobic "aktualizacje listy"
if len(activeListTasks) > 0:
    print("Lista pozostałych zadań: ")
    ShowActiveTasks(loggedUser)
else:
    print("Wszystkie dzienne cele zostaly zrealizowane gratulacje :)")

loginLogic.Save()
print("")
print("KONIEC")
