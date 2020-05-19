import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, url_for, request
import logging
import threading
from time import sleep

app = Flask(__name__)
app.config['TEMPLAES_AUTO_RELOAD'] = True
log = logging.getLogger("werkzeug")
log.disabled = True
run_flag = True
pitemps = (1, 2)

def piservers():
    url = [None] * len(pitemps)

    i = 0
    while i < len(url):
        url[i]=('http://pitemp' + str(pitemps[i]) + '/readings')
        i += 1

    return url

piurls = piservers()

def pidata():
    pitempdata = { }
    i = 0
    while i < len(pitemps):
        pitempdata["temp" + str(i+1)] = \
            BeautifulSoup(requests.get(piurls[i]).content, 'html.parser').find(id='temp').text
        pitempdata["time" + str(i+1)] = \
            BeautifulSoup(requests.get(piurls[i]).content, 'html.parser').find(id='time').text
        i += 1
    
    return pitempdata

pitempdata = pidata()

def background():
    while run_flag:
        global pitempdata
        pitempdata = pidata()
        sleep(30)

background_thread = threading.Thread(target = background)

@app.route('/')
def index():
    return render_template('index.html', **pitempdata)

if __name__ == '__main__':
    background_thread.start()
    sleep(1)
    try:
        app.run(debug = False, host = '0.0.0.0', port = 80, use_reloader = False)
    except Exception as e:
        print (e)
        pass
    run_flag = False
    print("Waiting for background to quit")
    background_thread.join()
