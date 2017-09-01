##Python library imports
import BeautifulSoup
from selenium import webdriver
import random 
import logging
import csv
from selenium.common.exceptions import NoSuchElementException
import time
from selenium.common.exceptions import TimeoutException




#Declaration global data
driver=None
url="https://www.nike.com/launch/?s=upcoming"
#url="https://www.nike.com/launch/"
implicit_wait_time=30
load_timeout=30



#Saving all error/warning logs to given file
#Change here for change in log filename or Log LEVEL
#logging.basicConfig(filename='aomScraper.log',level=logging.ERROR)



#
#Custom header used for PhantomJS driver |
#Bot detection system will find it hard to differ from normal user
#
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
           'Connection': 'keep-alive',

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
    # webdriver.DesiredCapabilities.PHANTOMJS[
    #     'phantomjs.page.settings.userAgent'] = random.choice(uaList)
    webdriver.DesiredCapabilities.PHANTOMJS[
        'phantomjs.page.settings.userAgent'] = 2
    
    if driver is not None:
        return driver
    else:
        driver = webdriver.PhantomJS("./phantomjs")
        print(driver.capabilities)
        driver.set_window_size(1120, 550)
        driver.implicitly_wait(implicit_wait_time)
        driver.set_page_load_timeout(load_timeout)
        return driver




#
#Fetch all content and save to temp variable
#
def fetchAllContent(tableRow):
  global allData
  for  row in tableRow:
    #print(row.text)
    single_row_data=row.find_elements_by_xpath('./td');
    singleData=[]
    singleData.append(single_row_data[0].text.encode('utf-8').strip())
    singleData.append(single_row_data[1].text.encode('utf-8').strip())
    singleData.append(single_row_data[2].text.encode('utf-8').strip())
    singleData.append(single_row_data[3].text.encode('utf-8').strip())
    singleData.append(single_row_data[4].text.encode('utf-8').strip())
    singleData.append(single_row_data[5].text.encode('utf-8').strip())
    allData.append(singleData);




        
def check_exists_by_xpath(xpath):
    try:
        webdriver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True



    
#
#Funtion to save data to CSV file
#
def writeToCSV():
  global allData,header
  with open("output.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(allData);





#
# Main function
#
if __name__ == "__main__":
    driver  = getOrCreateDriver()
    try:

        # service_args = [
        #     '--proxy=127.0.0.1:9999',
        #     '--proxy-type=http',
        #     '--ignore-ssl-errors=true'
        #     ]
#      driver  = getOrCreateDriver(service_args=service_args)
        driver.get(url) 
        time.sleep(2)
        print('Phantomjs driver started')
        driver.save_screenshot("home_page.png")

        link = driver.find_element_by_partial_link_text("Log In")
        link.click();
        time.sleep(2)
        print('sleep after login CLICK')
        driver.save_screenshot("login-modal.png")

        email="asda@ascs.co"
        password="sdcsdc"

        print('login screenshot saved')
        emailInput = driver.find_element_by_name("emailAddress")
        emailInput.clear()
        emailInput.send_keys(email)

        passwordInput = driver.find_element_by_name("password")
        passwordInput.clear()
        passwordInput.send_keys(password)

        driver.save_screenshot("filled-modal.png")
        print('sleep after login')

        loginButton = driver.find_element_by_xpath("//input[@type='button']")
        loginButton.click()

        time.sleep(5)
        driver.save_screenshot("final_page.png")

        print("Closing Phantomjs Driver")
    except TimeoutException as e:
        print("printing exception below     :")
        print(e)
    finally:
        driver.quit()