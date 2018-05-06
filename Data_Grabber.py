from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import sqlite3
from passlib.hash import sha256_crypt
import pandas as pd
from selenium.webdriver.support.ui  import WebDriverWait

status = True
database = "C:\\Users\\Uchenna\\Documents\\Python\\KCRW Source Files\\Credentials.db"
connection = sqlite3.connect(database)
cur = connection.cursor()
data = cur.execute("SELECT User, Pass FROM User_Pass")

credentials = data.fetchall()

credentials_username = credentials[0][0]
credentials_password = credentials[0][1]


while status:
    user = input('What is your Podtrac username?')
    password = input('What is your Podtrac password?')
    if sha256_crypt.verify(user, credentials_username) and sha256_crypt.verify(password, credentials_password):
        status = False
    else:
        print('Your username or password is incorrect, please try again')


driver = webdriver.Firefox()    # Most accessible browser
driver.get('http://publisher.podtrac.com/account/login')

current_window = driver.current_window_handle

element = driver.find_element_by_xpath('//*[@id="Email"]')
element.send_keys(user)         # Inputting username

element = driver.find_element_by_xpath('//*[@id="ClearPasscode"]')
element.send_keys(password)     # Inputting password

element = element.find_element_by_xpath('//*[@id="form0"]/div[3]/input')
element.send_keys(Keys.ENTER)

# Page is logged in

def find(pointer):
    element = pointer.find_element_by_xpath('//*[@id="tabs"]/ul/li[2]/a')
    if element:
        return element
    else:
        return False


# Navigating to Show information
element = WebDriverWait(driver,15).until(find)
# element = driver.find_element_by_xpath('//*[@id="tabs"]/ul/li[2]/a')
element.click()                 # Clicks 'Audience' tab, top right

element = driver.find_element_by_xpath('/html/body/div[3]/div/div/div/ul/li[1]/a')
element.click()                 # Clicks the Measurement Reports button

# Todo: Fix the staling exceptions...
# May need to click the website in between to keep it active?
element = element.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/div[1]/ul/li[2]/a')
element.click()                 # Clicks the 'By Source' option

options = Select(driver.find_element_by_id('podcastList'))
options.select_by_visible_text('Celestial Blood')

html_source = driver.page_source

File = open("C:\\Users\\Uchenna\\Documents\\Python\\Podtrac Analytics\\Podtrac_ShowSources.txt", 'w')

File.write(html_source)

table = pd.read_html(html_source)
