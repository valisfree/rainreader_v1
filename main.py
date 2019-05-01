# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        Rain.reader
# Created:     09.11.2018
# Version:     0.1
# Copyright:   (c) 2018, Vale_Phtor, valisfree@yandex.ru phtor.ru
# Licence:     Apache License version 2.0
#-------------------------------------------------------------------------------



import os
from tkinter import *
from tkinter import filedialog as fd
import func

# глобальные переменные
words_list = [] # список слов книги
cur = 0 # позиция в списке слов книги
speed = 0 # скорость чтения слов в минуту
flag = 0 # флаг включения режима чтения
adress = ''
func.createDataBase()

def openBook():
    global words_list
    global adress
    global cur
    adress = fd.askopenfilename(filetypes = (("txt files","*.txt"),("all files","*.*")))
    if adress == tuple():
        check_word_list()
        return
    else:
        words_list = func.open_and_read_book_file(adress)
        if not check_word_list():
            func.addToDataBase(adress, cur, speed)
            cur_and_speed = func.loadCurAndSpeedFromDataBase(adress)
            if cur_and_speed[1] == 0:
                return
            s1.set(cur_and_speed[1]) # меняет значение шкалы.
            cur = cur_and_speed[0] - 1
            l1.configure(text=words_list[cur])

def check_word_list():
    if len(words_list) == 0:
        word = 'no file open'
        f_top.configure(text=word)
        return False
    word = 'file open'
    f_top.configure(text=word)

########## WORK SUKA, WORK!

def flag_start_stop(event):
    global flag
    if flag == 0:
        flag = 1
        update_label()
        return
    if flag == 1:
        flag = 0
        return
def update_label(event=0):
    if check_word_list() == False:
        return
    global cur
    if flag == 1:
        word = func.get_word(words_list, cur)
        if word == False:
            l1.configure(text="End book")
            return
        l1.configure(text=word)
        cur += 1
        time = int(func.stream_time_pause(word, func.speed(speed)))
        root.after(time, update_label)

def scaleInput(i):
    global speed
    speed = int(i)

def savePos():
    if cvar1.get() == True:
        func.updateDataBase(adress, cur, speed)

def about():
    a = Toplevel()
    a.geometry('300x75')
    a.title("Rain reader")
    a['bg'] = 'gray'
    a.resizable(False, False)
    f_top = LabelFrame(a, bg='gray', text='About')
    t1 = 'Rain reader - program for speed reading.'
    t2 = 'Words like rain will fall on your head.'
    t3 = 'Open .txt files.'
    l1 = Label(f_top,text=t1, bg='gray')
    l2 = Label(f_top,text=t2, bg='gray')
    l3 = Label(f_top,text=t3, bg='gray')
    f_top.pack()
    l1.pack(fill=X)
    l2.pack(fill=X)
    l3.pack(fill=X)

root = Tk()
mainmenu = Menu(root)
root.geometry("450x300+300+300")
root.minsize(350,250)

if 'nt' == os.name:
    root.iconbitmap("fav.ico")
else:
    root.iconbitmap("@fav.xbm")

root.title("Rain reader")
root.config(menu=mainmenu)
mainmenu.add_command(label='File', command=openBook)
# mainmenu.add_command(label='Options')
mainmenu.add_command(label='About', command=about)

f_top = LabelFrame(root, text='Stream')
l1 = Label(f_top, width=150, height=5, text="stream", bg='gray', font="Arial 16")
l1['text'] = 'Click for start/pause'
l1.bind('<Button-1>', flag_start_stop)
root.bind('<space>', flag_start_stop)

'''
l1.bind('<FocusIn>', testirovka)
l1.bind('<FocusOut>', testirovka)
'''

s1 = Scale(f_top, from_=300, to=1000, resolution=5, tickinterval=200,
troughcolor='grey', orient=HORIZONTAL, command=scaleInput)
s1.set(320)

cvar1 = BooleanVar()
cvar1.set(0)
c1 = Checkbutton(root, text="Save", variable=cvar1, onvalue=1,
offvalue=0, command=savePos)

f_top.pack(fill=X, padx=5, pady=5)
l1.pack(fill=X)
s1.pack(fill=X, padx=5, pady=5)
c1.pack(anchor=NE, padx=5, pady=5)

root.mainloop()
