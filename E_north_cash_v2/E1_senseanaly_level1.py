import os
import numpy as np
import pandas as pd
import openpyxl as xl
import sys
sys.path.append("../../../PUBLIC_CLASS")
from ProcessBar import process_bar
from Split_Date_List import get_simulation_points
from Factor_Evaluation_Industry_level1 import *
from Factor_IC_level1 import *

for lookback in [5,10,15,20,25,30,35,40,50,60,80,100]:

    df_factor = pd.read_csv("Factor/A1_lgtratio_level1.csv", encoding="gbk")
    date_list = df_factor.iloc[:,0].to_numpy()
    date_idx = get_simulation_points(date_list, "Monthly", "/")

    out_mat = []
    date_out = []
    for col in range(1,len(date_idx)):
        if date_idx[col]-lookback < 0: continue
        df_temp = df_factor.iloc[(date_idx[col]-lookback):date_idx[col],1:].to_numpy()
        out_mat.append(np.nansum(df_temp, axis=0))
        date_out.append(date_list[date_idx[col]])

    out_mat = pd.DataFrame(out_mat)
    out_mat.columns = df_factor.columns[1:]
    out_mat.insert(0,"Date",date_out)
    out_mat.to_csv("Factor/B1_Mthly_lgtrationsum_level1.csv", encoding="gbk", index=None)
    #################
    ## Get IC
    ###################
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

    name_list = df_PE.columns[1:]

    # IC Evaluation
    df_idty_rtn = get_return(df_idty.iloc[:,1:].to_numpy())

    rankIC_arr = get_rankIC(df_idty_rtn, df_PE.iloc[:,1:].to_numpy())

    rankIC_df = IC_evaluate(rankIC_arr, return_df = False)[2]

    print(lookback)
    print(rankIC_df)