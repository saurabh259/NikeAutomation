##Python library imports
import BeautifulSoup
from selenium import webdriver
import random 
import logging
import csv
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import *


#Declaration global data
driver=None
url="https://www.nike.com/launch/"
implicit_wait_time=60
load_timeout=60



#Saving all error/warning logs to given file
#Change here for change in log filename or Log LEVEL
logging.basicConfig(filename='logs/nikeScript.log',level=logging.ERROR)




#
#Custom header used for PhantomJS driver |
#Bot detection system will find it hard to differ from normal user
#
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
           'Connection': 'keep-alive'
                     }



#
# List of User Agent's, each time driver is being instantiated
# we randomly choose one user agent for scraping
#
uaList=[
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Ubuntu/10.10 Chromium/8.0.552.237 Chrome/8.0.552.237 Safari/534.10',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36',
'Mozilla/5.0 (compatible; Origyn Web Browser; AmigaOS 4.0; U; en) AppleWebKit/531.0+ (KHTML, like Gecko, Safari/531.0+)',
'Mozilla/5.0 (compatible; Origyn Web Browser; AmigaOS 4.1; ppc; U; en) AppleWebKit/530.0+ (KHTML, like Gecko, Safari/530.0+)'
]





#
#Function creates a new driver or return an existing driver if any.
#uses custom header and random User Agent
#
def getOrCreateDriver():
    global driver

    for key, value in headers.iteritems():
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
    webdriver.DesiredCapabilities.PHANTOMJS[
        'phantomjs.page.settings.userAgent'] = random.choice(uaList)

#
#Use this section to set/unset proxy 
#

#    PROXY = "54.157.185.100:10000"    
#     webdriver.DesiredCapabilities.PHANTOMJS['proxy'] = {
#     "httpProxy":PROXY,
#     "ftpProxy":PROXY,
#     "sslProxy":PROXY,
#     "noProxy":None,
#     "proxyType":"MANUAL",
#     "class":"org.openqa.selenium.Proxy",
#     "autodetect":False
# }

    if driver is not None:
        return driver
    else:
        service_args = [
            '--load-images=no'
            ]
        driver = webdriver.PhantomJS("./phantomjs",service_args=service_args)
        driver.set_window_size(1120, 550)
        driver.implicitly_wait(implicit_wait_time)
        driver.set_page_load_timeout(load_timeout)
        return driver


     



##Check given element exists using Xpath        
def check_exists_by_xpath(xpath):
    try:
        webdriver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True







#Read CSV file and return reader to calling function
def csvReader():
    inputReader = csv.reader(open('input.csv'), delimiter=',', quotechar='|')
    next(inputReader)
    return inputReader



#
# Main function
#
if __name__ == "__main__":

    driver  = getOrCreateDriver()
    try:
        driver.implicitly_wait(100)
        driver.get(url) 
        print('Phantomjs driver started & fetched url -'+str(url))
        driver.save_screenshot("snapshots/home_page.png")

        #read all input data
        inputReader=csvReader();
        for row in inputReader:
            print("processing - "+str(row))

            username=row[0]
            password=row[1]
            ccnumber=row[2]
            expiration=row[3]
            fname=row[4]
            lname=row[5]
            add1=row[6]
            add2=row[7]
            city=row[8]
            state=row[9]
            zipcode=row[10]
            mobNo=row[11]



            link = driver.find_element_by_link_text("Join / Log In")
            link.click()
            time.sleep(4)


            emailInput = driver.find_element_by_name("emailAddress")
            emailInput.clear()
            emailInput.send_keys(username)

            passwordInput = driver.find_element_by_name("password")
            passwordInput.clear()
            passwordInput.send_keys(password)

           
            loginButton = driver.find_element_by_xpath("//input[@type='button']")
            driver.save_screenshot("snapshots/filled-modal.png")
            print('Login clicked |  sleep')

            loginButton.click()
            time.sleep(4)
                   

            menu=driver.find_element_by_xpath("//figcaption[@class='test-name small text-color-grey u-capitalize u-sm-ib u-va-m']")
            menu.click()
            driver.save_screenshot("snapshots/logged_in_menu.png")


            settings = driver.find_element_by_link_text("Settings")
            settings.click()
            time.sleep(1)
            driver.save_screenshot("snapshots/settings_page.png")



            print('Logged in adding new card')
            element = driver.find_element_by_partial_link_text("NEW CARD")
            element.click()
            time.sleep(5)
            driver.save_screenshot("snapshots/new_card.png");

         


            iframe = driver.find_element_by_xpath('//iframe[1]')
            # print(iframe.get_attribute("src"))
            # print(iframe.get_attribute("class"))
            # print(iframe.get_attribute("sandbox"))

            driver.switch_to_default_content();
            driver.switch_to_frame(1)
            print('switched to credit card frame')

            ccInput = driver.find_element_by_id("creditCardNumber")
            ccInput.clear()
            ccInput.send_keys(ccnumber)


            expirationInput = driver.find_element_by_xpath("//input[@id='expirationDate']")
            expirationInput.clear()
            expirationInput.send_keys(expiration)


            driver.switch_to.default_content();


            fnameInput = driver.find_element_by_id("first-name-shipping")
            fnameInput.clear()
            fnameInput.send_keys(fname)


            lnameInput = driver.find_element_by_id("last-name-shipping")
            lnameInput.clear()
            lnameInput.send_keys(lname)

            add1Input = driver.find_element_by_id("shipping-address-1")
            add1Input.clear()
            add1Input.send_keys(add1)


            add2Input = driver.find_element_by_id("shipping-address-2")
            add2Input.clear()
            add2Input.send_keys(add2)

            cityInput = driver.find_element_by_id("city")
            cityInput.clear()
            cityInput.send_keys(city)


            stateInput = driver.find_element_by_id("state")
            stateInput.clear()
            stateInput.send_keys(state)


            zipcodeInput = driver.find_element_by_id("zipcode")
            zipcodeInput.clear()
            zipcodeInput.send_keys(zipcode)

            mobInput = driver.find_element_by_id("phone-number")
            mobInput.clear()
            mobInput.send_keys(mobNo)

            driver.save_screenshot("snapshots/filled-credit-info.png")
            print('sleep after hitting save details!!')
            saveButton = driver.find_element_by_link_text("Save")
            saveButton.click()
            time.sleep(10)     
            
            driver.save_screenshot("snapshots/card-info-saved.png")
            menu=driver.find_element_by_xpath("//figcaption[@class='test-name small text-color-grey u-capitalize u-sm-ib u-va-m']")
            menu.click()

            print("ADDED card detals for user "+username)


            logout = driver.find_element_by_link_text("Logout")
            logout.click()
            driver.save_screenshot("snapshots/logging_out_page.png")                
            print("Logged out user!!")

    except TimeoutException as e:
        print("Got Exception | Logging out     :")
        print(e)

        driver.find_element_by_link_text("Logout").click()
        driver.save_screenshot("snapshots/logout.png")

    finally:
        print("closing phantom-js driver")
        driver.quit()