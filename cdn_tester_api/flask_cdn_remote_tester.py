import dns
import clientsubnetoption
import flask_get_server_info


def remote_tester(ip):
    global server_ip 
    #210.240.152.121
    #140.111.67.82#
    #client_ip = '140.128.53.34'
    client_ip = ip
    domain = 'mediavideocloudedutw.tanetcdn.edu.tw'
    edns_info = clientsubnetoption.ClientSubnetOption(client_ip)
    message = dns.message.make_query(domain, 'A')
    message.use_edns(options=[edns_info])
    r = dns.query.udp(message, '140.111.34.135')

    for answer in r.answer:
        if answer.rdtype == dns.rdatatype.A:
            for item in answer.items:
                server_ip = item.address
    tb = flask_get_server_info.get_server_organization(domain , server_ip , client_ip)

    #del client_ip , domain , edns_info , message , r ,answer , item , server_ip
    return server_ip
