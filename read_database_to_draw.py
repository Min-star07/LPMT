# -*- coding: utf-8 -*-

"""
@author: Min
@email: limin93@ihep.ac.cn
@file: read_database_to_draw.py
@time: 2022/11/7 13:54
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#plt.style.use("./mystyle.txt")
import pymysql as ms
from scipy import optimize
from scipy.optimize import curve_fit
from matplotlib.colors import  LogNorm
def func(x,k):
    return k*x
def connect_database():
    db = ms.connect(user="root", passwd="Min08240707", host="127.0.0.1", port=3306, db="junopmt")
    #db = ms.connect(user="limin", passwd="123456", host="127.0.0.1", port=3306, db="qualifiedlpmt")
    cursor = db.cursor()
    try:
        sql = """show tables"""
        #sql = """select * from lpmt_veto_list where classification ='pole'""";
        #sql = """select SN, DCR from lpmt_juno_list """;
        cursor.execute(sql)
        data = cursor.fetchall()
        print(data)
        return data
    except:
        print("Connect database failed")
    cursor.close()
    db.close()
def draw_data_from_database(data):
    SN_list = []
    DCR_list =[]
    NNVT_list= []
    HPK_list = []
    for item in data:
        #print(item[0], item[1])
        SN_list.append(item[0])
        DCR_list.append(float(item[1]))
        if item[0].startswith("P"):
            NNVT_list.append(float(item[1]))
        if item[0].startswith("E"):
            HPK_list.append(float(item[1]))
    all_mean = np.mean(DCR_list)
    all_std = np.std(DCR_list)
    nnvt_mean = np.mean(NNVT_list)
    nnvt_std = np.std(NNVT_list)
    hpk_mean = np.mean(HPK_list)
    hpk_std = np.std(HPK_list)
    ax = plt.axes(xlabel=r"DCR [kHz]", ylabel="# of Tubes  [/1 kHz]", xlim=[0,100])
    xrange=(0,100)
    bins = 100
    plt.ylim(0,200)

    plt.hist(DCR_list, bins, xrange, histtype="step", linewidth=2,  label = "All: %.2f, STD:%.2f"%(all_mean, all_std))
    plt.hist(NNVT_list, bins, xrange, histtype="step",linewidth=2, label = "NNVT: %.2f, STD:%.2f"%(nnvt_mean, nnvt_std))
    plt.hist(HPK_list, bins, xrange, histtype="step", linewidth=2, label = "HPK: %.2f, STD:%.2f"%(hpk_mean, hpk_std))
    plt.legend(fontsize=20)
    plt.savefig("dcr.png")
    plt.show()


def draw_data_from_database_to_compare(data):
    SN_list =[]
    nnvt_bare_list = []
    nnvt_potted_list = []
    hpk_bare_list = []
    hpk_potted_list = []
    for item in data:
        if  item[2]  is not None:
            if item[0].startswith("P"):
                nnvt_bare_list.append(float(item[1]))
                nnvt_potted_list.append(float(item[2]))
            if item[0].startswith("E"):
                if float(item[2]) < 60:
                    hpk_bare_list.append(float(item[1]))
                    hpk_potted_list.append(float(item[2]))
    bin =100
    hist_2d = plt.hist2d(nnvt_bare_list, nnvt_potted_list,bins=bin,range= [[0.,100], [0.1,100]],norm =LogNorm() )
    #ax = plt.axes(xlabel=r"DCR_Bare [kHz]", ylabel=r"DCR_potted [kHz]")
    plt.colorbar(hist_2d[3])
    popt, pcov = optimize.curve_fit(func, nnvt_bare_list, nnvt_potted_list)

    XX = np.arange(0, 100)
    YY = popt[0] * XX
    plt.plot(XX, YY, c="r", linestyle="-", label="DCR_potted = %.2f * DCR_bare" % (popt[0]))
    #ax = plt.axes(xlabel=r"DCR bare [kHz]", ylabel=r"DCR potted [kHz]$")
    plt.legend(fontsize=20)
    plt.xlabel("Bare PMT [kHz]")
    plt.ylabel("Potted PMT [kHz]")
    plt.savefig("E:/江门20英寸PMT中山测试站数据/20221101_暗计数效应/图片/dcr_compare_2d_nnvt.png", dpi=200)
    plt.show()

    hist_2d = plt.hist2d(hpk_bare_list, hpk_potted_list, bins=bin, range=[[0., 100], [0.1, 100]], norm=LogNorm())
    # ax = plt.axes(xlabel=r"DCR_Bare [kHz]", ylabel=r"DCR_potted [kHz]")
    plt.colorbar(hist_2d[3])
    popt, pcov = optimize.curve_fit(func, hpk_bare_list, hpk_potted_list)

    XX = np.arange(0, 100)
    YY = popt[0] * XX
    plt.plot(XX, YY, c="r", linestyle="-", label="DCR_potted = %.2f * DCR_bare" % (popt[0]))
    plt.legend(fontsize=20)
    plt.xlabel("Bare PMT [kHz]")
    plt.ylabel("Potted PMT [kHz]")
    plt.savefig("E:/江门20英寸PMT中山测试站数据/20221101_暗计数效应/图片/dcr_compare_2d_hpk.png", dpi=200)
    plt.show()
if __name__ == '__main__':
    data_from_db = connect_database()
    #draw_data_from_database(data_from_db)
    #draw_data_from_database_to_compare(data_from_db)

