# -*- coding: utf-8 -*-
"""
@author: dell
@email: limin93@ihep.ac.cn
@file: read_root.py
@time: 2023/2/1019:48
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import uproot as up
from matplotlib import colors
import time
import matplotlib.dates as mdate
from matplotlib.ticker import MultipleLocator
from pandas import DataFrame
import datetime
import dateutil
plt.style.use("./mystyle.txt")
def read_root_ana(path):
    result_time = []
    result_peak = []
    result_pe = []
    result_amp = []
    result_rt = []
    result_ft = []
    result_ht = []
    result_fwhm = []
    result_width = []
    for i in range(4):
        channel_tree = "Wave_channel" + str(i)
        time_num = "time_channel_" + str(i)
        peak_num = "peak_channel_" + str(i)
        amp_num = "risetime_channel" + str(i)
        pe_num = "pe_channel_" + str(i)
        rt_num = "risetime_channel" + str(i)
        ft_num = "falltimetime_channel" + str(i)
        ht_num = "hittime_channel" + str(i)
        fwhm_num = "fwhm_channel" + str(i)
        width_num = "width_channel" + str(i)
        with up.open(path) as f:
                time_num = np.array(f[channel_tree]["file_time"]).tolist()[:-1]
                peak_num = np.array(f[channel_tree]["peak_num"]).tolist()[:-1]
                amp_num = np.array(f[channel_tree]["amplitude"]).tolist()[:-1]
                pe_num = np.array(f[channel_tree]["pe"]).tolist()[:-1]
                rt_num = np.array(f[channel_tree]["risetime"]).tolist()[:-1]
                ft_num = np.array(f[channel_tree]["falltime"]).tolist()[:-1]
                ht_num = np.array(f[channel_tree]["hittime"]).tolist()[:-1]
                fwhm_num = np.array(f[channel_tree]["FWHM"]).tolist()[:-1]
                width_num = np.array(f[channel_tree]["width_bottom"]).tolist()[:-1]
        result_time.append(time_num)
        result_peak.append(peak_num)
        result_amp.append(amp_num)
        result_pe.append(pe_num)
        result_rt.append(rt_num)
        result_ft.append(ft_num)
        result_ht.append(ht_num)
        result_fwhm.append(fwhm_num)
        result_width.append(width_num)

    for i,item in enumerate(result_width):
        for j, jitem in  enumerate(item):
            if jitem > 300:
                print(i, j, jitem)
    return result_time, result_pe, result_amp, result_rt, result_ft, result_ht,result_fwhm,result_width

def read_data_transfer_time(data_time):
    time_list = []
    for item in data_time:
        time_local = time.localtime(item)
        time_transfer  = time.strftime("%m-%d %H:%M:%S", time_local) #unix时间转化为分钟表示
        #print(time_transfer)
        time_list.append(time_transfer)
    return time_list

def read_data_draw_hist1d(data, bin,xrange):
    #print(data[1])
    ax = plt.axes(xlim=[0, 1000], yscale="log", xlabel="pe", ylabel="# of events [/1]")
    plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)
    for i in range(4):
        plt.hist(data[i], bins=bin, range =xrange)
    plt.show()

def read_data_draw_hist2d(data, bin,xrange):
    ax = plt.axes(xlim=[0, 200],xlabel="pe", ylabel="# of events [/1]")
    plt.subplots_adjust(left=0.12, right=0.98, top=0.95, bottom=0.12)
    h = plt.hist2d(result[1][0], result[1][1], bins=bin,range= xrange, norm = colors.LogNorm())
    plt.colorbar(h[3])
    plt.show()
def read_data_draw_2D2(data_x, data_y,xlabel, ylabel):
    for i in range(4):
        time_list = []
        para_list = []
        for j, jitem in enumerate(zip(data_x[i],data_y[i])):
            for k, kitem in enumerate(jitem):
                if k !=0:
                    for i,item in enumerate(kitem):
                        para_list.append(item)
                if k == 0:
                    # print(len(jitem[1]))
                    itime_list = [kitem] * len(jitem[1])
                    for t,titem in enumerate(itime_list):
                        time_list.append(titem)
        result_info = zip(time_list, para_list)
        result_info_sort = sorted(result_info)
        time_info = [x[0]  for x in result_info_sort]
        para_info = [x[1] for x in result_info_sort]
        ##Cauculate time difference
        ##time_info_inter = [x - time_info[0] for x in time_info]
        ##time format transfer
        timeArray = [time.localtime(one) for one in time_info]
        datestrings = [time.strftime("%H:%M:%S", one) for one in timeArray]
        data_time_list = {"time_local": datestrings}
        data_time = DataFrame(data_time_list)
        para_info_list = {"data" : para_info}
        data_para = DataFrame(para_info_list)
        data_merge = pd.concat([data_time, data_para], axis=1)
        # print(data_merge)
        # data_merge.to_csv("merge.csv")
        ax = plt.axes(xlabel=xlabel, ylabel=ylabel)
        plt.subplots_adjust(left=0.12, right=0.95, top=0.95, bottom=0.15)
        plt.scatter(data_merge["time_local"], data_merge["data"],s=4)
        x = MultipleLocator(200)  # x轴每10一个刻度
        ax.xaxis.set_major_locator(x)
        plt.xticks(rotation=30, fontsize=12)
    plt.show()
def read_data_draw_2D1(data_x, data_y,xlabel, ylabel):
    ax = plt.axes(xlabel=xlabel, ylabel=ylabel)
    plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.12)
    for i in range(4):
        time_list = []
        para_list = []
        for j, jitem in enumerate(zip(data_x[i], data_y[i])):
            for k, kitem in enumerate(jitem):
                if k == 0:
                    time_list.append(kitem)
                else:
                    para_list.append(kitem)
        result_info = zip(time_list, para_list)
        result_info_sort = sorted(result_info)
        time_info = [x[0] for x in result_info_sort]
        para_info = [x[1] for x in result_info_sort]
        timeArray = [time.localtime(one) for one in time_info]
        datestrings = [time.strftime("%H:%M:%S", one) for one in timeArray]
        data_time_list = {"time_local": datestrings}
        data_time = DataFrame(data_time_list)
        para_info_list = {"data": para_info}
        data_para = DataFrame(para_info_list)
        data_merge = pd.concat([data_time, data_para], axis=1)
        data_merge.to_csv("merge.csv")
        ax = plt.axes(xlabel=xlabel, ylabel=ylabel)
        plt.subplots_adjust(left=0.12, right=0.95, top=0.95, bottom=0.15)
        plt.scatter(data_merge["time_local"], data_merge["data"], s=4)
        x = MultipleLocator(200)  # x轴每10一个刻度
        ax.xaxis.set_major_locator(x)
        plt.xticks(rotation=30, fontsize=12)
    plt.show()

if __name__ == '__main__':
    filepath = "/junofs/users/limin93/Large_photomultiplier_Tube/flasher/data/20230130camera/2023-1-30_2st.root"
    #filepath = "2023-1-30_2st.root"
    result = read_root_ana(filepath)
    #########################################################################################
    bin = 1000
    xrange=(0,1000)
    read_data_draw_hist1d(result[1],bin,xrange)
    ##########################################################################################
    bin = 200
    xrange = [[0,200], [0,200]]
    read_data_draw_hist2d(result[1], bin, xrange)
    #read_data_draw_hist2d(result[1], bin, xrange)
    ##########################################################################################
    xlabel = "Time"
    ylabel ="Amplitue"
    read_data_draw_2D2(result[0],result[2],xlabel, ylabel)
    ##########################################################################################
    xlabel = "Time"
    ylabel = "pe"
    read_data_draw_2D1(result[0], result[1],xlabel, ylabel)
    ##########################################################################################
    #    return result_time, result_pe, result_amp, result_rt, result_ft,result_ht,result_fwhm,result_width
    xlabel = "Time"
    ylabel = "Risetime [ns]"
    read_data_draw_2D2(result[0], result[3], xlabel, ylabel)
    # ##########################################################################################
    xlabel = "Time"
    ylabel = "Falltime [ns]"
    read_data_draw_2D2(result[0], result[4], xlabel, ylabel)
    # ##########################################################################################
    xlabel = "Time"
    ylabel = "Hittime [ns]"
    read_data_draw_2D2(result[0], result[5], xlabel, ylabel)
    # ##########################################################################################
    xlabel = "Time"
    ylabel = "FWHM [ns]"
    read_data_draw_2D2(result[0], result[6], xlabel, ylabel)
    # ##########################################################################################
    xlabel = "Time"
    ylabel = "Width bottom [ns]"
    read_data_draw_2D1(result[0], result[7], xlabel, ylabel)
