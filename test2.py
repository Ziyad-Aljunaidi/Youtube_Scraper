from urllib.request import urlretrieve
from PIL import Image
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import datetime
import imageio

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

#url = input('Please enter a URL: ')
##driver.get(url)
#url_list =[]
#
#def collect_vids_urls(chnl_url):
#
#    counter = 1
#    driver.get(chnl_url)
#
#    while True:
#        try:
#            #vid = driver.find_element_by_xpath('//*[@id="items"]/ytd-grid-video-renderer[{}]'.format(counter))
#            vid = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="items"]/ytd-grid-video-renderer[{}]'.format(counter))))
#            url_vid = vid.find_element_by_css_selector('#video-title')
#            url = url_vid.get_attribute('href')
#            print(url)
#            url_list.append(str(url))
#            counter+=1
#            driver.execute_script(javascript_2)
#            
#        except:
#            print('done')
#            print(url_list)
#            break
#        time.sleep(0.1)
#
#    return url_list
#
#
#def collect_vid_data(vids_url_list):
#
#    
#    #Creating the CSV File
#    csv_file = open('{}\{}.csv'.format(results_file_dir[0],channel_name+" "+ff_dt_string),'w', encoding='utf-8', newline='')
#    csv_writer = csv.writer(csv_file)
#    csv_writer.writerow(['Channel Name', 'Video URL',"Video ID", 'Views', 'Likes', 'Dislikes', 'Title','# Of Title Chars', '# Of Description Chars'])
#
#    if channel_name != "":
#        print(channel_name)
#    else:
#        print('Channel Name Not Found.')
#        pass
#
#    
#    for url in vids_url_list:
#        #url = 'http://foo.appspot.com/abc?def=ghi'
#        parsed = urlparse.urlparse(url)
#        video_id = parse_qs(parsed.query)['v']
#        print(video_id[0])
#        driver.get(url)
#        time.sleep(1)
#        v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
#        v_description =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#description yt-formatted-string"))).text
#        v_view = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count span"))).text
#        #v_date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string")))
#        v_likes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(1)"))).text
#        v_dislikes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(2)"))).text
#        print(v_title)
#        print(len(v_title))
#        print(len(v_description))
#        print(v_view, v_likes, v_dislikes)
#        csv_writer.writerow([channel_name, driver.current_url ,video_id[0], v_view, v_likes, v_dislikes, v_title, len(v_title), len(v_description)])

#def get_thumbnail():
#    img_counter = 1
#    df_read = pd.read_csv('Results_CSVs/Joma Tech 08-01-2021 19-28-38.csv')
#    vids_id = df_read['Video ID']
#    
#    for vid_id in vids_id:
#        img_vid_id = "VideoID{}.png".format(vid_id)
#        url =  "http://img.youtube.com/vi/" + vid_id +"/0.jpg"
#        urlretrieve(url, 'imgs/{}'.format(img_vid_id))
#        #driver.get(url)
#        #driver.save_screenshot("screenshot{}.png".format(img_counter))
#        print(img_vid_id + ' ...Downloaded!')
#        img_counter += 1
#        #time.sleep(1)

#img_path = "imgs/VideoID_wNNDPp9Hh8.png"
#def rgb_img(img_name):
#    img = Image.open(img_name)
#    img.show
#    colors = img.getpixel((240,180))
#    print(colors)
#
#rgb_img(img_path)

#image = Image.open("imgs/VideoID0oBi8OmjLIg.png")
#w, h = image.size
#cropped = image.crop((0, 45, w, h - 45))
#cropped.save('cropped.jpg')
pic = imageio.imread('imgs/VideoID0oBi8OmjLIg.png')
 #   gray = lambda rgb: np.dot(rgb[..., :3], [0.299, 0.587, 0.114])
 #   gray = gray(pic)
max_rbg = pic.max()
min_rbg = pic.min()
r = pic[100, 50, 0]
g = pic[100, 50, 1]
b = pic[100, 50, 2]

print(max_rbg)
print(min_rbg)
print(r)
print(b)
print(g)

#collect_vids_urls(url)
#channel_name = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="channel-name"]'))).text
#collect_vid_data(url_list)

#get_thumbnail()