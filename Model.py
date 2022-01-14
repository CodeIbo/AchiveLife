import datetime



class UserProfile:
    def __init__(self, login, password):
        self.Login = login
        self.Password = password
        self.Name = ""
        self.PointCouter = 0  # nieobowiązkowa własciwość klasy (bez niej mozna stworzyc klase)
        self.ListOfActivity = []  # tworzenie tabeli na klase aktywnosci
        self.ActivityEndDate = None
        self.NextResetDate = None

    def GetListActiveTasks (self):
        for oneActivity in self.ListOfActivity:
            for oneTask in oneActivity.ListOfTasks:
                if oneTask.IsAccepted == True and oneTask.IsComplete == False: #zmienione
                    yield oneTask               #yield dodaje do pustej listy oneTask

class Activity:
    def __init__(self, typeActivity):
        self.TypeActivity = typeActivity  # wlasciwosci klasy (prywatne - dla kazdego obiektu indywidualne)
        self.ListOfTasks = []
        self.WeeklyTasksEndDate = None


class Task:
    def __init__(self, contentOfTheTasks):
        self.PointValue = 1 # przyznawany 1pkt za wykonanie zadanie -0,5 za zaakceptowane ale nie ukończone - 1pkt za niezaakceptowane i nieukoncznone
        self.ContentOfTheTasks = contentOfTheTasks
        self.IsComplete = False
        self.IsAccepted = True


class GlobalNamesOfActivityTypes:
    physical = "Activity fizyczna"  # własciwość klasy która jest globalna
    education = "Edukacja"
    finance = "Finanse"
    recreation = "Rozrywka"
    journey = "Podroze"
    culinary = "Kulinaria"

    @staticmethod
    def ListOfAcitvityForUser():
        return [GlobalNamesOfActivityTypes.physical, GlobalNamesOfActivityTypes.finance,
                GlobalNamesOfActivityTypes.education, GlobalNamesOfActivityTypes.recreation]


class GlobalNamesOfTasksTypes:
    t1 = "Bieg"
    t2 = "Pompki"
    t3 = "Brzuszki"
    t4 = "Deska"
    t5 = "Prawo Jazdy"
    t6 = "Angielski"
    t7 = "Nauka inwestycyjna"
    t8 = "Lol ranga"
    t9 = "Lol postać (narzędzie treningowe)"
    t10 = "Refleks"
    t11 = "Oszczednosci"
    t12 = "Inwestycje"
    t13 = "Wydatki (limit płatniczy)"

    @staticmethod
    def ListOfPhysicalTasks():
        return [GlobalNamesOfTasksTypes.t1, GlobalNamesOfTasksTypes.t2, GlobalNamesOfTasksTypes.t3,
                GlobalNamesOfTasksTypes.t4]

    @staticmethod
    def ListOfEducationTasks():
        return [GlobalNamesOfTasksTypes.t5, GlobalNamesOfTasksTypes.t6, GlobalNamesOfTasksTypes.t7]

    @staticmethod
    def ListOfRecreationTasks():
        return [GlobalNamesOfTasksTypes.t8, GlobalNamesOfTasksTypes.t9, GlobalNamesOfTasksTypes.t10]

    @staticmethod
    def ListOfFinancialTasks():
        return [GlobalNamesOfTasksTypes.t11, GlobalNamesOfTasksTypes.t12, GlobalNamesOfTasksTypes.t13]

    @staticmethod
    def ReturnListOfTasksForTheTypeOfActivity(typeActivity):  # metoda sprawdzania ktory jest aktualnie typ aktywnosci
        if GlobalNamesOfActivityTypes.physical == typeActivity:
            return GlobalNamesOfTasksTypes.ListOfPhysicalTasks()

        elif GlobalNamesOfActivityTypes.finance == typeActivity:
            return GlobalNamesOfTasksTypes.ListOfFinancialTasks()

        elif GlobalNamesOfActivityTypes.recreation == typeActivity:
            return GlobalNamesOfTasksTypes.ListOfRecreationTasks()

        elif GlobalNamesOfActivityTypes.education == typeActivity:
            return GlobalNamesOfTasksTypes.ListOfEducationTasks()
        else:
            return []
    # dodac def do kazdego typu aktywnosci , ktora zawiera w sobie zadania , patrz przyklad wyzej

    # Wszystko wrzucasz do jednej listy, która później sortuje według klucza poszczegolne zadania do podrzędnych list
    # Przykładowy kod pomagajacy sortowac zadania:

    # Z1_F <- Z <- zadanie , 1 <- numer zadania , F <- aktywnosc do ktorej zadanie ma byc przypisane ( F - oznacza physical )
