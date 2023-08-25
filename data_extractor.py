# Etude des messages de Glims
import re
import pandas as pd

data = {
    "08/05/2022": """'Schema Area' (db glims) est presque plein (284588 blocks libres,  97.4 % utilisé)
Il n'y a que 2223 MB libre dans cet environnement
Veuillez ajouter un ou plusieurs DB extents à l'environnement 'Schema Area'"""

    , "16/05/2022": """'Schema Area' (db glims) est presque plein (255065 blocks libres,  97.6 % utilisé)
Il n'y a que 1992 MB libre dans cet environnement
Veuillez ajouter un ou plusieurs DB extents à l'environnement 'Schema Area'"""

    , "16/10/2022": """Il n'y a pas assez d'espace disque sur /glimsdbf/.Il ne reste que 10413 MB, 91.85% complet"""

    , "15/11/2022": """Il n'y a pas assez d'espace disque sur /glimsdbf/.Il ne reste que 7834 MB, 93.87% complet
'Schema Area' (db glims) est presque plein (512667 blocks libres,  95.6 % utilisé)
Il n'y a que 4005 MB libre dans cet environnement
Veuillez ajouter un ou plusieurs DB extents à l'environnement 'Schema Area'"""

    , "08/12/2022": """Il n'y a pas assez d'espace disque sur /glimsdbf/.Il ne reste que 7809 MB, 93.89% complet
'Schema Area' (db glims) est presque plein (419998 blocks libres,  96.4 % utilisé)
Il n'y a que 3281 MB libre dans cet environnement
Veuillez ajouter un ou plusieurs DB extents à l'environnement 'Schema Area'"""
}

order = ['date', 'vol_disque', 'vol_disp_MB', 'vol_occup%', "area", 'blk_libres', 'area_occup%', 'area_MB_libres', 'rem']

default_csv = "data.csv"

class Extracteur:


    def __init__(self, date_str, txt):
        self.date = date_str
        self.txt = txt
        self.lines = self.txt.split("\n")
        self.nb_lines = len(self.lines)
        self.cursor = 0

    def analyse(self):
        print(f"Le nombre de ligne est de {self.nb_lines}")
        data_tags = {}
        while self.cursor < self.nb_lines:
            line = self.lines[self.cursor]
            if line.startswith("Il n'y a pas assez d'espace disque"):
                disque = self.extraire_espace_disque(line)
                data_tags.update(disque)
                self.cursor += 1

            elif line.startswith("'Schema Area'"):
                data_tags.update(self.extraire_schema_area(self.lines[self.cursor: self.cursor + 3]))
                self.cursor += 3
            else:
                print(f"ERROR : ligne non prévue :  \n{line}\n")
                self.cursor += 1

        return data_tags

    @staticmethod
    def extraire_espace_disque(a_line):
        """Phrase est de type :
        Il n'y a pas assez d'espace disque sur /glimsdbf/.Il ne reste que 10413 MB, 91.85% complet

        >>> line = "Il n'y a pas assez d'espace disque sur /glimsdbf/.Il ne reste que 10413 MB, 91.85% complet"
        >>> Extracteur.extraire_espace_disque(line)
        {'vol_disque': '/glimsdbf/', 'vol_disp_MB': '10413', 'vol_occup%': '91.85'}
        """
        corresp = re.search(r"(/.*?/)\.Il ne reste que (\d+) MB, (.*)%.*", a_line)
        return {'vol_disque': corresp.group(1), 'vol_disp_MB': corresp.group(2), 'vol_occup%': corresp.group(3)}


    @staticmethod
    def extraire_schema_area(lines):
        """Extraction pour une phrase complexe :
        >>> lines_examples = [
        ... "'Schema Area' (db glims) est presque plein (419998 blocks libres,  96.4 % utilisé)",
        ...     "Il n'y a que 3281 MB libre dans cet environnement",
        ...  "Veuillez ajouter un ou plusieurs DB extents à l'environnement 'Schema Area'"
        ...            ]
        >>> expected_output = {
        ...    "area": "db glims",
        ...    "blk_libres": "419998",
        ...    "area_occup%": "96.4",
        ...    "area_MB_libres": "3281"
        ... }
        >>> results = Extracteur.extraire_schema_area(lines_examples)
        >>> results == expected_output
        True
        """

        pattern = r"'Schema Area' \((.*?)\) est presque plein \((\d+) blocks libres,  ([\d.]+) % utilisé\)"
        cor_line1 = re.search(pattern, lines[0])
        cor_line2 = re.search(r"(\d+) MB libre", lines[1])
        return {"area": cor_line1.group(1), 'blk_libres': cor_line1.group(2), 'area_occup%': cor_line1.group(3),
                'area_MB_libres': cor_line2.group(1)
                }



class DataIntegrateur:
    """A class to create structure like pandas Dataframe from dictionaries"""
    def __init__(self):
        self.df = pd.DataFrame()

    def add_line(self, index, dico):
        """Ajoute une ligne au tableau à partir d'un dictionnaire décrivant la ligne"""
        dico['date'] = index
        line_df = pd.DataFrame.from_records(dico, index = [1]         )
        self.df = pd.concat([self.df, line_df], axis=0)
        # self.df.concat(line_df, axis = 0)
        print(self.df)

    def order_columns(self):
        self.df = self.df.reindex(order, axis=1)

    def load_csv(self, csv_file=None):
        """Load a csv in self.df"""
        if csv_file is None:
            csv_file = default_csv
        self.df = pd.read_csv(csv_file)
        print("CSV chargé")

    def to_csv(self, file_name=None):
        self.order_columns()
        if file_name is None:
            file_name = default_csv
        self.df.to_csv(file_name, index=False)
        print("CSV enregistré")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    record = "08/12/2022"
    E = Extracteur(record, data[record])
    print(E.analyse())
    #
    # print("\nEtude pour l'extraction")
    # for record in list(data)[:2]:
    #     E = Extracteur(record, d
    #     ata[record])
    #     print(E.analyse())

    print("\nEtude pour l'intégration")
    I = DataIntegrateur()
    I.load_csv()

    for date in ["08/05/2022",  "16/10/2022", "08/12/2022"]:
        E = Extracteur(date, data[date])
        dico = E.analyse()
        I.add_line(date, dico)

    I.to_csv()
    print(I.df)

