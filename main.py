from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

DEBUG = True
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

    def collect(self):
        driver = webdriver.Chrome()
        driver.get(TARGET_SITE)
        actions = ActionChains(driver)
        buttons = driver.find_elements(By.CLASS_NAME, 't397__tab')[:3]

        for button in buttons:
            actions.move_to_element(button)
            actions.perform()
            button.click()
            time.sleep(1)


        elements = driver.find_elements(By.CLASS_NAME, 't544')
        for element in elements:
            name = element.find_element(By.CLASS_NAME,'t544__title').get_attribute('textContent')
            log(name)
            position = element.find_element(By.CLASS_NAME, 't544__descr').get_attribute('textContent')
            log(position)


    def json_dump(self):
        pass

    def csv_dump(self):
        pass


if __name__ == '__main__':
    data = Data()
    data.collect()
