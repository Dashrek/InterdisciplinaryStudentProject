from pddl.logic import Predicate, constants, variables
from pddl.core import Domain, Problem
from pddl.action import Action
from pddl.formatter import domain_to_string, problem_to_string
from pddl.requirements import Requirements
import pandas as pd
from functools import reduce
import subprocess
import sys
# translator
trans = str.maketrans('ąćęłńóśźżĄĆĘŁŃÓŚŹŻ', 'acelnoszzACELNOSZZ')
wejscie=(lambda a: "WEJŚCIE 1" if len(a)==1 else ( f"{a[-2]} {a[-1]}" if a[-2] == "WEJŚCIE" else "WEJŚCIE 1"))(sys.argv)

dodatki=(sys.argv[1:] if sys.argv[-2]!="WEJŚCIE" else ( sys.argv[1:-2] if len(sys.argv)>3 else ""))
class DomeneRegionowCreator:
    def __init__(self):
        [self.x, self.z] = variables("x z", types=["location"])
        [self.y] = variables("y", types=["item"])
        self.licznik_problemow=2
        self.from_region = Predicate("from-region", self.x, self.y)
        self.in_region = Predicate("in-region", self.x)
        self.connect_region = Predicate("connect-region", self.x, self.z)
        self.in_backpack = Predicate("in-backpack", self.y)
        self.kasa = Predicate("kasa", self.x)
        self.in_kasa = Predicate("in-kasa")

        self.move_to_region = Action(
            "move-to-region",
            parameters=[self.x, self.z],
            precondition=self.in_region(self.x) & self.connect_region(self.x, self.z),
            effect=~self.in_region(self.x) & self.in_region(self.z)
        )
        self.take_to_backpack = Action(
            "take-to-backpack",
            parameters=[self.x, self.y],
            precondition=self.in_region(self.x) & self.from_region(self.x, self.y),
            effect=self.in_backpack(self.y)
        )
        self.zaplac = Action(
            "zaplac",
            parameters=[self.x],
            precondition=self.in_region(self.x) & self.kasa(self.x),
            effect=~self.in_region(self.x) & self.in_kasa
        )

    def create_regions_domain(self):
        # Define the domain object.
        self.requirements_list = [Requirements.STRIPS, Requirements.TYPING, ":adl"]
        self.domain = Domain(
            "regions",
            requirements=self.requirements_list,
            types={"location": None, "item": None},
            predicates=[self.from_region, self.in_region, self.connect_region, self.in_backpack, self.kasa, self.in_kasa],
            actions=[self.move_to_region, self.take_to_backpack, self.zaplac]
        )
    def zapisz_domene_regionow(self):
        with open("./pddl1/domain.pddl", "w") as file:
            file.write(domain_to_string(self.domain))
            file.close()
    def wczytaj_plik(self):
        # Wczytaj plik CSV do DataFrame
        df = pd.read_csv('./mapa/trasa_dla_produktow.csv',encoding='Windows-1252')
        self.trasa_k = df#.to_dict(orient='list')
        df= pd.read_csv('./mapa/kasy.csv',encoding='Windows-1252')
        self.kasa_i= df#.to_dict(orient='list')
        df= pd.read_csv('./mapa/wejścia.csv',encoding='Windows-1252')
        self.wejscia = df#.to_dict(orient='list')
        # Wczytaj arkusze "Sheet1", "Sheet2" i "Sheet3" z pliku Excel
        self.df_pole_supermarketu = pd.read_excel('baza_danych.xlsx', sheet_name='POLE_SUPERMARKETU')
        result_df = pd.merge(self.df_pole_supermarketu, self.df_pole_supermarketu, left_on='TOP_ID', right_on='POLE_ID',suffixes=('_p', '_t'), how='left')
        result_df = pd.merge(result_df, self.df_pole_supermarketu, left_on='BOT_ID_p', right_on='POLE_ID', suffixes=('', '_b'), how='left')
        result_df.columns = [f'{col}_b' if not col.endswith(('_p', '_t')) else col for col in result_df.columns]
        result_df = pd.merge(result_df, self.df_pole_supermarketu, left_on='LEFT_ID_p', right_on='POLE_ID',suffixes=('', '_l'), how='left')
        result_df.columns = [f'{col}_l' if not col.endswith(('_p', '_t', '_b')) else col for col in result_df.columns]
        result_df = pd.merge(result_df, self.df_pole_supermarketu, left_on='RIGHT_ID_p', right_on='POLE_ID',suffixes=('', '_r'), how='left')
        result_df.columns = [f'{col}_r' if not col.endswith(('_p', '_t', '_b', '_l')) else col for col in result_df.columns]
        result_df = result_df[['NAZWA_p', 'OBSZAR_ID_p', 'NAZWA_t', 'OBSZAR_ID_t', 'NAZWA_b', 'OBSZAR_ID_b', 'NAZWA_l', 'OBSZAR_ID_l', 'NAZWA_r', 'OBSZAR_ID_r']]
        result_df['OBSZAR_ID_t'] = result_df['OBSZAR_ID_t'].fillna(-1).astype(int)
        result_df['OBSZAR_ID_b'] = result_df['OBSZAR_ID_b'].fillna(-1).astype(int)
        result_df['OBSZAR_ID_l'] = result_df['OBSZAR_ID_l'].fillna(-1).astype(int)
        result_df['OBSZAR_ID_r'] = result_df['OBSZAR_ID_r'].fillna(-1).astype(int)
        self.super_pola=result_df

        # Wybieramy interesujące nas kolumny


        self.df_obszar_supermarketu = pd.read_excel('baza_danych.xlsx', sheet_name='OBSZAR_SUPERMARKETU')
        self.df_polaczenia_obszarow = pd.read_excel('baza_danych.xlsx', sheet_name='POLĄCZENIA_OBSZARÓW')
        # Wykonaj połączenie na podstawie warunków
        self.df_polaczenia_obszarow1 = pd.merge(
            self.df_polaczenia_obszarow,
            self.df_obszar_supermarketu[['obszar_id'.upper(), 'nazwa'.upper()]],
            left_on='primary_id'.upper(),
            right_on='obszar_id'.upper(),
            how='inner'
        )
        self.df_polaczenia_obszarow1 = pd.merge(
            self.df_polaczenia_obszarow1,
            self.df_obszar_supermarketu[['obszar_id'.upper(), 'nazwa'.upper()]],
            left_on='conected_id'.upper(),
            right_on='obszar_id'.upper(),
            how='inner',
            suffixes=('_primary'.upper(), '_connected'.upper())
        )
        self.df_polaczenia_obszarow1 = self.df_polaczenia_obszarow1[
            (self.df_polaczenia_obszarow1['nazwa_primary'.upper()].str.upper().str.contains('REGAŁ') == False) &
            (self.df_polaczenia_obszarow1['nazwa_connected'.upper()].str.upper().str.contains('REGAŁ') == False)
            ]
        # Wybierz interesujące kolumny
        self.df_polaczenia_obszarow1 = self.df_polaczenia_obszarow1[['nazwa_primary'.upper(), 'nazwa_connected'.upper()]]
        self.df_obszar_supermarketu1 = self.df_obszar_supermarketu[self.df_obszar_supermarketu['nazwa'.upper()].str.upper().str.contains('REGAŁ') == False]
        self.trasa_ki = self.trasa_k[['Nazwa Sasiedniego Obszaru', 'Nazwa Produktu']]
        #" ".join([i.replace(" ","_") for i in self.df_obszar_supermarketu1["NAZWA"]]
        # Wyświetl wynik
    def stworz_pddl_obszar(self):
        #wczytanie itemow
        self.lokacje={}
        self.itemy={}
        #wczytanie obszarow do objects
        for i in self.df_obszar_supermarketu1["NAZWA"]:
            [self.lokacje[i]]=constants(i.replace(" ","_").translate(trans),type_="location" )
        #wstawienie wejśćia, którego nazwa jest na pocżątku pliku
        self.init = [self.in_region(self.lokacje[wejscie])]
        #wstawienie produktow do objects
        for i in self.trasa_ki["Nazwa Produktu"].drop_duplicates():
            [self.itemy[i]] = constants(i.replace(" ", "_").translate(trans), type_="item")
        #wstawienie polaczeń obszarow
        for i,j in zip(self.df_polaczenia_obszarow1["NAZWA_PRIMARY"],self.df_polaczenia_obszarow1["NAZWA_CONNECTED"]):
            self.init.append(self.connect_region(self.lokacje[i],self.lokacje[j]))
        #wstawienie przedmiotow na polki
        for i,j in zip(self.trasa_ki['Nazwa Sasiedniego Obszaru'],self.trasa_ki["Nazwa Produktu"]):
            self.init.append(self.from_region(self.lokacje[i],self.itemy[j]))
        #wstawianie kas
        for i in self.df_obszar_supermarketu1["NAZWA"][self.df_obszar_supermarketu1["NAZWA"].str.contains('KASA') == True]:
            self.init.append(self.kasa(self.lokacje[i]))
        #GOAL
        self.goal=[self.in_kasa()]
        for i in self.trasa_ki["Nazwa Produktu"].drop_duplicates():
            self.goal.append(self.in_backpack(self.itemy[i]))
        #najwazniejsze

        self.problem = Problem(
            "problem-1",
            domain=self.domain,
            objects=[self.lokacje[i] for i in self.lokacje]+[self.itemy[j] for j in self.itemy],
            init=self.init,
            goal=reduce(lambda a,b: a & b,self.goal)
        )
    def zapisz_problem_regionow(self):
        domain_path="./pddl1/domain.pddl"
        problem_path="./pddl1/problem.pddl"
        with open(f"{problem_path}", "w") as file:
            file.write(problem_to_string(self.problem).replace("\n    (:requirements :adl :strips :typing)",""))
            file.close()
        command = f'pyperplan {" ".join(dodatki)} {domain_path} {problem_path}'

        # Wykonaj polecenie za pomocą subprocess
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f'Błąd wykonania: {e}')
        pomniejszy_problem = open(f"{problem_path}.soln", "r")
        print("".join(pomniejszy_problem.readlines()))

    def odczyt_problemu(self,polecenia):
        lokacje={}
        itemy={}
        goal=[self.in_kasa()]
        init1=[]

        #wczytanie z ostatniego wersu move-to-region a b
        #wszystkie
        obszar_nazwa=self.df_obszar_supermarketu1[self.df_obszar_supermarketu1["NAZWA"].apply(lambda a: a.replace(" ", "_").translate(trans).lower())==polecenia[-1].split()[1].lower()]
        obszar_nazwa=obszar_nazwa["OBSZAR_ID"][obszar_nazwa.index[0]]
        kata=self.super_pola[self.super_pola['OBSZAR_ID_p'] == obszar_nazwa]
        #print(kata.to_string())
        tata = lambda a: a.replace("_", " ").replace("S", "Ś").lower() if ('WEJSCIE' in a) else (
            a.replace("_", " ").lower() if "KASA" in a else a)
        mama=lambda a: str(a).replace(" ","_").lower().translate(trans)
        #dodanie lokacji początkowych
        for i in kata["NAZWA_p"].apply(mama) :
            [lokacje[i]]=constants(i,type_="location" )

        #dodanie połączeń początkowych
        for i in ["_l", "_r", "_t", "_b"]:
            for k,j in enumerate(kata[f"NAZWA{i}"].apply(mama)):
                c=kata.index[k]
                if kata[f"OBSZAR_ID{i}"][c] == kata[f"OBSZAR_ID_p"][c] and kata[f"OBSZAR_ID{i}"][c]!=-1:
                    init1.append(self.connect_region(lokacje[j], lokacje[kata["NAZWA_p"][c].lower().replace(" ","_").translate(trans)]))

        if "move-to-region" in polecenia[-1]:
            #dodanie lokacji przyczepionego obszaru, wtym punktu wyjscia jako kasa i połączeń z istniejącymi regionami
            docelowa_nazwa=polecenia[-1].split()[2]
            docelowa_nazwa=self.df_obszar_supermarketu1[self.df_obszar_supermarketu1["NAZWA"].apply(lambda a: a.replace(" ", "_").translate(trans).lower())==docelowa_nazwa.lower()]
            docelowa_nazwa=docelowa_nazwa["OBSZAR_ID"][docelowa_nazwa.index[0]]
            wszystkie=kata[(kata["OBSZAR_ID_l"]==docelowa_nazwa)+(kata["OBSZAR_ID_r"]==docelowa_nazwa)+(kata["OBSZAR_ID_t"]==docelowa_nazwa)+(kata["OBSZAR_ID_b"]==docelowa_nazwa)]

            for i in ["_l","_r","_t","_b"]:
                if wszystkie[f"OBSZAR_ID{i}"][wszystkie.index[0]]==docelowa_nazwa:
                    for k,j in enumerate(wszystkie[f"NAZWA{i}"].apply(mama)):
                        c = wszystkie.index[k]
                        [lokacje[j]]=constants(j.replace(" ","_").translate(trans),type_="location" )
                        init1.append(self.kasa(lokacje[j]))
                        init1.append(self.connect_region(lokacje[wszystkie["NAZWA_p"].apply(mama)[c]],lokacje[j]))
                        init1.append(self.connect_region(lokacje[j], lokacje[wszystkie["NAZWA_p"].apply(mama)[c]]))
        elif "zaplac" in polecenia[-1]:
            init1.append(self.kasa(lokacje[tata(polecenia[-1].split()[-1])]))
        #dodanie punktu początkowego
        init1.append(self.in_region(lokacje[polecenia[0].split()[1]]))
        #dodanie itemow
        for i in range(1,len(polecenia)-1):
            t=polecenia[i].split()[1:]
            nazwa=tata(t[0])
            [itemy[t[1]]]=constants(t[1].replace(" ", "_").translate(trans), type_="item")
            goal.append(self.in_backpack(itemy[t[1]]))
            for naz in self.trasa_k[(self.trasa_k["Nazwa Sasiedniego Obszaru"].apply(mama) == nazwa) * (
                    self.trasa_k["Nazwa Produktu"].apply(mama) == t[1])][
                "Nazwa Sasiada"]:
                #print(naz,t[1])
                init1.append(self.from_region(lokacje[naz],itemy[t[1]]))

        problem2 = Problem(
            f"problem-{self.licznik_problemow}",
            domain=self.domain,
            objects=[lokacje[i] for i in lokacje] + [itemy[j] for j in itemy],
            init=init1,
            goal=reduce(lambda a, b: a & b, goal)
        )
        self.licznik_problemow+=1
        domain_path = 'pddl1/domain.pddl'
        problem_path = 'pddl1/problem1.pddl'
        with open(f"{problem_path}", "w") as file:
            file.write(problem_to_string(problem2).replace("\n    (:requirements :adl :strips :typing)",""))
            file.close()
        # Komenda do wykonania
        command = f'pyperplan {" ".join(dodatki)} {domain_path} {problem_path}'

        # Wykonaj polecenie za pomocą subprocess
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f'Błąd wykonania: {e}')
        pomniejszy_problem=open(f"{problem_path}.soln","r")
        pomniejszy_problem=[i.replace("(","").replace(")","").replace("\n","")for i in pomniejszy_problem.readlines()]

        #print("\n".join(pomniejszy_problem[:-1]))
        self.ostateczny_plik+=pomniejszy_problem[:-1]
        return pomniejszy_problem[-1].replace("zaplac", "in-region")

    def odczyt_regionow(self):
        fil=open("./pddl1/problem.pddl.soln","r")
        file=[i.replace("(","").replace(")","").replace("\n","")for i in fil.readlines()]
        k=[f"in-region {file[0].split()[1]}"]
        self.ostateczny_plik=[k[0]]
        z=len(file)
        for i,j in enumerate(file):
            if "move-to-region" in j or "zaplac" in j:
                k.append(j)
                print(k)
                k=[self.odczyt_problemu(k)]
            else:
                k.append(j)
        self.ostateczny_plik.append(k[0].replace("in-region","zaplac"))
        print("\n".join(self.ostateczny_plik))
        fil.close()
        d=open("./pddl1/ostateczny.txt","w")
        d.write("\n".join(self.ostateczny_plik))

domene_creator = DomeneRegionowCreator()
domene_creator.create_regions_domain()
domene_creator.zapisz_domene_regionow()
domene_creator.wczytaj_plik()
domene_creator.stworz_pddl_obszar()
domene_creator.zapisz_problem_regionow()
domene_creator.odczyt_regionow()
