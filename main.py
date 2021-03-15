from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

import time

# creds
username = raw_input("Enter your username:\n")
password = raw_input("Enter your password:\n")

# STATES
LOGIN_PAGE = 1
LOGGED_IN_PAGE = 2
REGAIN_ACCESS_PAGE = 3

DEBUG = False
fp = webdriver.FirefoxProfile()

if DEBUG:
    fp.set_preference('network.proxy.type', 1)  # int
    fp.set_preference('network.proxy.socks', 'localhost')  # string
    fp.set_preference('network.proxy.socks_port', 5556)  # int
    fp.set_preference('network.proxy.socks_version', 4)  # int



def wait_for_page_load():
    delay = 10 # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'usercheck_company_logo')))
        print "Page is ready!"
    except TimeoutException:
        print "Loading took too much time!"

    time.sleep(10)



while True:
    driver = webdriver.Firefox(firefox_profile=fp)

    driver.get("https://10.255.1.2/PortalMain")
    wait_for_page_load()
    print("Checking login status..\n")

    state = None;

    try:
        elem = driver.find_element_by_id("LoginUserPassword_auth_username")
        state = LOGIN_PAGE
    except NoSuchElementException:
        try:
            elem = driver.find_element_by_id("UserCheck_Logoff_Button")
            state = LOGGED_IN_PAGE
        except NoSuchElementException:
            state = REGAIN_ACCESS_PAGE

    print(state)


    if state == LOGGED_IN_PAGE:
        print("Already logged in..")
    elif state == LOGIN_PAGE:
        print("Trying to log in..")

        elem = driver.find_element_by_id("LoginUserPassword_auth_username")
        elem.send_keys(username)

        elem = driver.find_element_by_id("LoginUserPassword_auth_password")
        elem.send_keys(password)
        elem.send_keys(Keys.ENTER)
        wait_for_page_load()

    elif state == REGAIN_ACCESS_PAGE:
        print("REGAIN ACCESS.. navigating to login page..")
        elem = driver.find_elements_by_class_name("portal_link")
        elem[0].click()
        wait_for_page_load()

    else:
        "Something went wrong :("

    print("Sleeping for 1 min..\n")
    driver.close()
    time.sleep(60)