from selenium import webdriver

class Person:
    # Город, Имя, Должность, email.
    def __init__(self, city, name, position, email):
        self.city = city
        self.name = name
        self.position = position
        self.email = email


class Data:
    def __init__(self):
        self.Persons = []

    def collect(self):
        webdriver.Chrome()

    def json_dump(self):
        pass

    def csv_dump(self):
        pass


if __name__ == '__main__':
    data = Data()
    data.collect()
    print(data.json_dump())
