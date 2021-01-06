
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



x = 'https://www.youtube.com/watch?v=B-qXzZGJNJ4'
driver.get(x)
time.sleep(5)
v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string")))
v_view = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count span")))
v_date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string")))
v_likes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(1)")))
v_dislikes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(2)")))
print(v_title.text)
print(v_view.text, v_date.text, v_likes.text, v_dislikes.text)
time.sleep(1)
 
buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'yt-icon-button#button button')))
buttons_list = []
for button in buttons:
    buttons_list.append(button)
buttons_list[9].click()
time.sleep(1)  

transcript = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#items > ytd-menu-service-item-renderer:nth-child(2)')))
transcript.click()
transcript_script = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#body > ytd-transcript-body-renderer > div.cue-group.style-scope.ytd-transcript-body-renderer.active')))
time.sleep(1)
for script in transcript_script:
     time_frame = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#body > ytd-transcript-body-renderer')))
     print(time_frame.text)

print('haha')
time.sleep(1)