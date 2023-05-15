import requests
from lxml import html

def get_server_ip(url):
    r = requests.get(url, stream=True)
    #print('local IP port is '+str(r.raw._connection.sock.getsockname()))
    #print(str(r.raw._connection.sock.getpeername()))
    return str(r.raw._connection.sock.getpeername())

def get_server_organization(ip_port):
    ip_port = format_ip_info(ip_port)
    print ('\n\nserver IP port is '+ip_port[0]+':'+ip_port[1]+'\n\n')
    r = requests.get(r'https://whois.tanet.edu.tw/showWhoisPublic.php?queryString='+str(ip_port[0])+'&submit=%E9%80%81%E5%87%BA')
    data = html.fromstring(r.content.decode('UTF-8'))
    max = len(data.xpath('/html/body/center/table[2]/tr'))

    for i in range(1,max):
        if '網段' in str(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td/text()')) :
            print('--------------------------------------------')
            tmp_data  = format_data(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td/text()'))
            print(f"{tmp_data[0]:<20}:{tmp_data[1]:>20}")


            #print(tmp_data[0]+'     :     '+tmp_data[1])
        if len(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td')) == 2 :
            print(f"{format_data(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td[1]/text()')):<20}:{format_data(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td[2]/text()')):>20}")



            #print(format_data(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td[1]/text()'))+'     :     ',end='')
            #print(format_data(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td[2]/text()')))
            
        
    print('--------------------------------------------')


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
    url = 'https://media.video.cloud.edu.tw/vod/_definst_/mp4:uploads.video/2023/04/video_401468_1440.mp4/manifest.mpd'
    get_server_organization(get_server_ip(url))



if __name__ == '__main__':
    main()







'''
import dns.resolver

myResolver = dns.resolver.Resolver()
myResolver.nameservers = ['8.8.8.8', '8.8.4.4']
myAnswers = myResolver.resolve("www.momoshop.com.tw")
for rdata in myAnswers:
    ip = str(rdata)

print(ip)
'''