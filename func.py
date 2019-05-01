# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------
# Name:        Rain.reader
# Created:     09.11.2018
# Version:     0.1
# Copyright:   (c) 2018, Vale_Phtor, valisfree@yandex.ru phtor.ru
# Licence:     Apache License version 2.0
#-----------------------------------------------------------------------


import sqlite3
import time
import os
from datetime import datetime
import codecs

############ OPEN FILE ##########
def open_and_read_book_file(file_name):
    '''
    Открывает и считывает данные из файла(книги).
    Возвращает список слов.
    '''
    words_list = []
    if file_name == '':
        return
    else:
        with codecs.open(file_name, "r",encoding='utf-8', errors='ignore') as inf:
            for line in inf:
                line = line.strip()
                line = line.split()
                for str in line:
                    words_list.append(str)
        return words_list

def checkFileSize(file_name):
    return os.path.getsize(file_name)

def adressToNamefile(adress):
    adr = ''
    adress = adress[::-1]
    for i in adress:
        adr += i
        if i == '/' or i =='\\':
            adr = adr[::-1]
            return adr[1:]

def sizeFile(adress):
    return os.stat(adress).st_size

############# SQLite ############
def createDataBase():
    check_db = not os.path.exists('rain.db')
    if check_db:
        conn = sqlite3.connect("rain.db")
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE books
                          (adress text PRIMARY KEY, name text, cur number, speed number,
                          data1 number, size number)
                       """)
        conn.close()

def addToDataBase(adress, cur, speed):
    size = checkFileSize(adress)
    name = adressToNamefile(adress)
    '''
    data1 = datetime.utcfromtimestamp(timestamp)
    '''
    data1 = int(time.mktime(time.gmtime()))
    size = sizeFile(adress)

    conn = sqlite3.connect("rain.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO books VALUES (?, ?, ?, ?, ?, ?)",
                      (adress, name, cur, speed, data1, size)
                   )
    conn.commit()
    conn.close()

def loadCurAndSpeedFromDataBase(adress):
    conn = sqlite3.connect("rain.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT rowid, * FROM books ORDER BY adress"):
        if row[1] == adress:
            cur_speed = (row[3],row[4])
            conn.close()
            return cur_speed
    conn.close()

def updateDataBase(adress, cur, speed):
    size = checkFileSize(adress)
    name = adressToNamefile(adress)
    data1 = int(time.mktime(time.gmtime()))
    size = sizeFile(adress)
    conn = sqlite3.connect("rain.db")
    cursor = conn.cursor()

    cursor.execute("INSERT OR REPLACE INTO books VALUES (?, ?, ?, ?, ?, ?)",
                      (adress, name, cur, speed, data1, size)
                   )
    conn.commit()
    conn.close()

# for debug, print all table
def printDataBase():
    conn = sqlite3.connect("rain.db")
    cursor = conn.cursor()
    for row in cursor.execute("SELECT rowid, * FROM books ORDER BY adress"):
        print(row)
    conn.close()
# printDataBase()

############# GET WORD ##########

def get_word(words_list, cur):
    if cur >= len(words_list):
        return False
    return words_list[cur]

############# TIME ############

time_for_punctuation = 0.12
time_for_long_words = 0.08 # if len word > 5

def speed(speed):
    """
    Принимает скорость. Возвращает базовое время вывода одного слова.
    """
    x = 60 / speed
    y = x * 5 # препдолагаю, что 3 слова обычных, одно больше 5 букв и один знак пунктуации
    z = (3 * x) + (x + time_for_punctuation) + (x + time_for_long_words)
    a  = (z - y) / 5 # разница от среднего значения. Поправка на 2 из 5 слов
    base_time = x - a
    return base_time
def stream_time_pause(word, base_time):
    '''
    Создает задержку между выводом следующего слова.
    '''
    delta = word_time_lench(word) + time_punktuation(word)
    counting_time = base_time + delta
    return counting_time * 1000
def word_time_lench(word):
    """
    Считает длину слова. Возвращает значение прибавки к задержке
    """
    counted_time = 0
    if len(word) > 5:
        counted_time += time_for_long_words
    return counted_time
def time_punktuation(word):
    """
    Ищет знаки препинания. Возвращает значение прибавки к задержке.
    """
    counted_time = 0
    if ',' or '.' or '!' in word:
        counted_time += time_for_punctuation
    return counted_time

############ END TIME ###########
