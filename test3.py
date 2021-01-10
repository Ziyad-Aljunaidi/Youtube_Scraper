from urllib.request import urlretrieve
from PIL import Image
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import datetime
from os import listdir
import imageio
import pandas as pd
import csv
import time
import os
import shutil
import sys
os.system('cls')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#TESTING LINK
#https://www.youtube.com/c/LinusTechTips/videos
#https://www.youtube.com/c/JomaOppa/videos
#https://www.youtube.com/c/baldandbankrupt/videos
#https://www.youtube.com/user/TheVickshow/videos
#https://www.youtube.com/channel/UCBKCz2XLWQgDmHHfJuyoi4Q/videos

df = pd.read_csv('settings.csv')
chromedriver_dir = df['chromedriver_dir']
results_file_dir = df['results_file_dir']
imgs_file = df['imgs_file']

#print(chromedriver_dir[0])

#Formating Time 
now = datetime.now()
dt_string = str(now.strftime("%d/%m/%Y %H:%M:%S"))
f_dt_string = dt_string.replace('/','-')
ff_dt_string = f_dt_string.replace(':','-')

#Scrolling javascript executable code.
javascript_2 = "window.scrollBy(0, 70);"

chromedriver = chromedriver_dir[0]
driver = webdriver.Chrome(chromedriver)
wait = WebDriverWait(driver,0.5)
url = input('Please enter a URL: ')
driver.get(url)
url_list =[]

def collect_vids_urls(chnl_url):

    counter = 1
    driver.get(chnl_url)

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
        time.sleep(0.1)

    return url_list


def collect_vid_data(vids_url_list):


    
    #Creating the CSV File
    csv_file = open('{}\{}.csv'.format(results_file_dir[0],channel_name+" "+ff_dt_string),'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Channel Name', 'Video URL',"Video ID", 'Views', 'Likes', 'Dislikes', 'Title','# Of Title Chars', '# Of Description Chars'])

    if channel_name != "":
        print(channel_name)
    else:
        print('Channel Name Not Found.')
        pass

    
    for url in vids_url_list:
        parsed = urlparse.urlparse(url)
        video_id = parse_qs(parsed.query)['v']
        print(video_id[0])
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
        csv_writer.writerow([channel_name, driver.current_url ,video_id[0], v_view, v_likes, v_dislikes, v_title, len(v_title), len(v_description)])
        
count = 0
#Getting the thumbnail image and save it for RGB breakdown.
def get_thumbnail(counter):
    
    df_read = pd.read_csv('{}\{}.csv'.format(results_file_dir[0],channel_name+" "+ff_dt_string))

    csv_file = open('{}.csv'.format(channel_name+" "+final),'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Channel Name', 'Video URL',"Video ID", 'Views', 'Likes', 'Dislikes', 'Title','# Of Title Chars', '# Of Description Chars', 'Max RGB', 'Min RGB', 'R', 'G', 'B'])
    
    chnl_name = df_read['Channel Name']
    vid_url = df_read['Video URL']
    vids_id = df_read['Video ID']
    views = df_read['Views']
    likes= df_read['Likes']
    dislikes = df_read['Dislikes']
    title = df_read['Title']
    title_chars = df_read['# Of Title Chars']
    des_chars = df_read['# Of Description Chars']
    
    for vid_id in vids_id:
        img_vid_id = "VideoID{}.png".format(vid_id)
        url =  "http://img.youtube.com/vi/" + vid_id +"/0.jpg"
        urlretrieve(url, 'imgs/{}'.format(img_vid_id))
        print(img_vid_id + ' ...Downloaded!')

        pic = imageio.imread('imgs/{}'.format(img_vid_id))
        max_rgb = pic.max()
        min_rgb = pic.min()
        r = pic[100, 50, 0]
        g = pic[100, 50, 1]
        b = pic[100, 50, 2]
        
        #print(max_rgb)
        #print(min_rgb)
        #print(r)
        #print(b)
        #print(g)
        print(counter)
        #df["Max RGB"] = max_rbg
        #df["Min RGB"] = min_rbg
        #df["R"] = r
        #df["G"] = g
        #df["B"] = b

        csv_writer.writerow([ chnl_name[counter], vid_url[counter], vids_id[counter], views[counter], likes[counter], dislikes[counter], title[counter], title_chars[counter], des_chars[counter], max_rgb, min_rgb, r, g, b])
        counter += 1

collect_vids_urls(url)
channel_name = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="channel-name"]'))).text
collect_vid_data(url_list)
get_thumbnail(count)