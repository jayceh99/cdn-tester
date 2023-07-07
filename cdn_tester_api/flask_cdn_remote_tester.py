import os

def remote_tester(ip):
    print(ip)
    domain = 'mediavideocloudedutw.tanetcdn.edu.tw'
    tmp = os.popen(' dig @cdn-nsysu-cdrs03.tanetcdn.edu.tw mediavideocloudedutw.tanetcdn.edu.tw +subnet='+ip+' +short')
    server_ip = tmp.read().replace('\n','')

    #del client_ip , domain , edns_info , message , r ,answer , item , server_ip
    return server_ip
