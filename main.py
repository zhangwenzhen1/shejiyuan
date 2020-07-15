# encoding=utf-8
from ModifyGDFormat import *
from JJtGd import *
import warnings
warnings.filterwarnings('ignore')
path = r'D:/集团工单/gd'  # 指定存放文件的地址
filename = input("请输入您要读取的文件名：")
# filename = '两低两高小区问题跟踪表20200501.xlsx'
a = JJtGd(path, filename)
df = a.Run()
task = ModifyGDFormat(df)
send, v_return, df_all = task.Run()
print("集团下发派单数:{}".format(str(df_all.iloc[:, 0].size)))
print("实际可派工单数:{}".format(str(send.iloc[:, 0].size)))
send.to_csv(path + '/paidan1.csv', header=1, encoding='gbk', index=False)  # 保存列名存储
v_return.to_csv(path + '/回单1.csv', header=1, encoding='gbk', index=False)  # 保存列名存储
df_all.to_csv(path + '/pandan_all.csv', header=1, encoding='gbk', index=False)  # 保存列名存储
print("任务完成")
