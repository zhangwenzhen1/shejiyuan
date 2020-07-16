# encoding=utf-8
from ModifyGDFormat import *
from JJtGd import *
from JJtGdFK import *
from dateutil.relativedelta import relativedelta
from Postgresql import *
import warnings
warnings.filterwarnings('ignore')

path = r'D:/集团工单/gd'  # 指定存放文件的地址
path2 = r'D:/集团工单'  #  指定存放结果文件
# path = r'/data/ftp/python/xls'  # 指定存放文件的地址
# path2 = r'/data/ftp/python/fcsv'  # 指定存放结果文件

# filename = input("请输入您要读取的文件名：")
filename = '两低两高小区问题跟踪表20200401.xlsx'
###执行生成派单任务
paidan = JJtGd(path, filename)
df = paidan.Run()
task = ModifyGDFormat(df)
send, v_return, df_all = task.Run()
print("集团下发派单数:{}".format(str(df_all.iloc[:, 0].size)))
print("实际可派工单数:{}".format(str(send.iloc[:, 0].size)))
send.to_csv(path2 + '/paidan1.csv', header=1, encoding='gbk', index=False)  # 保存列名存储
v_return.to_csv(path2 + '/回单1.csv', header=1, encoding='gbk', index=False)  # 保存列名存储
df_all.to_csv(path2 + '/pandan_all.csv', header=1, encoding='gbk', index=False)  # 保存列名存储
print("派单任务完成")
df.to_csv(path2 + '/df.csv', header=1, encoding='gbk', index=False)  # 保存列名存储

###获取反馈指标日期
# df = pd.read_csv('D:\集团工单\gd/df.csv',encoding='gbk')
f_date = df[['vcequestiontype','日期']]
f_date = f_date.drop_duplicates()
f_date['starttime'] = pd.to_datetime(f_date['日期'], format='%Y/%m/%d').apply(lambda x: x - relativedelta(months=+1))
f_date['gd_startdate'] = f_date['starttime'].astype(np.str)
f_date['gd_startdate'] = f_date['gd_startdate'].apply([lambda x: x[:7]])
f_date['gd_startdate'] = pd.to_datetime(f_date['gd_startdate'], format='%Y/%m')
f_date['problemtype'] = np.where(f_date['vcequestiontype'].isin(['VOLTEJTD','ESRVCCQHC','VOLTERABDXG']),'周派单','月派单')
f_date.rename(columns={'starttime': 'data_date',}, inplace=True)
f_date = f_date[['gd_startdate','problemtype','data_date']]
f_date = f_date.drop_duplicates()
print('反馈指标日期获取成功')
f_date.to_csv(path2 + "/riqi1.csv", header=1, encoding='gbk', index=False)  # 保存列名存储'''
####执行反馈表任务
fankui = JJtGdFK(path, filename)
result = fankui.Go_run()
date = df_all[['vcequestiontype', 'starttime', 'endtime']]
date = date.drop_duplicates()
date['starttime'] = pd.to_datetime(date['starttime'], format='%Y/%m/%d').apply(lambda x: x - relativedelta(months=+1))
date['endtime'] = pd.to_datetime(date['endtime'], format='%Y/%m/%d').apply(lambda x: x - relativedelta(months=+1))
date.rename(columns={'starttime': 'startdate', 'endtime': 'enddate', 'vcequestiontype': 'problemtype'}, inplace=True)
result = pd.merge(result, date, on='problemtype', how='left', suffixes=('', '_y'))  # pandas csv表左连接
result = result[['province', 'city', 'cgi', 'startdate', 'enddate', 'problemtype', 'voltetraval', 'volteradconnratio',
                 'volteraddropratio', 'uppdcplossratio', 'downpdcplossratio', 'failoutgeran', 'srvcchosucratio',
                 'uptzsamprate', 'downtzsamprate', 'flag']]
ff = Postgresql()
ff.dateIntoPostgresql(result, "volte.vn_gdcellkpi_group")
print("反馈表数据入库完成")

ff = Postgresql()
ff.dateIntoPostgresql(f_date, "volte.vn_gd_group_date")
ff.finish()
print("反馈指标日期入库完成")
result.to_csv(path2 + "/back.csv", header=1, encoding='gbk', index=False)  # 保存列名存储
print("任务完成")


