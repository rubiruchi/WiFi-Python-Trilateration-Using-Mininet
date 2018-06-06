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

Conexion = MySQLdb.connect(host='localhost', user='testuser',passwd='test123', db='testMeasures')
cur = Conexion.cursor(MySQLdb.cursors.DictCursor)

try:
    cur.execute("START TRANSACTION;")
    cur.execute("DROP TABLE IF EXISTS RSSI;")
    Conexion.commit()
    print "Tabla creada"
except MySQLdb.Warning:
    print "La tabla no esta creada"

cur.execute("START TRANSACTION;")
cur.execute("CREATE TABLE IF NOT EXISTS RSSI(AP VARCHAR(25), SSI INT);")
Conexion.commit()

subprocess1 = Thread(target=execMininet)
subprocess1.start()

subproc2 = Thread(target=execScapy1)
subproc3 = Thread(target=execScapy2)
subproc4 = Thread(target=execScapy3)


time.sleep(10)
subproc2.start()
subproc3.start()
subproc4.start()

while subprocess1.isAlive():
    pass