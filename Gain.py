# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import *

fig1 = plt.figure(figsize=(12,9))
# file_path =("D:/工作报告/江门LPMT测试总结/PMT测试数据库/rawdata/potting_containerd.csv")
file_path =("D:/工作报告/江门LPMT测试总结/PMT测试数据库/rawdata/potting_containerab.csv")
data = pd.read_csv(file_path, sep=",", engine="python")

raw_data= data.loc[(data["Gain_at_0_1pe"]<1.15E7) &(data["Gain_at_0_1pe"]>0.95e7)]
raw_data_nnvt = data.loc[(data["MCP_Hama"] == 1001) & (data["Gain_at_0_1pe"]<1.15E7) &(data["Gain_at_0_1pe"]>0.95e7)]
raw_data_hpk = data.loc[ (data["MCP_Hama"] == 1000) & (data["Gain_at_0_1pe"]<1.15E7) &(data["Gain_at_0_1pe"]>0.95e7)]
raw_data_nnvt_High = data.loc[(data["MCP_Hama"] == 1) & (data["HiQE_MCP"] == 1) & (data["Gain_at_0_1pe"]<1.15E7) &(data["Gain_at_0_1pe"]>0.95e7)]
raw_data_nnvt_Low = data.loc[(data["MCP_Hama"] == 1) & (data["HiQE_MCP"] == 0) & (data["Gain_at_0_1pe"]<1.15E7) &(data["Gain_at_0_1pe"]>0.95e7)]

gain_tested_all=raw_data["Gain_at_0_1pe"]
gain_tested_nnvt=raw_data_nnvt["Gain_at_0_1pe"]
gain_tested_hpk=raw_data_hpk["Gain_at_0_1pe"]
gain_tested_nnvt_high=raw_data_nnvt_High["Gain_at_0_1pe"]
gain_tested_nnvt_low=raw_data_nnvt_Low["Gain_at_0_1pe"]

num_raw_all = len(raw_data)
num_raw_nnvt = len(raw_data_nnvt)
num_raw_hpk = len(raw_data_hpk)
num_raw_nnvt_High = len(raw_data_nnvt_High)
num_raw_nnvt_Low = len(raw_data_nnvt_Low)

gain_tested_all_mean = gain_tested_all.mean()
gain_tested_all_std = gain_tested_all.std()
gain_tested_nnvt_mean = gain_tested_nnvt.mean()
gain_tested_nnvt_std = gain_tested_nnvt.std()
gain_tested_hpk_mean = gain_tested_hpk.mean()
gain_tested_hpk_std = gain_tested_hpk.std()
gain_tested_nnvt_high_mean = gain_tested_nnvt_high.mean()
gain_tested_nnvt_high_std = gain_tested_nnvt_high.std()
gain_tested_nnvt_low_mean = gain_tested_nnvt_low.mean()
gain_tested_nnvt_low_std = gain_tested_nnvt_low.std()

bin=200
xrange=(9e6, 1.2e7)
plt.hist(gain_tested_all, bins=bin, range=xrange,density=False, color="k", linewidth=3, histtype="step",label = 'ALL:%.2e ± %.2e' %(gain_tested_all_mean,gain_tested_all_std))
plt.hist(gain_tested_nnvt, bins=bin, range=xrange,density=False, color="r", linewidth=3, histtype="step",label = 'NNVT: %.2e ± %.2e' %(gain_tested_nnvt_mean,gain_tested_nnvt_std))
plt.hist(gain_tested_hpk, bins=bin, range=xrange,density=False,color="b", linewidth=3, histtype="step",label = 'HPK:%.2e ± %.2e' %(gain_tested_hpk_mean,gain_tested_hpk_std))

ax=plt.gca();#获得坐标轴的句柄
ax.spines['bottom'].set_linewidth(2);###设置底部坐标轴的粗细
ax.spines['left'].set_linewidth(2);####设置左边坐标轴的粗细
ax.spines['right'].set_linewidth(2);###设置右边坐标轴的粗细
ax.spines['top'].set_linewidth(2);####设置上部坐标轴的粗细
plt.subplots_adjust(left=0.15, bottom=0.15, right=0.95, top=0.95, wspace=0, hspace=0)

plt.xlabel("Gain",fontsize = 30)
plt.ylabel("# of PMTs ",fontsize = 30)
ax.tick_params(axis='both', which='major',labelsize=30, pad=15)
ax.tick_params(axis='both', which='minor',labelsize=30, pad=15)
plt.legend(fontsize = 28)
plt.xlabel(r"Gain [$1 \times 10^7$]", fontsize=30)
plt.ylabel(r"# of PMTs [$2 \times 10^4$] ", fontsize=30)
plt.legend(fontsize=20)
# plt.xticks(rotation=20)
plt.xticks([0.9e7, 0.95e7, 1.0e7, 1.05e7, 1.1e7, 1.15e7, 1.2e7],
           labels=["0.90", "0.95", "1.00", "1.05", "1.10", "1.15", "1.20"])
plt.xlim(9e6, 1.2e7)
ax.tick_params(direction='in', length=10, width=2, colors='k',grid_color='k', grid_alpha=0.1)
plt.savefig('Gain_Tested.jpg',dpi=300)
plt.show()


