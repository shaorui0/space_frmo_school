import pymysql

'''
    执行操作后 调用close() 关闭连接
    再次操作前需执行connect()

'''
class MYSQL:
    '''
        地址
        用户名
        密码
        数据库
    '''
    def __init__(self,addr,user,password,database):
        self.db=None
        self.addr=addr
        self.user=user
        self.password=password
        self.database=database
        self.db=pymysql.connect(host=self.addr,user=self.user,passwd=self.password,db=self.database,port=3306,charset='utf8',ssl={})
    def close(self):
        self.db.close()
    
    '''
        例如：
            sql="INSERT INTO allPic(TimeStamp,Src) VALUES(%s,%s)"
            a='hello'
            b='world'
            data=(a,b)
            mysql.commit(sql,data)
            其中data参数是一个tuple类型对象
    '''
    def commit(self,sql='',data=()):   #插入或更新
        if(self.db is None):
            print('-> sql dicconnect')
            return 
        cursor = self.db.cursor()   
        cursor.execute(sql,data)
        self.db.commit()

    '''
        例如：
        sq1="select * from hello order by timeStamp desc  limit 3" 查降序前三
        data=queryData(sql)
    '''
    def queryData(self,sql=""):    #查询功能 返回list
        cur = self.db.cursor()
        cur.execute(sql)
        return list(cur)