
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import csv
import time

#TESTING LINK
#https://www.youtube.com/c/LinusTechTips/videos
#https://www.youtube.com/c/JomaOppa/videos
#https://www.youtube.com/c/baldandbankrupt/videos


df = pd.read_csv('settings.csv')
chromedriver_dir = df['chromedriver_dir']
results_file_dir = df['results_file_dir']
print(chromedriver_dir[0])

#Formating Time 
now = datetime.now()
dt_string = str(now.strftime("%d/%m/%Y %H:%M:%S"))
f_dt_string = dt_string.replace('/','-')
ff_dt_string = f_dt_string.replace(':','-')

#Scrolling javascript executable code.
javascript_2 = "window.scrollBy(0, 100);"

chromedriver = chromedriver_dir[0]
driver = webdriver.Chrome(chromedriver)
wait = WebDriverWait(driver,0.5)

url = input('Please enter a URL: ')
driver.get(url)



channel_name = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="channel-name"]'))).text

if channel_name != "":
    print(channel_name)
else:
    print('Channel Name Not Found.')
    pass

#Creating the CSV File
csv_file = open('{}\{}.csv'.format(results_file_dir[0],channel_name+" "+ff_dt_string),'w', encoding='utf-8', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Channel Name', 'Video URL', 'Views', 'Likes', 'Dislikes', 'Title','# Of Title Chars', '# Of Description Chars'])

url_list =[]
counter = 1
vid = None


while True:
    try:
        #vid = driver.find_element_by_xpath('//*[@id="items"]/ytd-grid-video-renderer[{}]'.format(counter))
        vid = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="items"]/ytd-grid-video-renderer[{}]'.format(counter))))
        url_vid = vid.find_element_by_css_selector('#video-title')
        url = url_vid.get_attribute('href')
        print(url)
        url_list.append(str(url))
        counter+=1
        driver.execute_script(javascript_2)
        
    except:
        print('done')
        print(url_list)
        break

for url in url_list:
    driver.get(url)
    time.sleep(1)
    v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text

    v_description =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#description yt-formatted-string"))).text
    v_view = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count span"))).text
    #v_date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string")))
    v_likes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(1)"))).text
    v_dislikes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(2)"))).text
    print(v_title)
    print(len(v_title))
    print(len(v_description))
    print(v_view, v_likes, v_dislikes)
    csv_writer.writerow([channel_name, driver.current_url , v_view, v_likes, v_dislikes, v_title, len(v_title), len(v_description)])
     
