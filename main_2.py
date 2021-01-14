import tkinter as tk
import numpy as np
#import YouTube_scraper_functions as YT
import matplotlib.pyplot as plt  # To visualize
from sklearn.linear_model import LinearRegression
from tkinter.ttk import *
from tkinter import HORIZONTAL
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
import time
import pandas as pd
import csv
import os
from tkinter import filedialog

class Redirect():

    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)
        self.widget.see("end")

window = tk.Tk()
window.title("Youtube Scraper")

OPTIONS = [
    "Views",
    "Likes",
    "Dislikes",
    "Title Capital Ratio",
    "# of Title Chars",
    "# of Description Chars",
    "Red Value",
    "Blue Value",
    "Green Value"
] 

url_text = tk.StringVar(window)

variable1 = tk.StringVar(window)
variable1.set(OPTIONS[0]) # default value

variable2 = tk.StringVar(window)
variable2.set(OPTIONS[0]) # default value

variable3 = tk.StringVar(window)
variable3.set(OPTIONS[0]) # default value


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
    window.update()

def collect_vids_urls(chnl_url):
    global total_vids_counter
    total_vids_counter = 1
    #driver.get(chnl_url)
    #Creating the CSV File
    csv_file = open('{}\{}.csv'.format(channel_name+" "+ff_dt_string,channel_name+" "+ff_dt_string),'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Channel Name', 'Video URL'])
    

    while True:
        try:
            #vid = driver.find_element_by_xpath('//*[@id="items"]/ytd-grid-video-renderer[{}]'.format(counter))
            vid = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="items"]/ytd-grid-video-renderer[{}]'.format(total_vids_counter))))
            url_vid = vid.find_element_by_css_selector('#video-title')
            url = url_vid.get_attribute('href')
            print(url, ' ', total_vids_counter)
            csv_writer.writerow([channel_name , url])
            total_vids_counter+=1
            driver.execute_script(javascript_2)
            window.update()
            
        except:
            print()
            print('Scraping Videos Libraries Completed!')
            
            total_vids_counter-=1
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
    
    counter = 1
    for url in video_url:
        window.update()
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
        v_view = v_view.replace(' views', '')
        v_view = v_view.replace(',', '')
        #v_date = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"div#date yt-formatted-string")))
        v_likes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(1)"))).text
        v_likes = v_likes.replace('.','')
        v_likes = v_likes.replace('K', '000')
        v_likes = v_likes.replace('M', '000000')

        v_dislikes = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#top-level-buttons > ytd-toggle-button-renderer:nth-child(2)"))).text
        v_dislikes = v_dislikes.replace('.','')
        v_dislikes = v_dislikes.replace('K', '000')
        v_dislikes = v_dislikes.replace('M', '000000')

        #Printing the results
        print()
        print('Video URL: ', url)
        print('Video ID: ', video_id[0])
        print('Title: ', v_title )
        print('Title Captial Ratio: ',formated_captial_ratio,  ' | ' ,'# Of Chars In Title: ', len(v_title))
        print('# Of Chars In Description: ', len(v_description))
        print('Views: ', v_view, ' | ' , 'Likes: ', v_likes, ' | ', 'Disikes: ', v_dislikes)
        print( counter , " of " , total_vids_counter , " scraped.")
        print('-----------------------------------')
        counter += 1
        csv_writer.writerow([channel_name, url, video_id[0], v_view, v_likes, v_dislikes, v_title, formated_captial_ratio, len(v_title), len(v_description)])
        
count = 0

#Getting the thumbnail image and save it for RGB breakdown.
def get_thumbnail(counter):
    
    csv_file = open('{}\{}.csv'.format(channel_name+" "+ff_dt_string, channel_name+" "+ ff_dt_string + " FINAL"),'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Channel Name', 'Video URL',"Video ID", 'Views', 'Likes', 'Dislikes', 'Title','Title Captial Ratio','# Of Title Chars', '# Of Description Chars', 'Max RGB', 'Min RGB', 'R', 'G', 'B'])
    file_name = '{}\{}.csv'.format(channel_name+" "+ff_dt_string, channel_name+" "+ ff_dt_string + " FINAL")
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
        window.update()
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
        img_counter = counter + 1        
        print('Max RGB: ', max_rgb , 'Min RGB: ', min_rgb, 'R: ', r, 'G: ', g, 'B: ', b)
        print(img_counter, ' of ', total_vids_counter)
        csv_writer.writerow([ chnl_name[counter], vid_url[counter], vids_id[counter], views[counter], likes[counter], dislikes[counter], title[counter], title_captial_ratio[counter], title_chars[counter], des_chars[counter], max_rgb, min_rgb, r, g, b])
        counter += 1


def opt1(value):
    global x_val

    if value == "Views":
        print("Views")
        x_val = 3

    elif value == "Likes":
        print("Likes")
        x_val = 4

    elif value == "Dislikes":
        print("Dislikes")
        x_val = 5

    elif value == "Title Capital Ratio":
        print("Title Capital Ratio")
        x_val = 7
        
    elif value == "# of Title Chars":
        print("# of Title Chars")
        x_val = 8

    elif value == "# of Description Chars":
        print("# of Description Chars")
        x_val = 9

    elif value == "Red Value":
        print("Red Value")
        x_val = 12

    elif value == "Blue Value":
        print("Blue Value")
        x_val = 13

    elif value == "Green Value":
        print("Green Value")
        x_val = 14
    

def opt2(value):

    global y_val

    if value == "Views":
        print("Views")
        y_val = 3

    elif value == "Likes":
        print("Likes")
        y_val = 4

    elif value == "Dislikes":
        print("Dislikes")
        y_val = 5

    elif value == "Title Capital Ratio":
        print("Title Capital Ratio")
        y_val = 7
        
    elif value == "# of Title Chars":
        print("# of Title Chars")
        y_val = 8

    elif value == "# of Description Chars":
        print("# of Description Chars")
        y_val = 9

    elif value == "Red Value":
        print("Red Value")
        y_val = 12

    elif value == "Blue Value":
        print("Blue Value")
        y_val = 13

    elif value == "Green Value":
        print("Green Value")
        y_val = 14

def opts():
    data = pd.read_csv(file_name)  # load data set
   
    X = data.iloc[:, y_val].values.reshape(-1, 1)  # values converts it into a numpy array
    Y = data.iloc[:, x_val].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X)  # make predictions
    plt.scatter(X, Y)
    plt.plot(X, Y_pred, color='red')
    plt.xlabel('Views')
    plt.ylabel('Capital Ratio')
    plt.gcf()
    plt.draw()
    plt.savefig('ratioviedsssssssws.png',dpi=100)
    plt.show()

def verify():
    global wait,driver

    driver = webdriver.Chrome(chromedriver)
    wait = WebDriverWait(driver,1)

    global url_link
    url_link = url_val.get()
    window.update()
    driver.get(url_link)
    #window.update()
    get_chnl_name()
    #window.update()
    collect_vids_urls(url_link)
    collect_vid_data(channel_name)
    get_thumbnail(count)

    if open_reg_btn["state"] == "disabled":
        open_reg_btn["state"] = "normal"
        var1["state"] = "normal"
        var2["state"] = "normal"
        
    print(' Scraping Completed Successfully!')
    driver.quit()

def opn_file():
    global file_name
    file_name = filedialog.askopenfilename(initialdir="./", title="Select a file")
    print(file_name)
    
    if open_reg_btn["state"] == "disabled":
        open_reg_btn["state"] = "normal"
        var1["state"] = "normal"
        var2["state"] = "normal"

frame = tk.Frame(master=window, width=480 ,height=550 )

url = tk.Label(master=frame, text="Enter URL")
url_val = tk.Entry(master=frame, width = 50, textvariable = url_text)
url_btn = tk.Button(master=frame, text="Start", width=10, command=verify)

chnl = tk.Label(master=frame, text="Channel Name")
chnl_val = tk.Text(master=frame, width = 57, height=22)
os.sys.stdout = Redirect(chnl_val)

open_results_btn = tk.Button(master=frame , text="Open Results Folder", width=20, command=opn_file)
open_reg_btn = tk.Button(master=frame , text="Open Regression", width=20, command=opts)

var1 = tk.OptionMenu(frame, variable1,  *OPTIONS , command=opt1)

var2 = tk.OptionMenu(frame, variable2,  *OPTIONS , command=opt2)


#btn = tk.Button(master=frame, text="open file", width=20, command=opn_file)

frame.pack(fill=tk.X)

url.place(x=10, y=15)
url_val.place(x=75, y=15)
url_btn.place(x=390, y=10)
chnl.place(x=10, y=45)
chnl_val.place(x=10, y=75)

open_results_btn.place(x=320, y=450)
open_reg_btn.place(x=10, y=450)

var1.place(x=8, y=480)
var2.place(x=87, y=480)

open_reg_btn["state"] = "disabled"
var1["state"] = "disabled"
var2["state"] = "disabled"
#btn.place(x=320, y=480)
#btn["state"] = 'disabled'

window.resizable(False, False)
window.mainloop()

