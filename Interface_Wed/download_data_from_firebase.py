import pyrebase
import firebase_admin
from math import *
import pandas as pd
import time

l = 30
E = 2 * pow(10, 8)  # đơn vị là kPa ₫> đơn vị của lực sau khi tính sẽ là kN.
A = 1.131 * pow(10, -4)  # đã đổi sang m^2

firebaseConfig = {
    'apiKey': "AIzaSyD0NwAM4KK6va_YhAtMSZp_MITw_ctl1Dw",
    'authDomain': "bts-nodejs-ab329.firebaseapp.com",
    'databaseURL': "https://bts-nodejs-ab329-default-rtdb.firebaseio.com",
    'projectId': "bts-nodejs-ab329",
    'storageBucket': "bts-nodejs-ab329.appspot.com",
    'messagingSenderId': "1005673319336",
    'appId': "1:1005673319336:web:448760263eb8b4debe2b9d"
}

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()


def downloadData():
    while True:
        toado_x = db.child("Coordinates").child("x").get()
        toado_y = db.child("Coordinates").child("y").get()
        toado_z = db.child("Coordinates").child("z").get()
        vanToc = db.child("SPEED").child("Speed").get()
        huongGio = db.child("SPEED").child("Direction").get()

        return (toado_x.val(), toado_y.val(), toado_z.val(), vanToc.val(), huongGio.val())


def calculator():
    x, y, z, v, t = downloadData()

    denta1 = sqrt(pow((8 * x / 9 - 5), 2) + pow((8 * y / 9), 2) + pow((8 * z / 9), 2))
    denta2 = sqrt(pow((16 * x / 27 - 5), 2) + pow((16 * y / 27), 2) + pow((16 * z / 27), 2))
    denta3 = sqrt(pow((8 * x / 27 - 5), 2) + pow((8 * y / 27), 2) + pow((8 * z / 27), 2))
    denta4 = sqrt(pow((8 * x / 27 + 2.5), 2) + pow((8 * y / 27 - 4.333), 2) + pow((8 * z / 27), 2))
    denta5 = sqrt(pow((16 * x / 27 + 2.5), 2) + pow((16 * y / 27 - 4.333), 2) + pow((16 * z / 27), 2))
    denta6 = sqrt(pow((8 * x / 9 + 2.5), 2) + pow((8 * y / 9 - 4.333), 2) + pow((8 * z / 9), 2))
    denta7 = sqrt(pow((8 * x / 27 + 2.5), 2) + pow((8 * y / 27 + 4.333), 2) + pow((8 * z / 27), 2))
    denta8 = sqrt(pow((16 * x / 27 + 2.5), 2) + pow((16 * y / 27 + 4.333), 2) + pow((16 * z / 27), 2))
    denta9 = sqrt(pow((8 * x / 9 + 2.5), 2) + pow((8 * y / 9 + 4.33), 2) + pow((8 * z / 9), 2))

    F1 = E * denta1 * A / l
    F2 = E * denta2 * A / l
    F3 = E * denta3 * A / l
    F4 = E * denta4 * A / l
    F5 = E * denta5 * A / l
    F6 = E * denta6 * A / l
    F7 = E * denta7 * A / l
    F8 = E * denta8 * A / l
    F9 = E * denta9 * A / l

    return F1, F2, F3, F4, F5, F6, F7, F8, F9

    # print(anpha)
    # print(status)  # push data len firebase luon chu khong return nua sua do dung threading
    # db.child("Status").set(status)


# def WriteData():
# fieldnames = ["x", "y", "z", "Speed"]

# with open('data.csv', 'w') as csv_file:
#     csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     csv_writer.writeheader()

# while True:
#     with open('data.csv', "a+") as csv_file:
#         csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#
#         toado_x, toado_y, toado_z, vanToc = downloadData()
#
#         info = {
#             "x": toado_x,
#             "y": toado_y,
#             "z": toado_z,
#             "Speed": vanToc
#         }
#
#         csv_writer.writerow(info)
#         calculator(toado_x,toado_y,toado_z,vanToc)
#         # print(toado_x, toado_y, toado_z, vanToc)
#     time.sleep(1)


# if __name__ == '__main__':
#     # x,y,z,v = downloadData()
#     # threading.Thread(target=WriteData).start()
#     # threading.Thread(target = calculator, args=(x,y,z,v,)).start()
#     # print(x,y,z,v)
#     WriteData()
if __name__ == '__main__':
    pass

# while True:
#     F1, F2, F3, F4, F5, F6, F7, F8, F9 = calculator()
#     print(F1, F2, F3, F4, F5, F6, F7, F8, F9)
#     time.sleep(5)
