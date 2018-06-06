import math
from random import gauss


class propagationModel():
   
      def pathLossCalculus(self, mobileCoord, APcoord):
            
            dist=self.calculeDistance(mobileCoord,APcoord)

            """Path Loss Model:
            (f) signal frequency transmited(Hz)
            (d) is the distance between the transmitter and the receiver (m)
            (c) speed of light in vacuum (m)
            (L) System loss"""
            f = 2.14 * (10 ** 9)  # Convert Ghz to Hz
            c = 299792458.0
            L = 1

            lambda_ = c / f  # lambda: wavelength (m)
            denominator = lambda_ ** 2
            numerator = (4 * math.pi * dist) ** 2 * L
            pathLoss_ = 10 * math.log10(numerator / denominator)

            return int(pathLoss_)

      def friisLoss(self, mobileCoord, APcoord, MobileAntennaGain, TXPowerMobile, APAntenaGain):
            """Friis Propagation Loss Model:
            (f) signal frequency transmited(Hz)
            (d) is the distance between the transmitter and the receiver (m)
            (c) speed of light in vacuum (m)
            (L) System loss"""
            gt = int(MobileAntennaGain) #antena gain of node mobile
            pt = int(TXPowerMobile) #tx power of node mobile
            gr = int(APAntenaGain) #antena gain of node AP
            gains = pt + gt + gr

            pathLoss = self.pathLossCalculus(mobileCoord,APcoord)
            totalLoss = pathLoss - gains

            return totalLoss

      def logDistanceLoss(self, mobileCoord, APcoord, MobileAntennaGain, TXPowerMobile, APAntenaGain):
            """Log Distance Propagation Loss Model:
            ref_dist (m): The distance at which the reference loss is
            calculated
            exponent: The exponent of the Path Loss propagation model, where 2
            is for propagation in free space
            (dist) is the distance between the transmitter and the receiver (m)"""
            gt = int(MobileAntennaGain) #antena gain of node mobile
            pt = int(TXPowerMobile) #tx power of node mobile
            gr = int(APAntenaGain) #antena gain of node AP
            exp=3 #exponent of losses due to massification or buildings, etc
            ref_dist = 1
            pathLoss = self.pathLossCalculus(mobileCoord,APcoord)
            gains = pt + gt + gr

            dist=self.calculeDistance(mobileCoord,APcoord)
      
            pathLossDb = 10 * exp * math.log10(dist / ref_dist)
            totalLoss = (int(pathLoss) + int(pathLossDb)) - gains

            return totalLoss

      def logNormalShadowingLoss(self, mobileCoord, APcoord, MobileAntennaGain, TXPowerMobile, APAntenaGain):
            """Log-Normal Shadowing Propagation Loss Model:
            ref_dist (m): The distance at which the reference loss is
            calculated
            exponent: The exponent of the Path Loss propagation model, where 2
            is for propagation in free space
            (d) is the distance between the transmitter and the receiver (m)
            gRandom is a Gaussian random variable"""
            gt = int(MobileAntennaGain) #antena gain of node mobile
            pt = int(TXPowerMobile) #tx power of node mobile
            gr = int(APAntenaGain) #antena gain of node AP
            exp=3 #exponent of losses due to massification or buildings, etc
            ref_dist=1
            
            mean=0
            variance=2
            gRandom = float('%.2f' % gauss(mean, variance))
            gains = pt + gt + gr
            pathLoss = self.pathLossCalculus(mobileCoord,APcoord)

            dist=self.calculeDistance(mobileCoord,APcoord)

            pathLossDb = 10 * exp * math.log10(dist / ref_dist) + \
                     gRandom

            totalLoss = (int(pathLoss) + int(pathLossDb)) - gains

            return totalLoss

      def ITU(self, mobileCoord, APcoord, MobileAntennaGain, TXPowerMobile, APAntenaGain):
            """International Telecommunication Union (ITU) Propagation Loss Model:"""
            gt = int(MobileAntennaGain) #antena gain of node mobile
            pt = int(TXPowerMobile) #tx power of node mobile
            gr = int(APAntenaGain) #antena gain of node AP
            exp=3 #exponent of losses due to massification or buildings, etc

            f = 2.14 * (10 ** 9)  # Convert Ghz to Hz
            c = 299792458.0
            L = 1

            N = 28  # Power Loss Coefficient
            pL = 28
            lF = 5  # Floor penetration loss factor
            nFloors = 6  # Number of Floors
            gains = pt + gt + gr

            """Power Loss Coefficient Based on the Paper 
            Site-Specific Validation of ITU Indoor Path Loss Model at 2.4 GHz 
            from Theofilos Chrysikos, Giannis Georgopoulos and Stavros Kotsopoulos"""
            dist=self.calculeDistance(mobileCoord,APcoord)

            if dist > 16:
                  N = 38
            if pL != 0:
                  N = pL

            pathLossDb = 20 * math.log10(f) + N * math.log10(dist) + \
                     lF * nFloors - 28

            totalLoss = int(pathLossDb) - gains

            return totalLoss

      def twoRayGroundLosses(self, mobileCoord, APcoord, MobileAntennaGain, TXPowerMobile, APAntenaGain, MobileAntennaHeight, APAntenaHeight):
            """Two Ray Ground Propagation Loss Model (does not give a good result for
            a short distance)"""
            
            hr = int(APAntenaHeight)
            ht = int(MobileAntennaHeight)
            gt = int(MobileAntennaGain) #antena gain of node mobile
            pt = int(TXPowerMobile) #tx power of node mobile
            gr = int(APAntenaGain) #antena gain of node AP
            gains = pt + gt + gr

            dist=self.calculeDistance(mobileCoord,APcoord)

            L = 1

            pathLossDb = (pt * gt * gr * ht ** 2 * hr ** 2) / (dist ** 4 * L)
            totalLoss = int(pathLossDb) - gains

            return totalLoss


      # LAST TWO NOT WORKING OKAY FOR SHORT DISTANCES (<1000 metres)

      def youngLosses(self, mobileCoord, APcoord, MobileAntennaGain, APAntenaGain, MobileAntennaHeight, APAntenaHeight):
            "Young Propagation Loss Model"

            hr = int(APAntenaHeight)
            ht = int(MobileAntennaHeight)
            gt = int(MobileAntennaGain) #antena gain of node mobile
            gr = int(APAntenaGain) #antena gain of node AP

            cf = 0.01075  # clutter factor

            dist=self.calculeDistance(mobileCoord,APcoord)

            totalLoss = int(dist ** 4 / (gt * gr) * (ht * hr) ** 2 * cf)

            return totalLoss

      def calculeDistance(self, mobileCoord, APcoord):

            xMobile=int(mobileCoord[0:2])
            yMobile=int(mobileCoord[3:5])

            xAP=int(APcoord[0:2])
            yAP=int(APcoord[3:5])

            dist=math.sqrt(abs(xAP-xMobile)**2 + abs(yAP-yMobile)**2)

            return dist
