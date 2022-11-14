import math
import time
from math import *

import pyrebase

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
    # while True:
    toado_x = db.child("Coordinates").child("x").get()
    toado_y = db.child("Coordinates").child("y").get()
    toado_z = db.child("Coordinates").child("z").get()
    vanToc = db.child("SPEED").child("Speed").get()
    huongGio = db.child("SPEED").child("Direction").get()

    x0 = toado_x.val()
    y0 = toado_y.val()
    z0 = toado_z.val()
    v = vanToc.val()
    t0 = huongGio.val()

    x = l * sin((y0 / 180) * math.pi)
    y = l * sin((x0 / 180) * math.pi)
    z = l - l * cos((x0 / 180) * math.pi)

    if (t0 >= 4 and t0 < 6.2857):
        t = 'B'
    elif (6.2857 <= t0 and t0 < 8.5714):
        t = 'DB'
    elif (8.5714 <= t0 and t0 < 10.8571):
        t = 'D'
    elif (10.8571 <= t0 and t0 < 13.1429):
        t = 'DN'
    elif (13.1429 <= t0 and t0 < 15.4286):
        t = 'N'
    elif (15.4286 <= t0 and t0 < 17.7143):
        t = 'TN'
    elif (17.7143 <= t0 and t0 < 20):
        t = 'T'
    else:
        t = 'TB'

    return round(x, 3), round(y, 3), round(z, 3), round(v, 3), t


def calculator():
    x, y, z, v, t = downloadData()

    # cần phải xác định được lực dựa vào tốc độ gió
    Fc1 = 10 * v  # do gió tác dụng phân bố không đều => tìm độ lớn lực theo độ cao
    Fc2 = 8 * v
    Fc3 = 5 * v

    # Góc giữa dây co và cột BTS
    anpha0 = math.atan(5 / (l - 3))
    anpha01 = math.atan(5 / (l - 9))
    anpha02 = math.atan(5 / (l - 15))

    # góc giữa lực trên mặt cắt ngang so với lực kéo dây co
    beta = math.pi / 2 - anpha0
    beta1 = math.pi / 2 - anpha01
    beta2 = math.pi / 2 - anpha02

    # tính góc của lực do gió tác dụng
    if t == 'B':
        anpha = 0
        anpha1 = math.pi / 3
        anpha2 = math.pi / 3
    if t == 'DB':
        anpha = math.pi / 4
        anpha1 = math.pi / 12
        anpha2 = math.pi * 7 / 12
    if t == 'D':
        anpha = math.pi / 2
        anpha1 = -math.pi / 6
        anpha2 = math.pi * 5 / 6
    if t == 'DN':
        anpha = math.pi * 3 / 4
        anpha1 = -math.pi * 5 / 12
        anpha2 = math.pi * 13 / 12
    if t == 'N':
        anpha = math.pi
        anpha1 = -math.pi * 2 / 3
        anpha2 = math.pi * 4 / 3
    if t == 'TN':
        anpha = math.pi * 5 / 4
        anpha1 = -math.pi * 11 / 12
        anpha2 = math.pi * 19 / 12
    if t == 'T':
        anpha = math.pi * 3 / 2
        anpha1 = -math.pi * 7 / 6
        anpha2 = math.pi * 11 / 6
    if t == 'TB':
        anpha = math.pi * 7 / 4
        anpha1 = -math.pi * 17 / 12
        anpha2 = math.pi * 25 / 12

    # tính lực hướng vào trọng tâm của cột vị trí cao nhất
    F1 = Fc1 * cos(anpha)
    F2 = Fc1 * cos(anpha1)
    F3 = Fc1 * cos(anpha2)
    # print(F1)

    # lực tác dụng lên cột ở vị trí cao thứ 2
    F4 = Fc2 * cos(anpha)
    F5 = Fc2 * cos(anpha1)
    F6 = Fc2 * cos(anpha2)
    # print(F5)

    # lực tác dụng lên cột ở vị trí cao thứ 3
    F7 = Fc3 * cos(anpha)
    F8 = Fc3 * cos(anpha1)
    F9 = Fc3 * cos(anpha2)
    # print(F9)

    # lực kéo đúng tâm với dây co ở đoạn cao nhất
    Nz1 = F1 * cos(beta)
    Nz2 = F2 * cos(beta)
    Nz3 = F3 * cos(beta)

    # lực kéo đúng tâm với dây co ở đoạn cao thứ 2
    Nz4 = F4 * cos(beta1)
    Nz5 = F5 * cos(beta1)
    Nz6 = F6 * cos(beta1)

    # lực kéo đúng tâm với dây co ở đoạn cao thứ 3
    Nz7 = F7 * cos(beta2)
    Nz8 = F8 * cos(beta2)
    Nz9 = F9 * cos(beta2)

    return abs(round(Nz1, 2)), abs(round(Nz2, 2)), abs(round(Nz3, 2)), abs(round(Nz4, 2)), abs(round(Nz5, 2)), abs(
        round(Nz6, 2)), abs(round(Nz7, 2)), \
           abs(round(Nz8, 2)), abs(round(Nz9, 2))


def calculatorCoor():
    pass


def calculatorWarn():
    x, y, z, v, t = downloadData()
    F1, F2, F3, F4, F5, F6, F7, F8, F9 = calculator()
    status = 'Normal'
    if (v > 32 and ((F1 > 51) or (F2 > 51) or (F3 > 51) or (F4 > 51) or (F5 > 51) or (F6 > 51))):
        status = 'Warning'
    else:
        status = 'Normal'
    return status

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
# if __name__ == '__main__':
#     print(atan(1))
# while True:
#     x, y, z, v, t = downloadData()
#     print(x, y, z, v, t)
#     time.sleep(3)

# while True:
#     F1, F2, F3, F4, F5, F6, F7, F8, F9 = calculator()
#     status = calculatorWarn()
#     print(status)
#     print(F1, F2, F3, F4, F5, F6, F7, F8, F9)
#     time.sleep(5)
# print(datetime.datetime.now())


