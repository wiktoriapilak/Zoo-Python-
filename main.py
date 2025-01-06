from zoo import Zoo
from zoo import Strefa
from zoo import Wybieg
from zoo import Gatunek
from zoo import Zwierze
from zoo import Pracownik
from zoo import Dozorca
from zoo import Zarzadca


if __name__ == '__main__':
    wroclawskie = Zoo()
    wroclawskie.wczytaj_gatunki()
    wroclawskie.wczytaj_strefy(wroclawskie)
    wroclawskie.wczytaj_zarzadce()

    for strefa in wroclawskie.strefy:
        for wybieg in strefa.wybiegi:
            wybieg.warunki_wybiegu()

    imie_nazwisko = input("Podaj swoje imie oraz nazwisko, aby sie zalogowac: ")
    print("")

    if imie_nazwisko == (f'{wroclawskie.zarzadca.imie}{wroclawskie.zarzadca.nazwisko}'):
        odp=0
        while odp!='6':
            print("1.Uplyw czasu")
            print("2.Zarzadzaj dozorcami")
            print("3.Zarzadzaj zwierzetami")
            print("4.Wyswietl dobrostan zwierzat")
            print("5.Sprawdz problemy zwierzecia")
            print("6.Wyjscie")
            odp= input("Co chcesz zrobic? ")
            print("")

            if odp=='1':
                ile = input("Ile dni ma minac? ")
                for i in range(0, int(ile)):
                    for strefa in wroclawskie.strefy:
                        strefa.zadania=[]
                        for wybieg in strefa.wybiegi:
                            if wybieg.jedzenie_proc < 50:
                                strefa.zadania.append((wybieg.jedzenie_proc,wybieg.nazwa_wybiegu,"jedzenie"))
                            if wybieg.picie_proc < 50:
                                strefa.zadania.append((wybieg.picie_proc, wybieg.nazwa_wybiegu, "picie"))
                            if wybieg.brud_proc > 50:
                                strefa.zadania.append((100-wybieg.brud_proc, wybieg.nazwa_wybiegu, "brud"))
                        strefa.zadania.sort(key=lambda x:x[0], reverse=True)

                        for dozorca in strefa.dozorcy:
                            wykonane_akcje = 0
                            while wykonane_akcje<3 and len(strefa.zadania)>0:
                                ile,gdzie,co = strefa.zadania.pop()
                                for wybieg in strefa.wybiegi:
                                    if wybieg.nazwa_wybiegu==gdzie:
                                        if co=="jedzenie":
                                            dozorca.daj_jedzenie(wybieg)
                                        elif co=="picie":
                                            dozorca.nalej_wode(wybieg)
                                        else:
                                            dozorca.posprzataj(wybieg)
                                wykonane_akcje+=1
                    for strefa in wroclawskie.strefy:
                        for wybieg in strefa.wybiegi:
                            for zwierze in wybieg.zwierzeta:
                                zwierze.zjedz(wybieg)
                                zwierze.wypij(wybieg)
                                zwierze.wybrudz(wybieg)
                            wybieg.warunki_zyciowe()
                print("")
            elif odp=='2':
                odp2=0
                while odp2!='4':
                    print("1. Dodaj dozorce")
                    print("2. Usun dozorce")
                    print("3. Przenies dozorce")
                    print("4. Wroc")
                    odp2 = input("Co chcesz zrobic? ")

                    if odp2=='1':
                        imie=input("Podaj imie: ")
                        nazwisko=input("Podaj nazwisko: ")
                        id_strefy=input("Podaj id strefy: ")
                        wroclawskie.zarzadca.dodaj_dozorce(wroclawskie,imie,nazwisko,id_strefy)
                        print("")

                    elif odp2=='2':
                        nazwisko = input("Podaj nazwisko: ")
                        wroclawskie.zarzadca.usun_dozorce(wroclawskie, nazwisko)
                        print("")

                    elif odp2=='3':
                        nazwisko = input("Podaj nazwisko: ")
                        id_strefy = input("Podaj id strefy: ")
                        wroclawskie.zarzadca.przenies_dozorce(wroclawskie, nazwisko,id_strefy)
                        print("")

                    else:
                        "Nie ma takiej opcji"
                print("")

            elif odp=='3':
                odp2=0
                while odp2!='4':
                    print("1. Dodaj zwierze")
                    print("2. Usun zwierze")
                    print("3. Przenies zwierze")
                    print("4. Wroc")
                    odp2 = input("Co chcesz zrobic? ")

                    if odp2=='1':
                        imie=input("Podaj imie: ")
                        nazwa_gatunku=input("Podaj nazwe gatunku: ")
                        nazwa_wybiegu = input("Podaj nazwe wybiegu: ")
                        data_urodzenia = input("Podaj date urodzenia: ")
                        plec = input("Podaj płeć: ")
                        wroclawskie.zarzadca.dodaj_zwierze(wroclawskie,imie,nazwa_gatunku,nazwa_wybiegu,data_urodzenia,plec)
                        for strefa in wroclawskie.strefy:
                            for wybieg in strefa.wybiegi:
                                if wybieg.nazwa_wybiegu==nazwa_wybiegu:
                                    wybieg.warunki_wybiegu()
                        print("")

                    elif odp2=='2':
                        nazwa=None
                        imie = input("Podaj imie: ")
                        for strefa in wroclawskie.strefy:
                            for wybieg in strefa.wybiegi:
                                for zwierze in wybieg.zwierzeta:
                                    if zwierze.imie==imie:
                                        nazwa=wybieg.nazwa_wybiegu

                        wroclawskie.zarzadca.usun_zwierze(wroclawskie, imie)
                        for strefa in wroclawskie.strefy:
                            for wybieg in strefa.wybiegi:
                                if wybieg.nazwa_wybiegu==nazwa:
                                    wybieg.warunki_wybiegu()
                        print("")

                    elif odp2=='3':
                        nazwa=None
                        imie = input("Podaj imie: ")
                        nazwa_wybiegu = input("Podaj nazwe wybiegu: ")
                        for strefa in wroclawskie.strefy:
                            for wybieg in strefa.wybiegi:
                                for zwierze in wybieg.zwierzeta:
                                    if zwierze.imie==imie:
                                        nazwa=wybieg.nazwa_wybiegu
                        wroclawskie.zarzadca.przenies_zwierze(wroclawskie, imie, nazwa_wybiegu)
                        for strefa in wroclawskie.strefy:
                            for wybieg in strefa.wybiegi:
                                if wybieg.nazwa_wybiegu==nazwa or wybieg.nazwa_wybiegu==nazwa_wybiegu:
                                    wybieg.warunki_wybiegu()
                        print("")
                    else:
                        print("Nie ma takiej opcji")
                print("")
            elif odp=='4':
                wroclawskie.zarzadca.wypisz_zwierzeta(wroclawskie)
                print("")
            elif odp=='5':
                imie = input("Podaj imie: ")
                wroclawskie.zarzadca.sprawdz_dobrostan(wroclawskie,imie)
                print("")
            else:
                print("")
    else:
        print("Niepoprawne dane")











