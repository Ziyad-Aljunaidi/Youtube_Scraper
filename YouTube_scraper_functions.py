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

#TESTING LINKS
#https://www.youtube.com/c/LinusTechTips/videos
#https://www.youtube.com/c/JomaOppa/videos
#https://www.youtube.com/c/baldandbankrupt/videos
#https://www.youtube.com/user/TheVickshow/videos
#https://www.youtube.com/channel/UCBKCz2XLWQgDmHHfJuyoi4Q/videos
#

df = pd.read_csv('settings.csv')
chromedriver_dir = df['chromedriver_dir']
results_file_dir = df['results_file_dir']

#Formating Time For Naming The Folder And Its Files
now = datetime.now()
dt_string = str(now.strftime("%d/%m/%Y %H:%M:%S"))
f_dt_string = dt_string.replace('/','-')
ff_dt_string = f_dt_string.replace(':','-')

#Scrolling javascript executable code.
javascript_2 = "window.scrollBy(0, 70);"

chromedriver = chromedriver_dir[0]
driver = webdriver.Chrome(chromedriver)
wait = WebDriverWait(driver,1)


url = ''
def get_url(url):
    driver.get(url)


#channel_name = ''
#print_name()
def get_chnl_name():
    global channel_name
    channel_name = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="channel-name"]'))).text
    print('Channel Name: ', channel_name)

    #Creating a Folder
    try:
        os.mkdir('./{}'.format(channel_name + " " + ff_dt_string))
        print ('Directory, {}'.format(channel_name + " " + ff_dt_string) + ' created..')

        os.mkdir('./{}/Images'.format(channel_name + " " + ff_dt_string))
        print ('Directory, {}/Images'.format(channel_name + " " + ff_dt_string) + ' created..')

        os.mkdir('./{}/Cropped Images'.format(channel_name + " " + ff_dt_string))
        print ('Directory, {}/ Cropped Images'.format(channel_name + " " + ff_dt_string) + ' created..')
    except FileExistsError:
        print('Directory existed.')
    


def collect_vids_urls(chnl_url):
    counter = 1
    #driver.get(chnl_url)
    #Creating the CSV File
    csv_file = open('{}\{}.csv'.format(channel_name+" "+ff_dt_string,channel_name+" "+ff_dt_string),'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Channel Name', 'Video URL'])
    

    while True:
        try:
            #vid = driver.find_element_by_xpath('//*[@id="items"]/ytd-grid-video-renderer[{}]'.format(counter))
            vid = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="items"]/ytd-grid-video-renderer[{}]'.format(counter))))
            url_vid = vid.find_element_by_css_selector('#video-title')
            url = url_vid.get_attribute('href')
            print(url)
            csv_writer.writerow([channel_name , url])
            counter+=1
            driver.execute_script(javascript_2)
            
        except:
            print('done')
            break
        time.sleep(0.1)

def collect_vid_data(channel_name):

    #Creating the semi-final CSV File for saving the NEW scraped data
    csv_file = open('{}\{}.csv'.format(channel_name+" "+ff_dt_string,channel_name+" "+ff_dt_string + " SEMI-FINAL"),'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Channel Name', 'Video URL','Video ID', 'Views', 'Likes', 'Dislikes', 'Title','Title Captial Ratio','# Of Title Chars', '# Of Description Chars'])

    #reading the URLs scraped data
    data_file = pd.read_csv('{}\{}.csv'.format(channel_name+" "+ff_dt_string,channel_name+" "+ff_dt_string))
    video_url = data_file['Video URL']
    
    counter = 0
    for url in video_url:
        parsed = urlparse.urlparse(url)
        video_id = parse_qs(parsed.query)['v']
        driver.get(url)
        time.sleep(1)
        v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
        remove_spaces = v_title.replace(' ', '')
        cap_letters = 0
        for letter in remove_spaces:
            if letter.isupper():
                cap_letters += 1
            else:
                pass

        captial_ratio = cap_letters/len(remove_spaces)
        formated_captial_ratio = "{:.2f}".format(captial_ratio)
        
        v_description =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#description yt-formatted-string"))).text
        v_view = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count span"))).text
        #v_date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string")))
        v_likes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(1)"))).text
        v_dislikes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(2)"))).text
        
        #Printing the results
        print('Video URL: ', url)
        print('Video ID: ', video_id[0])
        print('Title: ', v_title )
        print('Title Captial Ratio: ',formated_captial_ratio,  ' | ' ,'# Of Chars In Title: ', len(v_title))
        print('# Of Chars In Description: ', len(v_description))
        print('Views: ', v_view, ' | ' , 'Likes: ', v_likes, ' | ', 'Disikes: ', v_dislikes)
        print('-----------------------------------')
 
        csv_writer.writerow([channel_name, url, video_id[0], v_view, v_likes, v_dislikes, v_title, formated_captial_ratio, len(v_title), len(v_description)])

        
count = 0

#Getting the thumbnail image and save it for RGB breakdown.
def get_thumbnail(counter):
    
    csv_file = open('{}\{}.csv'.format(channel_name+" "+ff_dt_string, channel_name+" "+ ff_dt_string + " FINAL"),'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Channel Name', 'Video URL',"Video ID", 'Views', 'Likes', 'Dislikes', 'Title','Title Captial Ratio','# Of Title Chars', '# Of Description Chars', 'Max RGB', 'Min RGB', 'R', 'G', 'B'])
    
    df_read = pd.read_csv('{}\{}.csv'.format(channel_name+" "+ff_dt_string,channel_name+" "+ ff_dt_string + " SEMI-FINAL"))
    chnl_name = df_read['Channel Name']
    vid_url = df_read['Video URL']
    vids_id = df_read['Video ID']
    views = df_read['Views']
    likes= df_read['Likes']
    dislikes = df_read['Dislikes']
    title = df_read['Title']
    title_captial_ratio = df_read['Title Captial Ratio']
    title_chars = df_read['# Of Title Chars']
    des_chars = df_read['# Of Description Chars']
    
    for vid_id in vids_id:
        img_vid_id = "VideoID{}.png".format(vid_id)
        url =  "http://img.youtube.com/vi/" + vid_id +"/0.jpg"
        urlretrieve(url, '{}/Images/{}'.format(channel_name+" "+ff_dt_string,img_vid_id, img_vid_id))

        print(img_vid_id + ' ...Downloaded!')
        
        image = Image.open('{}/Images/{}'.format(channel_name+" "+ff_dt_string,img_vid_id,img_vid_id))
        w, h = image.size
        cropped = image.crop((0, 45, w, h - 45))
        cropped.save('{}/Cropped Images/{}'.format(channel_name+" "+ff_dt_string,img_vid_id, img_vid_id))

        pic = imageio.imread('{}/Cropped Images/{}'.format(channel_name+" "+ff_dt_string,img_vid_id, img_vid_id))
        max_rgb = pic.max()
        min_rgb = pic.min()
        r = pic[100, 50, 0]
        g = pic[100, 50, 1]
        b = pic[100, 50, 2]
        
        print('Max RGB: ', max_rgb , 'Min RGB: ', min_rgb, 'R: ', r, 'G: ', g, 'B: ', b)
        print(counter)
        csv_writer.writerow([ chnl_name[counter], vid_url[counter], vids_id[counter], views[counter], likes[counter], dislikes[counter], title[counter], title_captial_ratio[counter], title_chars[counter], des_chars[counter], max_rgb, min_rgb, r, g, b])
        counter += 1



#Runing the Required Functions
def run_functions(url_link):
    url = input('Please enter a URL: ')
    get_url()
    driver.get(url_link)
    get_chnl_name()
    collect_vids_urls(url_link)
    collect_vid_data(channel_name)
    get_thumbnail(count)

run_functions(url)