import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from progress.bar import IncrementalBar

DEBUG = False
TARGET_SITE = 'https://mediakit.iportal.ru/our-team'


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


    def __parse_element(self, element):
        name_ids = ['1635348635117', '1596441835055', '1596441301499', '1652702166877', '1599793822858', '1648717220470', '1642996413669', '1673600278514', '1643959011969', '1629779928279', '1652701798296', '1654226718646', '1652700872756', '1637296945024']
        city_ids = ['1635348635083', '1596441835050', '1596441248760']
        position_ids = ['1635348635122', '1596441835072', '1596441448712', '1652701973284', '1648717229809', '1642996413676', '1599793822884', '1673600278530', '1643959011978', '1629779928286', '1652701843642', '1596441835072', '1652700889499', '1652700178564', '1637296945030']
        person_left = None
        person_right = None

        def parse_name(data_element):
            return data_element.get_attribute('textContent').strip()
        def parse_city(data_element):
            return data_element.get_attribute('textContent').strip()
        def parse_position_email(data_element):
            position = data_element.get_attribute('textContent')
            try:
                email = data_element.find_element(By.TAG_NAME, 'a').get_attribute('textContent').strip()
            except:
                email = ''
            position = position.replace(person_left.email, '')
            position = re.sub(r'[^\w\s]+|[\d]+', r'', person_left.position).strip()
            position = position.split('   ')[0].strip()
            return position, email

        for data_element in element.find_elements(By.CLASS_NAME, 't396__elem'):
            if data_element.get_attribute('data-elem-id') in name_ids:  # это имя
                if int(data_element.get_attribute('data-field-left-value')) < 600:
                    if person_left == None:
                        person_left = Person('', '', '', '')
                    person_left.name = parse_name(data_element)
                else:
                    if person_right == None:
                        person_right = Person('', '', '', '')
                    person_right.name = parse_name(data_element)

            elif data_element.get_attribute('data-elem-id') in city_ids:  # это город
                if int(data_element.get_attribute('data-field-left-value')) < 600:
                    if person_left == None:
                        person_left = Person('', '', '', '')
                    person_left.city = parse_city(data_element)
                else:
                    if person_right == None:
                        person_right = Person('', '', '', '')
                    person_right.city = parse_city(data_element)

            elif data_element.get_attribute('data-elem-id') in position_ids:  # это город
                if int(data_element.get_attribute('data-field-left-value')) < 600:
                    if person_left == None:
                        person_left = Person('', '', '', '')
                    person_left.position,person_left.email = parse_position_email(data_element)
                else:
                    if person_right == None:
                        person_right = Person('', '', '', '')
                    person_right.position,person_right.email = parse_position_email(data_element)
        if not (person_left == None):
            self.Persons.append(person_left)
        if not (person_right == None):
            self.Persons.append(person_right)



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
        bar = IncrementalBar('Countdown', max=len(ids))
        for id in ids:

            elements = []
            try:
                element = driver.find_element(By.ID, f'rec{id}')
                elements.append(element)
            except:
                log(f'id {id} не имеет элемента')
            for element in elements:
                self.__parse_element(element)
            bar.next()
        bar.finish()
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
