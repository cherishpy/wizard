# -*- coding: UTF-8 -*- 

import MySQLdb

class DbOp(object):
    def __init__(self,host='172.168.0.10',port=5716,user='admin',password='123456',dbname='onepiece',charset="utf8"):
        self.host=host
        self.port=port
        self.user=user
        self.password=password
        self.dbname=dbname
        self.charset=charset
        try:
            self.conn=MySQLdb.connect(host=self.host,port=self.port,user=self.user,passwd=self.password,db=self.dbname)
            self.conn.autocommit(False)
            self.conn.set_character_set(self.charset)
            self.cur=self.conn.cursor()
        except MySQLdb.Error as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    def execute(self,sql):
        try:
            n=self.cur.execute(sql)
            return n
        except MySQLdb.Error as e:
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
