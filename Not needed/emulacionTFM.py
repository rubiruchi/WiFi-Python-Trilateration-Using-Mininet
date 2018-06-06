#!/usr/bin/python

'This example show how to configure Propagation Models'

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelAP
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import time

def topology():

    "Create a network."
    net = Mininet(controller=Controller, link=TCLink, accessPoint=OVSKernelAP, 
    	enable_wmediumd=True, enable_interference=True)

    print "*** Creating nodes"
    
    ap10 = net.addAccessPoint('Mobile1', ssid='Mobile1', equipmentModel='DI524',
    	mode='g', channel='1', position='0,10,0')

    ap1 = net.addAccessPoint('ap1', ssid='Antenna1', equipmentModel='DI524',
    	mode='g', channel='1', position='0,0,0')

    ap2 = net.addAccessPoint('ap2', ssid='Antenna2', equipmentModel='DI524',
    	mode='g', channel='1', position='100,0,0')

    ap3 = net.addAccessPoint('ap3', ssid='Antenna3', equipmentModel='DI524',
    	mode='g', channel='1', position='0,100,0')



    c1 = net.addController('c1', controller=Controller)

    net.propagationModel(model="logDistancePropagationLossModel", exp=3.5)


    print "*** Configuring wifi nodes"
    net.configureWifiNodes()

    net.plotGraph(max_x=100, max_y=100)

    net.seed(20)

    #net.startMobility(time=0, model='RandomDirection', max_x=90,min_x=10, max_y=90, min_y=90,min_v=0.5, max_v=0.8)

    print "*** Starting network"
    net.build()
    c1.start()
    ap1.start([c1])
    ap2.start([c1])
    ap3.start([c1])
    ap10.start([c1]) #Mobile from ap10 forward
	
    
    #AP1 TO MODE MONITOR
    ap1.cmd("ifconfig ap1-wlan1 down")
    ap1.cmd('iwconfig ap1-wlan1 mode monitor')
    ap1.cmd('ifconfig ap1-wlan1 up')

    #AP2 TO MODE MONITOR
    ap2.cmd("ifconfig ap2-wlan1 down")
    ap2.cmd('iwconfig ap2-wlan1 mode monitor')
    ap2.cmd('ifconfig ap2-wlan1 up')
    
    #AP3 TO MODE MONITOR
    ap3.cmd("ifconfig ap3-wlan1 down")
    ap3.cmd('iwconfig ap3-wlan1 mode monitor')
    ap3.cmd('ifconfig ap3-wlan1 up')

    print "*** Running CLI, le pasa la red a la consola de mininet"
    CLI(net)
    

	#sdo_py('sta1.params["rssi"]')

    print "*** Stopping network"
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()
