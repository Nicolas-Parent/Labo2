from gpiozero import DigitalInputDevice
from gpiozero import DigitalOutputDevice
from gpiozero import PWMOutputDevice
import numpy as np
import cv2
import thread
import time


# Auteur: Nicolas Parent
# But du projet: Contrôler un robot mobile à partir du clavier
#sortie echo
Echo = DigitalInputDevice(21)
#trigger
TR = DigitalOutputDevice(20)
#Led rouge
LED = DigitalInputDevice(16)

class Sonar: 
    def __init__(self,temps):
        self._temps = temps
    def activerCompteur(self):
        self._temps = time.perf_counter()
    #retourne la distance de l'onde en mètres
    def MesurerDistance(self):
        temps_stop = time.perf_counter()
        tempsR = temps_stop - self._temps
        distance = (tempsR * 343)/2
        return distance
# Roue
ENA = PWMOutputDevice(18)
IN_1 = DigitalOutputDevice(15)
IN_2 = DigitalOutputDevice(24)
ENB = PWMOutputDevice(25)
IN_3 = DigitalOutputDevice(23)
IN_4 = DigitalOutputDevice(14)

ALL_IN = [IN_1, IN_2, IN_3, IN_4]
ALL_EN = [ENA, ENB]


class Robot:
    def avancer(self):
        ENA.value = 0.3
        IN_1.off()
        IN_2.on()
        ENB.value = 0.3
        IN_3.on()
        IN_4.off()

    def reculer(self):
        ENA.value = 0.3
        IN_1.on()
        IN_2.off()
        ENB.value = 0.3
        IN_3.off()
        IN_4.on()

    def arreter(self):
        ENA.value = 0.2
        IN_1.on()
        IN_2.on()
        ENB.value = 0.2
        IN_3.on()
        IN_4.on()

    def tournerDroite(self):
        ENA.value = 0.7
        IN_1.off()
        IN_2.on()
        ENB.value = 0.3
        IN_3.off()
        IN_4.on()

    def tournerGauche(self):
        ENA.value = 0.3
        IN_1.on()
        IN_2.off()
        ENB.value = 0.7
        IN_3.on()
        IN_4.off()

    def avancerGauche(self):
        ENA.value = 0.12
        IN_1.off()
        IN_2.on()
        ENB.value = 0.8
        IN_3.on()
        IN_4.off()

    def avancerDroite(self):
        ENA.value = 0.8
        IN_1.off()
        IN_2.on()
        ENB.value = 0.12
        IN_3.on()
        IN_4.off()

    def augmenterVitesse(self, ALL_EN):
        for x in ALL_EN:
            #x.value = (x.value * 110)/100
            if x.value > 0.9:
                x.value = 1
            else:
                x.value += 0.1

    def diminuerVitesse(self, ALL_EN):
        for x in ALL_EN:
            #x.value = (x.value * 90)/100
            if x.value < 0.1:
                x.value = 0.0
            else:
                x.value -= 0.1
            print(x.value)

def main():
    try:
        im = cv2.imread("fordGt.jpg")
        dim = (1000, 600)
        resized = cv2.resize(im, dim)
        cv2.imshow('Labo1V2', resized)
        rt = Robot()
        S = Sonar(time.perf_counter())
        Echo.when_activated = S.activerCompteur()
        Echo.when_deactivated = S.MesurerDistance()
        x = S.MesurerDistance()

        while True:
            im = cv2.putText(im, x, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 255, 0), 2, cv2.LINE_AA)
            resized = cv2.resize(im, dim)
            cv2.imshow('Labo1V2', resized)

            key = cv2.waitKey(0)
            if key == ord('q'):
                rt.avancerGauche()
            elif key == ord('w'):
                rt.avancer()
            elif key == ord('e'):
                rt.avancerDroite()
            elif key == ord('a'):
                rt.tournerGauche()
            elif key == ord('d'):
                rt.tournerDroite()
            elif key == ord('s'):
                rt.reculer()
            elif key == ord(' '):
                rt.arreter()
            #le code du signe "+" est 171 pour moi, ord donne 43 en chiffre ascii
            elif key == 171:
                rt.augmenterVitesse(ALL_EN)
            #le code du signe "-" est 173 pour moi, ord donne 45
            elif key == 173:
                rt.diminuerVitesse(ALL_EN)
            elif key == ord('x'):
                break
    except:
        print("Le programme s'est terminé")

    finally:
        for i in ALL_IN:
            i.off()
        for x in ALL_EN:
            x.value = 0.0
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
