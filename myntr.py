print('hello world');
import requests
from bs4 import BeautifulSoup
import time
# get url
# myntraPage = requests.get('https://www.ikea.com/in/en/')
# time.sleep(5)
# soup = BeautifulSoup(myntraPage.content, 'html.parser')

# searchBar = soup.find('input', attrs={'role':'combobox', 'aria-label': 'Search for products, inspiration or new arrivals'})
# # print(soup.title)
# print(searchBar)
# searchBar["value"]='KIVIK 4-seat sofa'

# # requests.get('https://www.ikea.com/in/en/search/?q=KIVIK%204-seat%20sofa')
# time.sleep(5)
# prodlist = soup.find('plp-product-list__products')
# print(prodlist)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import twilio
from twilio.rest import Client
import re
# import twilio.rest

webpage = "https://www.ikea.com/in/en/" 
searchterm = "KIVIK 4-seat sofa" 
expectedAmount = 73000

driver = webdriver.Chrome()
driver.get(webpage)
time.sleep(5)

# sbox = driver.find_element(By.NAME,"q").send_keys('KIVIK 4-seat sofa')
sbox=driver.find_element(By.CLASS_NAME, "search-field__input")
sbox.send_keys('KIVIK 4-seat sofa')
sbox.send_keys(Keys.ENTER)
# print(sbox.get_attribute('outerHTML'))

time.sleep(5)

prodlist = driver.find_element(By.CLASS_NAME,'plp-product-list__products')
# print(prodlist)

# whatsapp configs twilio
account_sid = "" 
auth_token = ""
client = Client(account_sid, auth_token) 

prodlist = []
foundDiscount = False
expectedProdDetails = []
prodcards = driver.find_elements(By.CLASS_NAME, 'plp-fragment-wrapper')
for prodcard in prodcards: 
    title = prodcard.find_element(By.CLASS_NAME, "pip-header-section__title--small").text
    desc = prodcard.find_element(By.CLASS_NAME, "pip-header-section__description-text").text
    amount = prodcard.find_element(By.CLASS_NAME, "pip-price__integer").text
    productInfo = {'title': title, 'price': amount,'description':desc}
    prodlist.append(productInfo)
    amountTrim = re.sub(",","",amount)
    # print(amountTrim)
    if  int(amountTrim) <= expectedAmount:
        foundDiscount = True
        # print(foundDiscount)
        expectedProdDetails.append(productInfo)
        # print(productInfo)

print(prodlist)

if foundDiscount == True:
    notificationMsg = "You have your favorite couch on discounted price! check it out {expectedProdDetails}"
    try:
        message = client.messages.create(
                                body='Hello there!',
                                from_='whatsapp:+14155238886',
                                to='whatsapp:918825834718'
                            )
        print(message.sid)
    except twilio.TwilioRestException as err: print(err)

# plp-fragment-wrapper