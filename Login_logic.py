import pickle
import os.path
import Model


class LoginLogic:
    def __init__(self):
        self.Users = []
        if os.path.isfile('data.txt') == False:
            with open('data.txt', 'xb') as save:
                ListOfUsers = []  # dodanie listy do pustego pliku
                pickle.dump(ListOfUsers, save, pickle.HIGHEST_PROTOCOL)  # sprawdzanie czy istnieje plik

        with open('data.txt', 'rb') as load:
            x = pickle.load(load)
            self.Users = x

    def Login(self, login, password):
        for oneUser in self.Users:  # oneActivityForUser przybiera dana wartosc z listy [ o1, o2 , o3 ] -> [o1 = oneActivityForUser ,o2 , o3 ]
            if login == oneUser.Login and password == oneUser.Password:  # odniesienie do modelu (do profilu uzytkownika )
                return oneUser  # zwroc uzytkownika, wychodzi z petli for (podobne dzialanie do break )
        return None  # zwraca brak bo nie ma uzytkownika zgodnego z Loginem i Haslem

    def AddUser(self, login, password):
        login = login.strip()
        password = password.strip()
        if login == "" or len(login) < 3 or len(login) > 15:  # sprawdzanie czy jest pusty string , funkcja strip "odejmuje" spacje oraz sprawdzenie długości
            return None  # zwraca wartość NONE
        if password == "" or len(password) < 4 or len(password) > 20:
            return None

        p1 = Model.UserProfile(login, password)
        self.Users.append(p1)
        return p1

    def Save(self):
        with open('data.txt', 'wb') as save:
            pickle.dump(self.Users, save, pickle.HIGHEST_PROTOCOL)  # https://www.w3schools.com/python/ref_func_open.asp
