from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup

DEBUG = True
TARGET_SITE = 'https://mediakit.iportal.ru/our-team'


class Utils:
    @staticmethod
    def group(lst, n):
        return [lst[i:i + n] for i in range(0, len(lst), n)]

#метод чтобы не удалять print(X) со всего кода
def log(log_string):
    if DEBUG:
        print(log_string)

class Person:
    # Город, Имя, Должность, email.
    def __init__(self, city, name, position, email):
        self.city = city
        self.name = name
        self.position = position
        self.email = email

    def __str__(self):
        return f'City:{self.city}, Name:{self.name}, Position:{self.position}, Email:{self.email}'

class Data:
    def __init__(self):
        self.Persons = []

    def collect(self):
        driver = webdriver.Chrome()
        driver.get(TARGET_SITE)
        actions = ActionChains(driver)
        buttons = driver.find_elements(By.CLASS_NAME, 't397__tab')[:3]

        for button in buttons:
            actions.move_to_element(button)
            actions.perform()
            button.click()

        #t544
        elements = driver.find_elements(By.CLASS_NAME, 't544')
        for element in elements:
            name = element.find_element(By.CLASS_NAME,'t544__title').get_attribute('textContent')
            position = element.find_element(By.CLASS_NAME, 't544__descr').get_attribute('textContent')
            city = "..."
            email = element.find_element(By.TAG_NAME, 'a').get_attribute('textContent')
            person = Person(city,name,position,email)
            self.Persons.append(person)

        menu = driver.find_element(By.CLASS_NAME, 't397__wrapper_mobile')
        options = menu.find_elements(By.TAG_NAME, 'option')
        ids = []
        for option in options:
            for id in option.get_attribute('value').split(','):
                ids.append(id)

        #t396
        for id in ids:
            elements = []
            try:
                element = driver.find_element(By.ID, f'rec{id}')
                elements.append(element)
            except:
                log(f'id {id} не имеет элемента')
            for element in elements:
                persons = []
                for data_element in element.find_elements(By.CLASS_NAME,'t396__elem'):
                    if data_element.get_attribute('data-elem-id')=='1596441248760':
                        if len(persons)==0:
                            persons.append(Person('','','',''))
                        #это город перса0
                        persons[0].city = data_element.get_attribute('textContent')
                    elif data_element.get_attribute('data-elem-id')in ['1599793822858', '1596441301499']:
                        if len(persons)==0:
                            persons.append(Person('','','',''))
                        #это имя перса0
                        persons[0].name = data_element.get_attribute('textContent')
                    elif data_element.get_attribute('data-elem-id')=='1599793822884':
                        #это должность и мейл перса0
                        if len(persons)==0:
                            persons.append(Person('','','',''))
                        soup = BeautifulSoup(data_element.get_attribute("innerHTML"), 'html.parser')
                        persons[0].position = soup.find('div', {"class": "tn-atom"}).text
                        log(persons[0].position)
                        try:
                            persons[0].email=soup.find('a').text
                        except:
                            pass
                for person in persons:
                    self.Persons.append(person)

        for person in self.Persons:
            pass
            log(person)



    def json_dump(self):
        pass

    def csv_dump(self):
        pass


if __name__ == '__main__':
    data = Data()
    data.collect()
