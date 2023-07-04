import requests
import prettytable as pt
from lxml import html
import dns.resolver
import socket
import time  
import get_server_info
import os
class cdn_tester:
    def __init__(self,domain,dns_name):
        self.domain = domain
        self.dns = dns_name
        os.popen('netsh interface ip set dnsservers "乙太網路" static '+self.dns+' primary')
        #time.sleep(1)

    def dns_get_server_ip(self):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [self.dns]
        #resolver.nameservers = ['163.28.6.1', '140.111.233.5']
        answers = resolver.resolve(self.domain)

        for data in answers:
            server_ip = str(data)
        server_ip = self.format_data(server_ip)
        return server_ip 

    def httping(self):
        strat_time = time.time()
        r = requests.get('https://media.video.cloud.edu.tw/vod/_definst_/mp4:uploads.video/2021/09/video_391972_1080.mp4/manifest.mpd')
        #r = requests.get('https://media.video.cloud.edu.tw/vod/_definst_/mp4:uploads.video/2023/06/video_401669_1080.mp4/manifest.mpd')
        #r = requests.get('https://media.video.cloud.edu.tw')
        return str(int(((time.time() - strat_time)*1000))) +' ms'
    ''''
        if r.status_code == 200 :
            return str(int(((time.time() - strat_time)*1000))) +' ms'
        else :
            #return ' test failed status code  %s' % (r.status_code) 
            return str(int(((time.time() - strat_time)*1000))) +' ms'
    '''
        
        
    def get_client_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((self.dns, 80))
        client_ip = s.getsockname()[0]
        s.close()
        return client_ip 


    def format_data(self , data):
        formated_data = str(data).replace('[','').replace(']','').replace('\'','')
        if '：' in formated_data:
            formated_data = formated_data.split('：')
            return formated_data
        else:
            return formated_data
    
    def format_ip_info(self , ip_port):
        ip_port = str(ip_port).replace('(','').replace(')',"").replace('\'','').replace(' ','').split(',')
        return ip_port
        
def main():
    
    #domain = "media.video.cloud.edu.tw"
    domain = "mediavideocloudedutw.tanetcdn.edu.tw"
    '''
    opt = input('select dns   cht  or  moe \n')
    if opt  == 'cht':
        dns_name = '168.95.1.1'


    elif opt == 'moe':
        dns_name = '140.111.34.135'
    '''
    
    
    dns_name_s = ['168.95.1.1','140.111.34.135']
    for dns_name in dns_name_s:
        os.popen('ipconfig/flushdns')
        cdn_tester_q = cdn_tester(domain,dns_name)
        get_server_ip = cdn_tester_q.dns_get_server_ip()
        client_ip = cdn_tester_q.get_client_ip()
        httping = cdn_tester_q.httping()
        get_server_info.get_server_organization(domain , get_server_ip ,  client_ip , dns_name=dns_name , httping=httping)
        del cdn_tester_q , get_server_ip , client_ip , httping 
        time.sleep(90)

    
if __name__ == '__main__':
    main()

