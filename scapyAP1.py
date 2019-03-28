################################################
################################################
################################################
###        TFM Manuel Moya Ferrer            ###
###      -    Mininet Simulation     -       ###
#             Microservice AP1                 #
################################################
################################################
################################################

from scapy.all import *
import threading
from datetime import datetime
import MySQLdb
import networkFormation

def getAverageSSI():
    global ssiFinal
    return ssiFinal

def setParamsAP1():
    global window
    global timestamp
    global datetime
    global iterator
    global ssiArrayAP1

    window = 1
    timestamp = datetime.now()
    iterator = 0
    ssiArrayAP1 = []

def myPacketHandler(pkt) :
    global timestamp
    global iterator
    global ssiArrayAP1

    if pkt.haslayer(Dot11) :

        Conexion = MySQLdb.connect(host='manuelmoyatfmdb.co8n1ozzlu1i.eu-west-3.rds.amazonaws.com', port = 3306,user='manuelmoya',passwd='manuelmoya', db='ManuelMoyaTFMDB')
        cur = Conexion.cursor(MySQLdb.cursors.DictCursor)

        if pkt.type == 0 and pkt.subtype == 8 :

            ssiNew = -(256-ord(pkt.notdecoded[-4:-3]))
            ssiArrayAP1.append(ssiNew)

            SSID = pkt.info;

            if SSID.startswith("Mobile") :

                diffT=(datetime.now()-timestamp).seconds
             
                if diffT > window and len(ssiArrayAP1) > 0:

                    query = "START TRANSACTION;"
                    queryBack=cur.execute(query)

                    query = "INSERT INTO RSSI VALUES(%d,\"AP1\",%d);"%(iterator, sum(ssiArrayAP1)/len(ssiArrayAP1) )
                    queryBack = cur.execute(query)

                    ssiArrayAP1 = []

                    Conexion.commit()

                    iterator+=1

                    timestamp=datetime.now()


setParamsAP1()

try:
    sniff(iface="ap1-wlan1", prn = myPacketHandler, store=0)
except Exception as e:
    print e
    print "Sniff AP1 Off"