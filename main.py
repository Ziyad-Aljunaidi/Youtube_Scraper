import tkinter as tk
#import YouTube_scraper_functions as YT
from tkinter.ttk import *
from tkinter import HORIZONTAL
import time
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
import os

class Redirect():

    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)

#Opening the settings.csv
df = pd.read_csv('settings.csv')
chromedriver_dir = df['chromedriver_dir']
results_file_dir = df['results_file_dir']

#Formating Time For Naming The Folder And Its Files
now = datetime.now()
dt_string = str(now.strftime("%d/%m/%Y %H:%M:%S"))
f_dt_string = dt_string.replace('/','-')
ff_dt_string = f_dt_string.replace(':','-')

chromedriver = chromedriver_dir[0]
driver = webdriver.Chrome(chromedriver)
wait = WebDriverWait(driver,1)


def get_url(url):
    driver.get(url)

def get_chnl_name():
    channel_name = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="channel-name"]'))).text
    #print('Channel Name: ', channel_name)
    os.sys(channel_name)

#the UI
window = tk.Tk()
url_text = tk.StringVar(window)

def verify():
    url_link = url_val.get()
    print(url_link)
    get_url(url_link)


frame = tk.Frame(master=window, width=480 ,height=260 )

url = tk.Label(master=frame, text="Enter URL")
url_val = tk.Entry(master=frame, width = 50, textvariable = url_text)
url_btn = tk.Button(master=frame, text="Start", width=10, command=verify)


chnl = tk.Label(master=frame, text="Channel Name")
chnl_val = tk.Text(master=frame, width = 30, height=1)




title = tk.Label(master=frame, text="Title")
title_val = tk.Text(master=frame, width = 50, height=1)

title = tk.Label(master=frame, text="Title")
title_val = tk.Text(master=frame, width = 3, height=1)

ratio = tk.Label(master=frame, text="Capital Ratio")
ratio_val = tk.Text(master=frame, width = 7, height=1)

title_chars = tk.Label(master=frame, text="# of chars in title")
title_chars_val = tk.Text(master=frame, width = 8, height=1)

des_chars = tk.Label(master=frame, text="# of chars in description")
des_chars_val = tk.Text(master=frame, width = 8, height=1)

views = tk.Label(master=frame, text="Views")
views_val = tk.Text(master=frame, width = 13, height=1)

likes = tk.Label(master=frame, text="Likes")
likes_val = tk.Text(master=frame, width = 10, height=1)

dislikes = tk.Label(master=frame, text="Dislikes")
dislikes_val = tk.Text(master=frame, width = 10, height=1)

max_rgb = tk.Label(master=frame, text="Max RGB")
max_rgb_val = tk.Text(master=frame, width = 5, height=1)

min_rgb = tk.Label(master=frame, text="Min RGB")
min_rgb_val = tk.Text(master=frame, width = 5, height=1)

r = tk.Label(master=frame, text="R")
r_val = tk.Text(master=frame, width = 5, height=1)

g = tk.Label(master=frame, text="G")
g_val = tk.Text(master=frame, width = 5, height=1)

b = tk.Label(master=frame, text="B")
b_val = tk.Text(master=frame, width = 5, height=1)

progress = Progressbar(master=frame, orient = HORIZONTAL, length = 460, mode = 'determinate') 

open_results_btn = tk.Button(master=frame , text="Open Results Folder", width=20)

open_reg_btn = tk.Button(master=frame , text="Open Regression", width=20)


frame.pack(fill=tk.X)

url.place(x=10, y=15)
url_val.place(x=75, y=15)
url_btn.place(x=390, y=10)

chnl.place(x=10, y=45)
chnl_val.place(x=100, y=45)

title.place(x=10, y=75)
title_val.place(x=50, y=75)

ratio.place(x=330, y=75)
ratio_val.place(x=410, y=75)

title_chars.place(x=10, y=105)
title_chars_val.place(x=120, y=105)

des_chars.place(x=190, y=105)
des_chars_val.place(x=340, y=105)

views.place(x=10, y=135)
views_val.place(x=60 ,y=135)

likes.place(x=160, y=135)
likes_val.place(x=210 ,y=135)

dislikes.place(x=290, y=135)
dislikes_val.place(x=350 ,y=135)

max_rgb.place(x=10, y=165)
max_rgb_val.place(x=70, y=165)

min_rgb.place(x=110, y=165)
min_rgb_val.place(x=170, y=165)

r.place(x=230, y=165)
r_val.place(x=250, y=165)

g.place(x=310, y=165)
g_val.place(x=330, y=165)

b.place(x=400, y=165)
b_val.place(x=425, y=165)

progress.place(x=10, y=195)

open_results_btn.place(x=320, y=225)

open_reg_btn.place(x=10, y=225)


os.sys.stdout = Redirect(chnl_val)
window.resizable(False, False)
window.mainloop()

