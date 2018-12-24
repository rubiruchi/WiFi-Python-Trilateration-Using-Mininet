#!/usr/bin/env python
from scapy.all import *

import networkFormation
import time
import datetime
import os
from threading import Thread
import MySQLdb

def execMininet():
    networkFormation.topology()

def execScapy1():
    execfile("scapyAP1.py")

def execScapy2():
    execfile("scapyAP2.py")

def execScapy3():
    execfile("scapyAP3.py")	

Conexion = MySQLdb.connect(host='manuelmoyatfmdb.co8n1ozzlu1i.eu-west-3.rds.amazonaws.com', port = 3306,user='manuelmoya',passwd='manuelmoya', db='ManuelMoyaTFMDB')
cur = Conexion.cursor(MySQLdb.cursors.DictCursor)

try:
    cur.execute("START TRANSACTION;")
    cur.execute("DROP TABLE IF EXISTS RSSI;")
    Conexion.commit()
    print "Tabla creada"
except MySQLdb.Warning:
    print "La tabla no esta creada"

cur.execute("START TRANSACTION;")
cur.execute("CREATE TABLE IF NOT EXISTS RSSI(id INT, AP VARCHAR(25), SSI INT);")
Conexion.commit()

subprocess1 = Thread(target=execMininet)
subprocess1.start()

subproc2 = Thread(target=execScapy1)
subproc3 = Thread(target=execScapy2)
subproc4 = Thread(target=execScapy3)

time.sleep(10)
subproc2.start()
time.sleep(2)
subproc3.start()
time.sleep(2)
subproc4.start()

while subprocess1.isAlive():
    pass