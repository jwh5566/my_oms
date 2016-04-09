# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

from .models import HostList, Message
from my_oms.mysql import db_operate
from my_oms import settings
from .form import HostsListForm


def host_list(request):
    """
    List all Hosts
    """
    user = request.user
    host_list = HostList.objects.all().order_by('-status')
    # host_list = HostList.objects.all()
    paginator = Paginator(host_list,10)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        host_list = paginator.page(page)
    except :
        all_host = paginator.page(paginator.num_pages)

    return render(request, 'host_list.html', {'host_list': host_list, 'page': page, 'paginator':paginator})
    # return render(request, 'host_list.html',{'host_list': host_list})

def host_list_manage(request, id=None):   # 负责添加和修改和删除主机，删除，修改主机需要提供id号
    if id:
        host_list = get_object_or_404(HostList, pk=id)
        action = 'edit'
        # page_name = '编辑主机'
        db = db_operate()
        sql = 'select ip from asset_hostlist where id = %s' % (id)
        ret = db.mysql_command(settings.OMS_MYSQL, sql)   # settings.OMS_MYSQL 是mysql连接参数的字典
        # 这里ret 是ip
    else:
        host_list = HostList()
        action = 'add'
        # page_name = '新增主机'
        ret=[]

    if request.method == 'GET':
        delete = request.GET.get('delete')
        id = request.GET.get('id')
        if delete:
            Message.objects.create(type='host', action='manage', action_ip=ret, content='主机下架')
            host_list = get_object_or_404(HostList, pk=id)
            host_list.delete()
            return HttpResponseRedirect(reverse('host_list'))
    if request.method == 'POST':    # 修改主机或者添加新主机
        form = HostsListForm(request.POST,instance=host_list)
        print request.POST
        operate = request.POST.get('operate')  # 这里表示点击更新了按钮
        if form.is_valid():
            if action == 'add':   #  点击添加按钮
                form.save()
                ret.append(form.cleaned_data['ip'])
                Message.objects.create(type='host', action='manage', action_ip=ret, content='主机添加成功')
                return HttpResponseRedirect(reverse('host_list'))
            if operate:
                if operate == 'update':
                    form.save()
                    Message.objects.create(type='host', action='manage', action_ip=ret, content='主机信息更新')
                    return HttpResponseRedirect(reverse('host_list'))
                else:
                    pass
    else:
        form = HostsListForm(instance=host_list)

    return render(request, 'host_manage.html',
           {"form": form,
            # "page_name": page_name,
            "action": action,  # 这里action 要注意 如果是edit 页面显示edit按钮 如果是add页面显示add按钮
           })


def record(request):
    message_list = Message.objects.all().order_by('-audit_time')
    paginator = Paginator(message_list, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        message_list = paginator.page(page)
    except:
        all_host = paginator.page(paginator.num_pages)

    return render(request, 'record.html', {'message_list': message_list, 'page': page, 'paginator': paginator})