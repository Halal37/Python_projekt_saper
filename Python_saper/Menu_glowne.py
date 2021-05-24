from Punkt_na_planszy import *
from datetime import date



class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.wysokosc_i_szerokosc, self.liczba_min = dane_planszy
        self.macierz=np.arange(self.wysokosc_i_szerokosc)
        w = QWidget()
        hb = QHBoxLayout()

        self.wykaz_liczby_min = QLabel()

        self.zegar = QLabel()

        f = self.wykaz_liczby_min.font()
        f.setPointSize(24)
        f.setWeight(75)
        self.wykaz_liczby_min.setFont(f)
        self.zegar.setFont(f)

        self._timer = QTimer()
        self._timer.timeout.connect(self.status_zegara)
        self._timer.start(1000)  

        self.wykaz_liczby_min.setText("%03d" % self.liczba_min)
        self.zegar.setText("000")

        self.button = QPushButton()
        self.button.setIconSize(QSize(32, 32))

        self.button.pressed.connect(self.nacisniecie_buzki)

        hb.addWidget(self.wykaz_liczby_min)
        hb.addWidget(self.button)
        hb.addWidget(self.zegar)

        vb = QVBoxLayout()
        vb.addLayout(hb)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        vb.addLayout(self.grid)
        w.setLayout(vb)
        self.setCentralWidget(w)

        self.tworzenie_mapy()
        self.status_gry(gra_gotowa)
  
        self.reset_mapy()
        self.status_gry(gra_gotowa)

        self.show()
#tworzenie planszy o rozmiarze z pliku
    def tworzenie_mapy(self):
        for x in self.macierz:
            for y in self.macierz:
                punkt = Punkt(x, y)
                self.grid.addWidget(punkt, y, x)
#sygnaly dla przyciskow na planszy
                punkt.clicked.connect(self.czy_gra_rozpoczeta)
                punkt.rozszerzanie.connect(self.odkryj_pola)
                punkt.odkrycie.connect(self.wynik)
                punkt.klikniecie_miny.connect(self.porazka)
#tworzenie nowej rozgrywki
    def reset_mapy(self):
#tworzenie czystej planszy
        for x in self.macierz:
            for y in self.macierz:
                punkt = self.grid.itemAtPosition(y, x).widget()
                punkt.reset()

#dodanie min
        pozycje = []
        while len(pozycje) < self.liczba_min:
            x, y = random.randint(0, self.wysokosc_i_szerokosc - 1), random.randint(0, self.wysokosc_i_szerokosc - 1)
            if (x, y) not in pozycje:
                punkt = self.grid.itemAtPosition(y, x).widget()
                punkt.pole_miny = True
                pozycje.append((x, y))
        self.liczba_pol_do_zwyciestwa = (self.wysokosc_i_szerokosc * self.wysokosc_i_szerokosc) - (self.liczba_min + 1)

        def funkcja_przylegania(x, y):
            pozycje = self.otoczenie_punktu(x, y)
            liczba_min = sum(1 if punkt.pole_miny else 0 for punkt in pozycje)

            return liczba_min

#okreslenie pol przylegajacych do min
        for x in self.macierz:
            for y in self.macierz:
                punkt = self.grid.itemAtPosition(y, x).widget()
                punkt.przyleganie = funkcja_przylegania(x, y)

# losowanie punktu startowego
        while True:
            x, y = random.randint(0, self.wysokosc_i_szerokosc - 1), random.randint(0, self.wysokosc_i_szerokosc - 1)
            punkt = self.grid.itemAtPosition(y, x).widget()
# sprawdzenie czy punkt nie jest mina
            if (x, y) not in pozycje:
                punkt = self.grid.itemAtPosition(y, x).widget()
                punkt.pole_startowe = True
                punkt.pole_odkryte = True
                punkt.update()

# odkrywanie pozycji dopoki nie znajdzie takich, ktore granicza z mina odkryj all pozycje around this, if they are not wykaz_liczby_min either.
                for punkt in self.otoczenie_punktu(x, y):
                    if not punkt.pole_miny:
                        punkt.click()
                break
#pozycje okalajace dany punkt
    def otoczenie_punktu(self, x, y):
        pozycje = []

        for xi in range(max(0, x - 1), min(x + 2, self.wysokosc_i_szerokosc)):
            for yi in range(max(0, y - 1), min(y + 2, self.wysokosc_i_szerokosc)):
                pozycje.append(self.grid.itemAtPosition(yi, xi).widget())

        return pozycje
#nacisniecie "buzki", reset gry
    def nacisniecie_buzki(self):
            self.status_gry(gra_gotowa)
            self.reset_mapy()
#odkrycie mapy
    def odkryj_mape(self):
        for x in self.macierz:
            for y in self.macierz:
                punkt = self.grid.itemAtPosition(y, x).widget()
                punkt.odkryj()
#odkrywanie pol dopoki nie graniczy z mina
    def odkryj_pola(self, x, y):
        for xi in range(max(0, x - 1), min(x + 2, self.wysokosc_i_szerokosc)):
            for yi in range(max(0, y - 1), min(y + 2, self.wysokosc_i_szerokosc)):
                punkt = self.grid.itemAtPosition(yi, xi).widget()
                if not punkt.pole_miny:
                    punkt.click()
#po pierwszym nacisnieciu rozpoczyna gre, a nastepnie uruchamia timer
    def czy_gra_rozpoczeta(self, *args):
        if self.status != gra_w_trakcie_rozgrywki:
            self.status_gry(gra_w_trakcie_rozgrywki)
            self._timer_start_nsecs = int(time.time())
#zmiana buzki/okreslenie stanu gry np. porazka
    def status_gry(self, status):
        self.status = status
        if status==0:
         self.button.setIcon(QIcon("./obrazy/gra.png"))
        elif status==1:
         self.button.setIcon(QIcon("./obrazy/gra.png"))
        elif status==2:
         self.button.setIcon(QIcon("./obrazy/porazka.png"))
        elif status==3:
         self.button.setIcon(QIcon("./obrazy/zwyciestwo.png"))
#pokazywanie czasu przez zegar
    def status_zegara(self):
        if self.status == gra_w_trakcie_rozgrywki:
            n_secs = int(time.time()) - self._timer_start_nsecs
            self.zegar.setText("%03d" % n_secs)
#okreslenie porazki lub zwyciestwa
    def wynik(self, punkt):
        if punkt.pole_miny:
            self.porazka()
# jesli nie mina to zmniejsz liczbe pol do odkrycia o 1 jesli 0 zakoncz gre
        else:
            self.liczba_pol_do_zwyciestwa -= 1
            if self.liczba_pol_do_zwyciestwa == 0 and not punkt.pole_miny:
                self.wygrana()
#porazka
    def porazka(self):
        self.odkryj_mape()
        self.status_gry(gra_porazka)
#zwyciestwo
    def wygrana(self):
        self.plik=open("./wyniki/wyniki.txt","a")
        self.today=date.today()
        self.format=self.today.strftime("Data: %B %d, %Y ")
        lista =[]
        lista.append(self.format)
        lista.append(" Miny: ")
        lista.append(str(self.wysokosc_i_szerokosc))                
        lista.append(" Czas: ")
        lista.append(str(int(time.time()) - self._timer_start_nsecs))                
        self.plik.writelines(lista)
        self.plik.write("\n")
        self.odkryj_mape()
        self.status_gry(gra_sukces)


