# -*- coding: utf-8 -*-
"""
@author: Min
@email: limin93@ihep.ac.cn
@file: read_rawdata_to_waveform.py
@time: 2022/11/21 10:06
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
plt.style.use("./mystyle.txt")

def read_data_transfer_time(data_time):
    time_list = []
    for item in data_time:
        time_local = time.localtime(item)
        time_transfer  = time.strftime("%m-%d %H:%M:%S", time_local) #unix时间转化为分钟表示
        #print(time_transfer)
        time_list.append(time_transfer)
    return time_list

def read_single_event_to_draw(data):
    plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.15)
    ax = plt.axes(xlabel="Time [ns]", ylabel="Waveform [mv]",xlim=(0, 1007),ylim=(-1000,  10))  # xlim =["07-24 15:37", "07-25 10:48"],
    #print(data["PMT1"])
    time = np.arange(0, 1008, 1)
    plt.plot(time, data["PMT1"] *0.1,label="SPMT1")
    plt.plot(time, data["PMT2"] * 0.1,label="SPMT2")
    plt.plot(time, data["PMT3"] ,label="LPMT1")
    plt.plot(time, data["PMT4"] ,label="LPMT2")
    plt.legend()
    plt.savefig("single_3354.jpg")
    plt.show()

def read_data_to_trigger(rawdata):
    mean_value1 = rawdata.iloc[0:101, :]  # 求基线，前100ns的均值
    # print(mean_value1)
    mean_value = pd.DataFrame(mean_value1.values.T, index=mean_value1.columns, columns=mean_value1.index)
    mean_value["avg"] = mean_value.mean(axis=1)
    # print(mean_value)
    # print(mean_value.loc["SPMT1","avg"])
    min_value1 = rawdata.iloc[101:1000, :]  # 求最小值
    min_value = pd.DataFrame(min_value1.values.T, index=min_value1.columns, columns=min_value1.index)
    min_value["min"] = min_value.min(axis=1)
    # print(min_value)
    spmt1_amplitude_value = mean_value.loc["PMT1", "avg"] - min_value.loc["PMT1", "min"]
    spmt2_amplitude_value = mean_value.loc["PMT2", "avg"] - min_value.loc["PMT2", "min"]
    lpmt1_amplitude_value = mean_value.loc["PMT3", "avg"] - min_value.loc["PMT3", "min"]
    lpmt2_amplitude_value = mean_value.loc["PMT4", "avg"] - min_value.loc["PMT4", "min"]
    return [spmt1_amplitude_value, spmt2_amplitude_value], [lpmt1_amplitude_value, lpmt2_amplitude_value]

def read_rawdata(path1, path2):
    df = pd.read_csv(path1, names=["PMT1", "PMT2", "PMT3", "PMT4"], sep="\t")
    #print(df)
    #print(len(df["PMT1"])/1008)
    #print(list(df[:1008].index))
    # for item in range(0, len(df["PMT1"]), 1008):
    #     #print(item)
    #     #print(item / 1008)
    #     if item / 1008 == 438:
    #         print(item)
    #         print(df[item:item+1008])
    #         data = df[item:item+1008]
    #         #read_single_event_to_draw(data)
    df_time = pd.read_csv(path2, names=["file","time","SPMT1","SPMT2","LPMT1","LPMT2"], sep="\t")
    #print(df_time)
    data_time_transfer = read_data_transfer_time(df_time["time"])
    #print(data_time_transfer)
    for i, itime in enumerate(data_time_transfer):
        #if itime > '01-30 11:10' and  itime < '01-30 11:20':
        if i == 1562:
            #print(i, itime, df_time.loc[i, "file"])
            data = df[1008*i: 1008*(i+1)]
            print(data)

            result = read_data_to_trigger(data)
            #print(result)

            if any(ele > 6 for ele in result[0]) or any(ele > 2 for ele in result[1]):
                print(i)
                print(i, itime, df_time.loc[i, "file"])
                read_single_event_to_draw(data)





if __name__ == '__main__':
    # filepath1 = "/junofs/users/limin93/Large_photomultiplier_Tube/flasher/data/20230130camera/2023-1-30_2st.txt"
    # filepath2 = "/junofs/users/limin93/Large_photomultiplier_Tube/flasher/data/20230130camera/time/2023-1-30_2st.txt"
    filepath1 = "H:/LPMT_Flasher/Camera/2023-1-30_2st.txt"
    filepath2 = "2023-1-30_2st.txt"
    read_rawdata(filepath1,filepath2)
