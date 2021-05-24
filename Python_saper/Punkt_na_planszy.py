import numpy as np
import random
import time
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



#wczytywanie danych z pliku tekstowego
dane_planszy=np.array
dane_planszy=np.loadtxt("./rozmiary/mala.txt",dtype=int,delimiter=',')
#stan w jakim znajduje sie gra
gra_gotowa = 0
gra_w_trakcie_rozgrywki= 1
gra_porazka= 2
gra_sukces = 3

#klasa tworzaca plansze z podstawowymi interaakcjami jak flagowanie, czy nacisniecie przycisku
class Punkt(QWidget):
    clicked = pyqtSignal()
    odkrycie = pyqtSignal(object)
    klikniecie_miny = pyqtSignal()
    rozszerzanie = pyqtSignal(int, int)



    def __init__(self, x, y, *args, **kwargs):
        super(Punkt, self).__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.setFixedSize(QSize(30, 30))


#bazowe pole
    def reset(self):
        self.pole_odkryte = False
        self.pole_oflagowane = False
        self.pole_startowe = False
        self.pole_miny = False
        self.przyleganie = 0

        self.update()
#ustawienie kolorystyki pol odkrytych i zakrytych
    def paintEvent(self, event):
        p = QPainter(self)
        r = event.rect()

        if self.pole_odkryte:
            color = self.palette().color(QPalette.Background)
            outer, inner = color, color
        else:
            outer, inner = Qt.black, Qt.darkGray

        p.fillRect(r, QBrush(inner))
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        if self.pole_odkryte:

            if self.pole_miny:
                p.drawPixmap(r, QPixmap("./obrazy/bomb.png"))

            elif self.przyleganie > 0:
                if self.przyleganie==1:
                 pen = QPen(QColor('red'))
                elif self.przyleganie==2:
                 pen = QPen(QColor('blue'))
                elif self.przyleganie==3:
                 pen = QPen(QColor('cyan'))
                elif self.przyleganie==4:
                 pen = QPen(QColor('purple'))
                elif self.przyleganie==5:
                 pen = QPen(QColor('orange'))
                elif self.przyleganie==6:
                 pen = QPen(QColor('black'))
                elif self.przyleganie==7:
                 pen = QPen(QColor('yellow'))
                elif self.przyleganie==8:
                 pen = QPen(QColor('magenta'))
              
                p.setPen(pen)
                p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.przyleganie))

        elif self.pole_oflagowane:
            p.drawPixmap(r, QPixmap("./obrazy/flag.png"))
#funkcja realizujaca "polozenie" lub zdjecie flagi
    def flag(self):
        if self.pole_oflagowane ==True:
            self.pole_oflagowane=False
        else:
         self.pole_oflagowane = True
        self.update()

        self.clicked.emit()
#funkcja odslaniajaca pole
    def odkryj(self, emit=True):
        if not self.pole_odkryte:
            self.pole_odkryte = True
            self.update()

            if emit:
                self.odkrycie.emit(self)
#nacisniecie przycisku na planszy
    def click(self):
        if not self.pole_odkryte:
            self.odkryj()
            if self.przyleganie == 0:
                self.rozszerzanie.emit(self.x, self.y)

        self.clicked.emit()
#funkcja porownujaca mape z nacisnieciem myszy przez uzytkownika
    def mouseReleaseEvent(self, temp):

        if (temp.button() == Qt.RightButton and not self.pole_odkryte):
            self.flag()

        elif (temp.button() == Qt.LeftButton):

            if not self.pole_oflagowane and not self.pole_odkryte:
                self.click()
                if self.pole_miny:
                    self.klikniecie_miny.emit()


