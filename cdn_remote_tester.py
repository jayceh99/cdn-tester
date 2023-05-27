import dns
import clientsubnetoption
import dns.resolver

ip = 'IP_addr'
edns_info = clientsubnetoption.ClientSubnetOption(ip)
message = dns.message.make_query('media.video.cloud.edu.tw', 'A')
message.use_edns(options=[edns_info])
r = dns.query.udp(message, '8.8.8.8')

for answer in r.answer:
    if answer.rdtype == dns.rdatatype.A:
        for item in answer.items:
            ip_address = item.address
            print("IP Address:", ip_address)