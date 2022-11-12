import time
from flask import *
import sqlite3
from Interface_Wed import download_data_from_firebase


def logData(x, y, z, v):
    conn = sqlite3.connect("data.db")
    curs = conn.cursor()
    try:
        curs.execute("INSERT INTO tables_input VALUES(datetime('now'), ?, ?,?,?)", (x, y, z, v))
        conn.commit()
    except:
        print("Error")
    conn.close()


def insert_data_sql():
    # i = 0
    while True:
        # print(i)
        x, y, z, v, t = download_data_from_firebase.downloadData()
        logData(x, y, z, v)
        # i = i + 1
        time.sleep(1)


insert_data_sql()
