from snimanjaGUI import *
from evidencija import *

class PacijentiProzor(Toplevel):

    def ocisti_labele(self):
        self.__lbo_labela["text"] = ""
        self.__ime_labela["text"] = ""
        self.__prezime_labela["text"] = ""
        self.__datum_rodjenja_labela["text"] = ""
        self.__snimanja_labela["text"] = ""

    def popuni_labele(self, pacijent):
        self.__lbo_labela["text"] = pacijent.lbo
        self.__ime_labela["text"] = pacijent.ime
        self.__prezime_labela["text"] = pacijent.prezime
        self.__datum_rodjenja_labela["text"] = pacijent.datum_rodjenja.strftime("%d.%m.%Y.")
        snimanja = ''
        for snimanje in pacijent.snimanja:
            snimanja = snimanja + snimanje.datum_i_vreme.strftime("%d.%m.%Y. %H:%M") + ',\n'
        snimanja = snimanja[:len(snimanja)-2]
        self.__snimanja_labela['text'] = snimanja

    def popuni_pacijenti_listbox(self, pacijenti):
        self.__pacijenti_listbox.delete(0, END)
        self.__podaci.quick_sort(pacijenti)
        for pacijent in pacijenti:
            self.__pacijenti_listbox.insert(END, "{} {}".format(pacijent.prezime, pacijent.ime))
        self.ocisti_labele()

    def promena_selekcije_u_listbox(self, event=None):
        if not self.__pacijenti_listbox.curselection():
            self.ocisti_labele()

            self.__pacijent_meni.entryconfig(0, state=DISABLED)
            self.__pacijent_meni.entryconfig(2, state=DISABLED)
            self.__pacijent_meni.entryconfig(3, state=DISABLED)
            self.__pacijent_meni.entryconfig(4, state=DISABLED)
            return

        indeks = self.__pacijenti_listbox.curselection()[0]
        pacijent = self.__pacijenti_za_prikaz[indeks]
        self.popuni_labele(pacijent)

        self.__pacijent_meni.entryconfig(0, state=NORMAL)
        self.__pacijent_meni.entryconfig(2, state=NORMAL)
        self.__pacijent_meni.entryconfig(3, state=NORMAL)
        self.__pacijent_meni.entryconfig(4, state=NORMAL)

    def komanda_ocisti(self):
        self.__pacijenti_listbox.selection_clear(0, END)
        self.promena_selekcije_u_listbox()

    def komanda_dodaj(self):
        dodavanje_pacijenta_prozor = DodavanjePacijentaProzor(self, self.__podaci)
        self.wait_window(dodavanje_pacijenta_prozor)
        if dodavanje_pacijenta_prozor.otkazano:
            return

        pacijent = self.__podaci.pacijenti[-1]
        self.__pacijenti_za_prikaz = self.__podaci.pacijenti

        self.__pacijenti_listbox.selection_clear(0, END)
        self.popuni_pacijenti_listbox(self.__podaci.pacijenti)

        indeks = END
        for i in range(len(self.__podaci.pacijenti)):
            if pacijent == self.__podaci.pacijenti[i]:
                indeks = i

        self.__pacijenti_listbox.selection_set(indeks)
        self.promena_selekcije_u_listbox()
        self.__pretraga.set('')

    def komanda_izmeni(self):
        indeks = self.__pacijenti_listbox.curselection()[0]
        pacijent = self.__pacijenti_za_prikaz[indeks]

        izmena_pacijenta_prozor = IzmenaPacijentaProzor(self, self.__podaci, pacijent)
        self.wait_window(izmena_pacijenta_prozor)
        if izmena_pacijenta_prozor.otkazano:
            return

        self.__pacijenti_za_prikaz = self.__podaci.pacijenti
        self.__pacijenti_listbox.selection_clear(0, END)
        self.popuni_pacijenti_listbox(self.__podaci.pacijenti)

        indeks = END
        for i in range(len(self.__podaci.pacijenti)):
            if pacijent == self.__podaci.pacijenti[i]:
                indeks = i

        self.__pacijenti_listbox.selection_set(indeks)
        self.promena_selekcije_u_listbox()
        self.__pretraga.set('')

    def komanda_obrisi(self):
        if messagebox.askquestion("Upozorenje", "Da li ste sigurni da želite da obrišete pacijenta? Obrisaće se i sva njegova snimanja.", icon="warning") == "no":
            return

        indeks = self.__pacijenti_listbox.curselection()[0]
        pacijent = self.__pacijenti_za_prikaz[indeks]
        self.__podaci.obrisi_pacijenta(pacijent)

        self.config(cursor="wait")
        self.__podaci.sacuvaj_se()
        self.config(cursor="")

        self.__pacijenti_za_prikaz = self.__podaci.pacijenti
        self.__pacijenti_listbox.selection_clear(0, END)
        self.promena_selekcije_u_listbox()
        self.popuni_pacijenti_listbox(self.__podaci.pacijenti)
        self.__pretraga.set('')

    def komanda_snimanja(self):
        indeks = self.__pacijenti_listbox.curselection()[0] + 1
        snimanja_prozor = SnimanjaProzor(self, self.__podaci, indeks)
        self.wait_window(snimanja_prozor)

    def komanda_pretraga(self, event=None):
        pacijenti_za_prikaz = []
        unos = self.__pretraga.get().lower()
        for pacijent in self.__podaci.pacijenti:
            if unos == '':
                pacijenti_za_prikaz = self.__podaci.pacijenti
                break
            if (unos in pacijent.ime.lower()) or (unos in pacijent.prezime.lower()):
                pacijenti_za_prikaz.append(pacijent)

        self.__pacijenti_za_prikaz = pacijenti_za_prikaz
        self.popuni_pacijenti_listbox(pacijenti_za_prikaz)

    def __init__(self, master, podaci):
        super().__init__(master)
        self.__podaci = podaci
        self.__pacijenti_za_prikaz = podaci.pacijenti

        levi_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        levi_frame.pack(side=LEFT, fill=BOTH, expand=1)
        pretraga_frame = Frame(levi_frame, pady=5)
        pretraga_frame.pack()
        listbox_frame = Frame(levi_frame)
        listbox_frame.pack(fill=BOTH, expand=1)

        self.__pretraga = StringVar(master)
        self.__pretraga_entry = Entry(pretraga_frame, width=20, textvariable=self.__pretraga)
        self.__pretraga_entry.bind('<KeyRelease>', self.komanda_pretraga)

        red = 0
        kolona = 1
        Label(pretraga_frame, text="Pretraga:").grid(row=red, sticky=E)
        self.__pretraga_entry.grid(row=red, column=kolona, sticky=W)

        self.__pacijenti_listbox = Listbox(listbox_frame, activestyle='none')
        self.__pacijenti_listbox.pack(side=LEFT, fill=BOTH, expand=1)
        self.__pacijenti_listbox.bind("<<ListboxSelect>>", self.promena_selekcije_u_listbox)

        pacijent_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        pacijent_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        self.__lbo_labela = Label(pacijent_frame)
        self.__ime_labela = Label(pacijent_frame)
        self.__prezime_labela = Label(pacijent_frame)
        self.__datum_rodjenja_labela = Label(pacijent_frame)
        self.__snimanja_labela = Label(pacijent_frame)

        red = 0
        kolona = 1
        Label(pacijent_frame, text="LBO:").grid(row=red, sticky=E)
        self.__lbo_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(pacijent_frame, text="Ime:").grid(row=red, sticky=E)
        self.__ime_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(pacijent_frame, text="Prezime:").grid(row=red, sticky=E)
        self.__prezime_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(pacijent_frame, text="Datum rođenja:").grid(row=red, sticky=E)
        self.__datum_rodjenja_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(pacijent_frame, text="Snimajna:").grid(row=red, sticky=E)
        self.__snimanja_labela.grid(row=red, column=kolona, sticky=W)
        red += 1

        meni_bar = Menu(self)

        datoteka_meni = Menu(meni_bar, tearoff=0)
        datoteka_meni.add_command(label="Povratak", command=self.destroy)
        meni_bar.add_cascade(label="Datoteka", menu=datoteka_meni)

        self.__pacijent_meni = Menu(meni_bar, tearoff=0)
        self.__pacijent_meni.add_command(label="Očisti", state=DISABLED, command=self.komanda_ocisti)
        self.__pacijent_meni.add_command(label="Dodaj", command=self.komanda_dodaj)
        self.__pacijent_meni.add_command(label="Izmeni", state=DISABLED, command=self.komanda_izmeni)
        self.__pacijent_meni.add_command(label="Obriši", state=DISABLED, command=self.komanda_obrisi)
        self.__pacijent_meni.add_command(label='Snimanja', state=DISABLED, command=self.komanda_snimanja)
        meni_bar.add_cascade(label="Pacijent", menu=self.__pacijent_meni)

        self.config(menu=meni_bar)

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.title("Pacijenti")

        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.geometry('600x400')

        self.popuni_pacijenti_listbox(self.__pacijenti_za_prikaz)

        self.transient(master)
        self.focus_force()
        self.grab_set()

    @property
    def pretraga(self):
        return self.__pretraga

class PacijentProzor(Toplevel):

    def ime_validacija(self):
        ime = self.__ime.get()
        if len(ime) < 2:
            messagebox.showerror("Greška", "Ime mora da ima bar dva karaktera!")
            return None

        return ime.capitalize()

    def prezime_validacija(self):
        prezime = self.__prezime.get()
        if len(prezime) < 2:
            messagebox.showerror("Greška", "Prezime mora da ima bar dva karaktera!")
            return None

        return prezime.capitalize()

    def datum_rodjenja_validacija(self):
        try:
            dan = self.__dan.get()
            mesec = self.__mesec.get()
            godina = self.__godina.get()
            datum_rodjenja = date(godina, mesec, dan)
            if datum_rodjenja > date.today():
                messagebox.showerror("Greška", "Unesite datum zaključno sa današnjim!")
                return None
        except ValueError:
            messagebox.showerror("Greška", "Uneli ste nepostojeći datum!")
            return None

        return datum_rodjenja

    def lbo_validacija(self):
        try:
            lbo = self.__lbo.get()
            if len(str(lbo)) != 11:
                messagebox.showerror("Greška", "LBO mora da sadrži 11 cifara!")
                return None
            for pacijent in self.__podaci.pacijenti:
                if pacijent.lbo == lbo:
                    messagebox.showerror("Greška", "Već postoji pacijent sa ovim LBO-om!")
                    return None
        except TclError:
            messagebox.showerror("Greška", "LBO mora da sadrži samo cifre!")
            return None

        return lbo

    def komanda_ok(self):
        self.config(cursor="wait")
        self.podaci.sacuvaj_se()
        self.config(cursor="")

        self.__otkazano = False
        self.destroy()

    def __init__(self, master, podaci):
        super().__init__(master)

        self.__otkazano = True
        self.__podaci = podaci

        self.__lbo = IntVar(master)
        self.__ime = StringVar(master)
        self.__prezime = StringVar(master)
        self.__dan = IntVar(master)
        self.__mesec = IntVar(master)
        self.__godina = IntVar(master)

        pacijent_frame = Frame(self, padx=5, pady=5)
        datum_frame = Frame(pacijent_frame)
        button_frame = Frame(self, padx=5, pady=5)

        self.__ime_entry = Entry(pacijent_frame, width=20, textvariable=self.__ime)
        self.__prezime_entry = Entry(pacijent_frame, width=20, textvariable=self.__prezime)
        self.__lbo_entry = Entry(pacijent_frame, width=20, textvariable=self.__lbo)

        Spinbox(datum_frame, width=5, from_=1, to=31, textvariable=self.__dan).pack(side=LEFT)
        Spinbox(datum_frame, width=5, from_=1, to=12, textvariable=self.__mesec).pack(side=LEFT)
        Spinbox(datum_frame, width=10, from_=1, to=int(date.today().year), textvariable=self.__godina).pack(side=LEFT)

        self.__ok_button = Button(button_frame, width=10, command=self.komanda_ok)
        self.__ok_button.pack(side=TOP)
        Button(button_frame, width=10, text='Otkaži', command=self.destroy).pack(side=BOTTOM)

        red = 0
        kolona = 1
        Label(pacijent_frame, text="LBO:").grid(row=red, sticky=E)
        self.__lbo_entry.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(pacijent_frame, text="Ime:").grid(row=red, sticky=E)
        self.__ime_entry.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(pacijent_frame, text="Prezime:").grid(row=red, sticky=E)
        self.__prezime_entry.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(pacijent_frame, text="Datum rođenja:").grid(row=red, sticky=E)
        datum_frame.grid(row=red, column=kolona, sticky=W)

        pacijent_frame.pack()
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
    def ime(self):
        return self.__ime

    @property
    def prezime(self):
        return self.__prezime

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
    def lbo(self):
        return self.__lbo

    @property
    def lbo_entry(self):
        return self.__lbo_entry

    @property
    def ok_button(self):
        return self.__ok_button


class DodavanjePacijentaProzor(PacijentProzor):

    def komanda_ok(self):
        ime = self.ime_validacija()
        if not ime:
            return
        prezime = self.prezime_validacija()
        if not prezime:
            return
        datum_rodjenja = self.datum_rodjenja_validacija()
        if not datum_rodjenja:
            return
        lbo = self.lbo_validacija()
        if not lbo:
            return

        pacijent = Pacijent(str(lbo), ime, prezime, datum_rodjenja)
        self.podaci.dodaj_pacijenta(pacijent)

        super().komanda_ok()

    def __init__(self, master, podaci):
        super().__init__(master, podaci)

        self.lbo.set('')
        self.dan.set(date.today().day)
        self.mesec.set(date.today().month)
        self.godina.set(date.today().year)

        self.ok_button['text'] = "Dodaj"
        self.title("Dodavanje pacijenta")


class IzmenaPacijentaProzor(PacijentProzor):

    def komanda_ok(self):
        ime = self.ime_validacija()
        if not ime:
            return
        prezime = self.prezime_validacija()
        if not prezime:
            return
        datum_rodjenja = self.datum_rodjenja_validacija()
        if not datum_rodjenja:
            return

        self.__pacijent.ime = ime
        self.__pacijent.prezime = prezime
        self.__pacijent.datum_rodjenja = datum_rodjenja

        super().komanda_ok()

    def __init__(self, master, podaci, pacijent):
        super().__init__(master, podaci)

        self.__pacijent = pacijent

        self.ime.set(self.__pacijent.ime)
        self.prezime.set(self.__pacijent.prezime)
        self.dan.set(self.__pacijent.datum_rodjenja.day)
        self.mesec.set(self.__pacijent.datum_rodjenja.month)
        self.godina.set(self.__pacijent.datum_rodjenja.year)
        self.lbo.set(self.__pacijent.lbo)

        self.lbo_entry["state"] = DISABLED
        self.ok_button["text"] = 'Izmeni'

        self.title("Izmena pacijenta")