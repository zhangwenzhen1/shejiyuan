# encoding=utf-8
from ModifyGDFormat import *
from JJtGd import *
import pandas as pd
import warnings

warnings.filterwarnings('ignore')
path = r'D:/集团工单/gd'  # 指定存放文件的地址
# filename = input("请输入您要读取的文件名：")
filename = '两低两高小区问题跟踪表20200401.xlsx'

a = JJtGd(path, filename)
df_VOLTEJTD = a.Go('低接入小区明细参考表')
df_VOLTERABDXG = a.Go('高掉话小区明细参考表')
df_ESRVCCQHC = a.Go('低SRVCC无线切换成功率小区明细参考表')
df_VOLTESXGDB = a.Go('上行高丢包小区明细参考表')
df_VOLTEXXGDB = a.Go('下行高丢包小区明细参考表')
df_VOLTESXGTZ = a.Go('上行高吞字小区明细参考表')
df_VOLTEXXGTZ = a.Go('下行高吞字小区明细参考表')

df = df_VOLTEJTD.append(df_VOLTERABDXG).append(df_ESRVCCQHC).append(df_VOLTESXGDB).append(df_VOLTEXXGDB) \
    .append(df_VOLTESXGTZ).append(df_VOLTEXXGTZ)
df = df.reset_index(drop=False)
df.drop(['index'], axis=1, inplace=True)
# df = pd.read_csv('D:/集团工单/gd/paidan.csv',encoding='gbk')
task = ModifyGDFormat(df)
send, v_return, df_all = task.Run()
print("集团下发派单数:{}".format(str(df_all.iloc[:, 0].size)))
print("实际可派工单数:{}".format(str(send.iloc[:, 0].size)))
send.to_csv(path + '/paidan1.csv', header=1, encoding='gbk', index=False)  # 保存列名存储
v_return.to_csv(path + '/回单1.csv', header=1, encoding='gbk', index=False)  # 保存列名存储
df_all.to_csv(path + '/pandan_all.csv', header=1, encoding='gbk', index=False)  # 保存列名存储
print("任务完成")
