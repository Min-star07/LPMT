# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import *


fig1 = plt.figure(figsize=(12,9))
# file_path =("D:/工作报告/江门LPMT测试总结/PMT测试数据库/rawdata/potting_containerab.csv")
# file_path =("D:/工作报告/江门LPMT测试总结/PMT测试数据库/rawdata/potting_containerd.csv")
file_path =("D:/工作报告/江门LPMT测试总结/PMT测试数据库/rawdata/lpmt_juno_list.csv")
data = pd.read_csv(file_path, sep=",", engine="python")

raw_data= data.loc[(data["Resolution"]<100) & (data["Resolution"]>0)]
raw_data_nnvt = data.loc[(data["MCP_Hama"] == 1) & (data["Resolution"]<100) & (data["Resolution"]>0)]
raw_data_hpk = data.loc[(data["MCP_Hama"] ==0) & (data["Resolution"]<100) & (data["Resolution"]>0)]
raw_data_nnvt_High = data.loc[(data["MCP_Hama"] == 1) & (data["HiQE_MCP"] == 1) & (data["Resolution"]<100) &(data["Resolution"]>0)]
raw_data_nnvt_Low = data.loc[(data["MCP_Hama"] == 1) & (data["HiQE_MCP"] == 0) & (data["Resolution"]<100) &(data["Resolution"]>0)]

resolution_tested_all=raw_data["Resolution"]*100
resolution_tested_nnvt=raw_data_nnvt["Resolution"]*100
resolution_tested_hpk=raw_data_hpk["Resolution"]*100
resolution_tested_nnvt_high=raw_data_nnvt_High["Resolution"]*100
resolution_tested_nnvt_low=raw_data_nnvt_Low["Resolution"]*100

num_raw_all = len(raw_data)
num_raw_nnvt = len(raw_data_nnvt)
num_raw_hpk = len(raw_data_hpk)
num_raw_nnvt_High = len(raw_data_nnvt_High)
num_raw_nnvt_Low = len(raw_data_nnvt_Low)

resolution_tested_all_mean = resolution_tested_all.mean()
resolution_tested_all_std = resolution_tested_all.std()
resolution_tested_nnvt_mean = resolution_tested_nnvt.mean()
resolution_tested_nnvt_std = resolution_tested_nnvt.std()
resolution_tested_hpk_mean = resolution_tested_hpk.mean()
resolution_tested_hpk_std = resolution_tested_hpk.std()
resolution_tested_nnvt_high_mean = resolution_tested_nnvt_high.mean()
resolution_tested_nnvt_high_std = resolution_tested_nnvt_high.std()
resolution_tested_nnvt_low_mean = resolution_tested_nnvt_low.mean()
resolution_tested_nnvt_low_std = resolution_tested_nnvt_low.std()

bin=80
xrange=(0,80)
plt.hist(resolution_tested_all, bins=bin, range=xrange, density=False, color="k", linewidth=3, histtype="step",   label = 'ALL:%.1f ± %.1f%%' %(resolution_tested_all_mean,resolution_tested_all_std))
plt.hist(resolution_tested_nnvt, bins=bin, range=xrange, density=False, color="r", linewidth=3, histtype="step",  label = 'NNVT: %.1f ± %.1f%%' %(resolution_tested_nnvt_mean,resolution_tested_nnvt_std))
plt.hist(resolution_tested_hpk, bins=bin, range=xrange, density=False, color="b", linewidth=3, histtype="step",  label = 'HPK:%.1f ± %.1f%%' %(resolution_tested_hpk_mean,resolution_tested_hpk_std))

ax=plt.gca();#获得坐标轴的句柄
ax.spines['bottom'].set_linewidth(2);###设置底部坐标轴的粗细
ax.spines['left'].set_linewidth(2);####设置左边坐标轴的粗细
ax.spines['right'].set_linewidth(2);###设置右边坐标轴的粗细
ax.spines['top'].set_linewidth(2);####设置上部坐标轴的粗细
plt.subplots_adjust(left=0.15, bottom=0.15, right=0.95, top=0.95, wspace=0, hspace=0)
plt.xlim(0, 80)
ax.tick_params(axis='both', which='major',labelsize=30, pad=15)
ax.tick_params(axis='both', which='minor',labelsize=30, pad=15)
plt.xlabel("resolution [%]",fontsize = 30)
plt.ylabel("# of PMTs [/1%]",fontsize = 30)
plt.legend(fontsize = 28)
ax.tick_params(direction='in', length=10, width=2, colors='k',grid_color='k', grid_alpha=0.1)
plt.savefig('Resolution_Tested.jpg',dpi=300)
plt.show()
