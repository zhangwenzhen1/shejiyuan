import pandas as pd
import psycopg2
from io import StringIO
import numpy as np
# data1 = pd.read_csv('D:/集团工单/send12.csv',encoding='utf-8')
# data1['flonb'] = data1['flonb'].astype(str)
# data1['flat'] = data1['flat'].astype(str)
# v_eptable = pd.read_csv('D:/集团工单/v_eptable.csv',encoding='utf-8')
# # eptable.rename(columns={'grid.1': 'grid'},inplace = True)
# v_eptable.drop(['id'], axis=1,inplace=True)

eptable = pd.read_csv('D:/集团工单/volte_eptable.csv',encoding='utf-8')
eptable['azimuth'] = eptable['azimuth'].astype(str)
eptable['carrierffrequencynum'] = eptable['carrierffrequencynum'].astype(str)
# eptable['antennaheight'] = eptable['antennaheight'].astype(str)
# eptable['totaldowntiltangle'] = eptable['totaldowntiltangle'].astype(str)
# eptable['carrierffrequencynum'] = eptable['carrierffrequencynum'].astype(str)

c = eptable.columns
print(eptable.columns)
print(c)
print(eptable.info())
def function(a,b,c):
    #dataframe类型转换为IO缓冲区中的str类型
    output = StringIO()
    a.to_csv(output, sep='\t', index=False, header=False)
    output1 = output.getvalue()
    conn = psycopg2.connect(database="db", user="postgres_user", password="postgres_password", host="10.10.10.109", port="5432")
    cur = conn.cursor()
    cur.copy_from(StringIO(output1),b,null='',columns=c)
    conn.commit()
    cur.close()
    conn.close()
    # c ='派单数据入库成功'
#
function(eptable,'volte.v_eptable',c)
# function(v_return,'volte.v_volte_returnvaluation_2019111219')



#####连接数据库获取上次派单最大编号
# conn = psycopg2.connect(database="db", user="postgres_user", password="postgres_password", host="10.10.10.109", port="5432")
# cur = conn.cursor()
# cur.execute("SELECT vcauxiliarypointer6 FROM volte.v_volte_send where vcauxiliarypointer6 like 'JT%'")
# rows = cur.fetchall()
# t = pd.DataFrame(rows)
# cur.execute("SELECT * FROM volte.vnb_orderrule_set ")
# eptable  = cur.fetchall()
# eptable = pd.DataFrame(eptable)
# conn.commit()
# cur.close()
# conn.close()

# print(eptable.head())
# import psycopg2
# import os
# import csv
# ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
# CSV_SEP = '`'
#
# class Test():
#     def __init__(self):
#         self.database = 'test'
#         self.user = '###'
#         self.host = '###'
#         self.password = '###'
#         self.conn = psycopg2.connect("dbname='" + self.database + "' user='" + self.user + "' host='" + self.host + "' password='" + self.password + "'")
#         self.cursor = self.conn.cursor()
#         self.dump_file = 'test'
#
#     def dump_Test(self):
#         cmd='select * from public."Table1"'
#         print (cmd)
#         f = "%s_navstrand.csv" % (self.dump_file)
#         self.cursor.copy_expert("COPY (%s) TO STDOUT DELIMITER '`' CSV " % (cmd), open(f, "w"))
#
#     def read_csv2(self):
#         processcount = 0
#         f = "%s_navstrand" % (self.dump_file)
#         with open(f, "r", 1024 * 1024 * 1024) as csv_f:
#             for line in csv_f:
#                 print (line)
#     def read_csv(self):
#         processcount = 0
#         f = "%s_navstrand.csv" % (self.dump_file)
#         with open(f) as csvfile:
#             lines = csv.reader(csvfile,delimiter='`')
#             for line in lines:
#                 print (line)
#     def get_statistic(self):
#         self.dump_Test()
#         self.read_csv()
#
# if __name__ == "__main__":
#     t = Test()
#     t.get_statistic()