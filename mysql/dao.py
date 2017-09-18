# -*- coding: UTF-8 -*- 
from .mydb import MyDb
mydb=MyDb()
"""
dbop=MyDb("172.168.1.10",5717,"che","che123")
err,cursor=mydb.connect("172.168.1.12",5700,"che","che123")
sql = "select user,host from mysql.user where user not in ('root','mysql.sys','repl');"
n=cursor.execute(sql)
results=mydb.fetchAll()

userlist=[]
for r in results:
    userinfo={}
    userinfo["user"]=r["user"]
    
    userinfo["host"]=r["host"]
    u="\'%s\'@\'%s\'" % (userinfo["user"],userinfo["host"])
    print (u)
    sql = "show grants for %s;" % u
    n=cursor.execute(sql)
    rgrants=mydb.fetchAll()
    grants=[]
    for g in rgrants:
        for k in g:
            v=g[k]
            grants.append(v)
    userinfo["grants"]=grants
    print (userinfo)

"""

class Dao(object):
    def getClusterInfo(self, nodeInfo):
        clusterInfo={}
        err,cursor=mydb.connect(host=nodeInfo["dbhost"], port=nodeInfo["dbport"], user=nodeInfo["cluster_user"], password=nodeInfo["cluster_passwd"])
        if err != 0:
            clusterInfo["status"]="主库连接错误"
            return clusterInfo

        #获取实例上包含的数据库信息
        dbs=''
        sql = "select schema_name from information_schema.schemata where schema_name not in ('information_schema', 'performance_schema', 'mysql', 'test','sys');"
        n=cursor.execute(sql)
        results=mydb.fetchAll()
        for r in results:
            if dbs=='':
                dbs=r["schema_name"]
            else:
                dbs=dbs+'  , '+r["schema_name"]

        #获取实例上数据量的大小       
        sql="select concat(ROUND(SUM(DATA_LENGTH)/1024/1024,2),'MB') AS data_size, concat(ROUND(SUM(INDEX_LENGTH)/1024/1024,2),'MB') AS index_size FROM information_schema.TABLES;"
        n=cursor.execute(sql)
        s=cursor.fetchone()
        clusterInfo["data_size"]=s[0]
        clusterInfo["index_size"]=s[1]
        clusterInfo["dbs"]=dbs

        #获取实例上用户及授权信息
        grantslist=[]
        sql = "select user,host from mysql.user where user not in ('root','mysql.sys','repl');"
        n=cursor.execute(sql)
        results=mydb.fetchAll()
        for r in results:
            grantdict={}
            grantdict["user"]=r["user"]
            grantdict["host"]=r["host"]
            u="\'%s\'@\'%s\'" % (grantdict["user"],grantdict["host"])
            sql = "show grants for %s;" % u
            n=cursor.execute(sql)
            rgrants=mydb.fetchAll()
            grants=[]
            for g in rgrants:
                for k in g:
                    v=g[k]
                    grants.append(v)
            grantdict["grants"]=grants
            grantslist.append(grantdict)

        clusterInfo["grantslist"]=grantslist
        #print (grantslist)
        #[{'user': 'u1', 'host': '%', 'grants': ["GRANT USAGE ON *.* TO 'u1'@'%'", "GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, ALTER ON `mydb`.* TO 'u1'@'%'", "GRANT INSERT ON `db_monitor`.* TO 'u1'@'%'"]}, {'user': 'che', 'host': '172.168.1.%', 'grants': ["GRANT ALL PRIVILEGES ON *.* TO 'che'@'172.168.1.%'"]}]

        return clusterInfo

    def getNodeInfo(self, nodeInfo):
        err,cursor=mydb.connect(host=nodeInfo["dbhost"], port=nodeInfo["dbport"], user=nodeInfo["cluster_user"], password=nodeInfo["cluster_passwd"])
        if err != 0:
            nodeInfo["status"]="连接错误"
            nodeInfo["version"]=""
            nodeInfo["repl"]=""
            nodeInfo["seconds"]=""
            nodeInfo["seconds"]=""
            return nodeInfo

        sql = "select version();"
        n=cursor.execute(sql)
        version=cursor.fetchone()[0]
        nodeInfo["version"]=version
        nodeInfo["status"]="Ok"

        sql="show slave status;"
        n=cursor.execute(sql)
        if n == 0:
            nodeInfo["repl"]="--"
            nodeInfo["seconds"]="--"
            nodeInfo["Master_Host"]="--"
            nodeInfo["Master_Port"]="--"
        else:
            r=mydb.fetchAll()[0]
            if r["Slave_IO_Running"]=="Yes" and r["Slave_SQL_Running"]=="Yes":
                nodeInfo["repl"]="yes"
            else:
                nodeInfo["repl"]="no"
            nodeInfo["seconds"]=r["Seconds_Behind_Master"]
            nodeInfo["Master_Host"]=r["Master_Host"]
            nodeInfo["Master_Port"]=r["Master_Port"]

        mydb.close()
        return nodeInfo

    def getSlaveInfo(self, dbhost,dbport,cluster_user,cluster_passwd):
        dblist=[]
        err,cursor=mydb.connect(host=dbhost, port=dbport, user=cluster_user, password=cluster_passwd)
        if err != 0:
            return None
        sql = "select host from information_schema.processlist where COMMAND='Binlog Dump GTID';"
        n = cursor.execute(sql)
        data=cursor.fetchall()
        for d in data:
            slave={}
            slave['dbhost']=d[0].split(':')[0]
            slave['dbport']=dbport
            slave['dbrule']='slave'
            dblist.append(slave)

        mydb.close()
        return dblist

    def getReplInfo(self, dbhost,dbport,cluster_user,cluster_passwd):
        dblist=[]
        err,cursor=mydb.connect(host=dbhost, port=dbport, user=cluster_user, password=cluster_passwd)
        if err != 0:
            return None
        sql = "select host from information_schema.processlist where COMMAND='Binlog Dump GTID';"
        n = cursor.execute(sql)
        data=cursor.fetchall()
        for d in data:
            slave={}
            slave['dbhost']=d[0].split(':')[0]
            slave['dbport']=dbport
            slave['dbrule']='slave'
            dblist.append(slave)

        mydb.close()
        return dblist

    def getVariables(self, dbhost,dbport,cluster_user,cluster_passwd):
        err,cursor=mydb.connect(host=dbhost, port=dbport, user=cluster_user, password=cluster_passwd)
        if err != 0:
            return None
        sql = "show variables;"
        n = cursor.execute(sql)
        allVariablesList=mydb.fetchAll()
        mydb.close()


        mysql_variable = [
                        "sql_mode",
                        "max_connections",
                        "max_allowed_packet",
                        "tmp_table_size",
                        "key_buffer_size",
                        "sort_buffer_size",
                        "join_buffer_size",
                        "read_rnd_buffer_size",
                        "slow_query_log",
                        "slow_launch_time",
                        "log_queries_not_using_indexes",
                        "gtid_mode",
                        "binlog_format",
                        "sync_binlog",
                        "expire_logs_days",
                        "slave_parallel_type",
                        "slave_parallel_workers",
                        "rpl_semi_sync_master_wait_point",
                        "rpl_semi_sync_master_enabled",
                        "rpl_semi_sync_slave_enabled",
                        "rpl_semi_sync_master_wait_for_slave_count",
                        "rpl_semi_sync_master_timeout",
                        "innodb_file_per_table",
                        "innodb_page_size",
                        "innodb_buffer_pool_size",
                        "innodb_buffer_pool_instances",
                        "innodb_read_io_threads",
                        "innodb_write_io_threads",
                        "innodb_io_capacity",
                        "innodb_io_capacity_max",
                        "innodb_lock_wait_timeout",
                        "innodb_log_file_size",
                        "innodb_flush_log_at_trx_commit",
                        "innodb_flush_method",
                        "innodb_undo_tablespaces",
                        "innodb_thread_concurrency",
                        "innodb_max_dirty_pages_pct",
                        "innodb_lru_scan_depth",
                        "innodb_purge_threads"]

        variablesList=[]
        for i in range(n):
            d={}
            k=allVariablesList[i]['Variable_name']
            if k  in mysql_variable:
                d=allVariablesList[i]
                variablesList.append(d)

        return variablesList





