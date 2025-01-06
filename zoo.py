import psycopg2
from datetime import datetime, timedelta, time

def polaczenie():
    conn = psycopg2.connect(
        host = "localhost",
        database = "zoo2",
        user = "postgres",
        password = "admin"
        )
    return conn

class Zoo:
    """
    ...
    Atrybuty
    --------
    strefy : list
        lista stref w zoo
    gatunki : list
        lista gatunkow w zoo
    zarzadca : Zarzadca
        osoba uzywajaca programu

    Metody
    ------
    wczytaj_strefy(zoo)
        Wczytuje strefy z bazy danych
    wczytaj_gatunki()
        Wczytuje gatunki z bazy danych
    wczytaj_zarzadce()
        Wczytuje dane zarzadcy z bazy danych
    """
    def __init__(self):
        self.strefy = []
        self.gatunki = []
        self.zarzadca =" "

    def wczytaj_strefy(self,zoo):
        """Wczytuje strefy z bazy danych i przy okazji do kazdej strefy wczytuja sie wybiegi i dozorcy.

        Parametry
        ---------
        zoo : Zoo
            Obiekt klasy zoo, w ktorym maja się utworzyc strefy
        """
        conn = polaczenie()

        kursor = conn.cursor()
        kursor.execute("SELECT id_strefy, nazwa_strefy FROM strefy")
        wiersze = kursor.fetchall()

        for wiersz in wiersze:
            strefa = Strefa(wiersz[0], wiersz[1])
            self.strefy.append(strefa)
            strefa.wczytaj_wybiegi(zoo,strefa.id)
            strefa.wczytaj_dozorcow(strefa.id)
        conn.close()

    def wczytaj_gatunki(self):
        """Wczytuje gatunki z bazy danych"""
        conn = polaczenie()
        kursor = conn.cursor()
        kursor.execute("SELECT nazwa_gatunku, max_ilosc_zwierzat, max_ilosc_samic, max_ilosc_samcow, min_ilosc_zwierzat, min_powierzchnia_ladowa, min_powierzchnia_wodna, wiek_dorosly FROM gatunki")
        wiersze = kursor.fetchall()

        for wiersz in wiersze:
            gatunek = Gatunek(wiersz[0], wiersz[1],wiersz[2], wiersz[3], wiersz[4], wiersz[5], wiersz[6], wiersz[7])
            self.gatunki.append(gatunek)
        conn.close()

    def wczytaj_zarzadce(self):
        """Wczytuje dane zarzadcy z bazy danych"""

        conn = polaczenie()
        kursor = conn.cursor()
        kursor.execute("SELECT imie, nazwisko, id_strefy, stanowisko FROM pracownicy WHERE stanowisko='zarzadca'")
        wiersze = kursor.fetchall()
        for wiersz in wiersze:
            zarzadca = Zarzadca(wiersz[0],wiersz[1],wiersz[2],wiersz[3])
            self.zarzadca = zarzadca
        conn.close()

class Strefa:
    """
        ...
        Atrybuty
        --------
        nazwa_strefy : str
            nazwa strefy
        id : int
            id strefy
        wybiegi : list
            lista wybiegow w danej strefie
        dozorcy : list
            lista dozorcow w danej strefie
        zadania : list
            zadania, ktore dozorcy maja wykonac np. zaniesienie jedzenia na wybieg

        Metody
        ------
        wczytaj_wybiegi(zoo)
            Wczytuje wybiegi z bazy danych
        wczytaj_dozorcow()
            Wczytuje dozorcow z bazy danych
        """
    def __init__(self, id, nazwa_strefy):
        """
        Parametry
        --------
        nazwa_strefy : str
            nazwa strefy
        id : int
            id strefy
        """
        self.nazwa_strefy = nazwa_strefy
        self.id = id

        self.wybiegi = []
        self.dozorcy = []
        self.zadania = []

    def wczytaj_wybiegi(self,zoo,id_strefy):
        """Wczytuje wybiegi z bazy danych i przy okazji do kazdego wybiegu wczytuja sie zwierzeta, ktore na nim sa.

        Parametry
        ---------
        zoo : Zoo
            Obiekt klasy zoo, w ktorym maja się utworzyc wybiegi
        id_strefy : int
            id strefy, w ktorej maja się utworzyc wybiegi
        """
        conn = polaczenie()

        kursor = conn.cursor()
        kursor.execute("SELECT nazwa_wybiegu, powierzchnia_ladowa, powierzchnia_wodna FROM wybiegi WHERE id_strefy="+str(id_strefy))
        wiersze = kursor.fetchall()

        for wiersz in wiersze:
            wybieg = Wybieg(id_strefy,wiersz[0],wiersz[1],wiersz[2])
            self.wybiegi.append(wybieg)
            wybieg.wczytaj_zwierzeta(zoo,wybieg.nazwa_wybiegu)
        conn.close()

    def wczytaj_dozorcow(self,id_strefy):
        """Wczytuje dozorcow z bazy danych

        Parametry
        ---------
        id_strefy : int
            id strefy, w ktorej maja się utworzyc wybiegi
        """
        conn = polaczenie()
        kursor = conn.cursor()
        kursor.execute("SELECT imie, nazwisko, stanowisko FROM pracownicy WHERE stanowisko='dozorca' AND id_strefy="+str(id_strefy))
        wiersze = kursor.fetchall()
        for wiersz in wiersze:
            dozorca = Dozorca(wiersz[0],wiersz[1],id_strefy,wiersz[2])
            self.dozorcy.append(dozorca)
        conn.close()

class Wybieg():
    """
    ...
    Atrybuty
    --------
    id_strefy : id
        id strefy, w ktorej znajduje sie wybieg
    nazwa_wybiegu : str
        nazwa wybiegu
    powierzchnia_ladowa : int
        powierzchnia ladowa wybiegu wyrazona w m^2
    powierzchnia_wodna : int
         powierzchnia wodna wybiegu wyrazona w m^2
    brud_proc : int
        wyrazona w procentach wartosc brudu na wybiegu
    jedzenie_proc : int
        wyrazona w procentach wartosc jedzenia na wybiegu
    picie_proc : int
        wyrazona w procentach wartosc picia na wybiegu
    zwierzeta : list
        lista zwierzat na wybiegu

    Metody
    ------
    zwieksz_brud(ile)
        Zwieksza procent brudu na wybiegu o podana liczbe
    zmniejsz_brud()
        Procent brudu na wybiegu spada do zera
    zwieksz_jedzenie()
        Procent jedzenia na wybiegu rosnie do stu
    zmniejsz_jedzenie(ile)
        Zmniejsza procent jedzenia na wybiegu o podana liczbe
    zwieksz_picie()
        Procent picia na wybiegu rosnie do stu
    zmniejsz_picie(ile)
        Zmniejsza procent picie na wybiegu o podana liczbe
    wczytaj_zwierzeta(zoo,nazwa_wybiegu)
        Wczytuje zwierzeta na wybieg z bazy danych
    ile_zwierzat_na_wybiegu()
        Zwraca ilosc wszystkich zwierzat na wybiegu
    ile_zwierzat_doroslych(gatunek)
        Zwraca ilosc doroslych zwierzat z danego gatunku na wybiegu
    ile_samic(gatunek)
        Zwraca ilosc doroslych samic z danego gatunku na wybiegu
    ile_samcow(gatunek)
        Zwraca ilosc doroslych samcow z danego gatunku na wybiegu
    potrzebna_ladowa()
        Zwraca ile m^2 powierzchni ladowej potrzebuja zwierzeta, ktore sa na tym wybiegu
    potrzebna_wodna()
        Zwraca ile m^2 powierzchni wodnej potrzebuja zwierzeta, ktore sa na tym wybiegu
    warunki_zyciowe()
        Liczy dobrostan zwierzat znajdujacych sie na wybiegu, czyli czy maja jedzenie, picie i czysto, a za kazdy brak odejmuje 10 procent od dobrostanu oraz dodaje problem do listy problemow
    warunki_wybiegu()
        Sprawdza potrzeby zwierzat zwiazane z wybiegiem i za kazdy brak odejmuje 10 procent od dobrostanu oraz dodaje problem do listy problemow
    """
    def __init__(self,id_strefy,nazwa_wybiegu,powierzchnia_ladowa,powierzchnia_wodna):
        """
        Parametry
        --------
        id_strefy : id
            id strefy, w ktorej znajduje sie wybieg
        nazwa_wybiegu : str
            nazwa wybiegu
        powierzchnia_ladowa : int
            powierzchnia ladowa wybiegu wyrazona w m^2
        powierzchnia_wodna : int
            powierzchnia wodna wybiegu wyrazona w m^2
        """
        self.id_strefy = id_strefy
        self.nazwa_wybiegu = nazwa_wybiegu
        self.powierzchnia_ladowa = powierzchnia_ladowa
        self.powierzchnia_wodna = powierzchnia_wodna

        self.brud_proc = 0
        self.jedzenie_proc = 100
        self.picie_proc = 100

        self.zwierzeta = []

    def zwieksz_brud(self,ile):
        """Zwieksza procent brudu na wybiegu o podana liczbe

        Parametry
        ---------
        ile : int
            Liczba o ile procent ma byc zwiekszony poziom brudu na wybiegu
        """
        if self.brud_proc<100:
            self.brud_proc +=ile
            if self.brud_proc>100:
                self.brud_proc=100

    def zmniejsz_brud(self):
        """Zmniejsza procent brudu na wybiegu do zera"""
        self.brud_proc = 0

    def zwieksz_jedzenie(self):
        """Zwieksza procent jedzenia na wybiegu do stu"""
        self.jedzenie_proc=100

    def zmniejsz_jedzenie(self,ile):
        """Zmniejsza procent jedzenia na wybiegu o podana liczbe

        Parametry
        ---------
        ile : int
            Liczba o ile procent ma byc zmniejszony poziom jedzenia na wybiegu
        """
        if self.jedzenie_proc>0:
            self.jedzenie_proc -=ile
            if self.jedzenie_proc<0:
                self.jedzenie_proc=0

    def zwieksz_picie(self):
        """Zwieksza procent picia na wybiegu do stu"""
        self.picie_proc=100

    def zmniejsz_picie(self,ile):
        """Zmniejsza procent picia na wybiegu o podana liczbe

        Parametry
        ---------
        ile : int
            Liczba o ile procent ma byc zmniejszony poziom picia na wybiegu
        """
        if self.picie_proc>0:
            self.picie_proc -=ile
            if self.picie_proc<0:
                self.picie_proc=0

    def wczytaj_zwierzeta(self,zoo,nazwa_wybiegu):
        """Wczytuje zwierzeta z bazy danych
        Parametry
        ---------
        zoo : Zoo
            Obiekt klasy zoo, do ktorego maja zostac wczytane zwierzeta
        nazwa_wybiegu : str
            Nazwa wybiegu, na ktory maja zostac wczytane zwierzeta
        """
        conn = polaczenie()
        kursor = conn.cursor()
        kursor.execute("SELECT imie, nazwa_gatunku, data_urodzenia, plec FROM zwierzeta WHERE nazwa_wybiegu='" + str(nazwa_wybiegu) + "'")
        wiersze = kursor.fetchall()
        for wiersz in wiersze:
            gatune = wiersz[1]
            zwierze = Zwierze(wiersz[0], wiersz[1],nazwa_wybiegu, wiersz[2],wiersz[3])
            for gatunek in zoo.gatunki:
                if gatunek.nazwa_gatunku==gatune:
                    zwierze.doroslosc=gatunek.doroslosc
                    zwierze.max_ilosc_samic=gatunek.max_ilosc_samic
                    zwierze.max_ilosc_zwierzat=gatunek.max_ilosc_zwierzat
                    zwierze.max_ilosc_samcow=gatunek.max_ilosc_samcow
                    zwierze.min_powierzchnia_wodna=gatunek.min_powierzchnia_wodna
                    zwierze.min_powierzchnia_ladowa=gatunek.min_powierzchnia_ladowa
                    zwierze.min_ilosc_zwierzat=gatunek.min_ilosc_zwierzat
            self.zwierzeta.append(zwierze)
        conn.close()

    def ile_zwierzat_na_wybiegu(self):
        """Zwraca ilosc wszystkich zwierzat na wybiegu"""
        ile = 0
        for zwierze in self.zwierzeta:
            ile += 1
        return ile

    def ile_samcow(self,gatunek):
        """Zwraca ilosc samcow doroslych na wybiegu z danego gatunku

        Parametry
        ---------
        gatunek : str
            Nazwa gatunku
        """

        ile=0
        for zwierze in self.zwierzeta:
            if zwierze.czy_dorosle() and zwierze.nazwa_gatunku==gatunek and zwierze.plec=='M':
                ile+=1
        return ile

    def ile_samic(self,gatunek):
        """Zwraca ilosc samic doroslych na wybiegu z danego gatunku

        Parametry
        ---------
        gatunek : str
            Nazwa gatunku
        """
        ile = 0
        for zwierze in self.zwierzeta:
            if zwierze.czy_dorosle() and zwierze.nazwa_gatunku == gatunek and zwierze.plec == 'K':
                ile += 1
        return ile

    def ile_zwierzat_doroslych(self,gatunek):
        """Zwraca ilosc zwierzat doroslych na wybiegu z danego gatunku

        Parametry
        ---------
        gatunek : str
            Nazwa gatunku
        """
        return self.ile_samic(gatunek)+self.ile_samcow(gatunek)

    def potrzebna_ladowa(self):
        """Zwraca ile m^2 powierzchni ladowej potrzebuja zwierzeta, ktore sa na tym wybiegu"""
        powierzchnia = 0
        gatunki = []
        for zwierze in self.zwierzeta:
            if zwierze.czy_dorosle():
                if zwierze.nazwa_gatunku not in gatunki:
                    gatunki.append(zwierze.nazwa_gatunku)
                    powierzchnia += zwierze.min_powierzchnia_ladowa
                else:
                    powierzchnia += zwierze.min_powierzchnia_ladowa* 0.05
        return powierzchnia

    def potrzebna_wodna(self):
        """Zwraca ile m^2 powierzchni wodnej potrzebuja zwierzeta, ktore sa na tym wybiegu"""
        powierzchnia = 0
        gatunki = []
        for zwierze in self.zwierzeta:
            if zwierze.czy_dorosle():
                if zwierze.nazwa_gatunku not in gatunki:
                    gatunki.append(zwierze.nazwa_gatunku)
                    powierzchnia += zwierze.min_powierzchnia_wodna
                else:
                    powierzchnia += zwierze.min_powierzchnia_wodna*0.05
        return powierzchnia


    def warunki_zyciowe(self):
        """Liczy dobrostan zwierzat znajdujacych sie na wybiegu, czyli czy maja jedzenie, picie i czysto, a za kazdy brak odejmuje 10 procent od dobrostanu oraz dodaje problem do listy problemow"""
        for zwierze in self.zwierzeta:
            zwierze.problemy=[]
            zwierze.dobrostan=30
            if self.brud_proc>50:
                zwierze.dobrostan-=10
                zwierze.problemy.append("Brudny wybieg")
            if self.jedzenie_proc<50:
                zwierze.dobrostan-=10
                zwierze.problemy.append("Malo jedzenia")
            if self.picie_proc < 50:
                zwierze.dobrostan -= 10
                zwierze.problemy.append("Malo picia")

    def warunki_wybiegu(self):
        """Sprawdza potrzeby zwierzat zwiazane z wybiegiem i za kazdy brak odejmuje 10 procent od dobrostanu oraz dodaje problem do listy problemow"""
        for zwierze in self.zwierzeta:
            zwierze.populacja=[]
            zwierze.potrzeby_wybiegu=70
            if self.powierzchnia_ladowa<self.potrzebna_ladowa():
                zwierze.potrzeby_wybiegu-=10
                zwierze.populacja.append("Za mala powierzchnia ladowa wybiegu")
            if self.powierzchnia_wodna < self.potrzebna_wodna():
                zwierze.potrzeby_wybiegu -= 10
                zwierze.populacja.append("Za mala powierzchnia wodna wybiegu")
            if self.ile_samic(zwierze.nazwa_gatunku)>zwierze.max_ilosc_samic:
                zwierze.potrzeby_wybiegu -= 10
                zwierze.populacja.append("Za duzo samic")
            if self.ile_samcow(zwierze.nazwa_gatunku)>zwierze.max_ilosc_samcow:
                zwierze.potrzeby_wybiegu -= 10
                zwierze.populacja.append("Za duzo samcow")
            if self.ile_zwierzat_doroslych(zwierze.nazwa_gatunku)>zwierze.max_ilosc_zwierzat:
                zwierze.potrzeby_wybiegu -= 10
                zwierze.populacja.append("Za duzo zwierzat z gatunku")
            if self.ile_zwierzat_doroslych(zwierze.nazwa_gatunku)<zwierze.min_ilosc_zwierzat:
                zwierze.potrzeby_wybiegu -= 10
                zwierze.populacja.append("Za malo zwierzat z gatunku")
            for z in self.zwierzeta:
                if z.nazwa_gatunku not in zwierze.gatunki_dla(zwierze.nazwa_gatunku):
                    zwierze.potrzeby_wybiegu -= 10
                    zwierze.populacja.append("Zle dobrane gatunki na wybiegu")
                    break

class Gatunek:
    """
       ...
       Atrybuty
       --------
       nazwa_gatunku : str
           nazwa gatunku
       max_ilosc_zwierzat : int
           Maksymalna ilosc doroslych zwierzat jaka moze byc w tym samym czasie na jednym wybiegu z danego gatunku
       max_ilosc_samcow : int
           Maksymalna ilosc doroslych samcow jaka moze byc w tym samym czasie na jednym wybiegu z danego gatunku
       max_ilosc_samic : int
           Maksymalna ilosc doroslych samic jaka moze byc w tym samym czasie na jednym wybiegu z danego gatunku
       min_ilosc_zwierzat : int
           Minimalna ilosc doroslych zwierzat jaka musi byc w tym samym czasie na jednym wybiegu z danego gatunku
       min_powierzchnia_ladowa : int
           Minimalna powierzchnia ladowa w m^2 jaka potrzebuje pierwszy osobnik z danego gatunku (dla nastepnych ta powierzchnia wylicza sie automatycznie)
       min_powierzchnia_wodna : int
           Minimalna powierzchnia wodna w m^2 jaka potrzebuje pierwszy osobnik z danego gatunku (dla nastepnych ta powierzchnia wylicza sie automatycznie)

       Metody
       ------
       gatunki_polaczenia(ile)
           Zwraca slownik gatunkow na podstawie pliku txt, czyli gatunki z jakimi inne gatunki moga byc na jednym wybiegu
       gatunki_dla(nazwa_gatunku)
           Zwraca gatunki z jakimi konkretny osobnik moze przebywac na jednym wybiegu
      """
    def __init__(self, nazwa_gatunku, max_ilosc_zwierzat, max_ilosc_samic, max_ilosc_samcow, min_ilosc_zwierzat,
                 min_powierzchnia_ladowa, min_powierzchnia_wodna,doroslosc):
        """
        Parametry
        ---------
        nazwa_gatunku : str
           nazwa gatunku
        max_ilosc_zwierzat : int
           Maksymalna ilosc doroslych zwierzat jaka moze byc w tym samym czasie na jednym wybiegu z danego gatunku
        max_ilosc_samcow : int
           Maksymalna ilosc doroslych samcow jaka moze byc w tym samym czasie na jednym wybiegu z danego gatunku
        max_ilosc_samic : int
           Maksymalna ilosc doroslych samic jaka moze byc w tym samym czasie na jednym wybiegu z danego gatunku
        min_ilosc_zwierzat : int
           Minimalna ilosc doroslych zwierzat jaka musi byc w tym samym czasie na jednym wybiegu z danego gatunku
        min_powierzchnia_ladowa : int
           Minimalna powierzchnia ladowa w m^2 jaka potrzebuje pierwszy osobnik z danego gatunku (dla nastepnych ta powierzchnia wylicza sie automatycznie)
        min_powierzchnia_wodna : int
           Minimalna powierzchnia wodna w m^2 jaka potrzebuje pierwszy osobnik z danego gatunku (dla nastepnych ta powierzchnia wylicza sie automatycznie)
        """
        self.nazwa_gatunku = nazwa_gatunku
        self.max_ilosc_zwierzat = max_ilosc_zwierzat
        self.max_ilosc_samic = max_ilosc_samic
        self.max_ilosc_samcow = max_ilosc_samcow
        self.min_ilosc_zwierzat = min_ilosc_zwierzat
        self.min_powierzchnia_ladowa = min_powierzchnia_ladowa
        self.min_powierzchnia_wodna = min_powierzchnia_wodna
        self.doroslosc = doroslosc

    def gatunki_polaczenia(self):
        """Zwraca slownik gatunkow na podstawie pliku txt, czyli gatunki z jakimi inne gatunki moga byc na jednym wybiegu"""
        slownik={}
        with open('gatunki.txt', 'r') as plik:
            for linia in plik:
                klucz, wartosci = linia.strip().split(':')
                slownik[klucz] = wartosci
        return slownik

    def gatunki_dla(self,nazwa_gatunku):
        """Zwraca gatunki z jakimi konkretny osobnik moze przebywac na jednym wybiegu

        Parametry
        ---------
        nazwa_gatunku : str
            nazwa gatunku
        """
        slownik = self.gatunki_polaczenia()
        if nazwa_gatunku in slownik:
            return slownik[nazwa_gatunku]
        else:
            return []

class Zwierze(Gatunek):
    """
       ...
       Atrybuty
       --------
       imie : str
           imie zwierzecia
       nazwa_wybiegu : str
           nazwa wybiegu zwierzecia
       data_urodzenia : str
           data urodzenia zwierzecia
       plec : string
           plec zwierzecia
       dobrostan : int
           procent dobrostanu jaki zwierze aktualnie posiada, przyznawany jest za jedzenie, picie oraz czystosc
       potrzeby_wybiegu : int
           procent zaspokojenia potrzeb zwiazanych z wybiegiem czyli np. wielosc wybiegu
       problemy : list
           lista problemow zwierzecia zwiazanych z dobrostanem
       populacja : list
           lista problemow zwierzecia zwiazanych z wybiegiem

       Metody
       ------
       czy_dorosle()
           Zwraca wartosc True w przypadku gdy zwierze jest dorosle i False gdy nie jest dorosle
       zjedz(wybieg)
           Zwierze zjada swoja czesc jedzenia na wybiegu
       wypij(wybieg)
           Zwierze wypija swoja czesc wody na wybiegu
       wybrudz(wybieg)
           Zwierze brudzi wybieg
       """

    def __init__(self, imie, nazwa_gatunku, nazwa_wybiegu, data_urodzenia, plec,
                 max_ilosc_zwierzat=0, max_ilosc_samic=0, max_ilosc_samcow=0,
                 min_ilosc_zwierzat=0, min_powierzchnia_ladowa=0, min_powierzchnia_wodna=0, doroslosc=0):
        """
        Parametry
        ---------
        imie : str
            imie zwierzecia
        nazwa_wybiegu : str
            nazwa wybiegu zwierzecia
        data_urodzenia : str
            data urodzenia zwierzecia
        plec : string
            plec zwierzecia
        """
        super().__init__(nazwa_gatunku, max_ilosc_zwierzat, max_ilosc_samic, max_ilosc_samcow,
                         min_ilosc_zwierzat, min_powierzchnia_ladowa, min_powierzchnia_wodna, doroslosc)
        self.imie = imie
        self.nazwa_wybiegu = nazwa_wybiegu
        self.data_urodzenia = data_urodzenia
        self.plec = plec

        self.dobrostan = 30
        self.potrzeby_wybiegu = 70
        self.problemy = []
        self.populacja = []

    def czy_dorosle(self):
        """Zwraca wartosc True w przypadku gdy zwierze jest dorosle i False gdy nie jest dorosle"""
        data_urodzenia = datetime.combine(self.data_urodzenia, datetime.min.time())
        teraz = datetime.now()
        roznica_czasu = teraz - data_urodzenia

        wiek_w_latach = int(roznica_czasu.days/365)
        return wiek_w_latach>=self.doroslosc

    def zjedz(self,wybieg):
        """Zwierze zjada swoja czesc jedzenia na wybiegu

        Parametry
        ---------
        wybieg : Wybieg
            Obiekt klasy wybieg na ktorym znajduje sie zwierze
        """
        ile = wybieg.ile_zwierzat_na_wybiegu()
        porcja = 100/(ile*10)
        wybieg.zmniejsz_jedzenie(porcja)

    def wypij(self,wybieg):
        """Zwierze wypija swoja czesc wody na wybiegu

        Parametry
        ---------
        wybieg : Wybieg
            Obiekt klasy wybieg na ktorym znajduje sie zwierze
        """
        ile = wybieg.ile_zwierzat_na_wybiegu()
        porcja = 200/(ile*10)
        wybieg.zmniejsz_picie(porcja)

    def wybrudz(self,wybieg):
        """Zwierze brudzi wybieg

        Parametry
        ---------
        wybieg : Wybieg
            Obiekt klasy wybieg na ktorym znajduje sie zwierze
        """
        ile = wybieg.ile_zwierzat_na_wybiegu()
        porcja = 50/(ile*10)
        wybieg.zwieksz_brud(porcja)

class Worker:
    def __init__(self, name, surname, zone_id, profession):
        """
        Parameters
        --------
        name : str
            Worker name
        surname: str
            Worker last name
        zone_id : int
            zone to which the worker is assigned
        profession : str

        """
        self.imie = imie
        self.nazwisko = nazwisko
        self.id_strefy = id_strefy
        self.stanowisko = stanowisko

class Dozorca(Pracownik):
    """
    Metody
    ------
    posprzataj(wybieg)
        Dozorca sprzata wybieg, dzieki czemu procent brudu spada do zera
    nalej_wode(wybieg)
        Dozorca nalewa wode na wybieg, dzieki czemu procent wody rosnie do stu
    daj_jedzenie(wybieg)
        Dozorca daje jedzenie na wybieg, dzieki czemu procent jedzenia rosnie do stu
    """
    def posprzataj(self,wybieg):
        """Dozorca sprzata wybieg, dzieki czemu procent brudu spada do zera

        Parametry
        ---------
        wybieg : Wybieg
            Obiekt klasy wybieg ktory dozorca ma posprzatac
        """
        wybieg.zmniejsz_brud()

    def nalej_wode(self,wybieg):
        """Dozorca nalewa wode na wybieg, dzieki czemu procent wody rosnie do stu

        Parametry
        ---------
        wybieg : Wybieg
            Obiekt klasy wybieg na ktory dozorca ma przyniesc wode
        """
        wybieg.zwieksz_picie()

    def daj_jedzenie(self,wybieg):
        """Dozorca daje jedzenie na wybieg, dzieki czemu procent jedzenia rosnie do stu

        Parametry
        ---------
        wybieg : Wybieg
            Obiekt klasy wybieg na ktory dozorca ma przyniesc jedzenie
        """
        wybieg.zwieksz_jedzenie()

class Zarzadca(Pracownik):
    """
    Metody
    ------
    dodaj_zwierze(zoo,imie,nazwa_gatunku,nazwa_wybiegu,data_urodzenia,plec)
        Dodaje zwierze do zoo i bazy danych lub jesli jest jakis problem z danymi wypisuje blad
    usun_zwierze(zoo,imie)
        Usuwa zwierze z zoo i bazy danych
    przenies_zwierze(zoo,imie,wybiegu)
        Przenosi zwierze na podany wybieg w zoo oraz bazie danych
    dodaj_dozorce(zoo,imie,nazwisko,strefa_id)
        Dodaje dozorce do zoo i bazy danych lub jesli jest jakis problem z danymi wypisuje blad
    usun_dozorce(zoo,nazwisko)
        Usuwa dozorce z zoo i bazy danych
    przenies_dozorce(zoo,nazwisko,strefa)
        Przenosi dozorce do podanej strefy
    wypisz_zwierzeta(zoo)
        Wypisuje wszystkie zwierzeta w zoo oraz ich szczescie
    sprawdz_dobrostan(zoo,imie)
        Wypisuje wszystkie problemy jakie ma zwierze
    """
    def dodaj_zwierze(self, zoo,imie, nazwa_gatunku, nazwa_wybiegu, data_urodzenia, plec):
        """Dodaje zwierze do zoo i bazy danych lub jesli jest jakis problem z danymi wypisuje blad

        Parametry
        ---------
        zoo : Zoo
            obiekt klasy zoo, do ktorego ma zostac dodane zwierze
        imie : str
            imie zwierzecia
        nazwa_gatunku : str
            nazwa gatunku zwierzecia
        nazwa_wybiegu : str
            nazwa wybiegu zwierzecia
        data_urodzenia : str
            data urodzenia zwierzecia
        plec : str
            plec zwierzecia
        """
        czy_imie=False
        czy_gatunek=False
        czy_wybieg=False

        if plec !="K" and plec !="M" and plec!="":
            print("Zla plec")
            return

        for strefa in zoo.strefy:
            for wybieg in strefa.wybiegi:
                if wybieg.nazwa_wybiegu==nazwa_wybiegu:
                    czy_wybieg=True
                for zwierze in wybieg.zwierzeta:
                    if zwierze.imie == imie:
                        czy_imie=True

        for gatunek in zoo.gatunki:
            if gatunek.nazwa_gatunku==nazwa_gatunku:
                czy_gatunek=True
                break

        if czy_imie==False:
            if czy_wybieg==True:
                if czy_gatunek==True:
                    data = datetime.strptime(data_urodzenia, '%Y-%m-%d')
                    for strefa in zoo.strefy:
                        for wybieg in strefa.wybiegi:
                            if wybieg.nazwa_wybiegu == nazwa_wybiegu:
                                zwierze = Zwierze(imie, nazwa_gatunku, nazwa_wybiegu, data, plec)
                                wybieg.zwierzeta.append(zwierze)
                                for gatunek in zoo.gatunki:
                                    if gatunek.nazwa_gatunku == nazwa_gatunku:
                                        zwierze.doroslosc = gatunek.doroslosc
                                        zwierze.max_ilosc_samic = gatunek.max_ilosc_samic
                                        zwierze.max_ilosc_zwierzat = gatunek.max_ilosc_zwierzat
                                        zwierze.max_ilosc_samcow = gatunek.max_ilosc_samcow
                                        zwierze.min_powierzchnia_wodna = gatunek.min_powierzchnia_wodna
                                        zwierze.min_powierzchnia_ladowa = gatunek.min_powierzchnia_ladowa
                                        zwierze.min_ilosc_zwierzat = gatunek.min_ilosc_zwierzat

                    conn = polaczenie()
                    kursor = conn.cursor()
                    kursor.execute(
                        "INSERT INTO zwierzeta (imie, nazwa_gatunku, nazwa_wybiegu, data_urodzenia, plec) VALUES (%s, %s, %s, %s, %s)",
                        (imie, nazwa_gatunku, nazwa_wybiegu, data_urodzenia, plec))
                    conn.commit()
                    conn.close()
                    print("Dodano zwierze")
                else:
                    print("Nie ma takiego gatunku")
            else:
                print("Nie ma takiego wybiegu")
        else:
            print("Zwierze o podanym imieniu juz istnieje")


    def usun_zwierze(self,zoo,imie):
        """ Usuwa zwierze z zoo i bazy danych

        Parametry
        ---------
        zoo : Zoo
            obiekt klasy zoo, z ktorego ma zostac usuniete zwierze
        imie : str
            imie zwierzecia
        """
        czy_imie=False


        for strefa in zoo.strefy:
            for wybieg in strefa.wybiegi:
                for zwierze in wybieg.zwierzeta:
                    if zwierze.imie==imie:
                        wybieg.zwierzeta.remove(zwierze)
                        czy_imie=True
                        break

        if czy_imie==True:
            conn = polaczenie()
            kursor = conn.cursor()
            kursor.execute("DELETE FROM zwierzeta WHERE imie = %s",(imie,))
            conn.commit()
            conn.close()
            print("Usunieto zwierze")
        else:
            print("Nie ma zwierzecia o takim imieniu")

    def przenies_zwierze(self,zoo,imie,wybiegu):
        """Przenosi zwierze na podany wybieg w zoo oraz bazie danych

        Parametry
        ---------
        zoo : Zoo
            obiekt klasy zoo, w ktorym znajduje sie zwierze
        imie : str
            imie zwierzecia
        wybiegu : str
            nazwa wybiegu, na ktory zwierze ma zostac przeniesione
        """
        czy_imie=False
        czy_wybieg=False

        for strefa in zoo.strefy:
            for wybieg in strefa.wybiegi:
                if wybieg.nazwa_wybiegu==wybiegu:
                    czy_wybieg=True
                for zwierze in wybieg.zwierzeta:
                    if zwierze.imie == imie:
                        czy_imie=True

        if czy_imie==True:
            if czy_wybieg==True:
                for strefa in zoo.strefy:
                    for wybieg in strefa.wybiegi:
                        for zwierze in wybieg.zwierzeta:
                            if zwierze.imie==imie:
                                z=zwierze
                                wybieg.zwierzeta.remove(zwierze)

                for strefa in zoo.strefy:
                    for wybieg in strefa.wybiegi:
                        if wybieg.nazwa_wybiegu==wybiegu:
                            wybieg.zwierzeta.append(z)

                conn = polaczenie()
                kursor = conn.cursor()
                kursor.execute("UPDATE zwierzeta SET nazwa_wybiegu = %s WHERE imie = %s", (wybiegu,imie))
                conn.commit()
                conn.close()
                print("Przeniesiono zwierze")
            else:
                print("Nie ma takiego wybiegu")
        else:
            print("Nie ma takiego zwierzecia")

    def dodaj_dozorce(self,zoo,imie,nazwisko,strefa_id):
        """Dodaje dozorce do zoo i bazy danych lub jesli jest jakis problem z danymi wypisuje blad

        Parametry
        ---------
        zoo : Zoo
            obiekt klasy zoo, do ktorego ma zostac dodany dozorca
        imie : str
            imie dozorcy
        nazwisko : str
            nazwisko dozorcy
        strefa_id : int
            id strefy, do ktorej ma zostac dodany dozorca
        """
        czy_nazwisko = False
        czy_strefa = False

        for strefa in zoo.strefy:
            if strefa.id==int(strefa_id):
                czy_strefa=True
            for dozorca in strefa.dozorcy:
                if dozorca.nazwisko==nazwisko:
                    czy_nazwisko=True

        if czy_nazwisko == False:
            if czy_strefa == True:
                for strefa in zoo.strefy:
                    if strefa.id == int(strefa_id):
                        dozorca = Dozorca(imie, nazwisko, strefa_id,"Dozorca")
                        strefa.dozorcy.append(dozorca)
                conn = polaczenie()
                kursor = conn.cursor()
                kursor.execute("INSERT INTO pracownicy (imie, nazwisko, id_strefy, stanowisko) VALUES (%s, %s, %s, %s)",
                                   (imie, nazwisko, strefa_id, "Dozorca"))
                conn.commit()
                conn.close()
                print("Dodano dozorce")
            else:
                print("Nie ma takiej strefy")
        else:
            print("Dozorca o podanym nazwisku juz istnieje")


    def usun_dozorce(self,zoo,nazwisko):
        """Usuwa dozorce z zoo i bazy danych

        Parametry
        ---------
        zoo : Zoo
            obiekt klasy zoo, z ktorego ma zostac usuniety dozorca
        nazwisko : str
            nazwisko dozorcy
        """
        czy_nazwisko=False

        for strefa in zoo.strefy:
            for dozorca in strefa.dozorcy:
                if dozorca.nazwisko == nazwisko:
                    czy_nazwisko = True
        if czy_nazwisko == True:
            for strefa in zoo.strefy:
                for dozorca in strefa.dozorcy:
                    if dozorca.nazwisko==nazwisko:
                        strefa.dozorcy.remove(dozorca)

            conn = polaczenie()
            kursor = conn.cursor()
            kursor.execute("DELETE FROM pracownicy WHERE nazwisko = %s",(nazwisko))
            conn.commit()
            conn.close()
            print("Usunieto dozorce")
        else:
            print("Nie ma takiego dozorcy")

    def przenies_dozorce(self,zoo,nazwisko,strefa_id):
        """Przenosi dozorce do podanej strefy

        Parametry
        ---------
        zoo : Zoo
            obiekt klasy zoo, w ktorym jest dozorca
        nazwisko : str
            nazwisko dozorcy
        strefa_id : int
            id strefy, na ktora ma zostac przeniesiony dozorca
        """
        czy_nazwisko = False
        czy_strefa = False

        for strefa in zoo.strefy:
            if strefa.id == int(strefa_id):
                czy_strefa = True
            for dozorca in strefa.dozorcy:
                if dozorca.nazwisko == nazwisko:
                    czy_nazwisko = True
        if czy_nazwisko == True:
            if czy_strefa == True:
                for strefa in zoo.strefy:
                    for dozorca in strefa.dozorcy:
                        if dozorca.nazwisko == nazwisko:
                            d = dozorca
                            strefa.dozorcy.remove(dozorca)

                for strefa in zoo.strefy:
                    if strefa.id==int(strefa_id):
                        strefa.dozorcy.append(d)

                conn = polaczenie()
                kursor = conn.cursor()
                kursor.execute("UPDATE pracownicy SET id_strefy = %s WHERE nazwisko = %s", (strefa_id,nazwisko))
                conn.commit()
                conn.close()
                print("Przeniesiono dozorce")
            else:
                print("Nie ma takiej strefy")
        else:
            print("Nie ma takiego dozorcy")

    def wypisz_zwierzeta(self,zoo):
        """Wypisuje wszystkie zwierzeta w zoo oraz ich szczescie

        Parametry
        ---------
        zoo : Zoo
            obiekt klasy zoo, w ktorym jest dozorca
        """
        min=0
        szerokosc = 15
        naglowki = ["STREFA ID","STREFA NAZWA","IMIE","GATUNEK","WYBIEG","PŁEĆ","SZCZESCIE"]
        nag = " | ".join(naglowek.ljust(szerokosc) for naglowek in naglowki)
        print(nag)
        separator = "-" * (len(nag))
        print(separator)
        for i in range(0,101,10):
            for strefa in zoo.strefy:
                for wybieg in strefa.wybiegi:
                    for zwierze in wybieg.zwierzeta:
                        if i==zwierze.dobrostan + zwierze.potrzeby_wybiegu:
                            w = [str(strefa.id),strefa.nazwa_strefy,zwierze.imie, zwierze.nazwa_gatunku, wybieg.nazwa_wybiegu,zwierze.plec,str(zwierze.dobrostan + zwierze.potrzeby_wybiegu)]
                            wiersz = " | ".join(dane.ljust(szerokosc) for dane in w)
                            print(wiersz)

    def sprawdz_dobrostan(self,zoo,imie):
        """Wypisuje wszystkie problemy jakie ma zwierze

        Parametry
        ---------
        zoo : Zoo
            obiekt klasy zoo, w ktorym jest dozorca
        imie : str
            imie zwierzecia
        """
        czy = False
        for strefa in zoo.strefy:
            for wybieg in strefa.wybiegi:
                for zwierze in wybieg.zwierzeta:
                    if zwierze.imie==imie:
                        czy = True
                        if zwierze.dobrostan+zwierze.potrzeby_wybiegu==100:
                            print(f'{zwierze.imie} nie ma powodu do niezadowolenia:')
                        else:
                            print(f'{zwierze.imie} niezadowolone z powodu:')
                            for problem in zwierze.problemy:
                                print(problem)
                            for problem in zwierze.populacja:
                                print(problem)

        if czy==False:
          print("Nie ma takiego zwierzecia")