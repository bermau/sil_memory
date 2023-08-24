# Etude des messages de Glims
import re

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
                # if tags :
                #     tags.update(data_tags)
                #     print
                self.cursor += 1

            elif line.startswith("'Schema Area'"):
                data_tags.update(self.extraire_schema_area(self.lines[self.cursor: self.cursor + 3]))
                self.cursor += 3
            else:
                raise ValueError(f"ligne non prévue :  {line}")

        return data_tags

    @staticmethod
    def extraire_espace_disque(a_line):
        """Phrase est de type :
        Il n'y a pas assez d'espace disque sur /glimsdbf/.Il ne reste que 10413 MB, 91.85% complet"""
        print("Ligne est : ", a_line)
        corresp = re.search(r"(/.*?/)\.Il ne reste que (\d+).*(\d+\.\d+)%.*", a_line)
        return {"volume_disque": corresp.group(1), "Dispo_MB": corresp.group(2), 'occup%': corresp.group(3)}

    @staticmethod
    def extraire_schema_area(lines):
        """Extraction pour une phrase de type :
        'Schema Area' (db glims) est presque plein (419998 blocks libres,  96.4 % utilisé)
Il n'y a que 3281 MB libre dans cet environnement
Veuillez ajouter un ou plusieurs DB extents à l'environnement 'Schema Area'
"""
        print(lines)
        cor_line1 = re.search(r".*\((.*?)\).*(\d+).*(\d+)", lines[0])
        cor_line2 = re.search(r"(\d+) MB libre", lines[1])
        return {"area": cor_line1.group(1), 'blk_libres': cor_line1.group(2), 'area_occup%': cor_line1.group(3),
                'MB_libres': cor_line2.group(1)
                }


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    record = "08/12/2022"
    E = Extracteur(record, data[record])
    print(E.analyse())

    for record in data:
        E = Extracteur(record, data[record])
        print(E.analyse())
