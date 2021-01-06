
from selenium import webdriver 
import pandas as pd 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import time

javascript_2 = "window.scrollTo(0, 150);"

chromedriver = 'D:\Work\iamsick_scraper_selenium\chromedriver'
driver = webdriver.Chrome(chromedriver)
wait = WebDriverWait(driver,10)

url = input('Please enter a URL: ')
driver.get(url)

for info in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"div#meta yt-formatted-string"))):
    if info.text != "":
        print(info.text)

try:
    channel_verified = driver.find_element_by_xpath('//*[@id="channel-name"]/ytd-badge-supported-renderer/div')
    print('verified')
except:
    print('not verified')

video_links = driver.find_elements_by_xpath('//*[@id="video-title"]')

links = []

for i in video_links:
    links.append(i.get_attribute('href'))

#print(links)

wait = WebDriverWait(driver,10)

for x in links:
    driver.get(x)
    time.sleep(5)
    v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string")))
    v_description =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#description yt-formatted-string")))
    v_view = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count span")))
    v_date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string")))
    v_likes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(1)")))
    v_dislikes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(2)")))
    print(v_title.text)
    print(v_description.text)
    print(v_view.text, v_date.text, v_likes.text, v_dislikes.text)
    time.sleep(1)
     
