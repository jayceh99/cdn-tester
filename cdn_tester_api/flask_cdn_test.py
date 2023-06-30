import flask_cdn_remote_tester
from flask import Flask , render_template , request , redirect
import requests
app = Flask(__name__)


@app.route('/')

def index():
    ip = request.remote_addr 
    server_ip =flask_cdn_remote_tester.remote_tester(ip)
    r = requests.get(r'https://whois.tanet.edu.tw/showWhoisPublic.php?queryString='+str(server_ip)+'&submit=%E9%80%81%E5%87%BA')
    tmp  = r.text.split('\n')
    flag = 0
    for  k in tmp :
        flag = flag +1
        if '<TABLE>' in k:
            break
    tmp.insert(flag , '<h4> <b>Test Domain : mediavideocloudedutw.tanetcdn.edu.tw &nbsp</h4></b><h4> <b>YourIPaddr :&nbsp' + ip +'</h4></b><h4> <b>ServerIPaddr :&nbsp' + server_ip +'</h4></b>')

    q = ''
    for a in tmp :
        q = q +a
    return q
    

if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=8080)