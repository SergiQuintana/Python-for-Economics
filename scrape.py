from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium
import csv
import time
import os 
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

#============
#
#
#https://github.com/mozilla/geckodriver/releases
# load the browser:
options = Options()
options.headless = False
#driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
options.set_preference("network.cookie.cookieBehavior", 2)
driver = webdriver.Firefox( options=options)

url = r"https://www.carrefour.es/supermercado/leche-semidesnatada-carrefour-brik-1-l/R-521007071/p"
driver.get(url)

name = driver.find_element(By.XPATH, '//h1[@class="product-header__name"]').text
price = driver.find_element(By.XPATH, '//span[@class="buybox__price"]').text
print("Product is :",name," and price is : ",price)

## Now for the whole page of "lacteos"

url = r"https://www.carrefour.es/supermercado/la-despensa/lacteos/cat20011/c"

driver.get(url)

# Notice some products do not load until we scroll down!! This is the java rendering!


# Create the scroller

def scroll(browser, pixels):
    # introduce a browser and the amount of pixels you would like to scroll at each iteration!
    height = int(browser.execute_script("return document.documentElement.scrollHeight"))
    it = 0
    while ((it+1)*pixels) < height: 
        browser.execute_script(f"window.scrollBy({it*pixels},{(it+1)*pixels});")
        time.sleep(0.4)
        it = it+1
    if ((it+1)*pixels) > height:
        browser.execute_script(f"window.scrollBy({it*pixels},{height});")
    return

scroll(driver,400)


name_products =  driver.find_elements(By.XPATH, '//a[@class="product-card__title-link track-click"]')
price_products =  driver.find_elements(By.XPATH, '//span[@class="product-card__price"]')

print(len(name_products))
print((len(price_products)))

#for i in range(len(name_products)):
for i in range(len(price_products)):

    name = name_products[i].text
    price = price_products[i].text
    url = name_products[i].get_attribute('href')

    print(name,price,url)

# PROBLEM! we are considering the products in "offers"
    

# NOW FIND THE NEWXT PAGE!
    
nextpage =driver.find_element(By.XPATH, '//div[@class="pagination__row"]')
nextpage.find_element(By.TAG_NAME,'a').click()

# Repeat the process...! 

# TO BE DONE!

# Now identify the amount of pages ex-ante. 
def find_total_pages(browser):
    total_products = browser.find_element(By.XPATH, '//span[@class="plp-food-view__count"]').text
    number = int(total_products.replace('Mostrando ','').replace(' productos',''))
    if (number%24) == 0:
        total_pages = (number//24)
    else:
        total_pages = (number//24)+1
    return total_pages

print(find_total_pages(driver))

# Once we have identified the total amount of pages we can loop over the different pages
# until we have scrapped all the elements

#%%

from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
#from bs4 import BeautifulSoup
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium
import csv
import time
import os 
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

def find_total_pages(browser):
    total_products = browser.find_element(By.XPATH, '//span[@class="plp-food-view__count"]').text
    number = int(total_products.replace('Mostrando ','').replace(' productos',''))
    if (number%24) == 0:
        total_pages = (number//24)
    else:
        total_pages = (number//24)+1
    return total_pages

def scroll(browser, pixels):
    # introduce a browser and the amount of pixels you would like to scroll at each iteration!
    height = int(browser.execute_script("return document.documentElement.scrollHeight"))
    it = 0
    while ((it+1)*pixels) < height: 
        browser.execute_script(f"window.scrollBy({it*pixels},{(it+1)*pixels});")
        time.sleep(0.4)
        it = it+1
    if ((it+1)*pixels) > height:
        browser.execute_script(f"window.scrollBy({it*pixels},{height});")
    return


def scrappe_the_page():

    # first initiallize the browser:

    options = Options()
    options.headless = False
    options.set_preference("network.cookie.cookieBehavior", 2)
    driver = webdriver.Firefox( options=options)

    # Then open the url of interest

    url = r"https://www.carrefour.es/supermercado/la-despensa/lacteos/cat20011/c"
    driver.get(url)

    # Now identify the total amount of pages:

    total_pages = find_total_pages(driver)

    # Initialize current page
    current_page = 0

    while current_page < total_pages+1:

        # Scroll
        scroll(driver,400)

        # scrape all the page
        name_products =  driver.find_elements(By.XPATH, '//a[@class="product-card__title-link track-click"]')
        price_products =  driver.find_elements(By.XPATH, '//span[@class="product-card__price"]')

        for i in range(len(price_products)):

            name = name_products[i].text
            price = price_products[i].text
            url = name_products[i].get_attribute('href')

            print(name,price,url)

        # Now go to the next page
            
        nextpage =driver.find_element(By.XPATH, '//div[@class="pagination__row"]')
        nextpage.find_element(By.TAG_NAME,'a').click()

        current_page +=1
        print(current_page)

scrappe_the_page()  




# Loop over all the pages and store the elements in a dictionary. 
# store it! 
# %%

#Lets see now how to store the elements

def get_products(driver):

     # scrape all the page
    name_products =  driver.find_elements(By.XPATH, '//a[@class="product-card__title-link track-click"]')
    price_products =  driver.find_elements(By.XPATH, '//span[@class="product-card__price"]')

    products = []

    for i in range(len(price_products)):

        name = name_products[i].text
        price = price_products[i].text
        url = name_products[i].get_attribute('href')

        print(name,price,url)

        products.append(save_products(name,price,url))

    return products

    

def save_products(name,price,url):
    title = item.text
    url = item.get_attribute('href')
    price = price.get_attribute('app_price').replace(' €','').replace(',','.')
    products = {
        'title':name,
        'price':price,
        'url':url,
    }
    return products


def scrappe_the_page():

    # first initiallize the browser:

    options = Options()
    options.headless = False
    options.set_preference("network.cookie.cookieBehavior", 2)
    driver = webdriver.Firefox( options=options)

    # Then open the url of interest

    url = r"https://www.carrefour.es/supermercado/la-despensa/lacteos/cat20011/c"
    driver.get(url)

    # Now identify the total amount of pages:

    total_pages = find_total_pages(driver)

    # Initialize current page
    current_page = 0

    final_products = []

    while current_page < total_pages+1:

        # Scroll
        scroll(driver,400)

        products = get_products(driver)

        final_products.extend(products)

        # Now go to the next page
            
        nextpage =driver.find_element(By.XPATH, '//div[@class="pagination__row"]')
        nextpage.find_element(By.TAG_NAME,'a').click()

        current_page +=1
        print(current_page)
    
    return final_products

print(scrappe_the_page())