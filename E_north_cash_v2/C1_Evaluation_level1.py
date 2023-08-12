from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd
sys.path.append("../../../PUBLIC_CLASS")
from Factor_Evaluation_Industry_level1 import *

name = "北向资金I级"
df_PE = pd.read_csv("Factor/B1_Mthly_lgtrationsum_level1.csv", encoding="gbk")
# df_PE = pd.read_csv("G_factor_SplitNumber.csv")

df_idty = pd.read_csv(
    "../../../DATABASE/IndustryIndex/中信行业指数/中信一级行业指数_收盘价_日频_Wind.csv"
)

# get valid date
date_list = df_PE.iloc[:,0].to_numpy()

df_idty_date = [i.replace("-","/") for i in df_idty.iloc[:,0].to_numpy()]
date_idx = [i for i in range(df_idty.shape[0]) if df_idty_date[i] in date_list]
df_idty = df_idty.iloc[date_idx,:].reset_index(drop=True)

# get global variable
split_num = 5
freq = 12
df_score, df_out = auto_run(df_idty.iloc[:,1:].to_numpy(), 
        df_PE.iloc[:,1:].to_numpy(), split_num, freq, date_list)

temp = df_score.iloc[:,1].tolist()
best_idx = temp.index(np.max(temp))

df_score_group1 = yearly_eval_group1(date_list,
                    df_idty.iloc[:,1:].to_numpy(),
                    df_PE.iloc[:,1:].to_numpy(), split_num, freq, best_idx)

name_list = df_PE.columns[1:]
df_hist_posi = historical_position(df_PE.iloc[:,1:].to_numpy(), name_list, split_num, date_list, best_idx)

# output
df_out.to_excel("result/%s因子分%d层组合回测净值.xlsx"%(name,split_num), index=None)
df_score_group1.to_excel("result/%s因子分%d层组合多组回测净值.xlsx"%(name,split_num), index=None)
df_score.to_excel("result/%s因子分%d层组合绩效分析.xlsx"%(name,split_num), index=None)
df_hist_posi.to_excel("result/%s因子分%d层组合历史持仓.xlsx"%(name,split_num), index=None, encoding="gbk")

portf_rtn = split_portfolio_return(df_idty.iloc[:,1:].to_numpy(), 
        df_PE.iloc[:,1:].to_numpy(), split_num)
temp = portf_rtn[:,0] - portf_rtn[:,portf_rtn.shape[1]-1]
pd.DataFrame({
    "日期": date_list[1:],
    "%s因子多空组收益率"%name: temp,
    "多空组累计收益率": np.cumsum(temp)}).to_excel("result/%s因子分%d层多空组收益率及累计收益率.xlsx"%(name,split_num), index=None)

df_score.iloc[:,[0,1,3,7]].to_excel("result/%s因子分%d层组合绩效指标对比图示.xlsx"%(name,split_num), index=None)

