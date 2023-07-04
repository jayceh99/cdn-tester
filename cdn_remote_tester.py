import dns
import clientsubnetoption
import get_server_info
#210.240.152.121
#140.111.67.82
#client_ip = '140.128.53.34'
#140.128.51.17
client_ip = '140.111.67.82'
domain = 'media.video.cloud.edu.tw'
domain = 'mediavideocloudedutw.tanetcdn.edu.tw'
edns_info = clientsubnetoption.ClientSubnetOption(client_ip)
message = dns.message.make_query(domain, 'A')
message.use_edns(options=[edns_info])
r = dns.query.udp(message, '140.111.34.135')
#r = dns.query.udp(message, '163.28.6.1')
for answer in r.answer:
    if answer.rdtype == dns.rdatatype.A:
        for item in answer.items:
            server_ip = item.address

get_server_info.get_server_organization(domain , server_ip , client_ip)

del client_ip , domain , edns_info , message , r ,answer , item , server_ip