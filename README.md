# InterdisciplinaryStudentProject
Interdisciplinary Student Project Integrating Database Programming, PDDL-Based Artificial Intelligence, and Embedded Systems."
Podsumowanie dla cv:
Projekt ten zdał 3 przedmioty:
1. Bazy Danych (5).
2. Systemy wbudowane(4.5).
3. Sztuczna inteligencja(3.5).  
Założenia:  
Stworzyć w Oracle Apex serwer(1), który posługując się językiem python, będzie wykorzystywał sztuczną inteligencję napisaną w Planning Domain Definition Language zawartą w bibliotece pyperplan(3).  
Następnie wizualizacja w formie generatora filmów lub gifów oraz z wykorzystaniem manipulatora(2).  
Baza danych miała zawierać podstawowe dane sklepu, takie jak informacje o pracownikach, półkach, regałach, produktach i ich położeniu w sklepie.  
Podstawowymi plikami generującymi bazę danych, były dwa pliki graficzne. Na jednym kolorami oznaczone były kasy, regały, wejścia, magazyn i pola dostępu do regału. Na drugim były zaznaczone obszary, z których można przejść do innych obszarów.  
Było to podyktowane tym, by generowanie problemu w pddl było dwustopniowe.  
Są dwa problemy  w sklepie, jakie miałybyć rozwiązywane przez SI i oba są dwustopniowe. W jednym klient wpisuje towary do bazy danych, które chce kupić i otrzymuje trasę, wygenerowaną jako rozwiązanie problemu w pddl, od wejścia, przez produkty do kasy.  
W drugim pracownik odpowiedzialny otrzymuje trasę, by uzupełnić braki w produktach, które są przypisane do konkretnych półek, maszerując z magazynu, przez wszystkie półki zawierające dany towar do uzupełnienia i wraca do magazynu na koniec.  
Stopnie.  
W pierwszym stopniu generowany problem w pddl polegał na przejściu po sklepie między obszarami, podniesieniu/położeniu produktów i marszu do obszaru końcowego końcowego (obszaru z kasą/magazynem).  
W drugim stopniu- każde przejście po obszarze, było zamieniane na pola, bo obszar składał się z pól. Zastosowanie tego, to rozbicie problemu dużego na małe problemy. Gdyby całość sklepu była zawarta w jednym rysunku, to generowany problem w pddl, miałby bardzo dużo wierzchołków. Przeglądanie takiego grafu wszerz, generowałoby strasznie długi czas rozwiązywania, lub całkowite posypanie się solvera. Przeszukiwanie wszerz bez heurystyki generuje optymalną trasę, ale to nie jest w sumie sztuczna inteligencja, za co została obniżona ocena z tego przedmiotu.
  
  
Co udało się wykonać:  
1. Generator bazy danych z rysunków, które były zamieniane na csv i absorbowane przez Oracle Apex.  
2. Nie dało się stworzyć serwera z pythonem w obszarze roboczym oracle, co było pokazywane na tutorialach, ze względu na ograniczenia wersji studenckiej.  
3. Wszystko zostało zastąpione przesyłaniem plików, csv i xlsx.  
4. Aby stworzyć bazę danych obszarów, półek, należy załadować dwa rysunki: [Pola](./img/pola.png) [Obszary](./img/obszary.png).  
5. Następnie program [Interpretator](./interpretator.py), dokonuje konwersji rysunków na bazę danych w xlsx [baza](./baza_danych.xlsx).  
6. W oracle apex można było umieścić produkty na półki. Standardowo generator ustawiał wszędzie liczbę półek na 3 w każdym regale. Po umieszczeniu produktów na półki można było stworzyć trasę dla klienta, trasa dla magazyniera, czyli problem drugi został jedynie opracowany dla bazy danych, ale nie powstał żaden program, który by tworzył wizualizację dla pracownika.  
7. Po wybraniu trasy, apex, dawał do ściągnięcia 3 pliki: [pliki](./mapa/)  
8. W plikach były informacje o możliwej aktualizacji kas i wejść, jeżeli edytowaliby to potencjalni pracownicy sklepu, ale ostatecznie, dałem także możliwość pobrania baza_danych.xlsx, jako całości z oracle apex, więc pliki były generowane niepotrzebnie. Najważniejszy plik to [trasa](./mapa/trasa_dla_produktow.csv)  
9. mając do dyspozycji trasę, ikony koszyka i elementów sklepu można za pomocą plików [sklep](./obrazki.py), [trasa](route-creator.py), [wizualizacja](gify.py), oraz wymienionych wcześniej plików xlsx i csv, można stworzyć:  
9.1. pliki [pddl](./pddl1/), które są niezbędne dla tworzenia ruchów robota w arduino.  
9.2. podgląd sklepu - [obraz wynikowy](./img/obraz_wynikowy.png)  
9.3. wizualizację trasy [przejazd](./img/przejazd.gif)  
10. Całość można zobaczyć w filmach zamieszczonych poniżej.  
[filmy](https://drive.google.com/drive/folders/1RLVU0IjVzTDQKjDrKzV0_8MW3ztkj7lE?usp=sharing)  
Jak widać manipulator, składający się z dwóch silników serwo, ma niestety dokładność do 1 stopnia w obu stopniach swobody, co nie pozwala na precyzyjne celowanie laserem, a na mniej więcej +/- 1,5 pola w najgorszym miejscu, czyli na samej górze.
