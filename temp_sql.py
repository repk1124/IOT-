import mysql.connector
from mysql.connector import Error
import random
import time
import os

try:
    # 連接 MySQL/MariaDB 資料庫
    connection = mysql.connector.connect(
        host='100.100.100.100', # 主機名稱
        database='temp', # 資料庫名稱
        user='OOO', # 帳號
        password='XXX')  # 密碼
    while True:
        temp = round(random.uniform(20, 40), 2)
        humi = round(random.uniform(0, 100), 2)
        currentTime = time.strftime("%H:%M:%S")

        # 新增資料
        sql = "INSERT INTO sensor (humidity, temperature, time) VALUES (%s, %s, %s);"
        new_data = (humi,temp,currentTime)
        cursor = connection.cursor()
        cursor.execute(sql, new_data)
        print(humi, temp, currentTime)
        time.sleep(10)
        # 確認資料有存入資料庫
        connection.commit()

except Error as e:
    print("資料庫連接失敗：", e)

finally:
    if (connection.is_connected()):
        cursor.close()
        connection.close()
os.system("pause")
