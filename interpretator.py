import numpy as np
import sys
import pandas as pd
from PIL import Image
import colorsys
hsv_value =lambda a: colorsys.rgb_to_hsv(a[0] / 255.0, a[1] / 255.0, a[2] / 255.0)
normal_value=lambda a,b,c: [int(round(360*a,0)), int(round(100*b,0)),int(round(100*c,0))]
class Interpretator:
    def __init__(self, image_path, model_path,ilosc_polek):
        self.image_path = image_path
        self.model_path = model_path
        self.ilosc_polek =int(ilosc_polek)
        # pola/obszary[{numer_szeregu},{numer_kolumny},{numer_kanału_rgba}]
        self.pola=np.array(Image.open(self.image_path))[:,:,:3]
        self.obszary=np.array(Image.open(self.model_path))[:,:,:3]
        self.wymiary=self.pola.shape
    def create_pre_csv(self):
        # przypisywanie obszaru do koloru
        self.kolory=dict()
        # przypisywanie do pliku csv
        self.POLE_SUPERMARKETU={
            "POLE_ID" : [],
            "NAZWA" : [],
            "TOP_ID" : [],
            "BOT_ID" : [],
            "LEFT_ID" : [],
            "RIGHT_ID" : [],
            "OBSZAR_ID" : [],
            "TYP_POLA" : []
        }
        self.OBSZAR_SUPERMARKETU={
            "OBSZAR_ID" : [],
            "NAZWA" : [],
            "TYP_OBSZARU" : []
        }
        self.POLACZENIA_OBSZAROW={
            "PRIMARY_ID" : [],
            "CONECTED_ID" : [],
            "TYP" : []
        }
        self.POLKA={
            "POLKA_ID" : [],
            "POLE_ID" : [],
            "NAZWA" : [],
            "POJEMNOSC": []
        }
        self.KASA={
            "KASA_ID" : [],
            "NAZWA": [],
            "OBSZAR_ID": []
        }
        #pre połączenia obszarów
        self.prepol=set()
        #legenda dla pól supermarketu
        self.pola_legenda={
            0 : "PO",
            350 : "P",
            124 : "WE",
            180 : "PD",
            228 : "KA",
            44 : "MG"
        }
        self.obszary_legenda={
            "PO": "KO",
            "P": "RE",
            "WE": "WE",
            "PD": "KO",
            "KA": "KA",
            "MG": "MG"
        }
        self.rozw={
            "MG": "MAGAZYN",
            "KA": "KASA",
            'WE': "WEJŚCIE",
            "P": "REGAŁ"
        }
        self.antytyp={
            "LEWY":"PRAWY",
            "GÓRNY":"DOLNY"
        }
    def create_pole_id_nazwa(self,i,j):
        id=int(str(i).zfill(4)+str(j).zfill(4))
        nazwa=f"p_{i}_{j}"
        return id, nazwa
    def porownanie_pol(self, pole_glowne, pole_dodatkowe,typ):
        [typ1,id_ob1]=pole_glowne
        [typ2,id_ob2]=pole_dodatkowe
        if id_ob1!=id_ob2:
            if typ2=="PD" or typ1=="PD":
                self.prepol.add((id_ob1,id_ob2,typ))
                self.prepol.add((id_ob2,id_ob1,self.antytyp[typ]))
            elif typ1!="P" and typ2!="P":
                self.prepol.add((id_ob1, id_ob2, typ))
                self.prepol.add((id_ob2, id_ob1, self.antytyp[typ]))
    def get_pole_supermarket(self):
        # numer szeregu
        for i in range(self.wymiary[0]):
            # numer kolumny
            for j in range(self.wymiary[1]):
                [R,G,B]=self.pola[i,j] #wyciąganie rgb z piksela
                [H,S,V]=list(hsv_value([R,G,B])) #zamian w hsv
                [H,_,_]=normal_value(H,S,V) #normalizacja- zokrąglanie hsv
                [R1,G1,B1]=self.obszary[i,j]
                [H1,S1,V1]=list(hsv_value([R1,G1,B1]))
                [H1,S1,V1]=normal_value(H1,S1,V1)
                #print([H,S,V])
                #print([H1,S1,V1])
                #tworzymy nazwe pola i id
                id,nazwa=self.create_pole_id_nazwa(i,j)
                #dodajemy id
                self.POLE_SUPERMARKETU["POLE_ID"].append(id)
                self.POLE_SUPERMARKETU["TYP_POLA"].append(self.pola_legenda[H]) #dodajemy typ pola
                for k in ("KA","MG", "WE", "P"): #sprawdzamy czy pole jest jednym z pól specjalnych
                    if self.pola_legenda[H]==k:# jeżeli tak, to sprawdzamy, czy dany kolor nie ma przypisanego obszaru w postaci koloru obszaru, id obszaru i nazwy obszaru
                        if f"{H1}{S1}{V1}" in self.kolory:
                            id1,nazwa1=self.kolory[f"{H1}{S1}{V1}"]
                            #wyciągamy nazwę obszaru i jego dotychcasowe id
                            self.POLE_SUPERMARKETU["OBSZAR_ID"].append(id1) #dodajemy do pola obszar supermarketu
                            if nazwa1.split()[0]!=self.rozw[k]: # sprawdzamy, czy obecna nazwa jest polem specjalnym, bo mogła istnieć
                                #wyszukujemy maksymalny numer
                                if len(self.kolory)>0:
                                    t=max([(lambda a,b: int(a[1]) if a[0] == b else 0)(self.kolory[z][1].split(),self.rozw[k]) for z in self.kolory])
                                else:
                                    t=0
                                t=t+1
                                #zmieniamy nazwę korytarza na pole specjalne o określonym numerze
                                self.kolory[f"{H1}{S1}{V1}"][1]=f"{self.rozw[k]} {t}"
                                #wyszukujemy istniejący obszar, który był wcześniej korytarzem i zmieniamy go w obszar wejscia, kasy lub magazynu
                                l=self.OBSZAR_SUPERMARKETU["OBSZAR_ID"].index(id1)
                                self.OBSZAR_SUPERMARKETU["NAZWA"][l]=f"{self.rozw[k]} {t}"
                                self.OBSZAR_SUPERMARKETU["TYP_OBSZARU"][l]=self.obszary_legenda[self.pola_legenda[H]]
                                # To były dane dla pliku CSV, bo oryginalnie obszar nie ma koloru
                                if k != "P":
                                    self.POLE_SUPERMARKETU["NAZWA"].append(f"{self.rozw[k]} {t}")  # dodanie nazwy
                                else:
                                    self.POLE_SUPERMARKETU["NAZWA"].append(nazwa)#Dodany w tym ifie zostaje tylko to pole

                                if self.rozw[k]=="KASA":#dodatkowo sprawdzamy, czy pole jest kasą, jak tak, to dodajemy kasę
                                    self.KASA["KASA_ID"].append(t)#id kasy to kolejny numer
                                    self.KASA["OBSZAR_ID"].append(id1)
                                    self.KASA["NAZWA"].append(f"{self.rozw[k]} {t}")
                            else:

                                if k != "P":
                                    self.POLE_SUPERMARKETU["NAZWA"].append(nazwa1) # dodanie nazwy
                                else:
                                    self.POLE_SUPERMARKETU["NAZWA"].append(nazwa)
                        else:
                            if len(self.kolory) > 0:
                                t=max([(lambda a,b: int(a[1]) if a[0] == b else 0)(self.kolory[z][1].split(),self.rozw[k]) for z in self.kolory])
                            else:
                                t = 0
                            t=t+1
                            self.kolory[f"{H1}{S1}{V1}"]=[id,f"{self.rozw[k]} {t}"]#dodanie koloru obszaru
                            if k!="P":
                                self.POLE_SUPERMARKETU["NAZWA"].append(f"{self.rozw[k]} {t}")#dodanie nazwy
                            else:
                                self.POLE_SUPERMARKETU["NAZWA"].append(nazwa)
                            self.POLE_SUPERMARKETU["OBSZAR_ID"].append(id)# dodanie obszaru id
                            #w tym miejscu dodajemy nowy obszar, bo jeżeli nie ma takiego koloru, to nie ma takiego obszaru
                            self.OBSZAR_SUPERMARKETU["OBSZAR_ID"].append(id) #id obszaru to id pierwszego pola w lewym górnym rogu
                            self.OBSZAR_SUPERMARKETU["NAZWA"].append(f"{self.rozw[k]} {t}")
                            self.OBSZAR_SUPERMARKETU["TYP_OBSZARU"].append(self.obszary_legenda[self.pola_legenda[H]])
                            if self.rozw[k] == "KASA":  # dodatkowo sprawdzamy, czy pole jest kasą, jak tak, to dodajemy kasę
                                self.KASA["KASA_ID"].append(t)  # id kasy to kolejny numer
                                self.KASA["OBSZAR_ID"].append(id)
                                self.KASA["NAZWA"].append(f"{self.rozw[k]} {t}")
                        if k == "P":
                            for l in range(self.ilosc_polek):
                                self.POLKA["POLKA_ID"].append(int(f"{id}{str(l).zfill(2)}"))
                                self.POLKA["POLE_ID"].append(id)
                                self.POLKA["NAZWA"].append(f"{nazwa}_{str(l).zfill(2)}")
                                self.POLKA["POJEMNOSC"].append(100)
                        break  # zniszczenie pętli, by nie można było wykonąć klauzuli else
                else:
                    # jeżeli nie mamy do czynienia z polem specjalnym jak wejście, magazyn czy kasa, to wykonujemy kod
                    self.POLE_SUPERMARKETU["NAZWA"].append(nazwa) #dodajemy wygenerowaną nazwę dla pola
                    if f"{H1}{S1}{V1}" in self.kolory:
                        id1, _ = self.kolory[f"{H1}{S1}{V1}"]
                        self.POLE_SUPERMARKETU["OBSZAR_ID"].append(id1)
                    else:
                        self.kolory[f"{H1}{S1}{V1}"] =[id, f"p{nazwa[1:]}"]
                        self.POLE_SUPERMARKETU["OBSZAR_ID"].append(id)
                        self.OBSZAR_SUPERMARKETU["OBSZAR_ID"].append(id)  # id obszaru to id pierwszego pola w lewym górnym rogu
                        self.OBSZAR_SUPERMARKETU["NAZWA"].append(f"o{nazwa[1:]}")
                        self.OBSZAR_SUPERMARKETU["TYP_OBSZARU"].append(self.obszary_legenda[self.pola_legenda[H]])
                    # pozostaje także sprawdzenie, czy pole jest regałem, jeżeli tak to należy dodać półki

                    #sprawdzamy
                #teraz nastąpi dodanie połączeń pomiędzy polami i pomiędzy
                #na start pole prawe i dolne oznaczymy jako puste
                self.POLE_SUPERMARKETU["BOT_ID"].append("")
                self.POLE_SUPERMARKETU["RIGHT_ID"].append("")

                if i>0:
                    id2, _ = self.create_pole_id_nazwa(i-1, j)
                    #znalezienie indeksu graniczącego pola
                    l=self.POLE_SUPERMARKETU["POLE_ID"].index(id2)
                    #wstawienie wzajemne indeksów
                    self.POLE_SUPERMARKETU["TOP_ID"].append(id2)
                    self.POLE_SUPERMARKETU["BOT_ID"][l]=id
                    self.porownanie_pol([self.POLE_SUPERMARKETU["TYP_POLA"][-1], self.POLE_SUPERMARKETU["OBSZAR_ID"][-1]], [self.POLE_SUPERMARKETU["TYP_POLA"][l], self.POLE_SUPERMARKETU["OBSZAR_ID"][l]], "GÓRNY")

                else:
                    self.POLE_SUPERMARKETU["TOP_ID"].append("")
                if j>0:
                    id2, _ = self.create_pole_id_nazwa(i, j-1)
                    l=self.POLE_SUPERMARKETU["POLE_ID"].index(id2)
                    #wstawienie wzajemne indeksów
                    self.POLE_SUPERMARKETU["LEFT_ID"].append(id2)
                    self.POLE_SUPERMARKETU["RIGHT_ID"][l]=id
                    self.porownanie_pol(
                        [self.POLE_SUPERMARKETU["TYP_POLA"][-1], self.POLE_SUPERMARKETU["OBSZAR_ID"][-1]],
                        [self.POLE_SUPERMARKETU["TYP_POLA"][l], self.POLE_SUPERMARKETU["OBSZAR_ID"][l]], "LEWY")
                else:
                    self.POLE_SUPERMARKETU["LEFT_ID"].append("")
        for i in self.prepol:
            self.POLACZENIA_OBSZAROW["PRIMARY_ID"].append(i[0])
            self.POLACZENIA_OBSZAROW["CONECTED_ID"].append(i[1])
            self.POLACZENIA_OBSZAROW["TYP"].append(i[2])
    def display(self):
        dicts_to_print = [
            self.POLE_SUPERMARKETU,
            self.OBSZAR_SUPERMARKETU,
            self.POLACZENIA_OBSZAROW,
            self.POLKA,
            self.KASA
        ]

        for dic in dicts_to_print:
            # Ustal długość najdłuższego klucza
            max_key_length = max(map(len, dic.keys()))

            # Wypisz nagłówki
            for key in dic.keys():
                print(f"{key:{max_key_length}}", end=" | ")
            print()

            # Wypisz separator
            for _ in dic.keys():
                print("-" * (max_key_length + 2), end=" | ")
            print()

            # Wypisz dane
            num_rows = len(next(iter(dic.values())))
            for i in range(num_rows):
                for key in dic.keys():
                    value = dic[key][i]
                    print(f"{value:{max_key_length}}", end=" | ")
                print()
            print()
    def dp(self):
        print(self.kolory)
    def to_csv(self):
        # Tworzenie DataFrame z listy słowników
        dicts_to_print = [
            self.POLE_SUPERMARKETU,
            self.OBSZAR_SUPERMARKETU,
            self.POLACZENIA_OBSZAROW,
            self.POLKA,
            self.KASA
        ]
        nazwy=[
            "POLE_SUPERMARKETU",
            "OBSZAR_SUPERMARKETU",
            "POLĄCZENIA_OBSZARÓW",
            "PÓŁKA",
            "KASA"
        ]
        x=[pd.DataFrame(i) for i in dicts_to_print]
        # Zapis do pliku Excel (xlsx) z nadaniem nazw arkuszom
        file_path = 'baza_danych.xlsx'

        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            for i in range(len(x)):
                x[i].to_excel(writer, sheet_name=f'{nazwy[i]}', index=False)
if __name__ == "__main__":
    if len(sys.argv)==4:
        image_path = sys.argv[1]
        model_path = sys.argv[2]
        ilosc_polek=sys.argv[3]
        interpretator = Interpretator(image_path,model_path,ilosc_polek)
        interpretator.create_pre_csv()
        interpretator.get_pole_supermarket()
        interpretator.display()
        #interpretator.dp()
        interpretator.to_csv()
