# -*- coding: utf-8 -*-
from django.db import models

class HostList(models.Model):
    ip = models.CharField(max_length=20, verbose_name=u'IP地址')
    hostname = models.CharField(max_length=30, verbose_name=u'主机名')
    product = models.CharField(max_length=20, verbose_name=u'产品')
    application = models.CharField(max_length=20, verbose_name=u'应用')
    idc_jg = models.CharField(max_length=10, blank=True, verbose_name=u'机柜编号')
    status = models.CharField(max_length=10, verbose_name=u'使用状态', default=u'待装机')
    remark = models.TextField(max_length=50, blank=True, verbose_name=u'备注')

    def __unicode__(self):
        return u'%s - %s - %s' %(self.ip, self.hostname, self.application )

    class Meta:
        # verbose_name = u'主机列表'
        verbose_name_plural = u'主机列表管理'

class Message(models.Model):
    """
    Platform audit information
    """
    audit_time = models.DateTimeField(auto_now_add=True, verbose_name=u'时间')
    type = models.CharField(max_length=10, verbose_name=u'类型')
    action = models.CharField(max_length=10, verbose_name=u'动作')
    action_ip = models.CharField(max_length=15, verbose_name=u'执行IP')
    content = models.CharField(max_length=50, verbose_name=u'内容')

    class Meta:
        # verbose_name = u'审计信息'
        verbose_name_plural = u'审计信息管理'
