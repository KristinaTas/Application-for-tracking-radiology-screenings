from tkinter.ttk import Combobox
from tkinter import filedialog

from evidencija import *
from dicomGUI import *

class SnimanjaProzor(Toplevel):

    def ocisti_labele(self):
        self.__pacijent_labela["text"] = ""
        self.__datum_i_vreme_labela["text"] = ""
        self.__tip_labela["text"] = ""
        self.__lekar_labela["text"] = ""
        self.__izvestaj_labela["text"] = ""
        self.__putanja.set('')

    def popuni_labele(self, snimanje):
        self.__pacijent_labela['text'] = '{} {}'.format(snimanje.pacijent.prezime, snimanje.pacijent.ime)
        self.__datum_i_vreme_labela["text"] = snimanje.datum_i_vreme.strftime("%d.%m.%Y. %H:%M")
        self.__lekar_labela["text"] = snimanje.lekar
        self.__izvestaj_labela["text"] = snimanje.izvestaj
        self.__tip_labela['text'] = snimanje.tip[len(snimanje.tip)-3:-1]
        self.__putanja.set(snimanje.snimak)

    def popuni_snimanja_listbox(self, snimanja):
        self.__snimanja_listbox.delete(0, END)
        self.__podaci.quick_sort(snimanja)
        for snimanje in snimanja:
            self.__snimanja_listbox.insert(END, snimanje.datum_i_vreme.strftime("%d.%m.%Y. %H:%M"))

        self.ocisti_labele()

    def promena_selekcije_u_listbox(self, event=None):
        if not self.__snimanja_listbox.curselection():
            self.ocisti_labele()

            self.__snimanje_meni.entryconfig(0, state=DISABLED)
            self.__snimanje_meni.entryconfig(2, state=DISABLED)
            self.__snimanje_meni.entryconfig(3, state=DISABLED)
            self.__otvori_button['state'] = DISABLED
            return

        indeks = self.__snimanja_listbox.curselection()[0]
        snimanje = self.__snimanja_za_prikaz[indeks]
        self.popuni_labele(snimanje)

        self.__snimanje_meni.entryconfig(0, state=NORMAL)
        self.__snimanje_meni.entryconfig(2, state=NORMAL)
        self.__snimanje_meni.entryconfig(3, state=NORMAL)
        if snimanje.snimak == '':
            self.__otvori_button['state'] = DISABLED
        else:
            self.__otvori_button['state'] = NORMAL

    def postavi_combobox(self, snimanje):
        for indeks in range(len(self.__pacijenti)):
            pacijent = self.__pacijenti[indeks]
            if pacijent == '{} {}'.format(snimanje.pacijent.prezime, snimanje.pacijent.ime):
                self.__pacijent_combobox.current(indeks)
                break
        for indeks in range(len(self.__tipovi)):
            if self.__tipovi[indeks] == snimanje.tip:
                self.__tip_combobox.current(indeks)
                break

    def promena_selekcije_u_combobox(self, event=None):
        snimanja = []

        snimanja_pacijent = []
        indeks_pacijenta = self.__pacijent_combobox.current()
        pacijent = self.__pacijenti[indeks_pacijenta]
        if indeks_pacijenta == 0:
            snimanja_pacijent = self.__podaci.snimanja
        else:
            for snimanje in self.__podaci.snimanja:
                if pacijent == '{} {}'.format(snimanje.pacijent.prezime, snimanje.pacijent.ime):
                    snimanja_pacijent.append(snimanje)

        snimanja_tip = []
        indeks_tipa = self.__tip_combobox.current()
        tip = self.__tipovi[indeks_tipa]
        if indeks_tipa == 0:
            snimanja_tip = self.__podaci.snimanja
        for snimanje in self.__podaci.snimanja:
            if tip == snimanje.tip:
                snimanja_tip.append(snimanje)

        for snimanje_pacijent in snimanja_pacijent:
            for snimanje_tip in snimanja_tip:
                if snimanje_pacijent == snimanje_tip:
                    snimanja.append(snimanje_tip)
                    break

        self.__snimanja_za_prikaz = snimanja
        self.popuni_snimanja_listbox(snimanja)

    def komanda_ocisti(self):
        self.__snimanja_listbox.selection_clear(0, END)
        self.promena_selekcije_u_listbox()

    def komanda_dodaj(self):
        if len(self.__podaci.pacijenti) == 0:
            messagebox.showerror("Greška", "Nema pacijenata! Dodajte pacijenta kako biste mogli da mu dodate snimanje.")
            return None
        indeks_pacijenta = self.__pacijent_combobox.current()
        indeks_tipa = self.__tip_combobox.current()
        if indeks_pacijenta != 0:
            indeks_pacijenta -= 1
        if indeks_tipa != 0:
            indeks_tipa -= 1
        dodavanje_snimanja_prozor = DodavanjeSnimanjaProzor(self, self.__podaci, indeks_pacijenta, indeks_tipa)
        self.wait_window(dodavanje_snimanja_prozor)
        if dodavanje_snimanja_prozor.otkazano:
            return

        snimanje = self.__podaci.snimanja[-1]

        self.__snimanja_listbox.selection_clear(0, END)
        self.postavi_combobox(snimanje)
        self.promena_selekcije_u_combobox()

        indeks = END
        for i in range(len(self.__snimanja_za_prikaz)):
            if snimanje == self.__snimanja_za_prikaz[i]:
                indeks = i

        self.__snimanja_listbox.selection_set(indeks)
        self.promena_selekcije_u_listbox()

    def komanda_izmeni(self):
        indeks = self.__snimanja_listbox.curselection()[0]
        snimanje = self.__snimanja_za_prikaz[indeks]

        izmena_snimanja_prozor = IzmenaSnimanjaProzor(self, self.__podaci, snimanje)
        self.wait_window(izmena_snimanja_prozor)
        if izmena_snimanja_prozor.otkazano:
            return

        self.__snimanja_listbox.selection_clear(0, END)
        self.postavi_combobox(snimanje)
        self.promena_selekcije_u_combobox()

        indeks = END
        for i in range(len(self.__snimanja_za_prikaz)):
            if snimanje == self.__snimanja_za_prikaz[i]:
                indeks = i

        self.__snimanja_listbox.selection_set(indeks)
        self.promena_selekcije_u_listbox()

    def komanda_obrisi(self):
        if messagebox.askquestion("Upozorenje", "Da li ste sigurni da želite da obrišete snimanje?", icon="warning") == "no":
            return

        indeks = self.__snimanja_listbox.curselection()[0]
        snimanje = self.__snimanja_za_prikaz[indeks]
        self.__podaci.obrisi_snimanje(snimanje)

        self.config(cursor="wait")
        self.__podaci.sacuvaj_se()
        self.config(cursor="")

        self.__snimanja_listbox.selection_clear(0, END)
        self.promena_selekcije_u_listbox()
        self.__snimanja_za_prikaz = self.__podaci.snimanja
        self.popuni_snimanja_listbox(self.__podaci.snimanja)

        self.__pacijent_combobox.current(0)
        self.__tip_combobox.current(0)

    def komanda_otvori(self):
        indeks = self.__snimanja_listbox.curselection()[0]
        snimanje = self.__snimanja_za_prikaz[indeks]
        dicom_prozor = DICOMProzor(self, snimanje)
        self.wait_window(dicom_prozor)

    def __init__(self, master, podaci, indeks):
        super().__init__(master)
        self.__podaci = podaci
        self.__snimanja_za_prikaz = podaci.snimanja
        self.__indeks = indeks

        podaci.quick_sort(self.__podaci.pacijenti)
        self.__pacijenti = []
        self.__pacijenti.append('--Odaberi sve pacijente--')
        for pacijent in self.__podaci.pacijenti:
            self.__pacijenti.append("{} {}".format(pacijent.prezime, pacijent.ime))

        self.__tipovi = []
        self.__tipovi.append('--Odaberi sve tipove--')
        for tip in self.__podaci.tipovi:
            self.__tipovi.append(tip)

        levi_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        levi_frame.pack(side=LEFT, fill=BOTH, expand=1)
        combobox_frame = Frame(levi_frame, pady=5)
        combobox_frame.pack()
        listbox_frame = Frame(levi_frame)
        listbox_frame.pack(fill=BOTH, expand=1)

        self.__pacijent_combobox = Combobox(combobox_frame, state='readonly', width=25, values=self.__pacijenti)
        self.__tip_combobox = Combobox(combobox_frame, state='readonly', width=25, values=self.__tipovi)
        self.__pacijent_combobox.bind("<<ComboboxSelected>>", self.promena_selekcije_u_combobox)
        self.__tip_combobox.bind("<<ComboboxSelected>>", self.promena_selekcije_u_combobox)

        self.__pacijent_combobox.current(self.__indeks)
        self.__tip_combobox.current(0)

        red = 0
        kolona = 1
        Label(combobox_frame, text="Pretraga po pacijentu:").grid(row=red, sticky=E)
        self.__pacijent_combobox.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(combobox_frame, text="Pretraga po tipu:").grid(row=red, sticky=E)
        self.__tip_combobox.grid(row=red, column=kolona, sticky=W)

        self.__snimanja_listbox = Listbox(listbox_frame, activestyle='none')
        self.__snimanja_listbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.__snimanja_listbox.bind("<<ListboxSelect>>", self.promena_selekcije_u_listbox)

        snimanje_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        snimanje_frame.pack(side=RIGHT, fill=BOTH, expand=1)
        snimak_frame = Frame(snimanje_frame)

        self.__pacijent_labela = Label(snimanje_frame)
        self.__datum_i_vreme_labela = Label(snimanje_frame)
        self.__tip_labela = Label(snimanje_frame)
        self.__izvestaj_labela = Label(snimanje_frame)
        self.__lekar_labela = Label(snimanje_frame)

        self.__putanja = StringVar(master)
        self.__putanja_entry = Entry(snimak_frame, borderwidth=5, state=DISABLED, textvariable=self.__putanja)
        self.__putanja_entry.pack(side=LEFT)
        Button(snimak_frame, width=2, text='...', state=DISABLED).pack(side=LEFT)
        self.__otvori_button = Button(snimak_frame, width=5, text='Otvori', state=DISABLED, command=self.komanda_otvori)
        self.__otvori_button.pack(side=LEFT)

        red = 0
        kolona = 1
        Label(snimanje_frame, text="Pacijent:").grid(row=red, sticky=E)
        self.__pacijent_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(snimanje_frame, text="Datum i vreme:").grid(row=red, sticky=E)
        self.__datum_i_vreme_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(snimanje_frame, text="Tip:").grid(row=red, sticky=E)
        self.__tip_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(snimanje_frame, text="Izveštaj:").grid(row=red, sticky=E)
        self.__izvestaj_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(snimanje_frame, text="Lekar:").grid(row=red, sticky=E)
        self.__lekar_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(snimanje_frame, text='Snimak:').grid(row=red, sticky=E)
        snimak_frame.grid(row=red, column=kolona, sticky=E)

        meni_bar = Menu(self)

        datoteka_meni = Menu(meni_bar, tearoff=0)
        datoteka_meni.add_command(label="Povratak", command=self.destroy)
        meni_bar.add_cascade(label="Datoteka", menu=datoteka_meni)

        self.__snimanje_meni = Menu(meni_bar, tearoff=0)
        self.__snimanje_meni.add_command(label="Očisti", state=DISABLED, command=self.komanda_ocisti)
        self.__snimanje_meni.add_command(label="Dodaj", command=self.komanda_dodaj)
        self.__snimanje_meni.add_command(label="Izmeni", state=DISABLED, command=self.komanda_izmeni)
        self.__snimanje_meni.add_command(label="Obriši", state=DISABLED, command=self.komanda_obrisi)
        meni_bar.add_cascade(label="Snimanje", menu=self.__snimanje_meni)

        self.config(menu=meni_bar)

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.title("Snimanja")

        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.geometry('600x400')

        self.promena_selekcije_u_combobox()

        self.transient(master)
        self.focus_force()
        self.grab_set()


class SnimanjeProzor(Toplevel):

    def pacijent_validacija(self):
        indeks = self.__pacijent_combobox.current()
        if indeks < 0:
            messagebox.showerror("Greška", "Pacijent nije odabran!")
            return None

        indeks = self.pacijent_combobox.current()
        pacijent = self.podaci.pacijenti[indeks]
        return pacijent

    def datum_i_vreme_validacija(self, pacijent):
        try:
            dan = self.__dan.get()
            mesec = self.__mesec.get()
            godina = self.__godina.get()
            sat = self.__sat.get()
            minut = self.__minut.get()
            datum = date(godina, mesec, dan)
            datum_i_vreme = datetime(godina, mesec, dan, sat, minut)
            if datum_i_vreme > datetime.now():
                messagebox.showerror("Greška", "Unesite datum i vreme zaključno sa trenutnim!")
                return None
            if datum < pacijent.datum_rodjenja:
                messagebox.showerror("Greška", "Uneli ste datum pre rođenja pacijenta!")
                return None
        except ValueError:
            messagebox.showerror("Greška", "Uneli ste nepostojeći datum!")
            return None

        return datum_i_vreme

    def tip_validacija(self):
        indeks = self.__tip_combobox.current()
        if indeks < 0:
            messagebox.showerror("Greška", "Tip nije odabran!")
            return None

        indeks = self.tip_combobox.current()
        tip = self.podaci.tipovi[indeks]
        return tip

    def izvestaj_validacija(self):
        izvestaj = self.__izvestaj.get()
        if izvestaj == "":
            messagebox.showerror("Greška", "Unesite izveštaj!")
            return None

        return izvestaj

    def lekar_validacija(self):
        lekar = self.__lekar.get()
        if lekar == "":
            messagebox.showerror("Greška", "Unesite lekara!")
            return None

        return lekar.title()

    def snimak_validacija(self):
        return self.__snimak.get()

    def date_u_dicom(self, datum):
        dan = datum.day
        mesec = datum.month * 100
        godina = datum.year * 10000
        return str(godina + mesec + dan)

    def popuni_dcm(self, snimanje):
        putanja = snimanje.snimak.split('/')[-1]
        self.__dataset = pydicom.dcmread(putanja, force=True)
        self["cursor"] = "wait"
        self.update()

        self.__dataset.PatientID = snimanje.pacijent.lbo
        self.__dataset.PatientName = '{} {}'.format(snimanje.pacijent.prezime, snimanje.pacijent.ime)
        self.__dataset.PatientBirthDate = self.date_u_dicom(snimanje.pacijent.datum_rodjenja)
        self.__dataset.StudyDate = self.date_u_dicom(snimanje.datum_i_vreme)
        self.__dataset.Modality = snimanje.tip[len(snimanje.tip)-3:-1]
        self.__dataset.StudyDescription = snimanje.izvestaj
        self.__dataset.ReferringPhysicianName = snimanje.lekar

        try:
            self.__dataset.save_as(putanja)
        except Exception as ex:
            print()
            print(ex)
            messagebox.showerror("DICOM", "Greška pri čuvanju datoteke!")

        self["cursor"] = ""

    def komanda_ok(self):
        self.config(cursor="wait")
        self.podaci.sacuvaj_se()
        self.config(cursor="")

        self.__otkazano = False
        self.destroy()

    def komanda_odaberi(self):
        putanja = filedialog.askopenfilename(
            initialdir="",
            title="Izbor snimka",
            filetypes=[("All files", "*.*"), ("DICOM files", "*.dcm")])
        if putanja == "":
            return

        self["cursor"] = "wait"
        self.update()
        self["cursor"] = ""
        self.__snimak.set(putanja)

    def __init__(self, master, podaci):
        super().__init__(master)

        self.__otkazano = True
        self.__master = master
        self.__podaci = podaci

        pacijenti = []
        for pacijent in self.__podaci.pacijenti:
            pacijenti.append('{} {}'.format(pacijent.prezime, pacijent.ime))

        self.__izvestaj = StringVar(master)
        self.__lekar = StringVar(master)
        self.__dan = IntVar(master)
        self.__mesec = IntVar(master)
        self.__godina = IntVar(master)
        self.__sat = IntVar(master)
        self.__minut = IntVar(master)
        self.__snimak = StringVar(master)

        snimanje_frame = Frame(self, padx=5, pady=5)
        datum_frame = Frame(snimanje_frame)
        vreme_frame = Frame(snimanje_frame)
        snimak_frame = Frame(snimanje_frame)
        button_frame = Frame(self, padx=5, pady=5)

        self.__izvestaj_entry = Entry(snimanje_frame, width=20, textvariable=self.__izvestaj)
        self.__lekar_entry = Entry(snimanje_frame, width=20, textvariable=self.__lekar)

        Spinbox(datum_frame, width=5, from_=1, to=31, textvariable=self.__dan).pack(side=LEFT)
        Spinbox(datum_frame, width=5, from_=1, to=12, textvariable=self.__mesec).pack(side=LEFT)
        Spinbox(datum_frame, width=10, from_=1, to=int(date.today().year), textvariable=self.__godina).pack(side=LEFT)
        Spinbox(vreme_frame, width=5, from_=0, to=23, textvariable=self.__sat).pack(side=LEFT)
        Spinbox(vreme_frame, width=5, from_=0, to=59, textvariable=self.__minut).pack(side=LEFT)

        self.__pacijent_combobox = Combobox(snimanje_frame, state="readonly", values=pacijenti)
        self.__tip_combobox = Combobox(snimanje_frame, state="readonly", width=25, values=podaci.tipovi)

        self.__putanja_entry = Entry(snimak_frame, width=20, borderwidth=5, state=DISABLED, textvariable=self.__snimak)
        self.__putanja_entry.pack(side=LEFT)
        Button(snimak_frame, width=2, text='...', command=self.komanda_odaberi).pack(side=LEFT)
        Button(snimak_frame, width=5, text='Otvori', state=DISABLED).pack(side=LEFT)

        self.__ok_button = Button(button_frame, width=10, command=self.komanda_ok)
        self.__ok_button.pack(side=TOP)
        Button(button_frame, width=10, text='Otkaži', command=self.destroy).pack(side=BOTTOM)

        red = 0
        kolona = 1
        Label(snimanje_frame, text="Pacijent:").grid(row=red, sticky=E)
        self.__pacijent_combobox.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(snimanje_frame, text="Datum:").grid(row=red, sticky=E)
        datum_frame.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(snimanje_frame, text="Vreme:").grid(row=red, sticky=E)
        vreme_frame.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(snimanje_frame, text="Tip:").grid(row=red, sticky=E)
        self.__tip_combobox.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(snimanje_frame, text="Izveštaj:").grid(row=red, sticky=E)
        self.__izvestaj_entry.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(snimanje_frame, text="Lekar:").grid(row=red, sticky=E)
        self.__lekar_entry.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(snimanje_frame, text="Snimak:").grid(row=red, sticky=E)
        snimak_frame.grid(row=red, column=kolona, sticky=W)

        snimanje_frame.pack()
        button_frame.pack(side=BOTTOM)

        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)

        self.transient(master)
        self.focus_force()
        self.grab_set()

    @property
    def otkazano(self):
        return self.__otkazano

    @property
    def podaci(self):
        return self.__podaci

    @property
    def izvestaj(self):
        return self.__izvestaj

    @property
    def dan(self):
        return self.__dan

    @property
    def mesec(self):
        return self.__mesec

    @property
    def godina(self):
        return self.__godina

    @property
    def sat(self):
        return self.__sat

    @property
    def minut(self):
        return self.__minut

    @property
    def lekar(self):
        return self.__lekar

    @property
    def snimak(self):
        return self.__snimak

    @property
    def pacijent_combobox(self):
        return self.__pacijent_combobox

    @property
    def tip_combobox(self):
        return self.__tip_combobox

    @property
    def ok_button(self):
        return self.__ok_button


class DodavanjeSnimanjaProzor(SnimanjeProzor):

    def komanda_ok(self):
        lekar = self.lekar_validacija()
        if not lekar:
            return
        izvestaj = self.izvestaj_validacija()
        if not izvestaj:
            return
        pacijent = self.pacijent_validacija()
        if not pacijent:
            return
        tip = self.tip_validacija()
        if not tip:
            return
        datum_i_vreme = self.datum_i_vreme_validacija(pacijent)
        if not datum_i_vreme:
            return
        snimak = self.snimak_validacija()

        snimanje = Snimanje(pacijent, datum_i_vreme, tip, izvestaj, lekar, snimak)
        self.podaci.dodaj_snimanje(snimanje)
        if snimak != '':
            super().popuni_dcm(snimanje)
        super().komanda_ok()

    def __init__(self, master, podaci, indeks_pacijenta, indeks_tipa):
        super().__init__(master, podaci)

        self.dan.set(datetime.now().day)
        self.mesec.set(datetime.now().month)
        self.godina.set(datetime.now().year)
        self.sat.set(datetime.now().hour)
        self.minut.set(datetime.now().minute)

        self.pacijent_combobox.current(indeks_pacijenta)
        self.tip_combobox.current(indeks_tipa)

        self.ok_button['text'] = "Dodaj"
        self.title("Dodavanje snimanja")


class IzmenaSnimanjaProzor(SnimanjeProzor):

    def komanda_ok(self):
        lekar = self.lekar_validacija()
        if not lekar:
            return
        izvestaj = self.izvestaj_validacija()
        if not izvestaj:
            return
        tip = self.tip_validacija()
        if not tip:
            return
        pacijent = self.pacijent_validacija()
        datum_i_vreme = self.datum_i_vreme_validacija(pacijent)
        if not datum_i_vreme:
            return
        snimak = self.snimak_validacija()

        self.__snimanje.lekar = lekar
        self.__snimanje.izvestaj = izvestaj
        self.__snimanje.tip = tip
        self.__snimanje.datum_i_vreme = datum_i_vreme
        self.__snimanje.snimak = snimak

        if snimak != '':
            super().popuni_dcm(self.__snimanje)
        super().komanda_ok()

    def __init__(self, master, podaci, snimanje):
        super().__init__(master, podaci)

        self.__snimanje = snimanje

        self.izvestaj.set(self.__snimanje.izvestaj)
        self.lekar.set(self.__snimanje.lekar)
        self.dan.set(self.__snimanje.datum_i_vreme.day)
        self.mesec.set(self.__snimanje.datum_i_vreme.month)
        self.godina.set(self.__snimanje.datum_i_vreme.year)
        self.sat.set(self.__snimanje.datum_i_vreme.hour)
        self.minut.set(self.__snimanje.datum_i_vreme.minute)
        self.snimak.set(self.__snimanje.snimak)

        pacijenti = self.podaci.pacijenti
        for indeks in range(len(pacijenti)):
            if pacijenti[indeks] == snimanje.pacijent:
                self.pacijent_combobox.current(indeks)
                break

        tipovi = self.podaci.tipovi
        for indeks in range(len(tipovi)):
            if tipovi[indeks] == snimanje.tip:
                self.tip_combobox.current(indeks)
                break

        self.pacijent_combobox['state'] = DISABLED
        self.ok_button['text'] = "Izmeni"
        self.title("Izmena snimanja")