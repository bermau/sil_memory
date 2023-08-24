"""
Un utilitaire Tkinter pour récupérer le contenu de messages provenant du SIL.
"""
import tkinter as tk
import sys
from tkinter import filedialog
import data_extractor

init_date = "08/12/2022"
init_txt = """Il n'y a pas assez d'espace disque sur /glimsdbf/.Il ne reste que 7809 MB, 93.89% complet
'Schema Area' (db glims) est presque plein (419998 blocks libres,  96.4 % utilisé)
Il n'y a que 3281 MB libre dans cet environnement
Veuillez ajouter un ou plusieurs DB extents à l'environnement 'Schema Area'"""


def fonction_trt(txt: str):
    return txt.upper()


# J'utilise une classe qui ne dérive pas d'une classe de tkinter, comme préconisé par :
# https://stackoverflow.com/questions/16115378/tkinter-example-code-for-multiple-windows-why-wont-buttons-load-correctly
def ouvrir_fichier():
    """BUT  : ouvrir un fichier csv"""
    path = filedialog.askopenfilename()
    with open(path, "r") as f:
        text = f.read()
    print(text)


class MapApp():  # Ne dérive pas de Tkinter

    def __init__(self, tk_master, store_data_in:data_extractor.DataIntegrateur):

        self.data_manager = store_data_in
        self.files = ["fichier 1", "fichier 2"]

        self.tkmaster = tk_master
        self.tkmaster.title("Extracteur de messages")

        self.tkframe = tk.Frame(self.tkmaster)  # Premier objet tk.Frame.

        self.frame_top = tk.Frame(self.tkframe)
        self.frame_top.pack(side="top")

        self.frame_bottom = tk.Frame(self.tkframe)
        self.frame_bottom.pack(side="left")

        self.frame_right = tk.Frame(self.tkframe)
        self.frame_right.pack(side="right")

        # Une entrée pour la date :
        self.date_entry = tk.Entry(self.frame_top, width=20)
        # self.text_entry.place(height=20, width=30)
        self.date_entry.pack(side='top')

        # Une entrée en haut
        self.text_area = tk.Text(self.frame_top, height=20, width=120)
        # self.text_entry.place(height=20, width=30)
        self.text_area.pack(side='left')

        # Créer un bouton d'action
        self.button_action_1 = tk.Button(self.frame_right, text="Majuscules", command=self.to_upper)
        self.button_action_1.pack()

        # Créer un bouton de récupération
        self.button_extract_data = tk.Button(self.frame_right, text="Extraction", command=self.extract_data)
        self.button_extract_data.pack()

        # Créer un bouton Ouvrir
        self.button_open = tk.Button(self.frame_bottom, text="Ouvrir...", command=ouvrir_fichier)
        self.button_open.pack()

        # Créer un bouton quitter
        self.button_quit = tk.Button(self.frame_bottom, text="Quitter", command=tk_master.quit)
        self.button_quit.pack()

        # Initialisation des champs
        if init_txt:
            self.text_area.insert(tk.END, init_txt)
        if init_date:
            self.date_entry.insert(tk.END, str(init_date))

        # Créer une barre pour menu déroulant et y insérer des menus.
        menu_bar = tk.Menu(tk_master)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Ouvrir un fichier...", command=ouvrir_fichier)
        file_menu.add_command(label="Fermer le fichier")
        file_menu.add_command(label="Quitter l'application", command=root.quit)

        menu_bar.add_cascade(label="Fichier", menu=file_menu)

        # Configurer la fenêtre principale pour utiliser la barre de menus
        self.tkmaster.config(menu=menu_bar)
        self.tkframe.pack()

    def to_upper(self):
        txt_in = self.text_area.selection_get()

        print("Entrée : ", txt_in)
        txt_out = fonction_trt(txt_in)
        print("Sortie : ", txt_out)

        first_index = self.text_area.index("sel.first")
        last_index = self.text_area.index("sel.last")

        # Remplacer la sélection par le texte en majuscules
        self.text_area.delete(first_index, last_index)
        self.text_area.insert(first_index, txt_out)

    def extract_data(self):
        # getting values from Entry or Text objects are different methods
        date = self.date_entry.get()
        msg = self.text_area.get(1.0, "end-1c")
        print(f"""Données à traiter :\n date : {date}\n msg = {msg}""")
        extracteur = data_extractor.Extracteur(date, msg)
        dico = extracteur.analyse()
        if dico:
            self.data_manager.add_line(date, dico)




if __name__ == '__main__':
    # Le traitement des arguments n'est pas utilisé, mais je le laisse pour éventuellement plus tard.
    try:
        filename = sys.argv[1]
        all_files = sys.argv[1:]
    except:
        filename = None
        all_files = None
    # faire quelque chose avec le nom de fichier
    if filename:
        print(f"Lancement du programme avec le fichier {filename}")
        print(f"commande transmise : f{all_files}")
    else:
        print("Pas de fichier")

    extractor = data_extractor.DataIntegrateur()

    root = tk.Tk()
    root.geometry("800x400")
    app = MapApp(root, store_data_in=extractor)
    root.mainloop()
