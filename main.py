from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

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
            log(person)

        #t396
        elements = driver.find_elements(By.CLASS_NAME, 't396')
        for element in elements:
            if 't-rec_pb_60' in element.find_element(By.XPATH, "..").get_attribute('class'):
                log(element)
                persons_elements = Utils.group(element.find_elements(By.CLASS_NAME, 't396__elem'), 6)
                for person_element in persons_elements:
                    city = person_element[0].find_element(By.CLASS_NAME, 'tn-atom').get_attribute('textContent')
                    log(f'city {city}')
                    name = person_element[4].find_element(By.CLASS_NAME, 'tn-atom').get_attribute('textContent')
                    log(f'name {name}')
                    position = person_element[5].find_element(By.CLASS_NAME, 'tn-atom').get_attribute('textContent')
                    log(f'position {position}')
                    email = city = person_element[5].find_element(By.TAG_NAME, 'a').get_attribute('textContent')
                    log(f'email {email}')
                    person = Person(city, name, position, email)
                    log(person)

    def json_dump(self):
        pass

    def csv_dump(self):
        pass


if __name__ == '__main__':
    data = Data()
    data.collect()
