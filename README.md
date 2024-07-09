<h1 align="center">
<img src="https://raw.githubusercontent.com/subh-sk/nara/main/Logo/nara.png" width="300">
</h1><br>

<p>
    <a href="https://pypi.org/project/Nara" target="_blank">
        <img src="https://img.shields.io/pypi/v/nara" />
    </a>
    <a href="https://pepy.tech/project/Nara" target="_blank">
        <img src="https://pepy.tech/badge/nara" />
    </a>
    <a href="https://github.com/subh-sk/Nara" target="_blank">
        <img src="https://img.shields.io/badge/nara-v0.3-green" />
    </a>
    
</p>

# nara

Nara is a sophisticated Python package tailored for AI-powered automation, empowering users to effortlessly generate functions and Python templates based on intuitive prompts. Beyond this capability, it facilitates diverse tasks including creating temporary emails, generating random passwords, IDs, and names. Moreover, Nara features robust caching mechanisms to optimize performance and seamless JSON manipulation for efficient data handling.


## Key Features

- **Temporary Email Creation**: Easily generate and manage temporary emails for testing and other purposes.
- **Random Data Generation**: Generate random passwords, IDs, names, and other data with customizable options.
- **Caching**: Implement caching mechanisms to store data temporarily and improve performance.
- **JSON Manipulation**: Simplify JSON data modification and handling with built-in utilities.
- **AI Integration**: Access and interact with multiple AI models for real-time information and human-like chatbot conversations.
- **AI Training**: Train and customize AI models to enhance their performance and adaptability.
- **Async Functionality**: Utilize asynchronous capabilities for efficient task handling and performance optimization.
- **File Management**: Manage and manipulate files with ease, providing comprehensive support for file-related operations.

Whether you are developing applications, automating tasks, or integrating AI-based solutions, nara provides a robust and flexible toolkit to meet your needs.


## Installation

You can install the package using pip:

```bash
pip install nara
```
```bash
pip install -U git+https://github.com/subh-sk/Nara.git
```

## Usage
- Here is a simple example of how to use nara:

### Usage to Create template code Using AI
```py
from nara import CreateTemplate

#Example usage for create template code of the provided prompt. like here we give selenium so it will change your file and write code for selenium structure
CreateTemplate("selenium")

└── test.py :  CreateTemplate("selenium")
################## make code for selenium template 👇 ####################
test.py :
from selenium import webdriver
from selenium.webdriver.common.by import By

# Replace with your preferred browser
driver = webdriver.Chrome()  # For Chrome
# driver = webdriver.Firefox()  # For Firefox

def navigate_to_url(url):
    driver.get(url)

def find_element_by_xpath(xpath):
    element = driver.find_element(By.XPATH, xpath)
    return element

def close_browser():
    driver.quit()

# Example usage
url = "https://www.google.com"
navigate_to_url(url)
element = find_element_by_xpath("//input[@name='q']")
print(element.get_attribute("placeholder"))

close_browser()

```

### Usage to Create Function code Using AI
```py

# └── test.py :

from nara import CreateFunc

def main1():
    print("Don't change this function")

# @CreateFunc()
# def selenium_code_for_flipkart() -> None: #type your reuirements code as function name
    pass

########## OR ###########

#here you can specify your question in doc string.
@CreateFunc()
def test():
    '''selenium code for click flipkart login button'''


def main():
    print("Don't change this function")


        ###### RESULT ######## 
# └── test.py :
from nara import CreateFunc


def main1():
    print("Don't change this function")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def selenium_code_for_flipkart() -> int:
    driver = webdriver.Chrome()  # Replace with your preferred browser
    driver.get("https://www.flipkart.com")
    WebDriverWait(driver, 10).until(EC.title_contains("Flipkart"))
    # Add your custom code here to interact with the Flipkart webpage
    driver.quit()
    return 0

def main():
    print("Don't change this function")

```


### Usage with temporary Mail
- 1st Way
```py
from nara.Extra import OnlyMail,MailUrl,MailOtp

# Example usage for generating a temporary email
OnlyMail(Printable=True) #only for generate email

# Example usage for generating a temporary email and get verification link
mail_OBJ = MailUrl(Timeout=20,Printable=True)
print(next(mail_OBJ))
input("wait = ")
url = next(mail_OBJ)
print(url)

# Example usage for generating a temporary email and get verification Code
mail_OBJ = MailOtp(OtpLength=6,Timeout=20,Printable=True)
print(next(mail_OBJ))
input("wait = ")
url = next(mail_OBJ)
print(url)

```
- 2nd Way
```py
from nara.extra import tempmailio
domains = tempmailio().cheeck_domain()
print(domains) # print all available domain


obj1 = tempmailio(Printable=True,email_name="Naradone",domain="rfcdrive.com").mailioOtp(OtpLength=6)
next(obj1) # Print email address with given name and domain name
next(obj1) # Print otp's in List formate

obj2 = tempmailio(Printable=True,domain="rfcdrive.com").mailioOtp(OtpLength=6)
next(obj2) # Print email address give domain name and random name
next(obj2) # Print otp's in List formate

obj3 = tempmailio(Printable=True,email_name="Naradone").mailioOtp(OtpLength=6)
next(obj3) # Print email address give name and random domain name
next(obj3) # Print otp's in List formate

obj4 = tempmailio(Printable=True).mailioUrl()
next(obj4) # Print random email address give domain name and random name
next(obj3) #Print Link's in List formate

```

### Usage telegram Cloude Storage
- ### Setup your telegram channel
> - [click here to get your telegram App ID, App Hash](https://my.telegram.org/auth)
> - create a channel in your telegram account and copy the channel id
> - In ConfigureDatabase() you need to add channel id, Aapp ID,App Hash,Contact number with country code, your Session Name to create cache for faster response.

```py
from nara import tele_db

config = tele_db.ConfigureDatabase() #Used to configure Your Cloud Database.

all_table = tele_db.table_list() #Used to get list of all tables from Your Cloud Database. Note, This is confidential, So first time it will ask you for set authentication token. Then from next time it will ask you for authentication token. After that it will return list of all tables.

db = tele_db.user_db(table_id="100") #It will check configuration, If configuration not found it will ask you of your telegram app ID,Hash,etc. Afterwards it will check table name and create if not found.

print(db.count()) #used to count the number of tables

```
### Usage with CurrentDateTime
- ### Current time and date of all country

```py
from nara.extra import CurrentDateTime

# Initialize the CurrentDateTime object
datetime_obj = CurrentDateTime()

# Print current time of India in str
print(datetime_obj.time("in"))

# Print current time of India in datetime formate
print(datetime_obj.time("in", encode=True))

# Print current date of India datetime formate
print(datetime_obj.date("in", encode=True))

# Print current date of India in str 
print(datetime_obj.date("in"))

# Print country codes
print(datetime_obj.country_codes())

```
### Usage with RandomDataGenerator
```py
from nara.extra import RandomDataGenerator
generator = RandomDataGenerator()

# Example outputs
print("Name:", generator.name())  # e.g., "John Doe"
print("First Name:", generator.first_name())  # e.g., "John"

print("Last Name:", generator.last_name())  # e.g., "Doe"
print("Indian Name:", generator.indian_name())  # e.g., "राहुल राम"
print("Foreign Name:", generator.foreign_name())  # e.g., "Marie Martin"
print("Location:", generator.location())  # e.g., "Antarctica"
print("Address:", generator.address())  # e.g., "123 Main St, Springfield, IL"
print("Indian Address:", generator.indian_address())  # e.g., "मुंबई"
print("Foreign Address:", generator.foreign_address())  # e.g., "Paris, France"
print("Pincode:", generator.pincode())  # e.g., "123456"
print("Date of Birth:", generator.dob())  # e.g., "2000-05-20"
print("ID:", generator.id())  # e.g., "JohnDoe1234"
print("Username:", generator.username())  # e.g., "johndoe1234"
print("Random String:", generator.random_string(15))  # e.g., "aBcD1234eFgHiJkL"
print("Password:", generator.password(length=12, special_count=2, digit_count=2))  # e.g., "aB@1cD!2eF3gH4"


```
### Usage with TimeIt
```py
from nara.extra TimeIt

@TimeIt
def my_function():
    time.sleep(1)

my_function()

# Example Output: • Execution time for 'my_function' : 1.000956 Seconds.
```

### Usage with run_multiple_times
```py
from nara.extra run_multiple_times

@run_multiple_times(5)
async def task_runner():
    pass # Your Code Implementation

@run_multiple_times(5)
def task_runner():
    # # Your Code Implementation

# This will run `task_runner` 5 times concurrently when called.

# Note: This works for both synchronous and asynchronous functions.
```

### Usage with repeat_forever

```py
from nara.extra import repeat_forever

@repeat_forever(sleep_interval=2.0, end_after="10 minutes")
def my_function():
    print("Hello, World!")

@repeat_forever(sleep_interval=1.0, end_after="5 minutes")
async def my_function():
    print("Hello, World!")

"""
This code uses the @repeat_forever decorator to create two functions (my_function), one synchronous and one asynchronous, that will execute repeatedly at specified intervals (sleep_interval). They will continue to run until the specified end time (end_after) is reached, simulating a while True loop behavior.
"""
```
### Usage with async_threaded_task


```py
from nara.extra import async_threaded_task

@async_threaded_task
async def async_function(*args, **kwargs):
    # Function body

# Can also specify the number of threads to use for execution.
@async_threaded_task(1)
async def async_function(*args, **kwargs):
    # Function body

async def main():
    await async_function()

asyncio.run(main())

"""
This decorator is useful for running async functions that need to be executed in a thread-safe manner, typically when interfacing with synchronous libraries
or performing blocking I/O operations.
"""
```
### Usage with display_file_structure

```py
from nara.extra import display_file_structure

display_file_structure() # Call the function.

"""
This displays the working files and folders structure.
"""
```

### Usage with clear_pycache_directories
```py
import os
from nara.extra import clear_pycache_directories

clear_pycache_directories(directory=os.getcwd(), display_status=True)

"""
The provided code snippet clears all the `__pycache__` directories from the specified path. Setting `display_status` to True displays information about the deleted directories.
"""
```


### Usage with json Files
```py
from nara.Extra import LoadJson,JsonList,JsonDict,LoadTestResults

 #Example usage for create a json file if not exist and save your jason as list formate
JsonList(FileName="data.json", name="Alice", age=30)

└── test.py
└── data.json
data.json : [
                {
                "name": "Alice",
                "age": 30
                }
            ]


#Example usage for create a json file if not exist and save your jason as Dict formate
JsonDict(Key="username", Value="johndoe", FileName="config.json")

└── test.py
└── config.json
config.json : {
                "username": "johndoe"
            }

#Example usage for Load The json file
a = LoadJson(FileName="config.json")
print(a)
> OUTPUT : {'username': 'johndoe'}

```

### Usage For fast Processing

```py
#Example usage for create cache file that will help you to run your cache code in millisecond
from nara.Extra import CacheManager
a= CacheManager("cache.json")
@a.cache
def b():
    a,b=10,20
    c = 0
    c = a+b
    sleep(5)
    c = c+10
    return a+b
print(b()) #first time it store this function return in chache
print(b()) #it will retrun the function within a millisecond using cahe.json

```


## Authors
- Subhash Kumar
- Divyansh Shukla
- Yateesh Reddy

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome! Please read the CONTRIBUTING.md file for details on how to contribute to this project.

## Contact
If you have any questions or suggestions, feel free to contact us at naravirtualai@gmail.com.

## Acknowledgements
Special thanks to all the contributors and users who have supported this project.
