import prettytable as pt
from lxml import html
import requests

def get_server_organization(domain , server_ip , client_ip , httping = None):

    tb = pt.PrettyTable()
    tb.field_names = ['Key','Value']
    tb.add_row(['Domain Name',domain])
    tb.add_row(['Client IP Address',client_ip])
    tb.add_row(['Server IP Address',server_ip])
    if httping != None :
        tb.add_row(['httping',httping])
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
    del domain , server_ip , client_ip , httping , r , data , max , tmp_data , key , value , tb 

def format_data(data):
    formated_data = str(data).replace('[','').replace(']','').replace('\'','')
    if '：' in formated_data:
        formated_data = formated_data.split('：')
        return formated_data
    else:
        return formated_data