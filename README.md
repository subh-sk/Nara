<h1 align="center">
<img src="https://raw.githubusercontent.com/subh-sk/Nara/main/Logo/nara.png" width="300">
</h1><br>


# Nara

Nara is a comprehensive Python package designed to streamline various tasks such as creating temporary emails, generating random passwords, IDs, names, and more. It also includes features for caching to enhance response times, modifying JSON structures effortlessly, and integrating multiple AI models for real-time information retrieval and engaging chatbot interactions.


## Key Features

- **Temporary Email Creation**: Easily generate and manage temporary emails for testing and other purposes.
- **Random Data Generation**: Generate random passwords, IDs, names, and other data with customizable options.
- **Caching**: Implement caching mechanisms to store data temporarily and improve performance.
- **JSON Manipulation**: Simplify JSON data modification and handling with built-in utilities.
- **AI Integration**: Access and interact with multiple AI models for real-time information and human-like chatbot conversations.
- **AI Training**: Train and customize AI models to enhance their performance and adaptability.

Whether you are developing applications, automating tasks, or integrating AI-based solutions, Nara provides a robust and flexible toolkit to meet your needs.

## Installation

You can install the package using pip:

```bash
pip install Nara
```

## Usage
- Here is a simple example of how to use Nara:

### Usage with temporary Mail
```py
from Nara.Extra import OnlyMail,MailUrl,MailOtp

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

### Usage with json Files
```py
from Nara.Extra import LoadJson,JsonList,JsonDict,LoadTestResults

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
from Nara.Extra import CacheManager
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

### Usage to Create template code Using AI
```py
from Nara import CreateTemplate

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

from Nara import CreateFunc

def main1():
    print("Don't change this function")

@CreateFunc()
def selenium_code_for_flipkart() -> None: #type your reuirements code as function name
    pass

def main():
    print("Don't change this function")


        ###### RESULT ######## 
# └── test.py :
from Nara import CreateFunc


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
