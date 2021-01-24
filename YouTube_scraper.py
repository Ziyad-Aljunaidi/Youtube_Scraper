from distutils.core import setup # Need this to handle modules
import threading
import tkinter as tk
import numpy as np
from numpy.polynomial.polynomial import polyfit
import scipy.spatial.transform._rotation_groups
import re
import matplotlib.pyplot as plt  # To visualize
from matplotlib import pyplot
import matplotlib.ticker as tkr
from sklearn.linear_model import LinearRegression
from sklearn import datasets, linear_model
import statsmodels.api as sm
from scipy import stats
import sklearn.utils._weight_vector
from tkinter.ttk import *
from tkinter import HORIZONTAL
from urllib.request import urlretrieve
from PIL import Image
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import urllib.parse as urlparse
from urllib.parse import parse_qs
from datetime import datetime
from os import listdir
from os import system, name 
import imageio
import time
import pandas as pd
import csv
import os
from tkinter import filedialog
import statistics


class Redirect():

    def flush(self):
        pass

    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)
        self.widget.see("end")

window = tk.Tk()
window.title("Youtube Scraper")
window.iconbitmap("YouTubeScraper.ico")

OPTIONS = [
    "Views",
    "Likes",
    "Dislikes",
    "Video Length",
    "Title Capital Ratio",
    "# Of Title Chars",
    "# Of Description Chars",
    "# Of Links In Description",
    "# Of Comments",
    "R",
    "B",
    "G",
    "NONE"
    
] 

url_text = tk.StringVar(window)

variable_x1 = tk.StringVar(window)
variable_x1.set(OPTIONS[12]) # default value

variable_x2 = tk.StringVar(window)
variable_x2.set(OPTIONS[12]) # default value

variable_x3 = tk.StringVar(window)
variable_x3.set(OPTIONS[12]) # default value

variable_y = tk.StringVar(window)
variable_y.set(OPTIONS[0]) # default value

val_var = tk.IntVar()
val_var.set(1)

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

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--headless')

chromedriver = webdriver.Chrome(executable_path=chromedriver_dir[0], options=chrome_options) 



def clearTextInput():
    chnl_val.delete("1.0","end")


def get_chnl_name():
    window.update()
    global channel_name
    channel_name = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="channel-name"]'))).text
    print('Channel Name: ', channel_name)

    #Creating a Folder
    try:
        if not os.path.exists(results_file_dir[0]):
            os.makedirs(results_file_dir[0])

        os.mkdir('./{}/{}'.format(results_file_dir[0],channel_name + " " + ff_dt_string))
        print ('Directory, {}/{}'.format(results_file_dir[0],channel_name + " " + ff_dt_string) + ' created..')

        os.mkdir('./{}/{}/Images'.format(results_file_dir[0],channel_name + " " + ff_dt_string))
        print ('Directory, {}/{}/Images'.format(results_file_dir[0],channel_name + " " + ff_dt_string) + ' created..')

        os.mkdir('./{}/{}/Cropped Images'.format(results_file_dir[0],channel_name + " " + ff_dt_string))
        print ('Directory, {}/{}/ Cropped Images'.format(results_file_dir[0],channel_name + " " + ff_dt_string) + ' created..')
    except FileExistsError:
        print('Directory existed.')
    window.update()


def collect_vids_urls(chnl_url):
    window.update()
    global total_vids_counter
    total_vids_counter = 1

    #Creating the CSV File
    csv_file = open('{}\{}\{}.csv'.format(results_file_dir[0], channel_name+" "+ff_dt_string, channel_name+" "+ff_dt_string),'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Channel Name', 'Video URL' , 'Video Length'])
    while True:
        
        try:
            #vid = driver.find_element_by_xpath('//*[@id="items"]/ytd-grid-video-renderer[{}]'.format(counter))
            vid = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="items"]/ytd-grid-video-renderer[{}]'.format(total_vids_counter))))
            url_vid = vid.find_element_by_css_selector('#video-title')
            url = url_vid.get_attribute('href')

            try:
                vid_len = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer[{}]/div[1]/ytd-thumbnail/a/div[1]/ytd-thumbnail-overlay-time-status-renderer/span'.format(total_vids_counter)))).text
                vid_len_list = vid_len.split(':')
                vid_len_list.reverse()
                

                try:
                    secs = int(vid_len_list[0])
                except:
                    secs = 0

                try:
                    mins= int(vid_len_list[1])*60
                except:
                    mins = 0

                try:
                    hrs = int(vid_len_list[2])*60*60
                except:
                    hrs = 0
                    vid_length = secs+mins+hrs
            except:
                time.sleep(4)
                try:
                    vid_len = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer[{}]/div[1]/ytd-thumbnail/a/div[1]/ytd-thumbnail-overlay-time-status-renderer/span'.format(total_vids_counter)))).text
                    vid_len_list = vid_len.split(':')
                    vid_len_list.reverse()


                    try:
                        secs = int(vid_len_list[0])
                    except:
                        secs = 0

                    try:
                        mins= int(vid_len_list[1])*60
                    except:
                        mins = 0

                    try:
                        hrs = int(vid_len_list[2])*60*60
                    except:
                        hrs = 0
                        vid_length = secs+mins+hrs
                except:
                    #Probably tried to scrape a live stream
                    vid_length = 0

            try:
                if video_recent_link[0] == url:
                    print('Scraping NEW Videos URLs Completed')
                    break
                else:
                    pass
            except:
                pass

            print(url, ' ', total_vids_counter)
            print('Video Length: ', vid_length)
            csv_writer.writerow([channel_name , url, vid_length])
            total_vids_counter+=1
            driver.execute_script(javascript_2)
            
            window.update()
            
        except:
            print()
            print('Scraping Videos URL Completed!')
            
            total_vids_counter-=1
            break
        #time.sleep(0.1)

def collect_vid_data(channel_name):
    window.update()
    #Creating the semi-final CSV File for saving the NEW scraped data
    csv_file = open('{}\{}\{}.csv'.format(results_file_dir[0], channel_name+" "+ff_dt_string,channel_name+" "+ff_dt_string + " SEMI-FINAL"),'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Channel Name', 'Video URL','Video ID', 'Video Length', 'Views', 'Likes', 'Dislikes', 'Title','Title Capital Ratio','# Of Title Chars', '# Of Description Chars', '# Of Links In Description', '# Of Comments'])

    #reading the URLs scraped data
    data_file = pd.read_csv('{}\{}\{}.csv'.format(results_file_dir[0], channel_name+" "+ff_dt_string,channel_name+" "+ff_dt_string))
    video_url = data_file['Video URL']
    video_len = data_file['Video Length']
    
    counter = 1
    counter_vid_len = 0
    for url in video_url:
        window.update()
        parsed = urlparse.urlparse(url)
        video_id = parse_qs(parsed.query)['v']
        driver.get(url)
        v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#container > h1 > yt-formatted-string"))).text
        #v_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"h1.title yt-formatted-string"))).text
        remove_spaces = v_title.replace(' ', '')
        cap_letters = 0

        for letter in remove_spaces:
            if letter.isupper():
                cap_letters += 1
            else:
                pass
        try:

            captial_ratio = cap_letters/len(remove_spaces)
            formated_captial_ratio = "{:.2f}".format(captial_ratio)
        except:
            formated_captial_ratio='0'
            print(cap_letters, ' ', len(remove_spaces))

        v_description =''


        try:
            more_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#more")))
            more_btn.click()

            v_des = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#description')))

            for v in v_des:
                v.text
                v_description+=v.text

            less_btn =  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#less')))
            less_btn.click()
        except:
            v_description = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#description > yt-formatted-string'))).text
            pass

        try:
            #regualr expression to extract links from the description
            links_in_des = re.findall('http[s]?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', v_description) 
        except:
            pass

        v_view = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#count span"))).text
        v_view_list = v_view.split()
        v_view = v_view_list[0].replace(',', '')
        #v_date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string")))
        v_likes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(1)"))).text
        v_likes = v_likes.replace('.','')
        v_likes = v_likes.replace('K', '000')
        v_likes = v_likes.replace('M', '000000')

        v_dislikes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(2)"))).text
        v_dislikes = v_dislikes.replace('.','')
        v_dislikes = v_dislikes.replace('K', '000')
        v_dislikes = v_dislikes.replace('M', '000000')

        #driver.execute_script("window.scrollBy(0, 2200);")
        #print('testing comments appearance')

        try:
            driver.execute_script("window.scrollBy(0, 2200);")
            v_comments= wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#count > yt-formatted-string'))).text
            v_comments = v_comments.replace(' Comments','')
            v_comments = v_comments.replace(',', '')
        except:
            time.sleep(1)
            try:
                driver.execute_script("window.scrollBy(0, 2200);")
                v_comments= wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#count > yt-formatted-string'))).text
                v_comments = v_comments.replace(' Comments','') 
                v_comments = v_comments.replace(',', '')
            except:
                print('Cannot get # of Comments.')
                comments = 0


        #Printing the results
        print()
        print('Video URL: ', url)
        print('Video ID: ', video_id[0])
        print('Title: ', v_title )
        print('Title Captial Ratio: ',formated_captial_ratio,  ' | ' ,'# Of Chars In Title: ', len(v_title))
        print('# Of Chars In Description: ', len(v_description))
        print('# of links in Description: ', len(links_in_des))
        print('Views: ', v_view, ' | ' , 'Likes: ', v_likes, ' | ', 'Disikes: ', v_dislikes )
        print('# of Comments: ', v_comments)
        print('Video Length: ', video_len[counter_vid_len])
        print( counter , " of " , total_vids_counter , " scraped.")
        print('==============================================================================')
        
        csv_writer.writerow([channel_name, url, video_id[0], video_len[counter_vid_len], v_view, v_likes, v_dislikes, v_title, formated_captial_ratio, len(v_title), len(v_description), len(links_in_des), v_comments])
        counter += 1
        counter_vid_len +=1


count = 0
#Getting the thumbnail image and save it for RGB breakdown.
def get_thumbnail(counter): 
    global file_name2
    file_name2 = '{}\{}\{}.csv'.format(results_file_dir[0], channel_name+" "+ff_dt_string, channel_name+" "+ ff_dt_string + " FINAL")
    csv_file = open('{}\{}\{}.csv'.format(results_file_dir[0],channel_name+" "+ff_dt_string, channel_name+" "+ ff_dt_string + " FINAL"),'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Channel Name', 'Video URL',"Video ID", 'Video Length', 'Views', 'Likes', 'Dislikes', 'Title','Title Capital Ratio','# Of Title Chars', '# Of Description Chars', '# Of Links In Description', '# Of Comments', 'Max RGB', 'Min RGB', 'R', 'G', 'B'])
    
    df_read = pd.read_csv('{}\{}\{}.csv'.format(results_file_dir[0], channel_name+" "+ff_dt_string,channel_name+" "+ ff_dt_string + " SEMI-FINAL"))
    chnl_name = df_read['Channel Name']
    vid_url = df_read['Video URL']
    vids_id = df_read['Video ID']
    vid_length = df_read['Video Length']
    views = df_read['Views']
    likes= df_read['Likes']
    dislikes = df_read['Dislikes']
    title = df_read['Title']
    title_captial_ratio = df_read['Title Capital Ratio']
    title_chars = df_read['# Of Title Chars']
    des_chars = df_read['# Of Description Chars']
    des_links = df_read['# Of Links In Description']
    comments = df_read['# Of Comments']
    
    for vid_id in vids_id:
        try:
            window.update()
            img_vid_id = "VideoID{}.png".format(vid_id)
            url =  "http://img.youtube.com/vi/" + vid_id +"/0.jpg"
            urlretrieve(url, '{}/{}/Images/{}'.format(results_file_dir[0],channel_name+" "+ff_dt_string,img_vid_id, img_vid_id))

            print(img_vid_id + ' ...Downloaded!')

            image = Image.open('{}/{}/Images/{}'.format(results_file_dir[0],channel_name+" "+ff_dt_string,img_vid_id,img_vid_id))
            w, h = image.size
            cropped = image.crop((0, 45, w, h - 45))
            cropped.save('{}/{}/Cropped Images/{}'.format(results_file_dir[0],channel_name+" "+ff_dt_string,img_vid_id, img_vid_id))

            pic = imageio.imread('{}/{}/Cropped Images/{}'.format(results_file_dir[0],channel_name+" "+ff_dt_string,img_vid_id, img_vid_id))
            max_rgb = pic.max()
            min_rgb = pic.min()
            r = pic[100, 50, 0]
            g = pic[100, 50, 1]
            b = pic[100, 50, 2]
            img_counter = counter + 1        
            print('Max RGB: ', max_rgb , 'Min RGB: ', min_rgb, 'R: ', r, 'G: ', g, 'B: ', b)
            print(img_counter, ' of ', total_vids_counter)
            csv_writer.writerow([ chnl_name[counter], vid_url[counter], vids_id[counter], vid_length[counter], views[counter], likes[counter], dislikes[counter], title[counter], title_captial_ratio[counter], title_chars[counter], des_chars[counter], des_links[counter], comments[counter], max_rgb, min_rgb, r, g, b])
            counter += 1
        except:
            max_rgb = pic.max()
            min_rgb = pic.min()
            r = 0
            g = 0
            b = 0
            img_counter = counter + 1 
            print('Max RGB: ', max_rgb , 'Min RGB: ', min_rgb, 'R: ', r, 'G: ', g, 'B: ', b)
            print(img_counter, ' of ', total_vids_counter)
            csv_writer.writerow([ chnl_name[counter], vid_url[counter], vids_id[counter], vid_length[counter], views[counter], likes[counter], dislikes[counter], title[counter], title_captial_ratio[counter], title_chars[counter], des_chars[counter], des_links[counter], comments[counter], max_rgb, min_rgb, r, g, b])
            counter += 1
            pass

    os.remove('{}\{}\{}.csv'.format(results_file_dir[0],channel_name+" "+ff_dt_string, channel_name+" "+ ff_dt_string ))
    os.remove('{}\{}\{}.csv'.format(results_file_dir[0],channel_name+" "+ff_dt_string, channel_name+" "+ ff_dt_string + " SEMI-FINAL"))

#Option for X1
def optx1(value):
    global x1_val
    global x1_val_name

    if value == "Views":
        print("X1 = Views")
        x1_val = 4
        x1_val_name = "Views"

    elif value == "Likes":
        print("X1 = Likes")
        x1_val = 5
        x1_val_name = "Likes"

    elif value == "Dislikes":
        print("X1 = Dislikes")
        x1_val = 6
        x1_val_name = "Dislikes"

    elif value == "Video Length":
        print("X1 = Video Length")
        x1_val = 3
        x1_val_name = "Video Length"

    elif value == "Title Capital Ratio":
        print("X1 = Title Capital Ratio")
        x1_val = 8
        x1_val_name = "Title Capital Ratio"

    elif value == "# Of Title Chars":
        print("X1 = # Of Title Chars")
        x1_val = 9
        x1_val_name = "# Of Title Chars"

    elif value == "# Of Description Chars":
        print("X1 = # Of Description Chars")
        x1_val = 10
        x1_val_name = "# Of Description Chars"

    elif value == "# Of Links In Description":
        print("X1 = # Of Links In Description")
        x1_val = 11
        x1_val_name = "# Of Links In Description"

    elif value == "# Of Comments":
        print("X1 = # Of Comments")
        x1_val = 12
        x1_val_name = "# Of Comments"

    elif value == "R":
        print("X1 = R")
        x1_val = 15
        x1_val_name = "R"

    elif value == "B":
        print("X1 = B")
        x1_val = 16
        x1_val_name = "B"

    elif value == "G":
        print("X1 = G")
        x1_val = 17
        x1_val_name = "G"
    else:
        print("X1 = NONE")
        x1_val=None
        pass
    
#Option for X2
def optx2(value):
    global x2_val
    global x2_val_name
    if multi_var["state"] == "disabled":
        multi_var["state"] ="normal"
        uni_var["state"] = "normal"
    else:
        pass

    if value == "Views":
        print("X2 = Views")
        x2_val = 4
        x2_val_name = "Views"

    elif value == "Likes":
        print("X2 = Likes")
        x2_val = 5
        x2_val_name = "Likes"

    elif value == "Dislikes":
        print("X2 = Dislikes")
        x2_val = 6
        x2_val_name = "Dislikes"

    elif value == "Video Length":
        print("X2 = Video Length")
        x2_val = 3
        x2_val_name = "Video Length"

    elif value == "Title Capital Ratio":
        print("X2 = Title Capital Ratio")
        x2_val = 8
        x2_val_name = "Title Capital Ratio"

    elif value == "# Of Title Chars":
        print("X2 = # Of Title Chars")
        x2_val = 9
        x2_val_name = "# Of Title Chars"

    elif value == "# Of Description Chars":
        print("X2 = # Of Description Chars")
        x2_val = 10
        x2_val_name = "# Of Description Chars"

    elif value == "# Of Links In Description":
        print("X2 = # Of Links In Description")
        x2_val = 11
        x2_val_name = "# Of Links In Description"

    elif value == "# Of Comments":
        print("X2 = # Of Comments")
        x2_val = 12
        x2_val_name = "# Of Comments"

    elif value == "R":
        print("X2 = R")
        x2_val = 15
        x2_val_name = "R"

    elif value == "B":
        print("X2 = B")
        x2_val = 16
        x2_val_name = "B"

    elif value == "G":
        print("X2 = G")
        x2_val = 17
        x2_val_name = "G"
    else:
        print("X2 = NONE")
        x2_val=None
        pass

#Option for X3
def optx3(value):
    global x3_val
    global x3_val_name
    if multi_var["state"] == "disabled":
        multi_var["state"] ="normal"
        uni_var["state"] = "normal"
    else:
        pass

    if value == "Views":
        print("X3 = Views")
        x3_val = 4
        x3_val_name = "Views"

    elif value == "Likes":
        print("X3 = Likes")
        x3_val = 5
        x3_val_name = "Likes"

    elif value == "Dislikes":
        print("X3 = Dislikes")
        x3_val = 6
        x3_val_name = "Dislikes"

    elif value == "Video Length":
        print("X3 = Video Length")
        x3_val = 3
        x3_val_name = "Video Length"

    elif value == "Title Capital Ratio":
        print("X3 = Title Capital Ratio")
        x3_val = 8
        x3_val_name = "Title Capital Ratio"

    elif value == "# Of Title Chars":
        print("X3 = # Of Title Chars")
        x3_val = 9
        x3_val_name = "# Of Title Chars"

    elif value == "# Of Description Chars":
        print("X3 = # Of Description Chars")
        x3_val = 10
        x3_val_name = "# Of Description Chars"

    elif value == "# Of Links In Description":
        print("X3 = # Of Links In Description")
        x3_val = 11
        x3_val_name = "# Of Links In Description"

    elif value == "# Of Comments":
        print("X3 = # Of Comments")
        x3_val = 12
        x3_val_name = "# Of Comments"

    elif value == "R":
        print("X3 = R")
        x3_val = 15
        x3_val_name = "R"

    elif value == "B":
        print("X3 = B")
        x3_val = 16
        x3_val_name = "B"

    elif value == "G":
        print("X3 = G")
        x3_val = 17
        x3_val_name = "G"
    else:
        print("X3 = NONE")
        x3_val = None
        pass

#Option for Y
y_val = 4 #DEFAULT for VIEWS
y_val_name = "Views" #DEFAULT for VIEWS

def opty(value):
    global y_val
    global y_val_name
    
    
    if value == "Views":
        print("Y = Views")
        y_val = 4
        y_val_name = "Views"

    elif value == "Likes":
        print("Y = Likes")
        y_val = 5
        y_val_name = "Likes"

    elif value == "Dislikes":
        print("Y = Dislikes")
        y_val = 6
        y_val_name = "Dislikes"

    elif value == "Video Length":
        print("Y = Video Length")
        y_val = 3
        y_val_name = "Video Length"

    elif value == "Title Capital Ratio":
        print("Y = Title Capital Ratio")
        y_val = 8
        y_val_name = "Title Capital Ratio"  

    elif value == "# Of Title Chars":
        print("Y = # Of Title Chars")
        y_val = 9
        y_val_name = "# Of Title Chars"

    elif value == "# Of Description Chars":
        print("Y = # Of Description Chars")
        y_val = 10
        y_val_name = "# Of Description Chars"

    elif value == "# Of Links In Description":
        print("Y = # Of Links In Description")
        y_val = 11
        y_val_name = "# Of Links In Description"

    elif value == "# Of Comments":
        print("Y = # Of Comments")
        y_val = 12
        y_val_name = "# Of Comments"

    elif value == "R":
        print("Y = R")
        y_val = 15
        y_val_name = "R"

    elif value == "B":
        print("Y = B")
        y_val = 16
        y_val_name = "B"

    elif value == "G":
        print("Y = G")
        y_val = 17
        y_val_name = "G"    
    else:
        y_val == None
        print("Y = NONE")
        pass


def opts():

    
    try:
        data = pd.read_csv(file_name)  # load data set
    except:
        data = pd.read_csv(file_name2)


    def func(x, pos):  # formatter function takes tick label and tick position
        s = '{:0,d}'.format(int(x))
        return s

    def reg_info(x, y):
       X2 = sm.add_constant(X1)
       est = sm.OLS(y, X2)
       est2 = est.fit()
       return est2.summary()
    
    try:
        try:
        

            X1 = data.iloc[:, x1_val].values.reshape(-1, 1)  # values converts it into a numpy array
            X2 = data.iloc[:, x2_val].values.reshape(-1,1)
            X3 = data.iloc[:, x3_val].values.reshape(-1,1)
            Y = data.iloc[:, y_val].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
            linear_regressor = LinearRegression()  # create object for the class

            clearTextInput()


            
            

            try:  
                col_data = data[x1_val_name]
                print('\n\n')
                print('==============================================================================')
                print('                                     X1                                       ')
                print('==============================================================================')
                print('X1 Mean: ',statistics.mean(col_data))
                print('X1 Median: ',statistics.median(col_data))
                print('X1 Mode: ',statistics.mode(col_data))
                print('==============================================================================')
                print(reg_info(X1,Y))
            except:
                print('==============================================================================')
                print('                     Cannot get Regression Results For X1                     ')
                print('==============================================================================')
                pass

            try:
                col_data2 = data[x2_val_name]
                print('\n')              
                print('==============================================================================')
                print('                                     X2                                       ')
                print('==============================================================================')
                print('X2 Mean: ',statistics.mean(col_data2))
                print('X2 Median: ',statistics.median(col_data2))
                print('X2 Mode: ',statistics.mode(col_data2))
                print('==============================================================================')
                print(reg_info(X2,Y))  
            except:
                print('==============================================================================')
                print('                     Cannot get Regression Results For X2                     ')
                print('==============================================================================')
                pass

            try:
                col_data3 = data[x3_val_name]
                print('\n')
                print('==============================================================================')
                print('                                     X3                                       ')
                print('==============================================================================')
                print('X3 Mean: ',statistics.mean(col_data3))
                print('X3 Median: ',statistics.median(col_data3))
                print('X3 Mode: ',statistics.mode(col_data3))
                print('==============================================================================')
                print(reg_info(X3,Y)) 
            except:
                print('==============================================================================')
                print('                     Cannot get Regression Results For X3                     ')
                print('==============================================================================')
                pass

            if val_var.get() == 1:
                linear_regressor.fit(X1, Y)  # perform linear regression
                X1_pred = linear_regressor.predict(X1) # make predictions
                plt.scatter(X1, Y, label=x1_val_name)
                
                linear_regressor.fit(X2, Y)
                X2_pred = linear_regressor.predict(X2)
                plt.scatter(X2, Y, label=x2_val_name)
                
                linear_regressor.fit(X3, Y)
                X3_pred = linear_regressor.predict(X3)
                plt.scatter(X3, Y, label=x3_val_name)
                
                plt.legend(loc='upper right')
                plt.ticklabel_format(style='plain', axis='y')
                plt.ticklabel_format(style='plain', axis='x')
                plt.ylabel(y_val_name)


                y_format = tkr.FuncFormatter(func)
                x_format = tkr.FuncFormatter(func)  # make formatter

                ax = plt.subplot(111)
                ax.plot(X1, X1_pred)
                ax.plot(X2, X2_pred)
                ax.plot(X3,X3_pred)
                ax.yaxis.set_major_formatter(y_format)
                ax.xaxis.set_major_formatter(x_format)   # set formatter to needed axis
                fig = plt.gcf() 
                fig.set_size_inches(11,8)
                plt.show()

                print('multivariate')


            else:

                xt = (X1 + X2 + X3)/3
                linear_regressor.fit(xt, Y)  # perform linear regression
                Y_pred = linear_regressor.predict(xt)  # make predictions
                X2_pred = linear_regressor.predict(X2)
                X3_pred = linear_regressor.predict(X3)
                plt.scatter(X1, Y, label=x1_val_name)
                plt.scatter(X2, Y, label=x2_val_name)
                plt.scatter(X3, Y,  label=x3_val_name)
                plt.ylabel(y_val_name)

                plt.legend(loc='upper right')
                plt.ticklabel_format(style='plain', axis='y')
                plt.ticklabel_format(style='plain', axis='x')

                y_format = tkr.FuncFormatter(func)
                x_format = tkr.FuncFormatter(func)  # make formatter

                ax = plt.subplot(111)
                ax.plot(xt,Y_pred, color='red')
                ax.yaxis.set_major_formatter(y_format)
                ax.xaxis.set_major_formatter(x_format)   # set formatter to needed axis
                fig = plt.gcf() 
                fig.set_size_inches(11,8)
                plt.show()
                print('univariate')

        except:
            try:
                clearTextInput()
                X1 = data.iloc[:, x1_val].values.reshape(-1, 1)  # values converts it into a numpy array
                X2 = data.iloc[:, x2_val].values.reshape(-1,1)
                Y = data.iloc[:, y_val].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
                linear_regressor = LinearRegression()  # create object for the class
                
                
                col_data2 = data[x2_val_name]
                try:
                    col_data = data[x1_val_name]
                    print('\n\n')
                    print('==============================================================================')
                    print('                                     X1                                       ')
                    print('==============================================================================')
                    print('X1 Mean: ',statistics.mean(col_data))
                    print('X1 Median: ',statistics.median(col_data))
                    print('X1 Mode: ',statistics.mode(col_data))
                    print('==============================================================================')
                    print(reg_info(X1,Y))
                except:
                    print('==============================================================================')
                    print('                     Cannot get Regression Results For X1                     ')
                    print('==============================================================================')
                    pass  

                try:
                    col_data2 = data[x2_val_name]
                    print('\n')
                    print('==============================================================================')
                    print('                                     X2                                       ')
                    print('==============================================================================')
                    print('X2 Mean: ',statistics.mean(col_data2))
                    print('X2 Median: ',statistics.median(col_data2))
                    print('X2 Mode: ',statistics.mode(col_data2))
                    print('==============================================================================')
                    print(reg_info(X2,Y))   
                except:
                    print('==============================================================================')
                    print('                     Cannot get Regression Results For X2                     ')
                    print('==============================================================================')
                    pass

                if val_var.get() == 1:
                    linear_regressor.fit(X1, Y)  # perform linear regression
                    X1_pred = linear_regressor.predict(X1) # make predictions
                    plt.scatter(X1, Y, label=x1_val_name)
                    
                    linear_regressor.fit(X2, Y)
                    X2_pred = linear_regressor.predict(X2)
                    plt.scatter(X2, Y, label=x2_val_name)
 
                    plt.ylabel(y_val_name)
                    plt.legend(loc='upper right')
                    plt.ticklabel_format(style='plain', axis='y')
                    plt.ticklabel_format(style='plain', axis='x')

                    y_format = tkr.FuncFormatter(func)
                    x_format = tkr.FuncFormatter(func)  # make formatter

                    ax = plt.subplot(111)
                    ax.plot(X1, X1_pred)
                    ax.plot(X2,X2_pred)
                    ax.yaxis.set_major_formatter(y_format)
                    ax.xaxis.set_major_formatter(x_format)   # set formatter to needed axis
                    fig = plt.gcf() 
                    fig.set_size_inches(11,8)
                    plt.show()

                    print('multivariate')

                else:

                    xt = (X1 + X2)/2
                    linear_regressor.fit(xt, Y)  # perform linear regression
                    Y_pred = linear_regressor.predict(xt)  # make predictions
                    X2_pred = linear_regressor.predict(X2)
                    plt.scatter(X1, Y, label=x1_val_name)
                    #plt.plot(xt, Y_pred, color = 'red')
                    plt.scatter(X2, Y, label=x2_val_name)
                    plt.ylabel(y_val_name)
                    plt.legend(loc='upper right')

                    
                    plt.ticklabel_format(style='plain', axis='y')
                    plt.ticklabel_format(style='plain', axis='x')

                    y_format = tkr.FuncFormatter(func)
                    x_format = tkr.FuncFormatter(func)  # make formatter

                    ax = plt.subplot(111)
                    ax.plot(xt, Y_pred, color = 'red')
                    ax.yaxis.set_major_formatter(y_format)
                    ax.xaxis.set_major_formatter(x_format)   # set formatter to needed axis
                    fig = plt.gcf() 
                    fig.set_size_inches(11,8)
                    plt.show()
                    print('univariate')
                    
                    
            except:

                X1 = data.iloc[:, x1_val].values.reshape(-1, 1)  # values converts it into a numpy array
                Y = data.iloc[:, y_val].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
                linear_regressor = LinearRegression()  # create object for the class
                
                clearTextInput()
                try:
                    col_data = data[x1_val_name]
                    print('\n\n')
                    print('==============================================================================')
                    print('                                     X1                                       ')
                    print('==============================================================================')
                    print('X1 Mean: ',statistics.mean(col_data))
                    print('X1 Median: ',statistics.median(col_data))
                    print('X1 Mode: ',statistics.mode(col_data))
                    print('==============================================================================')
                
                    print(reg_info(X1,Y))
                except: 
                    print('==============================================================================')
                    print('                     Cannot get Regression Results For X1                     ')
                    print('==============================================================================')
                    pass

                linear_regressor.fit(X1, Y)  # perform linear regression
                X1_pred = linear_regressor.predict(X1) # make predictions
                plt.scatter(X1, Y, label=x1_val_name)

                plt.ylabel(y_val_name)
        
                plt.legend(loc='upper right')
            
                plt.ticklabel_format(style='plain', axis='y')
                plt.ticklabel_format(style='plain', axis='x')

                y_format = tkr.FuncFormatter(func)
                x_format = tkr.FuncFormatter(func)  # make formatter

                ax = plt.subplot(111)
                ax.plot(X1,X1_pred)
                ax.yaxis.set_major_formatter(y_format)
                ax.xaxis.set_major_formatter(x_format)   # set formatter to needed axis
                fig = plt.gcf() 
                fig.set_size_inches(11,8)
                plt.show()



                
    except:
        print('Please Select X Vriables')



def verify():
    global data
    global video_recent_link
    global wait,driver
    global url_link

    driver=chromedriver
    wait = WebDriverWait(driver,5)

    try:
        data = pd.read_csv(file_name)
        video_recent_link = data['Video URL']
        print('Starting a new videos only scraping process')
        print(video_recent_link[0])
    except:
        print('Starting a whole new scraping process')

    window.update()
    url_link = url_val.get()

    t1=threading.Thread(target=driver.get(url_link))
    t1.start()
    window.update()
    get_chnl_name()
    window.update()
    collect_vids_urls(url_link)
    window.update()
    collect_vid_data(channel_name)
    driver.quit()
    window.update()
    get_thumbnail(count)
    t1.join()

    try:
        combine_csv = pd.read_csv(file_name)
        combine_csv.to_csv(file_name2, index=False, mode='a', header=False)
    except:
        pass

    if open_reg_btn["state"] == "disabled":
        open_reg_btn["state"] = "normal"
        var_x1["state"] = "normal"
        var_x2["state"] = "normal"
        var_x3["state"] = "normal"
        var_y["state"] = "normal"
        #multi_var["state"] = "normal"
        #uni_var["state"] = "normal"



    print(' Scraping Completed Successfully!')


def opn_file():
    global file_name
    file_name = filedialog.askopenfilename(initialdir="./{}".format(results_file_dir[0]), title="Select a file")
    print(file_name)
    
    if open_reg_btn["state"] == "disabled":
        open_reg_btn["state"] = "normal"
        var_x1["state"] = "normal"
        var_x2["state"] = "normal"
        var_x3["state"] = "normal"
        var_y["state"] = "normal"
        #multi_var["state"] = "normal"
        #uni_var["state"] = "normal"

frame = tk.Frame(master=window, width=650 ,height=900 )

url = tk.Label(master=frame, text="Enter YouTube URL")
url_val = tk.Entry(master=frame, width = 70, textvariable = url_text)
url_btn = tk.Button(master=frame, text="Start", width=10, command=verify)

chnl = tk.Label(master=frame, text="Output")
chnl_val = tk.Text(master=frame, width = 78, height=42)
os.sys.stdout = Redirect(chnl_val)

open_results_btn = tk.Button(master=frame , text="Open Results Folder", width=20, command=opn_file)
open_reg_btn = tk.Button(master=frame , text="Open Regression", width=20, command=opts)

text_x1= tk.Label(master=frame, text="X1")
var_x1 = tk.OptionMenu(frame, variable_x1,  *OPTIONS , command=optx1)

text_x2= tk.Label(master=frame, text="X2")
var_x2 = tk.OptionMenu(frame, variable_x2,  *OPTIONS , command=optx2)

text_x3= tk.Label(master=frame, text="X3")
var_x3 = tk.OptionMenu(frame, variable_x3,  *OPTIONS , command=optx3)

text_y = tk.Label(master=frame, text="Y")


var_y = tk.OptionMenu(frame, variable_y,  *OPTIONS , command=opty)

multi_var = tk.Radiobutton(frame, text="Multi-variate",variable=val_var, value = 1)
uni_var = tk.Radiobutton(frame, text='Uni-variate',variable=val_var, value = 2)


#btn = tk.Button(master=frame, text="open file", width=20, command=opn_file)

frame.pack(fill=tk.X)

url.place(x=10, y=15)
url_val.place(x=125, y=15)
url_btn.place(x=560, y=10)
chnl.place(x=10, y=45)
chnl_val.place(x=10, y=75)

open_results_btn.place(x=490, y=765)
open_reg_btn.place(x=10, y=765)

text_x1.place(x=70, y=800)
var_x1.config(width=15)
var_x1.place(x=10, y=830)

text_x2.place(x=235, y=800)
var_x2.config(width=15)
var_x2.place(x=175, y=830)

text_x3.place(x=400,y=800)
var_x3.config(width=15)
var_x3.place(x=340, y=830)

text_y.place(x=570, y=800)
var_y.config(width=15)
var_y.place(x=506, y=830)
multi_var.place(x=10, y= 870)
uni_var.place(x=120, y=870)

open_reg_btn["state"] = "disabled"
var_x1["state"] = "disabled"
var_x2["state"] = "disabled"
var_x3["state"] = "disabled"
var_y["state"] = "disabled"
multi_var["state"] = "disabled"
uni_var["state"] = "disabled"
#btn.place(x=320, y=480)
#btn["state"] = 'disabled'

window.resizable(False, False)
window.mainloop()

#TESTING LINKS 

#https://www.youtube.com/c/LinusTechTips/videos
#https://www.youtube.com/c/JomaOppa/videos
#https://www.youtube.com/c/baldandbankrupt/videos
#https://www.youtube.com/user/TheVickshow/videos
#https://www.youtube.com/channel/UCBKCz2XLWQgDmHHfJuyoi4Q/videos
#header=False,encoding='utf-8-sig'