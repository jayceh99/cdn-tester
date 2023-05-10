import requests
from lxml import html
from requests.packages.urllib3.connectionpool import HTTPConnectionPool

def _make_request(self,conn,method,url,**kwargs):
    response = self._old_make_request(conn,method,url,**kwargs)
    sock = getattr(conn,'sock',False)
    if sock:
        setattr(response,'peer',sock.getpeername())
    else:
        setattr(response,'peer',None)
    return response

HTTPConnectionPool._old_make_request = HTTPConnectionPool._make_request
HTTPConnectionPool._make_request = _make_request



r = requests.get('https://video.cloud.edu.tw/video/co_video_content.php?p=401467')
#r = requests.get('https://media.video.cloud.edu.tw/vod/_definst_/mp4:uploads.video/2023/04/video_401468_1440.mp4/manifest.mpd')
ip_port = (r.raw._original_response.peer)
ip_port = str(ip_port).replace('(','').replace(')',"").replace('\'','').replace(' ','').split(',')
print (ip_port[0]+':'+ip_port[1])
#print(r.content)
r = requests.get(r'https://whois.tanet.edu.tw/showWhoisPublic.php?queryString='+str(ip_port[0])+'&submit=%E9%80%81%E5%87%BA')
data = html.fromstring(r.content.decode('UTF-8'))
max = len(data.xpath('/html/body/center/table[2]/tr'))
for i in range(1,max):
    print(data.xpath('/html/body/center/table[2]/tr['+str(i)+']/td/text()'))