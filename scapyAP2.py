from scapy.all import *
import threading
import MySQLdb
from datetime import datetime
import networkFormation

def getAverageSSI():
    global ssiFinal
    return ssiFinal

def setParams():
    global window
    global timestamp
    global SSID
    global datetime
    window = 1
    timestamp = datetime.now()
    SSID='DefaultName'

def myPacketHandler(pkt) :
    global SSID
    global timestamp

    if pkt.haslayer(Dot11) :

        Conexion = MySQLdb.connect(host='localhost', user='testuser',passwd='test123', db='testMeasures')
        cur = Conexion.cursor(MySQLdb.cursors.DictCursor)

        #type 0 = Management subtype 4 = Beacon
        if pkt.type == 0 and pkt.subtype == 8 :
            #if pkt.addr2 not in ap_list :
            ssiNew = -(256-ord(pkt.notdecoded[-4:-3]))
            SSID = pkt.info;
            if SSID.startswith("Mobile") :

                diffT=(datetime.now()-timestamp).seconds
                
                if diffT>window:

                    query = "START TRANSACTION;"
                    queryBack=cur.execute(query)

                    query = "INSERT INTO RSSI VALUES(\"AP2\",%d);"%(ssiNew)
                    queryBack = cur.execute(query)

                    Conexion.commit()

                    timestamp=datetime.now()

try:
    sniff(iface="ap2-wlan1", prn = myPacketHandler, store=0)
except Exception as e:
    print e
    print "Sniff AP2 Off"