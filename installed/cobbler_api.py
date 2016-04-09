# -*- coding: utf-8 -*-
# import cobbler
import xmlrpclib 

class CobblerAPI(object):
    def __init__(self,url,user,password):   # 初始化cobbler api对象
        self.cobbler_user= user
        self.cobbler_pass = password
        self.cobbler_url = url
    
    def add_system(self,hostname,ip_add,mac_add,profile):
        '''
        Add Cobbler System Infomation
        '''
        ret = {
            "result": True,
            "comment": [],
        }
        hostname = '_'.join(hostname.split())
        remote = xmlrpclib.Server(self.cobbler_url) 
        token = remote.login(self.cobbler_user,self.cobbler_pass) 
        system_id = remote.new_system(token) 
        remote.modify_system(system_id,"name",hostname,token) 
        remote.modify_system(system_id,"hostname",hostname,token) 
        remote.modify_system(system_id,'modify_interface', { 
            "macaddress-eth0" : mac_add, 
            "ipaddress-eth0" : ip_add, 
            "dnsname-eth0" : hostname, 
        }, token) 
        remote.modify_system(system_id,"profile",profile,token) 
        remote.save_system(system_id, token) 
        try:
            remote.sync(token)
            ret['comment'].append(' add system success')
        except Exception as e:
            ret['result'] = False
            ret['comment'].append(str(e))
        return ret

def main():
    cobbler = CobblerAPI(url='http://10.0.0.151/cobbler_api',user='cobbler',password='cobbler',)
    ret = cobbler.add_system(hostname='test',ip_add='10.0.0.123',mac_add='00:0C:29:70:A1:16',profile='CentOS-6.6-mini-x86_64')
    print ret

if __name__ == '__main__':
    main()
