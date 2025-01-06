import unittest
from datetime import datetime
from zoo import Zoo
from zoo import Strefa
from zoo import Wybieg
from zoo import Gatunek
from zoo import Zwierze

wybieg = Wybieg(1, "Kotowate", 2000, 0)

kot1 = Zwierze('Simba','Lew','Kotowate',datetime.strptime('2023-02-07', '%Y-%m-%d'),'M',30,29,1,2,1593,0,3)
kot2 = Zwierze('Mufasa','Lew','Kotowate',datetime.strptime('2015-06-09', '%Y-%m-%d'),'M',30,29,1,2,1593,0,3)
kot3 = Zwierze('Nala','Lew','Kotowate',datetime.strptime('2020-04-08', '%Y-%m-%d'),'K',30,29,1,2,1593,0,3)
kot4 = Zwierze('Skaza','Lew','Kotowate',datetime.strptime('2012-05-30', '%Y-%m-%d'),'M',30,29,1,2,1593,0,3)
kot5 = Zwierze('Zdrada','Lew','Kotowate',datetime.strptime('2014-08-21', '%Y-%m-%d'),'K',30,29,1,2,1593,0,3)
kot6 = Zwierze('Lidka','Gepard','Kotowate',datetime.strptime('2016-09-25', '%Y-%m-%d'),'K',3,1,2,1,1593,0,2)
wybieg.zwierzeta.append(kot1)
wybieg.zwierzeta.append(kot2)
wybieg.zwierzeta.append(kot3)

class TestWybieg(unittest.TestCase):
    def test_zwieksz_brud(self):
        wybieg.zwieksz_brud(10)
        self.assertEqual(wybieg.brud_proc,10)
        wybieg.zwieksz_brud(110)
        self.assertEqual(wybieg.brud_proc, 100)

    def test_zmniejsz_brud(self):
        wybieg.zmniejsz_brud()
        self.assertEqual(wybieg.brud_proc,0)

    def test_ile_zwierzat_na_wybiegu(self):
        ile = wybieg.ile_zwierzat_na_wybiegu()
        self.assertEqual(ile, 3)

    def test_ile_samic(self):
        ile = wybieg.ile_samic('Lew')
        self.assertEqual(ile,1)

    def test_ile_samcow(self):
        ile = wybieg.ile_samcow('Lew')
        self.assertEqual(ile, 1)

    def test_powierzchnia_ladowa(self):
        powierzchnia = wybieg.potrzebna_ladowa()
        self.assertEqual(powierzchnia, 1672.65)

    def test_warunki_zyciowe(self):
        wybieg.warunki_zyciowe()
        self.assertEqual(kot1.dobrostan,30)

    def test_warunki_wybiegu(self):
        wybieg.warunki_wybiegu()
        self.assertEqual(kot1.potrzeby_wybiegu,70)

class TestZwierze(unittest.TestCase):

    def test_czy_dorosle(self):
        self.assertIs(kot1.czy_dorosle(), False)
        self.assertIs(kot2.czy_dorosle(), True)

    def test_zjedz(self):
        kot1.zjedz(wybieg)
        self.assertEqual(wybieg.jedzenie_proc, 96.66666666666667)


