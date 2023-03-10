import re
import csv
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
        log(ids)
        name_ids = ['1635348635117', '1596441835055', '1596441301499', '1652702166877', '1599793822858', '1648717220470', '1642996413669', '1673600278514', '1643959011969', '1629779928279', '1652701798296', '1654226718646', '1652700872756', '1637296945024']
        city_ids = ['1635348635083', '1596441835050', '1596441248760']
        position_ids = ['1635348635122', '1596441835072', '1596441448712', '1652701973284', '1648717229809', '1642996413676', '1599793822884', '1673600278530', '1643959011978', '1629779928286', '1652701843642', '1596441835072', '1652700889499', '1652700178564', '1637296945030']
        for id in ids:
            elements = []
            try:
                element = driver.find_element(By.ID, f'rec{id}')
                elements.append(element)
            except:
                log(f'id {id} не имеет элемента')
            for element in elements:
                person_left = None
                person_right = None
                for data_element in element.find_elements(By.CLASS_NAME, 't396__elem'):
                    if data_element.get_attribute('data-elem-id') in name_ids: #это имя
                        if int(data_element.get_attribute('data-field-left-value'))<600:
                            if person_left == None:
                                person_left = Person('','','','')
                            person_left.name = data_element.get_attribute('textContent')
                        else:
                            if person_right == None:
                                person_right = Person('','','','')
                            person_right.name = data_element.get_attribute('textContent')

                    elif data_element.get_attribute('data-elem-id') in city_ids: #это город
                        if int(data_element.get_attribute('data-field-left-value'))<600:
                            if person_left == None:
                                person_left = Person('','','','')
                            person_left.city = data_element.get_attribute('textContent')
                        else:
                            if person_right == None:
                                person_right = Person('','','','')
                            person_right.city = data_element.get_attribute('textContent')

                    elif data_element.get_attribute('data-elem-id') in position_ids: #это город
                        if int(data_element.get_attribute('data-field-left-value'))<600:
                            if person_left == None:
                                person_left = Person('','','','')
                            person_left.position = data_element.get_attribute('textContent')
                            try:
                                person_left.email = data_element.find_element(By.TAG_NAME, 'a').get_attribute('textContent')
                            except:
                                pass
                            person_left.position = person_left.position.replace(person_left.email,'')
                            person_left.position = re.sub(r'[^\w\s]+|[\d]+', r'',person_left.position).strip()
                            person_left.position = person_left.position.split('   ')[0]
                        else:
                            if person_right == None:
                                person_right = Person('','','','')
                            person_right.position = data_element.get_attribute('textContent')
                            try:
                                person_right.email = data_element.find_element(By.TAG_NAME, 'a').get_attribute('textContent')
                            except:
                                pass
                            person_right.position = person_right.position.replace(person_right.email, '')
                            person_right.position = re.sub(r'[^\w\s]+|[\d]+', r'', person_right.position).strip()
                            person_right.position = person_right.position.split('   ')[0]
                if not (person_left == None):
                    self.Persons.append(person_left)
                if not (person_right == None):
                    self.Persons.append(person_right)
        for person in self.Persons:
            log(person)



    def json_dump(self):
        pass

    def csv_dump(self, filename):
        with open(f'{filename}.csv', 'w', newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter = ",", lineterminator="\r")
            writer.writerow(["Имя", "Город", "Позиция", "имейл"])
            for person in self.Persons:
                writer.writerow([person.name, person.city, person.position, person.email])


if __name__ == '__main__':
    data = Data()
    data.collect()
    data.csv_dump('dump')
