from datetime import date
from tkinter import *
from tkinter import messagebox
import pydicom
from PIL import Image, ImageTk
import pydicom_PIL


class DICOMProzor(Toplevel):

    def dicom_u_date(self, datum):
        godina = datum // 10000
        datum = datum % 10000
        mesec = datum // 100
        dan = datum % 100
        return date(godina, mesec, dan).strftime("%d.%m.%Y.")

    def popuni_prozor(self):
        try:
            self["cursor"] = "wait"
            self.update()

            self.title(self.__snimanje.snimak.split('/')[-1])

            self.__lbo_labela["text"] = self.__dataset.PatientID
            self.__pacijent_labela["text"] = self.__dataset.PatientName
            self.__datum_rodjenja_labela["text"] = self.dicom_u_date(int(self.__dataset.PatientBirthDate))
            self.__datum_snimanja_labela["text"] = self.dicom_u_date(int(self.__dataset.StudyDate))
            self.__tip_labela["text"] = self.__dataset.Modality
            self.__izvestaj_labela["text"] = self.__dataset.StudyDescription
            self.__lekar_labela["text"] = self.__dataset.ReferringPhysicianName
        except Exception as ex:
            print()
            print(ex)
            messagebox.showwarning("DICOM", "Greška pri učitavanju datoteke!")
        try:
            pil_slika = pydicom_PIL.get_PIL_image(self.__dataset)
            sirina = pil_slika.width
            visina = pil_slika.height

            maks_dimenzija = 900
            if sirina > maks_dimenzija or visina > maks_dimenzija:
                if sirina > visina:
                    odnos = maks_dimenzija/sirina
                    sirina = maks_dimenzija
                    visina = int(odnos*visina)
                else:
                    odnos = maks_dimenzija/visina
                    sirina = int(odnos*sirina)
                    visina = maks_dimenzija
            pil_slika = pil_slika.resize((sirina, visina), Image.LANCZOS)

            slika = ImageTk.PhotoImage(pil_slika)
            self.__slika_label["image"] = slika
            self.__slika_label.image = slika
        except Exception as ex:
            slika = ImageTk.PhotoImage(Image.open("DICOM-Logo.jpg"))
            self.__slika_label["image"] = slika
            self.__slika_label.image = slika

            print()
            print(ex)
            messagebox.showwarning("DICOM", "Greška pri otvaranju slike!")

        self.update_idletasks()
        sirina = self.winfo_width()
        visina = self.winfo_height()
        self.minsize(sirina, visina)
        self["cursor"] = ""

    def __init__(self, master, snimanje):
        super().__init__(master)
        self.__snimanje = snimanje
        self.__dataset = pydicom.dcmread(self.__snimanje.snimak, force=True)

        dicom_frame = Frame(self, borderwidth=2, relief="ridge", padx=10, pady=10)
        dicom_frame.pack(side=RIGHT, fill=BOTH, expand=1)

        self.__lbo_labela = Label(dicom_frame)
        self.__pacijent_labela = Label(dicom_frame)
        self.__datum_rodjenja_labela = Label(dicom_frame)
        self.__datum_snimanja_labela = Label(dicom_frame)
        self.__tip_labela = Label(dicom_frame)
        self.__izvestaj_labela = Label(dicom_frame)
        self.__lekar_labela = Label(dicom_frame)

        self.__slika_label = Label(self)
        self.__slika_label.pack(side=LEFT, expand=1)

        red = 0
        kolona = 1
        Label(dicom_frame, text="LBO:").grid(row=red, sticky=E)
        self.__lbo_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(dicom_frame, text="Pacijent:").grid(row=red, sticky=E)
        self.__pacijent_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(dicom_frame, text="Datum rođenja:").grid(row=red, sticky=E)
        self.__datum_rodjenja_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(dicom_frame, text="Datum snimanja:").grid(row=red, sticky=E)
        self.__datum_snimanja_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(dicom_frame, text="Tip:").grid(row=red, sticky=E)
        self.__tip_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(dicom_frame, text="Izveštaj:").grid(row=red, sticky=E)
        self.__izvestaj_labela.grid(row=red, column=kolona, sticky=W)
        red += 1
        Label(dicom_frame, text="Lekar:").grid(row=red, sticky=E)
        self.__lekar_labela.grid(row=red, column=kolona, sticky=W)

        meni_bar = Menu(self)

        self.__datoteka_meni = Menu(meni_bar, tearoff=0)
        self.__datoteka_meni.add_command(label="Povratak", command=self.destroy)
        meni_bar.add_cascade(label="Datoteka", menu=self.__datoteka_meni)

        self.config(menu=meni_bar)

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.title("DICOM")
        self.update_idletasks()

        self.popuni_prozor()
        print(self.__dataset)
        print()

        self.transient(master)
        self.focus_force()
        self.grab_set()