from distutils.core import setup # Need this to handle modules
import py2exe 
import tkinter as tk
import numpy as np
from numpy.polynomial.polynomial import polyfit
import scipy.spatial.transform._rotation_groups

#import YouTube_scraper_functions as YT
import matplotlib.pyplot as plt  # To visualize
from matplotlib import pyplot
from sklearn.linear_model import LinearRegression
import sklearn.utils._weight_vector
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
    "Title Capital Ratio",
    "# of Title Chars",
    "# of Description Chars",
    "Red",
    "Blue",
    "Green"
] 

url_text = tk.StringVar(window)

variable_x1 = tk.StringVar(window)
variable_x1.set('X1 value') # default value

variable_x2 = tk.StringVar(window)
variable_x2.set('X2 value') # default value

variable_x3 = tk.StringVar(window)
variable_x3.set('X3 value') # default value

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
chromedriver = chromedriver_dir[0]




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
    #driver.get(chnl_url)
    #Creating the CSV File
    csv_file = open('{}\{}\{}.csv'.format(results_file_dir[0], channel_name+" "+ff_dt_string, channel_name+" "+ff_dt_string),'w', encoding='utf-8', newline='')
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
    window.update()
    #Creating the semi-final CSV File for saving the NEW scraped data
    csv_file = open('{}\{}\{}.csv'.format(results_file_dir[0], channel_name+" "+ff_dt_string,channel_name+" "+ff_dt_string + " SEMI-FINAL"),'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Channel Name', 'Video URL','Video ID', 'Views', 'Likes', 'Dislikes', 'Title','Title Captial Ratio','# Of Title Chars', '# Of Description Chars'])

    #reading the URLs scraped data
    data_file = pd.read_csv('{}\{}\{}.csv'.format(results_file_dir[0], channel_name+" "+ff_dt_string,channel_name+" "+ff_dt_string))
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
        

        v_description =''
        try:
            more_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,"#more")))
            more_btn.click()

            v_des = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#description')))
            for v in v_des:
                v.text
                v_description+=v.text
        except:
            pass

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
    global file_name2
    file_name2 = '{}\{}\{}.csv'.format(results_file_dir[0], channel_name+" "+ff_dt_string, channel_name+" "+ ff_dt_string + " FINAL")
    csv_file = open('{}\{}\{}.csv'.format(results_file_dir[0],channel_name+" "+ff_dt_string, channel_name+" "+ ff_dt_string + " FINAL"),'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Channel Name', 'Video URL',"Video ID", 'Views', 'Likes', 'Dislikes', 'Title','Title Captial Ratio','# Of Title Chars', '# Of Description Chars', 'Max RGB', 'Min RGB', 'R', 'G', 'B'])
    
    df_read = pd.read_csv('{}\{}\{}.csv'.format(results_file_dir[0], channel_name+" "+ff_dt_string,channel_name+" "+ ff_dt_string + " SEMI-FINAL"))
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
        csv_writer.writerow([ chnl_name[counter], vid_url[counter], vids_id[counter], views[counter], likes[counter], dislikes[counter], title[counter], title_captial_ratio[counter], title_chars[counter], des_chars[counter], max_rgb, min_rgb, r, g, b])
        counter += 1

    os.remove('{}\{}\{}.csv'.format(results_file_dir[0],channel_name+" "+ff_dt_string, channel_name+" "+ ff_dt_string ))
    os.remove('{}\{}\{}.csv'.format(results_file_dir[0],channel_name+" "+ff_dt_string, channel_name+" "+ ff_dt_string + " SEMI-FINAL"))

#Option for X1
def optx1(value):
    global x1_val
    global x1_val_name

    if value == "Views":
        print("X1 = Views")
        x1_val = 3
        x1_val_name = "Views"

    elif value == "Likes":
        print("X1 = Likes")
        x1_val = 4
        x1_val_name = "Likes"

    elif value == "Dislikes":
        print("X1 = Dislikes")
        x1_val = 5
        x1_val_name = "Disikes"

    elif value == "Title Capital Ratio":
        print("X1 = Title Capital Ratio")
        x1_val = 7
        x1_val_name = "Title Capital Ratio"

    elif value == "# of Title Chars":
        print("X1 = # of Title Chars")
        x1_val = 8
        x1_val_name = "# of Title Chars"

    elif value == "# of Description Chars":
        print("X1 = # of Description Chars")
        x1_val = 9
        x1_val_name = "# of Description Chars"

    elif value == "Red":
        print("X1 = Red")
        x1_val = 12
        x1_val_name = "Red"

    elif value == "Blue":
        print("X1 = Blue")
        x1_val = 13
        x1_val_name = "Blue"

    elif value == "Green":
        print("X1 = Green")
        x1_val = 14
        x1_val_name = "Green"
    else:
        print("Please Select A variable")
        pass
    
#Option for X2
def optx2(value):
    global x2_val
    global x2_val_name

    if value == "Views":
        print("X2 = Views")
        x2_val = 3
        x2_val_name = "Views"

    elif value == "Likes":
        print("X2 = Likes")
        x2_val = 4
        x2_val_name = "Likes"

    elif value == "Dislikes":
        print("X2 = Dislikes")
        x2_val = 5
        x2_val_name = "Disikes"

    elif value == "Title Capital Ratio":
        print("X2 = Title Capital Ratio")
        x2_val = 7
        x2_val_name = "Title Capital Ratio"

    elif value == "# of Title Chars":
        print("X2 = # of Title Chars")
        x2_val = 8
        x2_val_name = "# of Title Chars"

    elif value == "# of Description Chars":
        print("X2 = # of Description Chars")
        x2_val = 9
        x2_val_name = "# of Description Chars"

    elif value == "Red":
        print("X2 = Red")
        x2_val = 12
        x2_val_name = "Red"

    elif value == "Blue":
        print("X2 = Blue")
        x2_val = 13
        x2_val_name = "Blue"

    elif value == "Green":
        print("X2 = Green")
        x2_val = 14
        x2_val_name = "Green"
    else:
        print("Please Select A variable")
        pass

#Option for X3
def optx3(value):
    global x3_val
    global x3_val_name

    if value == "Views":
        print("X3 = Views")
        x3_val = 3
        x3_val_name = "Views"

    elif value == "Likes":
        print("X3 = Likes")
        x3_val = 4
        x3_val_name = "Likes"

    elif value == "Dislikes":
        print("X3 = Dislikes")
        x3_val = 5
        x3_val_name = "Disikes"

    elif value == "Title Capital Ratio":
        print("X3 = Title Capital Ratio")
        x3_val = 7
        x3_val_name = "Title Capital Ratio"

    elif value == "# of Title Chars":
        print("X3 = # of Title Chars")
        x3_val = 8
        x3_val_name = "# of Title Chars"

    elif value == "# of Description Chars":
        print("X3 = # of Description Chars")
        x3_val = 9
        x3_val_name = "# of Description Chars"

    elif value == "Red":
        print("X3 = Red")
        x3_val = 12
        x3_val_name = "Red"

    elif value == "Blue":
        print("X3 = Blue")
        x3_val = 13
        x3_val_name = "Blue"

    elif value == "Green":
        print("X3 = Green")
        x3_val = 14
        x3_val_name = "Green"
    else:
        print("Please Select A variable")
        pass

#Option for Y
y_val = 3 #DEFAULT for VIEWS
y_val_name = "Views" #DEFAULT for VIEWS

def opty(value):
    global y_val
    global y_val_name

    if value == "Views":
        print("Y = Views")
        y_val = 3
        y_val_name = "Views"

    elif value == "Likes":
        print("Y = Likes")
        y_val = 4
        y_val_name = "Likes"

    elif value == "Dislikes":
        print("Y = Dislikes")
        y_val = 5
        y_val_name = "Dislikes"

    elif value == "Title Capital Ratio":
        print("Y = Title Capital Ratio")
        y_val = 7
        y_val_name = "Title Capital Ratio"  

    elif value == "# of Title Chars":
        print("Y = # of Title Chars")
        y_val = 8
        y_val_name = "# of Title Chars"

    elif value == "# of Description Chars":
        print("Y = # of Description Chars")
        y_val = 9
        y_val_name = "# of Description Chars"

    elif value == "Red":
        print("Y = Red")
        y_val = 12
        y_val_name = "Red"

    elif value == "Blue":
        print("Y = Blue")
        y_val = 13
        y_val_name = "Blue"

    elif value == "Green":
        print("Y = Green")
        y_val = 14
        y_val_name = "Green"    
    else:
        print("Please Select A variable")
        pass


def opts():
    try:
        data = pd.read_csv(file_name)  # load data set
    except:
        data = pd.read_csv(file_name2)
        
    X1 = data.iloc[:, x1_val].values.reshape(-1, 1)  # values converts it into a numpy array
    X2 = data.iloc[:, x2_val].values.reshape(-1,1)
    X3 = data.iloc[:, x3_val].values.reshape(-1,1)
    Y = data.iloc[:, y_val].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
    linear_regressor = LinearRegression()  # create object for the class

    if val_var.get() == 1:
        linear_regressor.fit(X1, Y)  # perform linear regression
        X1_pred = linear_regressor.predict(X1) # make predictions
        plt.scatter(X1, Y, label=x1_val_name)
        plt.plot(X1, X1_pred)

        linear_regressor.fit(X2, Y)
        X2_pred = linear_regressor.predict(X2)
        plt.scatter(X2, Y, label=x2_val_name)
        plt.plot(X2, X2_pred)

        linear_regressor.fit(X3, Y)
        X3_pred = linear_regressor.predict(X3)
        plt.scatter(X3, Y, label=x3_val_name)
        plt.plot(X3, X3_pred)

        plt.ylabel(y_val_name)

        plt.legend(loc='upper right')
        #plt.gcf()
        #plt.draw()
        #plt.savefig('ratioviedsssssssws1.png',dpi=100)
        plt.show()

        print('multivariate')

        
    else:
        xt = (X1 + X2 + X3)/3
        linear_regressor.fit(xt, Y)  # perform linear regression
        Y_pred = linear_regressor.predict(xt)  # make predictions
        X2_pred = linear_regressor.predict(X2)
        X3_pred = linear_regressor.predict(X3)
        plt.scatter(X1, Y, label=x1_val_name)
        plt.plot(xt, Y_pred, color = 'red')
        plt.scatter(X2, Y, label=x2_val_name)
        plt.scatter(X3, Y,  label=x3_val_name)
        plt.ylabel(y_val_name)

        plt.legend(loc='upper right')
       #plt.gcf()
       #plt.draw()
       #plt.savefig('ratioviedsssssssws.png',dpi=100)
        plt.show()
        print('univariate')

def verify():
    global wait,driver
    global url_link
    driver = webdriver.Chrome(chromedriver)
    wait = WebDriverWait(driver,3)
    
    window.update()
    url_link = url_val.get()
    
    driver.get(url_link)
    #window.update()
    get_chnl_name()
    #window.update()
    collect_vids_urls(url_link)
    collect_vid_data(channel_name)
    get_thumbnail(count)

    if open_reg_btn["state"] == "disabled":
        open_reg_btn["state"] = "normal"
        var_x1["state"] = "normal"
        var_x2["state"] = "normal"
        var_x3["state"] = "normal"
        var_y["state"] = "normal"
        multi_var["state"] = "normal"
        uni_var["state"] = "normal"


    print(' Scraping Completed Successfully!')
    driver.quit()

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
        multi_var["state"] = "normal"
        uni_var["state"] = "normal"

frame = tk.Frame(master=window, width=480 ,height=580 )

url = tk.Label(master=frame, text="Enter URL")
url_val = tk.Entry(master=frame, width = 50, textvariable = url_text)
url_btn = tk.Button(master=frame, text="Start", width=10, command=verify)

chnl = tk.Label(master=frame, text="Output")
chnl_val = tk.Text(master=frame, width = 57, height=22)
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
url_val.place(x=75, y=15)
url_btn.place(x=390, y=10)
chnl.place(x=10, y=45)
chnl_val.place(x=10, y=75)

open_results_btn.place(x=320, y=450)
open_reg_btn.place(x=10, y=450)

text_x1.place(x=45, y=485)
var_x1.config(width=6)
var_x1.place(x=10, y=510)

text_x2.place(x=170, y=485)
var_x2.config(width=6)
var_x2.place(x=135, y=510)

text_x3.place(x=300,y=485)
var_x3.config(width=6)
var_x3.place(x=265, y=510)
#
text_y.place(x=425, y=485)
var_y.config(width=6)
var_y.place(x=390, y=510)
multi_var.place(x=10, y= 550)
uni_var.place(x=120, y=550)

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