from selenium import webdriver
from selenium.webdriver.common.by import By

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
        #button_parts = driver.find_elements(By.CLASS_NAME, 't397__width_33')
        parts = driver.find_elements(By.CLASS_NAME, "t397__wrapper_mobile")[0]
        log(parts)
        ids=[]
        for option in parts.find_elements(By.TAG_NAME, 'option'):
            ids.append([int(i) for i in option.get_attribute('value').split(',')])
        log(ids)
        for ids_list in ids:
            for card_id in ids_list:
                log(card_id)
                log(driver.find_elements(By.ID, f'rec{card_id}'))


    def json_dump(self):
        pass

    def csv_dump(self):
        pass


if __name__ == '__main__':
    data = Data()
    data.collect()
    print(data.json_dump())
