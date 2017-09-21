

# Nike Automation Script #

Automation script developed for - [https://www.nike.com/launch/](https://www.nike.com/launch/).


## Module Requirements :

> Python  - 2.7.10 , 
> Selenium , 
> Phantomjs , 
> BeautifulSoup 



## Module  Abstract :

* A multi-threaded python module(using Thread Pool) developed in Python version 2.7.10.
* Uses `Beautiful Soup` - as HTML parser and `phantomsjs/chrome` driver as JS parser.
* Steps @ a glance -
	* Read all user-password details
	* Create 4 threads (thread pool size) at a time, which will login using available proxy IP's (wait if none available).
	* Each thread move to settings and add new card details as per input CSV.
	* Save thread output into output CSV file with status and logout from the account.
	* iterate until all inputs processed.


## Basic module configurations details :

+ Current Thread Pool size is - 4
+ Uses proxy IP to connect to nike account, with proxy reuse wait time ~ 60 seconds.
+ Script logs will be saved inside *“logs/nikeScript.log”* file
+ All script snapshots will be saved inside *"snapshots"* folder
+ All script inputs will be inside *"inputs"* folder
+ All script outputs will be inside *"outputs"* folder



## Installing module dependencies :

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



### Running the script :

* Open terminal and move to project folder by using command -
```
cd /path/to/script/
```
* After that run script using below command -
```
python nike.py
```

### Providing Input to script :

+ All input files will be inside inputs folder :
	+ All credit card details  will be saved in - *creditCards.csv*
		+ It has following columns - (id,CCnumber,Expiration,Fname,Lname,Address1,Address2,City,State,Zipcode,mobile_no)
	+ All user credentials & card used by them will be saved in  - *userCredentials.csv*
		+ It has following columns - (Username,password,Credit-Card-ID)    [id used in cerditCards.csv ]
	+ All Proxy server details will be saved in - *proxyList.csv*
		+ It has following columns - (ProxyIP:port  or ProxyIP:port:username:password,Timestamp)




### Checking / Verifying script Output :

* Module output will be saved in - **outputs/output_status.csv** file - 
	* It has following columns - ( Username | Mobile verification status | Job status | Error snapshot)
		* Mobile verification status ~ Verified | Unverified | Unknown.
		* Job status ~ Success | Error
		* Error Snapshot ~ path to error image
		

### Checking for Errors 
* All script errors are logged in *logs/nikeScript.log* file.
* Error snapshots are saved in *snapshots/<rand-name>.png* [name can be fetched from either logs or output CSV ]