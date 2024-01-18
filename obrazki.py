import numpy as np
from PIL import Image

def sklej_obrazki():
    # Wczytaj obraz z polami
    pola_img = Image.open('./img/pola.png')
    pola_img_hsv = np.array(pola_img.convert('HSV'))

    # Definicja legenda
    pola_legenda = {
        0: "PO",
        350: "P",
        123: "WE",
        179: "PD",
        227: "KA",
        44: "MG"
    }

    # Stwórz pustą tablicę wynikową
    szerokosc, wysokosc = pola_img.size
    ii, jj = Image.open('./img/PO.png').size
    wynikowa_tablica = np.zeros((wysokosc*ii, szerokosc*jj, 4), dtype=np.uint8)
    print(np.round(pola_img_hsv[:, :, 0] / 255.0 * 360))
    # Iteruj po polach legendy
    for hue, nazwa in pola_legenda.items():
        # Odczytaj obrazek z pliku
        obrazek_path = f'./img/{nazwa}.png'
        obrazek = np.array(Image.open(obrazek_path))

        # Ustal rozmiar obszaru na podstawie atrybutu shapes
        obszar_szerokosc, obszar_wysokosc,_= obrazek.shape

        # Wybierz piksele z pola o danym HUE
        maska = (np.round(pola_img_hsv[:, :, 0]/255.0*360) == hue)

        # Pobierz indeksy pikseli w polu
        indeksy_pola = np.argwhere(maska)

        # Iteruj po indeksach pikseli w polu i wstaw obszar z obrazka
        for indeks_pola_x, indeks_pola_y in indeksy_pola:
            obszar_x = indeks_pola_x * obszar_szerokosc
            obszar_y = indeks_pola_y * obszar_wysokosc
            wynikowa_tablica[obszar_x:obszar_x+obszar_szerokosc, obszar_y:obszar_y+obszar_wysokosc, :4] = obrazek

    # Stwórz obraz PIL z tablicy wynikowej
    obraz_wynikowy = Image.fromarray(wynikowa_tablica)

    # Zapisz obraz wynikowy
    obraz_wynikowy.save('./img/obraz_wynikowy.png')

if __name__ == "__main__":
    sklej_obrazki()