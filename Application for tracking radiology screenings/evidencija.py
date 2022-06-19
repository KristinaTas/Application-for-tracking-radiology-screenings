import pickle
from datetime import date, datetime

class Pacijent:

    @property
    def lbo(self):
        return self.__lbo

    @lbo.setter
    def lbo(self, lbo):
        self.__lbo = lbo

    @property
    def ime(self):
        return self.__ime

    @ime.setter
    def ime(self, ime):
        self.__ime = ime

    @property
    def prezime(self):
        return self.__prezime

    @prezime.setter
    def prezime(self, prezime):
        self.__prezime = prezime

    @property
    def datum_rodjenja(self):
        return self.__datum_rodjenja

    @datum_rodjenja.setter
    def datum_rodjenja(self, datum_rodjenja):
        self.__datum_rodjenja = datum_rodjenja

    @property
    def snimanja(self):
        return self.__snimanja

    def __init__(self, lbo, ime, prezime, datum_rodjenja):
        self.__lbo = lbo
        self.__ime = ime
        self.__prezime = prezime
        self.__datum_rodjenja = datum_rodjenja
        self.__snimanja = []

    def dodaj_snimanje(self, snimanje):
        self.__snimanja.append(snimanje)

class Snimanje:

    @property
    def pacijent(self):
        return self.__pacijent

    @pacijent.setter
    def pacijent(self, pacijent):
        self.__pacijent = pacijent

    @property
    def tip(self):
        return self.__tip

    @tip.setter
    def tip(self, tip):
        self.__tip = tip

    @property
    def izvestaj(self):
        return self.__izvestaj

    @izvestaj.setter
    def izvestaj(self, izvestaj):
        self.__izvestaj = izvestaj

    @property
    def lekar(self):
        return self.__lekar

    @lekar.setter
    def lekar(self, lekar):
        self.__lekar = lekar

    @property
    def datum_i_vreme(self):
        return self.__datum_i_vreme

    @datum_i_vreme.setter
    def datum_i_vreme(self, datum_i_vreme):
        self.__datum_i_vreme = datum_i_vreme

    @property
    def snimak(self):
        return self.__snimak

    @snimak.setter
    def snimak(self, snimak):
        self.__snimak = snimak

    def __init__(self, pacijent, datum_i_vreme, tip, izvestaj, lekar, snimak):
        self.__pacijent = pacijent
        self.__datum_i_vreme = datum_i_vreme
        self.__tip = tip
        self.__izvestaj = izvestaj
        self.__lekar = lekar
        self.__snimak = snimak

class Podaci:

    @property
    def pacijenti(self):
        return self.__pacijenti

    @property
    def snimanja(self):
        return self.__snimanja

    @property
    def tipovi(self):
        return self.__tipovi

    def __init__(self):
        self.__pacijenti = []
        self.__snimanja = []
        self.__tipovi = ['Magnetic Resonance (MR)', 'Computed Tomography (CT)', 'X-Ray (RX)',  'Ultrasound Scan (US)']

    def dodaj_pacijenta(self, pacijent):
        self.__pacijenti.append(pacijent)

    def obrisi_pacijenta(self, pacijent):
        for snimanje in pacijent.snimanja:
            self.__snimanja.remove(snimanje)
        self.__pacijenti.remove(pacijent)

    def dodaj_snimanje(self, snimanje):
        self.__snimanja.append(snimanje)
        snimanje.pacijent.snimanja.append(snimanje)

    def obrisi_snimanje(self, za_brisanje):
        pacijent = za_brisanje.pacijent
        pacijent.snimanja.remove(za_brisanje)
        self.__snimanja.remove(za_brisanje)

    def podela_snimanja(self, snimanja, prvi_indeks, poslednji_indeks):
        srednje_snimanje = snimanja[(prvi_indeks + poslednji_indeks) // 2]
        i = prvi_indeks - 1
        j = poslednji_indeks + 1
        while True:
            i += 1
            while snimanja[i].datum_i_vreme < srednje_snimanje.datum_i_vreme:
                i += 1

            j -= 1
            while snimanja[j].datum_i_vreme > srednje_snimanje.datum_i_vreme:
                j -= 1

            if i >= j:
                return j

            snimanja[i], snimanja[j] = snimanja[j], snimanja[i]

    def podela_pacijenti(self, pacijenti, prvi_indeks, poslednji_indeks):
        srednji_pacijent = pacijenti[(prvi_indeks + poslednji_indeks) // 2]
        i = prvi_indeks - 1
        j = poslednji_indeks + 1
        while True:
            i += 1
            while (pacijenti[i].prezime + pacijenti[i].ime) < (srednji_pacijent.prezime + srednji_pacijent.ime):
                i += 1

            j -= 1
            while (pacijenti[j].prezime + pacijenti[j].ime) > (srednji_pacijent.prezime + srednji_pacijent.ime):
                j -= 1

            if i >= j:
                return j

            pacijenti[i], pacijenti[j] = pacijenti[j], pacijenti[i]

    def _quick_sort(self, lista, prvi_indeks, poslendji_indeks):
        if prvi_indeks < poslendji_indeks:
            podeljen_indeks = 0
            if isinstance(lista[0], Pacijent):
                podeljen_indeks = self.podela_pacijenti(lista, prvi_indeks, poslendji_indeks)
            if isinstance(lista[0], Snimanje):
                podeljen_indeks = self.podela_snimanja(lista, prvi_indeks, poslendji_indeks)
            self._quick_sort(lista, prvi_indeks, podeljen_indeks)
            self._quick_sort(lista, podeljen_indeks + 1, poslendji_indeks)

    def quick_sort(self, lista):
        self._quick_sort(lista, 0, len(lista) - 1)

    @classmethod
    def napravi_pocetne(cls):
        podaci = Podaci()

        tipovi = podaci.tipovi

        pacijent1 = Pacijent('12345678912', 'Marta', 'Mitic', date(1993, 11, 4))
        snimanje1 = Snimanje(pacijent1, datetime(2019, 5, 1, 13, 40), tipovi[0], 'izvestaj1', 'Dr. Marko Markovic', 'C:/Users/Komarci/Desktop/Tina/FTN/2. semestar/Uvod u medicinsku informatiku/Projekat UUMI Kristina Taš BI11-2019/MR-MONO2-16-head.dcm')
        snimanje2 = Snimanje(pacijent1, datetime(2020, 5, 8, 13, 50), tipovi[3], 'izvestaj2', 'Dr. Jovan Jovanovic', '')

        pacijent2 = Pacijent('12312312312', 'Ana', 'Babic', date(1960, 8, 12))
        snimanje3 = Snimanje(pacijent2, datetime(2016, 8, 5, 8, 0), tipovi[3], 'izvestaj3', 'Dr. Jovan Jovanovic', '')
        pacijent3 = Pacijent('45645645645', 'Zarko', 'Ristic', date(2001, 2, 25))
        snimanje4 = Snimanje(pacijent3, datetime(2020, 6, 3, 16, 35), tipovi[1], 'izvestaj4', 'Dr. Marko Markovic', 'C:/Users/Komarci/Desktop/Tina/FTN/2. semestar/Uvod u medicinsku informatiku/Projekat UUMI Kristina Taš BI11-2019/CT-MONO2-16-ankle.dcm')

        snimanja = podaci.snimanja
        snimanja.append(snimanje1)
        snimanja.append(snimanje2)
        snimanja.append(snimanje3)
        snimanja.append(snimanje4)

        pacijent1.dodaj_snimanje(snimanje1)
        pacijent1.dodaj_snimanje(snimanje2)
        pacijent2.dodaj_snimanje(snimanje3)
        pacijent3.dodaj_snimanje(snimanje4)

        pacijenti = podaci.pacijenti
        pacijenti.append(pacijent1)
        pacijenti.append(pacijent2)
        pacijenti.append(pacijent3)

        return podaci

    __naziv_datoteke = "Podaci"

    @classmethod
    def sacuvaj(cls, podaci):
        datoteka = open(cls.__naziv_datoteke, "wb")
        pickle.dump(podaci, datoteka)
        datoteka.close()

    @classmethod
    def ucitaj(cls):
        try:
            datoteka = open(cls.__naziv_datoteke, "rb")
            podaci = pickle.load(datoteka)
            datoteka.close()
        except FileNotFoundError:
            return Podaci.napravi_pocetne()

        return podaci

    def sacuvaj_se(self):
        self.sacuvaj(self)