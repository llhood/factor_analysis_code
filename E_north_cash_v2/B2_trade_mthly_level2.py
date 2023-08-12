import os
import numpy as np
import pandas as pd
import openpyxl as xl
import sys
sys.path.append("../../../PUBLIC_CLASS")
from ProcessBar import process_bar
from Split_Date_List import get_simulation_points
df_factor = pd.read_csv("Factor/A2_lgtratio_level2.csv", encoding="gbk")
date_list = df_factor.iloc[:,0].to_numpy()
date_idx = get_simulation_points(date_list, "Monthly", "/")

out_mat = []
for col in range(1,len(date_idx)):
    if date_idx[col]-20 < 0: continue
    df_temp = df_factor.iloc[(date_idx[col]-20):date_idx[col],1:].to_numpy()
    out_mat.append(np.nansum(df_temp, axis=0))

out_mat = pd.DataFrame(out_mat)
out_mat.columns = df_factor.columns[1:]
out_mat.insert(0,"Date",date_list[date_idx[1:]])
out_mat.to_csv("Factor/B2_Mthly_lgtrationsum_level2.csv", encoding="gbk", index=None)