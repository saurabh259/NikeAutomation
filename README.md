
# Nike Automation Script #

Automation script for `"https://www.nike.com/launch/"`.

+ Login into all available nike accounts -> Save respective credit card details -> logout.


## Module Requirements :

> Python  - 2.7.10 , 
> Selenium , 
> Phantomjs , 
> BeautifulSoup 



## Module  Abstract :

A multi-threaded python module(using Thread Pool) developed in Python version 2.7.10.
Read all user credentials and login using available proxy IP's in a Thread Pool of size - 4 (can be configured), 
then save card details into respective Nike account and logout from the machine.



## Basic module configurations details :

+ Current Thread Pool size is - 4
+ Uses proxy IP to connect to nike account, with proxy reuse wait time ~ 60 seconds.
+ All input files will be inside inputs folder :
	+ Credentials & card used  - *userCredentials.csv*
	+ Credit card details   - *creditCards.csv*
	+ Proxy server details - *proxyList.csv*
+ All script logs will be saved inside *“logs/nikeScript.log”* file
+ All script snapshots will be saved inside *"snapshots"* folder


## How to install module dependencies :

* Download and install Python -  [Python download](https://www.python.org/downloads/)

* Install Selenium using below command -  [Read more](https://pypi.python.org/pypi/selenium)

```
sudo pip install selenium
```


* Install BeautifulSoup-3 using below command  - 
```
sudo pip install BeautifulSoup
```


* Phantomjs for OSx is added within this repository, incase you want to download phantomjs executable for other Operating System download  [download here](http://phantomjs.org/download.html). 



### How to run :

* Open terminal and move to project folder by using command -
```
cd /path/to/script/
```
* After that run script using below command -
```
python nike.py
```


### Verifying Output :

* Script output can be verified by script- snapshot in snapshots folder.




### Checking for Errors 
* All script errors are logged in logs/nikeScript.log file.





