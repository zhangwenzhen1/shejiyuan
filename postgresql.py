# encoding=utf-8
import psycopg2
from io import StringIO
import pandas as pd
class Postgresql(object):
    # __slots__ = ('database', 'conn','user','password','host','port')
    def __init__(self):
        '''
        初始化数据库名，用户，密码，地址，端口
        :param database: 数据库名
        :param user: 用户
        :param password: 密码
        :param host: 地址
        :param port: 端口
        '''
        self.database = 'db'
        self.user = 'postgres_user'
        self.password = 'postgres_password'
        self.host = '10.10.10.109'
        self.port = '5432'
        self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host,
                                     port=self.port)

    def dateIntoPostgresql(self, a, b):
        """
        csv数据入postgresql库
        :param a: 要入的数据
        :param b: 入库的表名
        :return:
        """
        col = a.columns
        # dataframe类型转换为IO缓冲区中的str类型
        output = StringIO()
        a.to_csv(output, sep='\t', index=False, header=False)
        output1 = output.getvalue()
        conn = self.conn
        cur = conn.cursor()
        cur.copy_from(StringIO(output1), b, null='', columns=col)
        cur.close()

    def GetData(self, sql):
        """
        获取查询数据
        :param sql: 查询数据sql
        :return date: 查询数据
        """
        conn = self.conn
        cur = conn.cursor()
        cur.execute(sql)
        date = cur.fetchall()
        cur.close()
        return date

    def finish(self):
        self.conn.commit()
        self.conn.close()

if __name__ == "__main__":
    a = Postgresql()
    sql = "SELECT cgi,state,cityname,districtandcounty,vendor FROM volte.v_eptable"
    sql1 = "SELECT max(cast(replace(vcauxiliarypointer6,'JT','') as bigint)) as suoyin FROM volte.v_volte_send where vcauxiliarypointer6 like 'JT%' "
    eptable = a.GetData(sql)
    suoying = a.GetData(sql1)
    eptable = pd.DataFrame(eptable)
    a.finish()
    print(eptable.head())

    print(suoying)