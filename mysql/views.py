# -*- coding: UTF-8 -*-
import json
import re

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,render_to_response
from django.db.models import Q


from .models import schema_info,service_line,ENVIRONMENT_STATUS
from .dao import Dao
from .mydb import MyDb

mydb=MyDb()
dao=Dao()

def mysql_list(request):
    #一个页面展示
    PAGE_LIMIT = 12
    pageNo = 0

    #参数检查
    if 'pageNo' in request.GET:
        pageNo = request.GET['pageNo']
    else:
        pageNo = '0'
    
    try:
        pageNo = int(pageNo)
        if pageNo < 0:
            pageNo = 0
    except ValueError as ve:
        context = {'errMsg': 'pageNo参数不是int.'}
        return render(request, 'error.html', context)

    offset = pageNo * PAGE_LIMIT

    dbs=schema_info.objects.raw('select * from mysql_schema_info   order by cluster_service,cluster_name limit %s,%s;' % (offset,PAGE_LIMIT) )
    context = {'dbs':dbs,'pageNo':pageNo,'ENVIRONMENT_STATUS':ENVIRONMENT_STATUS}
    return render(request, 'mysql/mysql_list.html', context)

def cluster_list(request):
    #一个页面展示
    PAGE_LIMIT = 12
    pageNo = 0

    #参数检查
    if 'pageNo' in request.GET:
        pageNo = request.GET['pageNo']
    else:
        pageNo = '0'
    
    try:
        pageNo = int(pageNo)
        if pageNo < 0:
            pageNo = 0
    except ValueError as e:
        context = {'errMsg': 'pageNo参数不是int.',"errException":e}
        return render(request, 'error.html', context)

    offset = pageNo * PAGE_LIMIT

    if 'navStatus' in request.GET:
        navStatus = request.GET['navStatus']
    else:
        navStatus = 'all'

    if navStatus == 'all':
        dbs=schema_info.objects.raw('select * FROM mysql_schema_info  group by cluster_name order by environment limit %s,%s;' % (offset,PAGE_LIMIT) )
    elif navStatus == 'online':
        dbs=schema_info.objects.raw('select * FROM mysql_schema_info where environment=1  group by cluster_name order by environment limit %s,%s;' % (offset,PAGE_LIMIT) )
    elif navStatus == 'pre':
        dbs=schema_info.objects.raw('select * FROM mysql_schema_info where environment=2  group by cluster_name order by environment  limit %s,%s;' % (offset,PAGE_LIMIT) )
    elif navStatus == 'test':
        dbs=schema_info.objects.raw('select * FROM mysql_schema_info where environment=3  group by cluster_name order by environment limit %s,%s;' % (offset,PAGE_LIMIT) )
    else:
        context = {'errMsg': '传入的navStatus参数有误！'}
        return render(request, 'mysql/error.html', context)
    
    context = { 
        'navStatus': navStatus,
        'dbs':dbs,
        'pageNo':pageNo,
        'ENVIRONMENT_STATUS':ENVIRONMENT_STATUS}

    return render(request, 'mysql/cluster_list.html', context)


def cluster_add(request):
    if request.method =='GET':
        allServiceName=service_line.objects.raw('select id,service_name FROM mysql_service_line;' )
        context = {'allServiceName':allServiceName,'ENVIRONMENT_STATUS':ENVIRONMENT_STATUS}
        return render(request,'mysql/cluster_add.html',context)

    try:
        cluster_name=request.POST.get("cluster_name")
        environment=request.POST.get("environment")
        dbhost=request.POST.get("dbhost")
        dbport=int(request.POST.get("dbport"))
        dbrule=request.POST.get("dbrule")
        cluster_user=request.POST.get("cluster_user")
        cluster_passwd=request.POST.get("cluster_passwd")
        cluster_development=request.POST.get("cluster_development")
        remarks=request.POST.get("remarks")

        #获取environment值
        serviceNum=int(request.POST.get("serviceNum"))
        cluster_service=''
        for i in range (1,serviceNum+1):
            service_name=request.POST.get("service_name"+str(i))
            print (service_name)
            if service_name is not None:
                if cluster_service=='':
                    cluster_service=service_name
                else:
                    cluster_service=cluster_service+','+service_name

    except Exception as e:
        context = {'errMsg': "参数获取失败","errException":e}
        return render(request, 'mysql/error.html', context)


    err,cursor=mydb.connect(host=dbhost, port=dbport, user=cluster_user, password=cluster_passwd)
    if err != 0:
        context = {'errMsg': cluster_name+'集群连接失败，请验证IP地址、用户和密码是否填写正确.'}
        return render(request, 'mysql/error.html', context)

    try:
        id = request.POST.get('id')
        if id=='':
            p1 = schema_info(
                cluster_service=cluster_service,
                environment=environment,
                cluster_name=cluster_name,
                cluster_user=cluster_user,
                cluster_passwd=cluster_passwd,
                cluster_development=cluster_development,
                dbhost=dbhost,
                dbport=dbport,
                dbrule=dbrule,
                remarks=remarks)
        else:
            p1=schema_info.objects.get(id=id)
            p1.cluster_service=cluster_service
            p1.environment=int(environment)
            p1.cluster_name=cluster_name
            p1.cluster_user=cluster_user
            p1.cluster_passwd=cluster_passwd
            p1.cluster_development=cluster_development
            p1.dbhost=dbhost
            p1.dbport=dbport
            p1.dbrule=dbrule
            p1.remarks=remarks
        p1.save()
    except Exception as e:
        context = {'errMsg': "修改数据失败","errException":e}
        return render(request, 'mysql/error.html', context)
    return HttpResponseRedirect('/mysql/mysqlDetail/'+cluster_name)

def cluster_edit(request,cluster_name):
    try:
        info = schema_info.objects.raw('select * from mysql_schema_info where  cluster_name="%s" and dbrule="master";' % cluster_name)[0] 
    except Exception as e:
        context = {'errMsg': "获取数据失败","errException":e}
        return render(request, 'mysql/error.html', context)

    allServiceName=service_line.objects.raw('select id,service_name FROM mysql_service_line;' )
    environmentId=info.environment

    info.environment=ENVIRONMENT_STATUS[environmentId]

    alreadyService=info.cluster_service.split(',')

    context = {'alreadyService':alreadyService,'allServiceName':allServiceName,'environmentId':environmentId,'info':info}
    return render(request, 'mysql/cluster_add.html', context)

def cluster_dele(request,cluster_name):
    if cluster_name:
        schema_info.objects.filter(cluster_name=cluster_name).delete()
    return HttpResponseRedirect('/mysql/cluster_list')

def mysqlDetail(request,clusterName):
    navStatus=0
    if 'navStatus' in request.GET:
        navStatus = request.GET['navStatus']
    else:
        navStatus = 'baseInfo'

    nodes=schema_info.objects.filter(cluster_name=clusterName)
    nodesInfo=[]
    clusterInfo={}
    for node in nodes:
        nodeInfo={}
        nodeInfo["id"]=node.id
        nodeInfo["dbhost"]=node.dbhost
        nodeInfo["dbport"]=node.dbport
        nodeInfo["cluster_user"]=node.cluster_user
        nodeInfo["cluster_passwd"]=node.cluster_passwd
        nodeInfo["dbrule"]=node.dbrule
        if nodeInfo["dbrule"]=='master':
            clusterInfo=dao.getClusterInfo(nodeInfo)
            clusterInfo["cluster_service"]=node.cluster_service
            clusterInfo["environment"]=ENVIRONMENT_STATUS[node.environment]
            clusterInfo["cluster_development"]=node.cluster_development
            clusterInfo["cluster_user"]=node.cluster_user
            clusterInfo["cluster_passwd"]=node.cluster_passwd
            clusterInfo["remarks"]=node.remarks

        nodeInfo=dao.getNodeInfo(nodeInfo)
        nodesInfo.append(nodeInfo)
    clusterInfo["clusterName"]=clusterName

    context={
        'nodesInfo': nodesInfo,
        'clusterInfo': clusterInfo,
        'navStatus': navStatus,
        }
    return render(request,'mysql/mysqlDetail.html',context)

def node_info(request,id):
    node=schema_info.objects.get(id=id)
    cluster_name=node.cluster_name
    dbhost=node.dbhost
    dbport=node.dbport
    cluster_user=node.cluster_user
    cluster_passwd=node.cluster_passwd
    variablesList=dao.getVariables(dbhost,dbport,cluster_user,cluster_passwd)

    context={
        'variablesList': variablesList,
        'cluster_name':cluster_name,
        'id':id,
        }
    return render(request,'mysql/node_info.html',context)

def node_dele(request,id):
    cluster_name = schema_info.objects.get(id=id).cluster_name
    if id:
        schema_info.objects.filter(id=id).delete()
    return HttpResponseRedirect('/mysql/mysqlDetail/'+cluster_name)


def auto_add_slave(request,clusterName):
    try:
        #info=schema_info.objects.get(cluster_name=clusterName,dbrule="master")
        info = schema_info.objects.raw('select * from mysql_schema_info where cluster_name="%s" and dbrule="master";' % clusterName)[0] 
    except Exception as e:
        context = {'errMsg': "获取数据失败","errException":e}
        return render(request, 'mysql/error.html', context)
    cluster_service=info.cluster_service
    environment=info.environment
    cluster_name=info.cluster_name
    cluster_user=info.cluster_user
    cluster_passwd=info.cluster_passwd
    cluster_development=info.cluster_development
    dbhost=info.dbhost
    dbport=info.dbport
    dbrule=info.dbrule
    remarks=info.remarks
    slavelist =dao.getSlaveInfo(dbhost,int(dbport),cluster_user,cluster_passwd)
    if slavelist is None:
        context = {'errMsg': "master无法连接"}
        return render(request, 'mysql/error.html', context)

    schema_info.objects.filter(cluster_name=cluster_name,dbrule='slave').delete()
    for slave in slavelist:
        p1 = schema_info(
            cluster_service=cluster_service,
            environment=environment,
            cluster_name=cluster_name,
            cluster_user=cluster_user,
            cluster_passwd=cluster_passwd,
            cluster_development=cluster_development,
            dbhost=slave["dbhost"],
            dbport=slave["dbport"],
            dbrule=slave["dbrule"],
            remarks=remarks)
        p1.save()
    return HttpResponseRedirect('/mysql/mysqlDetail/'+cluster_name)


