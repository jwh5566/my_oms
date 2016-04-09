# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

from asset.models import HostList, Message
from .models import SystemInstall, InstallRecord
from cobbler_api import CobblerAPI
from my_oms import settings
from form import SystemInstallForm
from my_oms.mysql import db_operate


def system_install(request):
    """
    1.Add Some Info to Cobbler System
    2.Remote starting up
    3.screen put in System Install process //这块信息暂且空着，日后有IPMI实践补上
    """

    cobbler = CobblerAPI(url=settings.Cobbler_API['url'],user=settings.Cobbler_API['user'],password=settings.Cobbler_API['password'])
    if request.method == 'GET':
       ip = request.GET.get('ip')
       hostname = request.GET.get('host')
       mac_add = request.GET.get('mac')
       version = request.GET.get('ver')
       profile = request.GET.get('profile')
       ret = cobbler.add_system(hostname=hostname,ip_add=ip,mac_add=mac_add,profile=profile)
       if ret['result']:
           data = SystemInstall.objects.filter(ip=ip)   # data 表示一条安装信息 格式 ip--日期
           install_date = str(data[0]).split('--')[1].strip()
           InstallRecord.objects.create(ip=ip,system_version=profile,install_date=install_date)
           HostList.objects.filter(ip=ip).update(status='已使用')     #主机信息加入cobbler system，主机列表的状态变更为已使用状态，不再是待装机状态！
           SystemInstall.objects.filter(ip=ip).delete()               #安装后，装机列表此IP信息删除，转让到安装记录里供审计
           Message.objects.create(type='system', action='install', action_ip=ip, content='主机信息添加至cobbler，进入安装模式')
       return HttpResponseRedirect(reverse('install_list'))


def system_install_list(request):
    """
    List all waiting for the host operating system is installed
    """
    user = request.user

    #获取待装机的信息,从数据库中查询是否存在，未存在的插入到列表
    result = HostList.objects.filter(status='待装机')
    # print result
    install_list = []
    for i in range(len(result)):
        ip = str(result[i]).split('-')[0]
        hostname = str(result[i]).split('-')[1].strip()
        ret = SystemInstall.objects.filter(ip=ip)
        if ret:
            message = ip + ' 已经在待安装列表'
        # else:
            # data = {'ip': ip, 'hostname': hostname, 'macaddress':ret['macaddress'], 'system_version':ret['system_version']}
            # install_list.append(data)

    # #列表数据插入数据库
    # for i in range(len(install_list)):
    #     p = SystemInstall(ip=install_list[i]['ip'],hostname=install_list[i]['hostname'],macaddress=install_list[i]['macaddress'],system_version=install_list[i]['system_version'])
    #     p.save()

    all_system_list = SystemInstall.objects.all().order_by('-install_date')
    # print all_system_list
    paginator = Paginator(all_system_list,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        all_system_list = paginator.page(page)
    except :
        all_system_list = paginator.page(paginator.num_pages)

    return render(request, 'install_list.html', {'all_system_list': all_system_list })


def system_install_managed(request,id=None):
    """
    Management host to be installed
    """
    user = request.user
    if id:
        system_install = get_object_or_404(SystemInstall, pk=id)
        action = 'edit'
        # page_name = '编辑主机'
    else:
        system_install = SystemInstall()
        action = 'add'
        # page_name = '添加主机'
    if request.method == 'POST':
        operate = request.POST.get('operate')
        form = SystemInstallForm(request.POST,instance=system_install)
        if form.is_valid():
            if action == 'add':
                form.save()
                ret = form.cleaned_data['ip']
                Message.objects.create(type='system', action='install', action_ip=ret, content='主机信息已添加(macadd、system_version)，准备装机')
                return HttpResponseRedirect(reverse('install_list'))
            if operate:
                if operate == 'update':
                    form.save()
                    db = db_operate()
                    sql = 'select ip from installed_systeminstall where id = %s' % (id)
                    ret = db.mysql_command(settings.OMS_MYSQL,sql)
                    Message.objects.create(type='system', action='install', action_ip=ret, content='主机信息已更新(macadd、system_version)，准备装机')
                    return HttpResponseRedirect(reverse('install_list'))
                else:
                    pass
    else:
        form = SystemInstallForm(instance=system_install)
        action = 'add'

    return render(request, 'install_manage.html',
           {"form": form,
            'action':action
            # "page_name": page_name,
           })

def system_install_record(request):
    """
    List all operating system installation records
    """

    user = request.user

    record = InstallRecord.objects.all().order_by('-install_date')
    paginator = Paginator(record,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        record = paginator.page(page)
    except :
        record = paginator.page(paginator.num_pages)

    return render(request, 'install_record_list.html', {'record': record, 'page': page, 'paginator':paginator})