from scapy.all import *
import threading
import MySQLdb
from datetime import datetime
import networkFormation

def getAverageSSI():
    global ssiFinal
    return ssiFinal

def setParamsAP3():
    global window
    global timestampAP3
    global SSID
    global datetime
    global iterator3
    global ssiArrayAP3

    window = 1
    timestampAP3 = datetime.now()
    SSID='DefaultName'
    iterator3 = 0
    ssiArrayAP3 = []

def myPacketHandler(pkt) :
    global SSID
    global timestampAP3
    global iterator3
    global ssiArrayAP3

    if pkt.haslayer(Dot11) :

        Conexion = MySQLdb.connect(host='manuelmoyatfmdb.co8n1ozzlu1i.eu-west-3.rds.amazonaws.com', port = 3306,user='manuelmoya',passwd='manuelmoya', db='ManuelMoyaTFMDB')
        cur = Conexion.cursor(MySQLdb.cursors.DictCursor)

        #type 0 = Management subtype 4 = Beacon
        if pkt.type == 0 and pkt.subtype == 8 :

            ssiNew = -(256-ord(pkt.notdecoded[-4:-3]))
            ssiArrayAP3.append(ssiNew)

            SSID = pkt.info;
            if SSID.startswith("Mobile") :

                diffT=(datetime.now()-timestampAP3).seconds
                
                if diffT > window and len(ssiArrayAP3) > 0:

                    query = "START TRANSACTION;"
                    queryBack=cur.execute(query)

                    iterator3+=1

                    query = "INSERT INTO RSSI VALUES(%d,\"AP3\",%d);"%(iterator3, sum(ssiArrayAP3)/len(ssiArrayAP3))
                    queryBack = cur.execute(query)

                    ssiArrayAP3 = []

                    Conexion.commit()

                    timestampAP3=datetime.now()

setParamsAP3()          

try:
    sniff(iface="ap3-wlan1", prn = myPacketHandler, store=0)
except Exception as e:
    print e
    print "Sniff AP3 Off"