import tkinter as tk
from tkinter.ttk import *
from tkinter import HORIZONTAL



window = tk.Tk()



frame = tk.Frame(master=window, width=480 ,height=260 )

url = tk.Label(master=frame, text="Enter URL")
url_val = tk.Entry(master=frame, width = 50)
url_btn = tk.Button(master=frame, text="Start", width=10)

chnl = tk.Label(master=frame, text="Channel Name")
chnl_val = tk.Entry(master=frame, width = 30)

title = tk.Label(master=frame, text="Title")
title_val = tk.Entry(master=frame, width = 50)

title = tk.Label(master=frame, text="Title")
title_val = tk.Entry(master=frame, width = 45)

ratio = tk.Label(master=frame, text="Capital Ratio")
ratio_val = tk.Entry(master=frame, width = 8)

title_chars = tk.Label(master=frame, text="# of chars in title")
title_chars_val = tk.Entry(master=frame, width = 8)

des_chars = tk.Label(master=frame, text="# of chars in description")
des_chars_val = tk.Entry(master=frame, width = 8)

views = tk.Label(master=frame, text="Views")
views_val = tk.Entry(master=frame, width = 13)

likes = tk.Label(master=frame, text="Likes")
likes_val = tk.Entry(master=frame, width = 10)

dislikes = tk.Label(master=frame, text="Dislikes")
dislikes_val = tk.Entry(master=frame, width = 10)

max_rgb = tk.Label(master=frame, text="Max RGB")
max_rgb_val = tk.Entry(master=frame, width = 5)

min_rgb = tk.Label(master=frame, text="Min RGB")
min_rgb_val = tk.Entry(master=frame, width = 5)

r = tk.Label(master=frame, text="R")
r_val = tk.Entry(master=frame, width = 5)

g = tk.Label(master=frame, text="G")
g_val = tk.Entry(master=frame, width = 5)

b = tk.Label(master=frame, text="B")
b_val = tk.Entry(master=frame, width = 5)

progress = Progressbar(master=frame, orient = HORIZONTAL, length = 460, mode = 'determinate') 

open_results_btn = tk.Button(master=frame , text="Open Results Folder", width=20)

open_reg_btn = tk.Button(master=frame , text="Open Regression", width=20)


#chnl = tk.Label(master=frame, text="Channel Name")
#chnl_val = tk.Entry(master=frame, width = 30)
#
#
#chnl = tk.Label(master=frame, text="Channel Name")
#chnl_val = tk.Entry(master=frame, width = 30)
#


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
b_val.place(x=430, y=165)

progress.place(x=10, y=195)

open_results_btn.place(x=320, y=225)

open_reg_btn.place(x=10, y=225)

window.mainloop()