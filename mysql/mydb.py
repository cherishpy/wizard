# -*- coding: UTF-8 -*- 

import pymysql

class MyDb(object):
    def connect(self,host=None, port=None, user=None, password=None):
        try:
            self.conn = pymysql.connect(host=host,port=port,user=user,password=password,charset="utf8mb4") 
            self.cur=self.conn.cursor()
        except pymysql.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
            return e, None
        return 0,self.cur
    def execute(self,sql):
        try:
            n=self.cur.execute(sql)
            return n
        except pymysql.Error as e:
            print("Mysql Error:%s\nSQL:%s" %(e,sql))
    def fetchRow(self):
        result = self.cur.fetchone()
        return result
    def fetchAll(self):
        result=self.cur.fetchall()
        desc =self.cur.description
        d = []
        for inv in result:
            _d = {}
            for i in range(0,len(inv)):
                _d[desc[i][0]] = str(inv[i])
            d.append(_d)
        return d
    def commit(self):
        self.conn.commit()
    def rollback(self):
        self.conn.rollback()
    def close(self):
        self.cur.close()
        self.conn.close()
