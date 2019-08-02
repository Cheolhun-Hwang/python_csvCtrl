import pandas as pd
import numpy as np
import os

path = "./Datasets/raws/"
remakePath = "./Datasets/Remake/"
savePath = './Datasets/ships/'

resultPath = './Results/'
resultFile = 'results.csv'

def reMakeFile(file):
    count = 0
    print('##### read original file #####')
    f = open(path+file, 'r')
    for s in f:
        if(count < 2):
            print("removing column : " + str(count))
            count = count + 1
        else :
            # print(s, end='')
            saveFile = open(remakePath+file, 'a')
            saveFile.write(s)
            saveFile.close()
    f.close()

def splitShipData(file):
    df = pd.read_csv(remakePath + file, encoding='utf-8')
    print(df.head())

    df.columns = ["MMSI", "TIME", "LONG", "LAT", "SOG", "COG", "HEADING"]

    ship_list = df.MMSI.unique()
    print(ship_list)

    for ship_name in ship_list:
        print("Ship Name : " + str(ship_name))
        ship_data = df.loc[df['MMSI'] == ship_name]

        third_Speed(ship_data, ship_name)

        if ship_name == (str(ship_name)+'.csv'):
            with open(savePath+str(ship_name)+".csv", 'a') as f:
                ship_data.to_csv(f, header=False, index=False)
        else :
            ship_data.to_csv(savePath+str(ship_name)+".csv", header=True, index=False)

def first_Remake():
    for root, dirs, files in os.walk(path):
        for file in files:
            print("file name : " + path + file)
            reMakeFile(file)

def second_Split():
    for root, dirs, files in os.walk(remakePath):
        for file in files:
            print("file name : " + remakePath + file)
            splitShipData(file)

def third_Speed(ship_data, ship_name):     ## ship_data is DataFrame
    from datetime import datetime
    from haversine import haversine

    print(ship_data.head())

    head_row = ship_data.head(1)
    last_row = ship_data.tail(1)

    depart = (head_row['LONG'].iloc[0], head_row['LAT'].iloc[0])
    endpoint = (last_row['LONG'].iloc[0], last_row['LAT'].iloc[0])
    Distance = haversine(depart, endpoint)


    test_time = pd.to_datetime(ship_data['TIME'], infer_datetime_format=True)
    print(test_time.head())

    time_start = test_time.head(1).iloc[0]
    time_end = test_time.tail(1).iloc[0]

    print("Start : " + str(time_start) + "/ End : " + str(time_end))

    Time = (time_end-time_start).seconds / 3600

    print("Distance : " + str(Distance))
    print("hourly Time : " + str(Time))

    if( (Distance == 0.0) | (Time == 0.0)) :
        speed = 0
    else:
        speed = (Distance / Time)

    saveResult(ship_name, time_start, time_end, Time, Distance, speed)

def saveResult(ship_name, time_start, time_end, Time, Distance, speed):
    saveFile = open(resultPath + resultFile, 'a')
    saveFile.write(str(ship_name)+','+str(time_start)+','+str(time_end)
                   +','+str(Time)+','+str(Distance)+','+str(speed)+'\n')
    saveFile.close()

# first_Remake()
second_Split()