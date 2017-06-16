# -*- coding: UTF-8 -*-
import json

from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from .models import cluster_config, CLUSTER_TYPE, CLUSTER_STATUS
from .dbconfigDal import setClusterStatusByPort
from common.aes_decryptor import Prpcrypt

# Create your views here.
# 显示用户列表
def index(request):
    clusters = cluster_config.objects.all()
    for cluster in clusters:
        cluster.cluster_type = CLUSTER_TYPE.get(cluster.cluster_type)
        # cluster.cluster_status = CLUSTER_STATUS.get(cluster.cluster_status)
        cluster.cluster_hosts = json.loads(cluster.cluster_hosts)
    context = {
        'clusters': clusters,
        'currentMenu': 'clusterconfig',
    }
    return render(request, 'dbconfig/index.html', context)


def add(request):
    if request.POST:
        cluster_type = request.POST.get("cluster_type")
        cluster_name = request.POST.get("cluster_name")
        cluster_hosts = request.POST.get("cluster_hosts")
        cluster_port = request.POST.get("cluster_port")
        cluster_user = request.POST.get("cluster_user")
        cluster_password = request.POST.get("cluster_password")
        # 验证重复的帐号名
        cluster_names = cluster_config.objects.filter(cluster_name__iexact=cluster_name)
        # 验证重复的邮件地址
        cluster_ports = cluster_config.objects.filter(cluster_port__iexact=cluster_port)
        if cluster_names:
            response_data = {}
            response_data["statusCode"] = 403
            response_data["message"] = u'集群名称已经存在不能添加'
            return HttpResponse(json.dumps(response_data),
                                content_type='application/json')
        if cluster_ports:
            response_data = {}
            response_data["statusCode"] = 403
            response_data["message"] = u'集群端口已经存在不能添加'
            return HttpResponse(json.dumps(response_data),
                                content_type='application/json')

        # 保存用户信息
        cluster = cluster_config(
            cluster_type=cluster_type,
            cluster_name=cluster_name,
            cluster_hosts=json.dumps(cluster_hosts.split(',')),
            cluster_port=cluster_port,
            cluster_user=cluster_user,
            cluster_password=cluster_password)
        cluster.save()

        return HttpResponseRedirect("/dbconfig/index")

    context = {'CLUSTER_TYPE': CLUSTER_TYPE}
    return render(request, 'dbconfig/add.html', context)


def edit(request, cluster_id):
    cluster = cluster_config.objects.get(id=int(cluster_id))
    if not cluster:
        return HttpResponseBadRequest(u"错误请求")
    if request.POST:
        cluster.cluster_type = request.POST.get("cluster_type")
        cluster.cluster_name = request.POST.get("cluster_name")
        cluster.cluster_hosts = json.dumps((request.POST.get("cluster_hosts")).split(','))
        cluster.cluster_port = request.POST.get("cluster_port")
        cluster.cluster_user = request.POST.get("cluster_user")
        cluster.cluster_password = request.POST.get("cluster_password")
        cluster.cluster_status = request.POST.get("cluster_status")
        cluster.save()
        return HttpResponseRedirect("/dbconfig/index")

    pc = Prpcrypt()  # 初始化
    cluster.cluster_password = pc.decrypt(cluster.cluster_password)
    cluster.cluster_hosts = ",".join(json.loads(cluster.cluster_hosts))
    context = {'cluster':cluster, 'CLUSTER_TYPE':CLUSTER_TYPE, 'CLUSTER_STATUS':CLUSTER_STATUS}
    return render(request, 'dbconfig/edit.html', context)

def detail(request, cluster_id):
    cluster = cluster_config.objects.get(id=int(cluster_id))
    if not cluster:
        return HttpResponseRedirect("/dbconfig/index")

    cluster.cluster_type = CLUSTER_TYPE.get(cluster.cluster_type)
    cluster.cluster_hosts = json.loads(cluster.cluster_hosts)
    context = {'cluster': cluster}
    return render(request, 'dbconfig/detail.html', context)

def delete(request, cluster_id):
    try:
        cluster = cluster_config.objects.get(id = int(cluster_id))
    except BaseException:
        return HttpResponse(json.dumps({"statusCode":400,"message":u'此用户不存在!'}), content_type='application/json')
    # 删除此用户
    cluster.delete()
    return HttpResponseRedirect("/dbconfig/index")

@csrf_exempt
def setclusterstatus(request):
    port = request.POST.get("port")
    stat = request.POST.get("stat")
    rets = setClusterStatusByPort(port,stat)
    return HttpResponse(json.dumps(rets), content_type='application/json')
