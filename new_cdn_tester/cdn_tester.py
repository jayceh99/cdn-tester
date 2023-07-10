import requests
import prettytable as pt
from lxml import html
import dns.resolver
import socket
import time  
import get_server_info
import os
import json
class cdn_tester:
    def __init__(self,domain,dns_name,requests_target):
        self.domain = domain
        self.dns = dns_name
        self.requests_target = requests_target
        os.popen('netsh interface ip set dnsservers "乙太網路" static '+self.dns+' primary')
        #time.sleep(1)

    def dns_get_server_ip(self):
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [self.dns]
        answers = resolver.resolve(self.domain)

        for data in answers:
            server_ip = str(data)
        server_ip = self.format_data(server_ip)
        return server_ip 

    def httping(self):
        try:
            r = requests.get(self.requests_target)
            strat_time = time.time()
            r = requests.get(self.requests_target)
            return str(int(((time.time() - strat_time)*1000))) +' ms'

        except Exception:
            return "Test Failed"
        
        
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
    j = open(r'C:\Users\jayce\cdn-tester\new_cdn_tester\config.json','r')
    j = json.loads(j.read())
    domain = j["domain"]
    requests_target = j["requests_target"]
    for dns_name in j['dns'] :
        os.popen('ipconfig/flushdns')
        cdn_tester_q = cdn_tester(domain,dns_name['ip'],requests_target)
        get_server_ip = cdn_tester_q.dns_get_server_ip()
        client_ip = cdn_tester_q.get_client_ip()
        httping = cdn_tester_q.httping()
        get_server_info.get_server_organization(domain , get_server_ip ,  client_ip , dns_name=dns_name['ip'] , httping=httping)
        del cdn_tester_q , get_server_ip , client_ip , httping 


    
if __name__ == '__main__':
    main()

