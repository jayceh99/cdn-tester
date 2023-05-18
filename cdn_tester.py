import requests
import prettytable as pt
from lxml import html

def get_server_ip(url):
    r = requests.get(url, stream=True)
    return str(r.raw._connection.sock.getpeername()) , str(r.raw._connection.sock.getsockname())

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
    url = 'https://video.cloud.edu.tw/video/co_video_content.php?p=401467'
    #url = 'https://media.video.cloud.edu.tw/vod/_definst_/mp4:uploads.video/2023/04/video_401468_1440.mp4/manifest.mpd'
    #url = 'https://media.video.cloud.edu.tw/vod/_definst_/mp4:uploads.video/2023/04/video_401468_1440.mp4/chunk_ctvideo_ridp0va0br708614_cs5400000_mpd.m4s'
    get_server_organization(get_server_ip(url))



if __name__ == '__main__':
    main()







'''
    import dns.resolver

    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8', '8.8.4.4']
    answers = resolver.resolve("video.cloud.edu.tw")
    for data in answers:
        ip = str(data)

    print(ip)
'''