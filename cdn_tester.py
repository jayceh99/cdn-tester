import requests
import prettytable as pt
from lxml import html
import dns.resolver
import socket
import time
from ping3 import ping  
def get_server_ip(url):
    r = requests.get(url, stream=True)
    print(dir(r.raw._connection.sock))
    return str(r.raw._connection.sock.getpeername()) , str(r.raw._connection.sock.getsockname())

def dns_get_server_ip(domain):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    answers = resolver.resolve(domain)

    for data in answers:
        ip = str(data)
    return ip , domain

def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    my_ip = s.getsockname()[0]
    s.close()
    return my_ip 
def domain_ping(domain):
    strat_time = time.time()
    r  = requests.get('https://media.video.cloud.edu.tw/')
    #r = requests.get('https://203.68.82.33')
    #print(r.status_code)
    if r.status_code == 200 :
        return time.time() - strat_time
    else :
        return 'test failed'
    
def get_server_organization2(server_ip , my_ip , ping_):
    server_ip , domain = server_ip
    server_ip = format_data(server_ip) 
    my_ip = format_data(my_ip)
    tb = pt.PrettyTable()
    tb.field_names = ['Key','Value']
    tb.add_row(['Domain',domain])
    tb.add_row(['My IP Address',my_ip])
    tb.add_row(['Server IP Address',server_ip])
    tb.add_row(['httping',str(ping_)+' s'])
    #print(str(ping_*1000)+' ms')
    r = requests.get(r'https://whois.tanet.edu.tw/showWhoisPublic.php?queryString='+str(server_ip)+'&submit=%E9%80%81%E5%87%BA')
    data = html.fromstring(r.content.decode('UTF-8'))
    max = len(data.xpath('/html/body/center/table[2]/tr'))


    for i in range(1,max):
        if '網段' in str(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td/text()')) :
            tmp_data  = format_data(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td/text()'))
            key = format_data(str(tmp_data[0]))
            value = format_data(str(tmp_data[1]))
            tb.add_row(['-'*30,'-'*30])
            tb.add_row([key,value])

        if len(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td')) == 2 :
            key = format_data(str(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td[1]/text()')))
            value = format_data(str(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td[2]/text()')))
            tb.add_row([key,value])
    print(tb)


def get_server_organization(ip_port):
    server_ip , your_ip = (ip_port)
    server_ip = format_ip_info(server_ip)
    your_ip = format_ip_info(your_ip)
    tb = pt.PrettyTable()
    tb.field_names = ['Key','Value']
    tb.add_row(['My IP Address',your_ip[0]])
    tb.add_row(['Server IP Address',server_ip[0]])
    r = requests.get(r'https://whois.tanet.edu.tw/showWhoisPublic.php?queryString='+str(server_ip[0])+'&submit=%E9%80%81%E5%87%BA')
    data = html.fromstring(r.content.decode('UTF-8'))
    max = len(data.xpath('/html/body/center/table[2]/tr'))


    for i in range(1,max):
        if '網段' in str(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td/text()')) :
            tmp_data  = format_data(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td/text()'))
            key = format_data(str(tmp_data[0]))
            value = format_data(str(tmp_data[1]))
            tb.add_row(['-'*30,'-'*30])
            tb.add_row([key,value])

        if len(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td')) == 2 :
            key = format_data(str(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td[1]/text()')))
            value = format_data(str(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td[2]/text()')))
            tb.add_row([key,value])
    print(tb)

def format_data(data):
    formated_data = str(data).replace('[','').replace(']','').replace('\'','')
    if '：' in formated_data:
        formated_data = formated_data.split('：')
        return formated_data
    else:
        return formated_data
    

def format_ip_info(ip_port):
    ip_port = str(ip_port).replace('(','').replace(')',"").replace('\'','').replace(' ','').split(',')
    return ip_port


def main():
    #url = 'https://video.cloud.edu.tw/video/co_video_content.php?p=401467'
    #url = 'https://media.video.cloud.edu.tw/vod/_definst_/mp4:uploads.video/2023/04/video_401468_1440.mp4/manifest.mpd'
    #url = 'https://media.video.cloud.edu.tw/vod/_definst_/mp4:uploads.video/2023/04/video_401468_1440.mp4/chunk_ctvideo_ridp0va0br708614_cs5400000_mpd.m4s'
    #get_server_organization(get_server_ip(url))
    domain = "media.video.cloud.edu.tw"
    get_server_organization2(dns_get_server_ip(domain),get_my_ip(),domain_ping(domain))
if __name__ == '__main__':
    #domain_ping('https://media.video.cloud.edu.tw')
    main()