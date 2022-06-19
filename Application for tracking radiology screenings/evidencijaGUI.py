from pacijentiGUI import *
from snimanjaGUI import *
from PIL import Image, ImageTk

class GlavniProzor(Tk):

    def komanda_pacijenti(self):
        pacijenti_prozor = PacijentiProzor(self, self.__podaci)
        self.wait_window(pacijenti_prozor)

    def komanda_snimanja(self):
        indeks = 0
        snimanja_prozor = SnimanjaProzor(self, self.__podaci, indeks)
        self.wait_window(snimanja_prozor)

    def __init__(self, podaci):
        super().__init__()
        self.__podaci = podaci

        slika = ImageTk.PhotoImage(Image.open("dom zdravlja novi sad.png"))

        self.__slika_label = Label(self, image=slika)
        self.__slika_label.image = slika
        self.__slika_label.pack(side=LEFT, expand=1)

        frame = Frame(self)
        frame.pack()

        meni_bar = Menu(self)

        datoteka_meni = Menu(meni_bar, tearoff=0)
        datoteka_meni.add_command(label="Izlaz", command=self.destroy)
        meni_bar.add_cascade(label="Datoteka", menu=datoteka_meni)

        pacijent_meni = Menu(meni_bar, tearoff=0)
        pacijent_meni.add_command(label = 'Pacijenti', command=self.komanda_pacijenti)
        pacijent_meni.add_command(label = 'Snimanja', command=self.komanda_snimanja)
        meni_bar.add_cascade(label="Prozor", menu=pacijent_meni)

        self.config(menu=meni_bar)

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.title("Evidencija snimanja na radiologiji")

        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self.geometry("600x400")

        self.focus_force()
        self.grab_set()

def main():
    podaci = Podaci.ucitaj()

    glavni_prozor = GlavniProzor(podaci)
    glavni_prozor.mainloop()


main()