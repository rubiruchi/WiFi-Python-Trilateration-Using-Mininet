
#        TFM Manuel Moya Ferrer            ###
##      -    Mininet Simulation     -       ##
##                   README                 ##



1º In order to execute the simulation, first you can consider changing the devices parameters at the beginning of networkFormation.py File, you will see something like the following ->


```PositionMobile1='20,20,00'  # x, y, z from 0 to 99 m
positionAP1='00,00,00'
positionAP2='50,00,00'
positionAP3='00,50,00'

antennaGainMobile1='0'
txpowerMobile1='0'
antennaHeightMobile1='2'
channelMobile1='36'
rangeMobile1=100

antennaGainAP1='3'
...
```

Feel free to modify it at your convenience

2º Once you have set the parameters as needed, you can start the emulator by running the following command:

> sudo python execNetworkEmulator.py

3º After some time, once the database has data from the three microservices (AP1, AP2 and AP3), the networkServer.py script will be able to get the device location by executing the algorithm with the data it has queried from AWS. To run it, you just need to execute the following command:

> sudo python networkServer.py
