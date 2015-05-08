__author__ = 'roman'

import unittest
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select
import time

class SubstringSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def calculate_result(self, dataToSearch):
        result = 0
        with open ("static/task/data.txt", "r") as myfile:
            text = myfile.read()
            toSearchLines = dataToSearch.split("\n")
            for i in range(text.__len__()):
                for line in toSearchLines:
                    if text[i:i+line.__len__()] == line:
                        result += 1
        return result

    def wait_for_work_done(self, driver):
        result = None
        try:
            result = WebDriverWait(driver, 100).until(
                     EC.presence_of_element_located((By.ID, "totalResult"))
                     )
        except TimeoutException:
            return None
        return result

    def test_clients_do_tasks(self):
        driver = self.driver
        driver.get("localhost:8080/server")

        main_window = driver.current_window_handle

        dataToSearch = ".\n,\nsmall\nbig\nab\nac"

        driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL +"t");
        driver.get("localhost:8080");
        driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL +"t");
        driver.get("localhost:8080");
        driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL +"t");
        driver.get("localhost:8080");


        # Go back to First Tab
        driver.find_element_by_tag_name("body").send_keys(Keys.ALT + Keys.NUMPAD1)
        driver.switch_to.window(main_window)

        # find text input field
        i = 0
        delay = 2 # seconds
        searchInputElem = None
        client = None
        for i in range(10):
            try:
                searchInputElem = driver.find_element_by_id('substringToSearch')
                client = driver.find_element_by_name('client')
            except NoSuchElementException:
                time.sleep(delay)
                driver.refresh()
            if searchInputElem and client:
                print "Page is ready!"
                break

        if searchInputElem != None:
            searchInputElem = driver.find_element_by_id("substringToSearch")
            searchInputElem.send_keys(dataToSearch)
            goButton = driver.find_element_by_id("goButton")
            if goButton:
                print "goButton clicked"
                goButton.click()

            result = self.wait_for_work_done(driver)


            if result != None:
                print "result ", result.get_attribute("innerHTML")
                python_result = self.calculate_result(dataToSearch)
                print "python result ", python_result
                assert str(result.get_attribute("innerHTML")) == str(python_result)
        else:
            print "searchInputElem not found"



    def tearDown(self):
        self.driver.close()
