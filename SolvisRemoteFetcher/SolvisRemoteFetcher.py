#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from random import randint
from datetime import datetime, time
from os import getenv
import sys 
import requests
from requests.auth import HTTPDigestAuth
import queue
import threading
import signal
import pprint

q = queue.Queue()
threads = []
num_worker_threads = 1

def convertAtoInt(s):
    v = ''
    while len(s):
        v = v + s[-2:]
        s = s [:-2]
    return int(v, 16)

class SolvisRemote:
    """ Class to read sensor data from a Solvis Remote and parse values """
    def __init__(self):
        self._fields = (("Header", 12, "Header", None),
                        ("Uhrzeit", 6, "Systemzeit", self._parseTime),
                        ("Anlagentyp", 4, "Anlagentyp", None),
                        ("Systemnummer", 4, "Systemnummer", None),
                        ("S1", 4, "Speicher Oben", self._parseTemp),
                        ("S2", 4, "Warmwasser", self._parseTemp),
                        ("S3", 4, "Speicherreferenz", self._parseTemp),
                        ("S4", 4, "H.puffer oben", self._parseTemp),
                        ("S5", 4, "Solar-VL", self._parseTemp),
                        ("S6", 4, "Solar-RL", self._parseTemp),
                        ("S7", 4, "Solar-Druck", self._parseTemp),
                        ("S8", 4, "Kollektor", self._parseTemp),
                        ("S9", 4, "H.puffer unten", self._parseTemp),
                        ("S10", 4, "Aussentemperatur", self._parseTemp),
                        ("S11", 4, "Zirkulation", self._parseTemp),
                        ("S12", 4, "Vorlauf HK1", self._parseTemp),
                        ("S13", 4, "Vorlauf HK2", self._parseTemp),
                        ("S14", 4, "Kesselfühler", self._parseTemp),
                        ("S15", 4, "", self._parseTemp),
                        ("S16", 4, "Holzkessel", self._parseTemp),
                        ("S18", 4, "Durchfluss l/m", self._parse4div10),
                        ("S17", 4, "Durchfluss Solarpumpe l/h", self._parse4),
                        ("AI1", 4, "", self._parse4div10),
                        ("AI2", 4, "", self._parse4div10),
                        ("AI3", 4, "", self._parse4div10),
                        ("P1", 2, "", self._parseSwitch),
                        ("P2", 2, "", self._parseSwitch),
                        ("P3", 2, "", self._parseSwitch),
                        ("P4", 2, "", self._parseSwitch),
                        ("RF1", 4, "Raumfuehler Heizkreis1", self._parseTemp),
                        ("RF2", 4, "Raumfuehler Heizkreis2", self._parseTemp),
                        ("RF3", 4, "Raumfuehler Heizkreis3", self._parseTemp),
                        ("A1", 2, "Pumpe Solar", self._parseSwitch),
                        ("A2", 2, "Pumpe Warmwasser", self._parseSwitch),
                        ("A3", 2, "Pumpe HK1", self._parseSwitch),
                        ("A4", 2, "Pumpe HK2", self._parseSwitch),
                        ("A5", 2, "Pumpe Zirkulation", self._parseSwitch),
                        ("A6", 2, "Pumpe HK3", self._parseSwitch),
                        ("A7", 2, "Ladepumpe1", self._parseSwitch),
                        ("A8", 2, "HK1 Mischer auf", self._parseSwitch),
                        ("A9", 2, "HK1 Mischer zu", self._parseSwitch),
                        ("A10", 2, "HK2 Mischer auf", self._parseSwitch),
                        ("A11", 2, "HK2 Mischer zu", self._parseSwitch),
                        ("A12", 2, "Brenner Fremdgerät", self._parseSwitch),
                        ("A13", 2, "Ladepumpe2", self._parseSwitch),
                        ("A14", 2, "Brenner", self._parseSwitch),
                        ("skip_1", 16, "", None),
                        ("SEv", 4, "Solarertrag kWh", self._parse4),
                        ("skip_2", 10, "", None),
                        ("P5v", 2, "", self._parseSwitch),
                        ("skip_3", 18, "", None),
                        ("SLv", 4, "Solarleistung kW", self._parse4div10))
        self.values = {}
        self._now = None
        self._server = None
        self._baseurl = None
        self._auth = None

    def connect(self, server, user, passwd):
        """ Connect to Solvis Remote via HTTP Digest auth and fest data"""
        self._server = server
        self._baseurl = 'http://{}'.format(server)
        self._auth = HTTPDigestAuth(user, passwd)
        self.update()

    def update(self):
        """ Fetch latest sensor and parse """
        dummy = randint(10000000,99999999)
        # todo: handle connection problems
        # seen so far: no network, no dns, auth failed
        try:
            r = requests.get('{}/sc2_val.xml?dummy={}'.format(self._baseurl, dummy), auth=self._auth)
        except requests.exceptions.RequestException as e:
            print(datetime.now(), "- Error", e)
            return False
        data = r.text[11:450] if r.status_code == 200 else None
        # print(data)
        if data:
            self.parseValues(data)
            self._now = datetime.now()
            return True
        else:
            return False

    def parseValues(self, data):
        """ Parse measurement string from Remote into dictionary """
        offset = 0
        for key, length, _, func in self._fields:
            val = data[offset:offset+length]
            if func:
                val = func(val)
            self.values[key] = val
            offset += length

    def _parseTime(self, s):
        """ Convert time string to datetime object """
        t = time(hour = int(s[0:2], 16), minute = int(s[2:4], 16), second = int(s[4:6], 16))
        d = datetime.today()
        return datetime.combine(d, t)

    def _parseTemp(self, s):
        """ Convert temperature string to integer """
        value = convertAtoInt(s)
        value = value - 65536 if value > 32767 else value
        return value / 10

    def _parse4(self, s):
        """ Convert 4 charater string to integer value """
        value = convertAtoInt(s)
        return value

    def _parse4div10(self, s):
        """ Convert integer to float (.e.g Temperature 0192 to 19.2 °C) """
        return self._parse4(s)/10

    def _parseSwitch(self, s):
        """ Convert Relais string to boolean """
        return False if convertAtoInt(s) == 0 else True

    def checkTime(self):
        """ Calculate and print lag between system time and solvis remote time (it drifts a lot) """
        print("Time lag is: {} s (negative means Solvis is ahead of real time)".format(round((self._now - self.values['Uhrzeit']).total_seconds())))
        return

    def toInfluxLineProtocolValues(self):
        """ Convert dictionary of measurement values into InfluxDB line protocol string """
        r = []
        for key, val in self.values.items():
            if type(val) == int:
                s='{}={}i'.format(key, val)
            elif type(val) == bool:
                s='{}={}'.format(key, val)
            elif type(val) == str:
                s='{}="{}"'.format(key, val)
            elif type(val) == float:
                s='{}={}'.format(key, val)
            elif type(val) == datetime:
                s='{}="{}"'.format(key, val)
            else:
                s='{}="{}"'.format(key, str(val))

            r.append(s)

        return ','.join(r)

# https://stackoverflow.com/questions/18499497/how-to-process-sigterm-signal-gracefully
class GracefulKiller:
    kill_now = False
    def __init__(self):
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        signal.signal(signal.SIGINT, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        print("Exiting ...")
        self.kill_now = True
        q.join()
        for _ in range(num_worker_threads):
            q.put(None)
        for t in threads:
            t.join()
            sys.exit(0)

# https://docs.python.org/3/library/queue.html
def worker():
    while True:
        item = q.get()
        if item is None:
            break
        sendInfluxRequest(item)
        q.task_done()

def sendInfluxRequest(req):
    url, auth, payload = req
    rc = 0
    # retry until we successfully deliver our data: rc.status_code=204
    while rc != 204:
        try:
            r = requests.post(url, auth = auth, data = payload)
            rc = r.status_code
        except requests.exceptions.Timeout as r:
            print(datetime.now(), "- Timeout")
            sleep(10)
            pass
        except requests.exceptions.ConnectionError as r:
            print(datetime.now(), "- ConnectionError")
            sleep(10)
            pass

def main_fetch():
    server = getenv('SOLVIS_SERVER', 'solvisremote')
    user = getenv('SOLVIS_USER', 'solvis')
    pw = getenv('SOLVIS_PASSWORD', 'solvis')
    
    print("Solvis\n Server  : {}\n User    : {}".format(server, user))
    sr = SolvisRemote()
    sr.connect(server, user, pw)

    measurement = 'solvis'

    while True:
        sr.update()
        #print(sr.getTime().isoformat(timespec='auto'), 'S11: {} C'.format(sr.getTemp(11)))
        now = int(datetime.utcnow().timestamp()) # use seconds instead of us*1e6)
        # print(now, sr.values)
        print("{} {} {}".format(measurement, sr.toInfluxLineProtocolValues(), now))
#        pprint.pprint(sr.values)
        sleeptime = 60 - datetime.utcnow().second
        sleep(sleeptime)

def main_sendToInflux():
    influx_server = getenv('INFLUX_SERVER', 'http://localhost:8086')
    influx_database = getenv('INFLUX_DATABASE', 'solvis')
    influx_username = getenv('INFLUX_USERNAME', 'solvis')
    influx_password = getenv('INFLUX_PASSWORD', 'solvis')
    url = influx_server + "/write?db=" + influx_database + "&precision=s"

    print("Influx\n Server  : {}\n Database: {}\n User    : {}".format(influx_server, influx_database, influx_username))

    server = getenv('SOLVIS_SERVER', 'solvisremote')
    user = getenv('SOLVIS_USER', 'solvis')
    pw = getenv('SOLVIS_PASSWORD', 'solvis')

    print("Solvis\n Server  : {}\n User    : {}".format(server, user))

    sr = SolvisRemote()
    sr.connect(server, user, pw)

    killer = GracefulKiller()

    for i in range(num_worker_threads):
        t = threading.Thread(target = worker)
        t.start()
        threads.append(t)
       
    while True:
        sleeptime = 60 - datetime.utcnow().second
        # sleeptime = 5
        sleep(sleeptime)
        if sr.update():
            # did use utcnow() instead of now() to generate UTC timestamps to send to Influx
            # but time was off. Seems that Influx automatically converts locla timestamp
            # to UTC before storing. Keep an eye on it.
            now = int(datetime.now().timestamp()) # use seconds instead of us*1e6)
            payload = "{} {} {}".format(server, sr.toInfluxLineProtocolValues(), now)
            q.put((url, (influx_username, influx_password), payload))

def main_stdin():
    measurement = 'SolvisRemote/'

    sr = SolvisRemote()
    for line in sys.stdin:
        ts, val = line.split()
        sr.parseValues(val)
        print("{} {} {}".format(measurement, sr.toInfluxLineProtocolValues(), ts))

if __name__ == '__main__':
    main_fetch()
