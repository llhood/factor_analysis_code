import os
import numpy as np
import pandas as pd
import openpyxl as xl
import sys
sys.path.append("../../../PUBLIC_CLASS")
from ProcessBar import process_bar

# 数据为1000倍

# 获取时间数据
date_list = []
for root, dirs, files in os.walk("../../../DATABASE/StockPrice/stock_lgtratio_cn_raw_csv_北向资金交易额占比"):
    date_list.append(files)
date_list = np.unique([i.split(".")[1] for i in date_list[0]])
date_list = np.sort(date_list)

# 合成一级行业平均流入比率
name_list = pd.read_csv("../../../DATABASE/IndustryIndex/中信行业指数/中信二级行业指数_收盘价_日频_Wind.csv").columns[1:]
out_mat = np.ones((len(date_list), len(name_list))) - 1

for row in range(len(date_list)):
    print(process_bar(row,len(date_list)), len(name_list))
    date_name = date_list[row]

    df_info_i = pd.read_csv("../../../DATABASE/StockPrice/stock_info_csv/stock_info.%s.csv"%date_name,
        encoding="gbk", dtype={"id":str})
    df_lgtr_i = pd.read_csv(
        "../../../DATABASE/StockPrice/stock_lgtratio_cn_raw_csv_北向资金交易额占比/lgtratio_cn_raw.%s.csv"%date_name,
        header=None, dtype={0:str})
    df_stock_prc = pd.read_csv(
        "../../../DATABASE/StockPrice/stock_daily_csv/stock_daily.%s.csv"%date_name,
        dtype={"id":str})

    df_stock_prc = df_stock_prc[["id","close","totalshr"]]
    df_stock_prc["MktVal"] = df_stock_prc["close"].to_numpy() * df_stock_prc["totalshr"].to_numpy()

    for col in range(len(name_list)):
        index_name_i = name_list[col]
        df_info_i_col = df_info_i[df_info_i["indzx2_name"]==index_name_i]
        if df_info_i_col.shape[0] == 0: continue
        df_info_validstk = df_info_i_col["id"].to_numpy()

        df_lgtr_i_valid = df_lgtr_i[df_lgtr_i[0].isin(df_info_validstk)]
        df_lgtr_i_valid.columns = ["id","AmtPct"]
        df_lgtr_i_valid = pd.merge(df_lgtr_i_valid, df_stock_prc, how="left", on="id")

        amtpct_temp = df_lgtr_i_valid["AmtPct"].to_numpy()
        mktval_temp = df_lgtr_i_valid["MktVal"].to_numpy()
        
        out_mat[row,col] = np.nansum(amtpct_temp * mktval_temp / np.nansum(mktval_temp))

out_mat = pd.DataFrame(out_mat)
out_mat.columns = name_list
date_list_str = [str(i)[:4]+"/"+str(i)[4:6]+"/"+str(i)[6:] for i in date_list]
for i in range(len(date_list_str)):
    if date_list_str[i][5] == "0":
        date_list_str[i] = date_list_str[i][:5] + date_list_str[i][6:]
out_mat.insert(0,"Date",date_list_str)
out_mat.to_csv("Factor/A2_lgtratio_level2.csv", index=None, encoding="gbk")