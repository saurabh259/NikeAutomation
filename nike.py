##Python library imports

from multiprocessing.dummy import Pool as ThreadPool
import BeautifulSoup
from selenium import webdriver
import random 
import logging
import csv
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import *
import sys
import webbrowser
import os
import time
import thread
import threading




#Declaration global data
thread_count=4
lock = threading.Lock()
driver=None
url="https://www.nike.com/launch/"
implicit_wait_time=25
load_timeout=40




#Saving all error/warning logs to given file
#Change here for change in log filename or Log LEVEL
logging.basicConfig(filename='logs/nikeScript.log',level=logging.ERROR)
logger = logging.getLogger('nikeScript')






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
#Fetch proxy ip which is not used recently in last 5 minutes
#
def getAvailableProxyIP():
    try:    
        ip=""
        now = int(time.time())
        file1 = open("inputs/proxyList.csv", 'rb')
        file2 = open("inputs/proxyListTemp.csv","wb")

        reader = csv.reader(file1)
        writer = csv.writer(file2)
        check=False
        for rows in reader:
            if(check==False):
                timestamp = int(rows[1])
                difference=(int(now)-timestamp)
                print("Difference in  seconds "+str(difference))
                if(abs(difference)>60):
                    ip=rows[0]
                    rows[1]=now
                    
                    check=True
                else:
                    print("failed proxy IP "+str(ip)+"as time stamp was "+str(timestamp))
            writer.writerow(rows)
        
        file1.close()
        file2.close()
        os.rename("inputs/proxyListTemp.csv","inputs/proxylist.csv")
        return ip
    except Exception as e:
        print(e)




# def fetchAllUserDetails():
#     with open('inputs/.txt', 'r') as f:
#         for line in f.readlines():






#
# Function creates a new driver.
# uses custom header and random User Agent
# if proxy available use it
#
def createDriverWithProxy():
    global driver
    ip=getAvailableProxyIP()

#   testing with and without proxy 
    #ip="13.56.91.112:443"
    # ip="40.71.33.56:3128"
    # ip="127.0.0.1:9999"
    
    # ip=""


    for key, value in headers.iteritems():
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
    webdriver.DesiredCapabilities.PHANTOMJS[
        'phantomjs.page.settings.userAgent'] = random.choice(uaList)
    print('proxy ip fetched = '+ip)
       
    while True:
        if len(ip)<1:
            service_arg = [
                '--load-images=no',
                ]
            driver = webdriver.PhantomJS("./phantomjs",service_args=service_arg)    
            break
            # time.sleep(40)
            # ip=getAvailableProxyIP()
        else:
            print('using proxy ip = '+ip)
            service_arg = [
                '--proxy='+ip,
                '--proxy-type=http',
                '--web-security=no',
                '--ignore-ssl-errors=yes',
                    ]
            driver = webdriver.PhantomJS('./phantomjs',service_args=service_arg)
            print(driver.capabilities)
            break    


# # -----    Using chrome for UI testing --------------
    # chromedriver = "/usr/local/bin/chromedriver"
    # chromeOptions = webdriver.ChromeOptions()
    # prefs = {"profile.managed_default_content_settings.images":2}
    # chromeOptions.add_experimental_option("prefs",prefs)
    # driver = webdriver.Chrome(chromedriver,chrome_options=chromeOptions)



# driver.setLogLevel(Level.OFF)
# driver.implicitly_wait(implicit_wait_time)


    driver.set_window_size(1120, 550)
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
def csvReader(filename):
    with lock:
        inputReader = csv.reader(open(filename), delimiter=',')
        return inputReader




#
#    SEARCH  for credit card from given ID  
#
def creditCardFetcher(rowId):
    row=[]
    with open("inputs/creditCards.csv", 'rb') as f:
        for row in f:
            if row[0]==rowId:
                rowL = row.split(",")
                return rowL


#
# fetch and fill all data
#
def loginAndSave(row):

#Fetch available proxy IP in locked condition
    with lock:
        retry=0
        while True:
            try:
                retry+=1
                driver  = createDriverWithProxy()
                break
            except Exception as e:
                print('Exception fetching driver')
                print(e)
                if(retry>3):
                    break

    

#Hitting login
    ccid=""
    username=""
    retry=0
    while True:
        try:
            retry+=1
            driver.implicitly_wait(30)
            driver.get(url) 
            print('Phantomjs driver started &  url fetched - '+str(url))
            driver.save_screenshot("snapshots/home_page.png")        
                
            username=row[0]
            password=row[1]
            ccid=row[2]


            link = driver.find_element_by_link_text("Join / Log In")
            link.click()
            time.sleep(3)

            emailInput = driver.find_element_by_name("emailAddress")
            emailInput.clear()
            emailInput.send_keys(username)

            passwordInput = driver.find_element_by_name("password")
            passwordInput.clear()
            passwordInput.send_keys(password)
            print(username)


            loginButton = driver.find_element_by_xpath("//input[@type='button']")
            driver.save_screenshot("snapshots/filled-modal.png")
            print('Login clicked |  sleep for 4 sec. ')

            loginButton.click()
            time.sleep(3)

            break
        except Exception as e:
            print('Exception  logging in retry '+str(retry))
            print(e)
            driver.save_screenshot("snapshots/login-error.png")
            
            if(retry>2):
                logger.error('Error loging in user   - '+str(username))
                if driver != None:
                    driver.quit()
                return
                



    retry=0
    while True:
        try:
            retry+=1

            menu=driver.find_element_by_xpath("//figcaption[@class='test-name small text-color-grey u-capitalize u-sm-ib u-va-m']")
            menu.click()
            driver.save_screenshot("snapshots/logged_in_menu.png")


            settings = driver.find_element_by_link_text("Settings")
            settings.click()
            time.sleep(3)
            driver.save_screenshot("snapshots/settings_page.png")
        
        

            break
        except Exception as e:
            print('Exception moving to settings .. retrying.. '+str(retry))
            print(e)

            if(retry>2):
                logger.error('Error in user homepage, cannot move to settings(Mobile verification?)   - '+str(username))
                if driver != None:
                    driver.quit()
                return




    row2= creditCardFetcher(ccid)
    ccnumber=row2[1]
    expiration=row2[2]
    fname=row2[3]
    lname=row2[4]
    add1=row2[5]
    add2=row2[6]
    city=row2[7]
    state=row2[8]
    zipcode=row2[9]
    mobNo=row2[10]


    retry=0
    while True:
        try:
            retry+=1

            element = driver.find_element_by_partial_link_text("NEW CARD")
            element.click()
            time.sleep(4)
            driver.save_screenshot("snapshots/new_card.png");

            # iframe = driver.find_element_by_xpath('//iframe[1]')

            driver.switch_to_default_content();
#Change wen switching b/w phantom and chrome
#            driver.switch_to_frame(0)
            driver.switch_to_frame(1)


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
            saveButton = driver.find_element_by_link_text("Save")
            saveButton.click()
            time.sleep(2)     

            driver.save_screenshot("snapshots/card-info-saved.png")

            break
        except Exception as e:
            print("Got Exception Retrying count - "+str(retry))
            print(e)
            driver.save_screenshot("snapshots/card-save-error.png")

            if(retry>2):
                logoutUser()
                logger.error('Error saving card details in user settings   - '+str(username))
                if driver != None:
                    driver.quit()
                return


                logger.error('Error in user homepage, cannot move to settings(Mobile verification?)   - '+str(username))
                if driver != None:
                    driver.quit()
                return

                

    retry=0
    while True:
        try:
            retry+=1
            logoutUser()
            if driver != None:
                driver.quit()
            break               
        except Exception as e:
            print("exception logging out retrying - "+str(retry))
            print(e)
            if(retry>2):
                break




#
#logout user from his nike account
#
def logoutUser():
    try:
        menu=driver.find_element_by_xpath("//figcaption[@class='test-name small text-color-grey u-capitalize u-sm-ib u-va-m']")
        menu.click()            
        logout = driver.find_element_by_link_text("Logout")
        logout.click()
        time.sleep(1)
    except Exception as e:
        print("exception logging out - ")
        print(e)






#
# Main function | fetch all user credentials list and 
# spawn  child threads.
#
if __name__ == "__main__":

# fetch all user credentials and
    userCredentials=csvReader('inputs/userCredentials.csv');
    userCredentialsList = list(userCredentials)

    try:

# Create pool with max_thread_count and 
# pass all user credentials list
        pool = ThreadPool(thread_count)
        results = pool.map(loginAndSave, userCredentialsList)
        pool.close()
        pool.join()
        
        # print("Saved card details for all users :)") 
    except Exception as e:
       print "Error: Exception in main thread :"
       print e





