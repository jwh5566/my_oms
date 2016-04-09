# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from saltapi import SaltAPI
from my_oms import settings
from asset.models import Message
from asset.models import HostList
from my_oms.mysql import db_operate


def salt_key_list(request):
    """
    list all key
    """

    user = request.user
    sapi = SaltAPI(url=settings.SALT_API['url'], username=settings.SALT_API['user'],
                   password=settings.SALT_API['password'])
    minions, minions_pre = sapi.list_all_key()

    return render(request, 'salt_key_list.html', {'all_minions': minions, 'all_minions_pre': minions_pre})


def salt_accept_key(request):
    """
    accept salt minions key
    """

    node_name = request.GET.get('node_name')
    sapi = SaltAPI(url=settings.SALT_API['url'], username=settings.SALT_API['user'],
                   password=settings.SALT_API['password'])
    ret = sapi.accept_key(node_name)
    Message.objects.create(type='salt', action='key', action_ip=node_name, content='saltstack accept node key')
    return HttpResponseRedirect(reverse('key_list'))


def salt_delete_key(request):
    """
    delete salt minions key
    """

    node_name = request.GET.get('node_name')
    sapi = SaltAPI(url=settings.SALT_API['url'], username=settings.SALT_API['user'],
                   password=settings.SALT_API['password'])
    ret = sapi.delete_key(node_name)
    Message.objects.create(type='salt', action='key', action_ip=node_name, content='saltstack delete node key')
    return HttpResponseRedirect(reverse('key_list'))


def module_deploy(request):
    """
    deploy (nginx/php/mysql..etc) module
    """

    ret = []
    jid = []
    user = request.user
    if request.method == 'POST':
        action = request.get_full_path().split('=')[1]
        if action == 'deploy':
            tgt = request.POST.get('tgt')
            arg = request.POST.getlist('module')
            tgtcheck = HostList.objects.filter(hostname=tgt)
        if tgtcheck:
            Message.objects.create(type='salt', action='deploy', action_ip=tgt,
                                   content='saltstack %s module depoy' % (arg))
            sapi = SaltAPI(url=settings.SALT_API['url'], username=settings.SALT_API['user'],
                           password=settings.SALT_API['password'])
            db = db_operate()

            if 'sysinit' in arg:
                obj = sapi.async_deploy(tgt, arg[-1])  # 先执行初始化模块,其他任意 sysinit 在最后的模块
                sql = "insert INTO salt_returns VALUES(%s) " % obj
                print sql
                jid.append(obj)
                arg.remove('sysinit')
                if arg:
                    for i in arg:
                        obj = sapi.async_deploy(tgt, i)
                        jid.append(obj)
            else:
                for i in arg:
                    obj = sapi.async_deploy(tgt, i)
                    sql = "insert INTO salt_returns VALUES(%s) " % obj
                    db.mysql_command(settings.OMS_MYSQL, sql)
                    jid.append(obj)
                    msg = '%s deploy %s module success,jid is %s' % (tgt, i, obj)
                    ret.append(msg)
                    # db = db_operate()
                    # for i in jid:
                    #     # time.sleep(10)
                    #     sql = 'select returns from salt_returns where returns=%s'
                    #     result=db.select_table(settings.OMS_MYSQL,sql,str(i))    #通过jid获取执行结果
                    #     print result
                    #     ret.extend(result)
                    # sapi.async_deploy('test-01','zabbix.api')   #调用zabbix.api执行模块监控
        else:
            ret = '亲，目标主机不对，请重新输入'

    return render(request, 'salt_module_deploy.html', {'ret': ret})


def remote_execution(request):
    """
    remote command execution
    """

    ret = ''
    tgtcheck = ''
    danger = ('rm', 'reboot', 'init ', 'shutdown', 'll')
    user = request.user
    if request.method == 'POST':
        action = request.get_full_path().split('=')[1]
        if action == 'exec':
            tgt = request.POST.get('tgt')
            arg = request.POST.get('arg')
            tgtcheck = HostList.objects.filter(hostname=tgt)
            argcheck = arg not in danger
            if tgtcheck and argcheck:
                sapi = SaltAPI(url=settings.SALT_API['url'], username=settings.SALT_API['user'],
                               password=settings.SALT_API['password'])
                ret = sapi.remote_execution(tgt, 'cmd.run', arg)
            elif not tgtcheck:
                ret = '亲，目标主机不正确，请重新输入'
            elif not argcheck:
                ret = '亲，命令很危险, 你这样子老大会不开森'
        Message.objects.create(type='salt', action='execution', action_ip=tgt,
                               content='saltstack execution command: %s ' % (arg))

    return render(request, 'salt_remote_execution.html',
                  {'ret': ret})

# def code_deploy(request):
#     """
#     Pull code for building, pushed to the server
#     """
#
#     ret = ''
#     host = {'ga': 'test-01', 'beta': 'localhost.localdomain'}
#     user = request.user
#     if request.method == 'POST':
#         action = request.get_full_path().split('=')[1]
#         if action == 'push':
#             pro = request.POST.get('project')
#             url = request.POST.get('url')
#             ver = request.POST.get('version')
#             env = request.POST.get('env')
#             capi = Code_Work(pro=pro,url=url,ver=ver)
#             data = {pro:{'ver':ver}}
#             obj = capi.work()      #构建rpm包
#             if obj['comment'][0]['result'] and obj['comment'][1]['result'] and obj['comment'][2]['result']:
#                 json_api = BuildJson()
#                 json_api.build_data(host[env],data)   #刷新pillar数据，通过deploy下发SLS执行代码发布
#                 sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
#                 if env == 'beta':
#                     jid = sapi.target_deploy('beta','deploy_1.'+pro)
#                 elif env == 'ga':
#                     jid = sapi.target_deploy('tg','deploy_1.'+pro)
#                 else:
#                     jid = sapi.target_deploy('beta','deploy_1.'+pro)
#                 time.sleep(8)
#                 db = db_operate()
#                 sql = 'select returns from salt_returns where jid=%s'
#                 ret=db.select_table(settings.RETURNS_MYSQL,sql,str(jid))    #通过jid获取执行结果
#     return render_to_response('code_deploy.html',
#            {'ret': ret},context_instance=RequestContext(request))
