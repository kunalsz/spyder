import time
from selenium import webdriver
from bs4 import BeautifulSoup

#settings
options = webdriver.EdgeOptions()
options.add_argument('--headless')
driver = webdriver.Edge(options=options)

class Input:
    def __init__(self,url):
        self.url = url

    def get_input(self):
        driver.get(self.url)
        time.sleep(3)
        html = driver.page_source
        soup = BeautifulSoup(html,'lxml')
        forms = soup.find_all('form') #find all the forms
        #print(html)

        for form in forms:
            inputs = []
            action = form.get('action')
            for input in form.find_all('input'):
                input_name = input.get('name')
                if input_name:
                    inputs.append(input_name)
                else:
                    pass
            if action:
                return action,inputs