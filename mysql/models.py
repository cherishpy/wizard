# -*- coding: UTF-8 -*-

from django.db import models

# Create your models here.
# 各个线上主库地址。
class schema_info(models.Model):
    id = models.AutoField('ID',primary_key=True)
    cluster_name = models.CharField('集群名称', max_length=50)
    dbhost = models.CharField('主机地址',max_length=40)
    dbport = models.IntegerField('端口')
    dbrule = models.CharField('角色',max_length=50)
    cluster_user = models.CharField('用户名',max_length=50)
    cluster_passwd = models.CharField('密码',max_length=300)
    cluster_service = models.CharField('所属业务线',max_length=50)
    cluster_development = models.CharField('开发',max_length=50)
    environment = models.IntegerField('环境')
    remarks = models.CharField('备注',max_length=50)

class service_line(models.Model):
    id = models.AutoField('ID',primary_key=True)
    service_name = models.CharField('集群名称', max_length=50)



# 工单状态
ENVIRONMENT_STATUS = {
    1: '线上',
    2: '预发',
    3: '测试',
}