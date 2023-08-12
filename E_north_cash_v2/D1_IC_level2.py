import pandas as pd
import numpy as np
import sys
sys.path.append("../../../PUBLIC_CLASS")
from Factor_Evaluation_Industry_level2 import *
from Split_Date_List import get_simulation_points
from Factor_IC_level2 import *

name = "北向资金II级"
df_PE = pd.read_csv("Factor/B2_Mthly_lgtrationsum_level2.csv", encoding="gbk").iloc[4:,:]
# df_PE = pd.read_csv("G_factor_SplitNumber.csv")

df_idty = pd.read_csv(
    "../../../DATABASE/IndustryIndex/中信行业指数/中信二级行业指数_收盘价_日频_Wind.csv"
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

rankIC_df = IC_evaluate(rankIC_arr)

df_rankIC = pd.DataFrame(rankIC_arr)
df_rankIC.insert(0, "Date", date_list[1:])
df_rankIC["rankIC_cumsum"] = np.cumsum(rankIC_arr)


# output

df_rankIC.to_excel("result/%s因子rankIC值_level2.xlsx"%(name), index=None)

rankIC_df.to_excel("result/%s因子rankIC值绩效分析_level2.xlsx"%(name), index=None)
