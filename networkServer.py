import MySQLdb
import math
from networkFormation import positionAP1, positionAP2, positionAP3

def getOptimalPosition(distanceToSensor, positionAntennaX, positionAntennaY):

	gradient_x = 0.0
	gradient_y = 0.0

	positionMobileX = 10.0
	positionMobileY = 10.0

	nAntennas = 3

	for iteration in (0,20):

		for i in range (0,nAntennas):
			a = positionMobileX - positionAntennaX[i]
			b = positionMobileY - positionAntennaY[i]
			c = math.sqrt(math.pow(a,2)+math.pow(b,2)) + 0.001

			gradient_x += a*(1 - distanceToSensor[i]/c)
			gradient_y += b*(1 - distanceToSensor[i]/c)

		gradient_x *= 2.0/nAntennas
		gradient_y *= 2.0/nAntennas

		positionMobileX -= gradient_x*0.5
		positionMobileY -= gradient_y*0.5

		print distanceToSensor[i]

	print "X: "
	print positionMobileX
	print "Y: "
	print positionMobileY

def getAntenna1RX(conexionCursor):

	query = "START TRANSACTION;"
	queryBack=cur.execute(query)

	query = "SELECT * FROM RSSI WHERE AP='AP1' ORDER BY id DESC LIMIT 1;"
	powerRX = cur.execute(query)

	Conexion.commit()

	return cur.fetchone()['SSI']

def getAntenna2RX(conexionCursor):

	query = "START TRANSACTION;"
	queryBack=cur.execute(query)

	query = "SELECT * FROM RSSI WHERE AP='AP2' ORDER BY id DESC LIMIT 1;"
	powerRX = cur.execute(query)

	Conexion.commit()

	return cur.fetchone()['SSI']

def getAntenna3RX(conexionCursor):

	query = "START TRANSACTION;"
	queryBack=cur.execute(query)

	query = "SELECT * FROM RSSI WHERE AP='AP3' ORDER BY id DESC LIMIT 1;"
	powerRX = cur.execute(query)

	Conexion.commit()

	return cur.fetchone()['SSI']

if __name__ == '__main__':

	Conexion = MySQLdb.connect(host='localhost', user='testuser',passwd='test123', db='testMeasures')
	cur = Conexion.cursor(MySQLdb.cursors.DictCursor)

	while True:
		
		antenna1RX = getAntenna1RX(cur)
		time.sleep(0.2)
		antenna2RX = getAntenna2RX(cur)
		time.sleep(0.2)
		antenna3RX = getAntenna3RX(cur)

		antennaRX = [antenna1RX, antenna2RX, antenna3RX]
		positionAntennaX = [int(positionAP1[0:2]),int(positionAP2[0:2]),int(positionAP3[0:2])]
		positionAntennaY = [int(positionAP1[3:5]),int(positionAP2[3:5]),int(positionAP3[3:5])]

		
		distanceToSensor=[0.0138*math.exp(-0.081*antennaRX[0]), 0.0138*math.exp(-0.081*antennaRX[1]) ,0.0138*math.exp(-0.081*antennaRX[2])]


		getOptimalPosition(distanceToSensor, positionAntennaX, positionAntennaY)

		time.sleep(1)
