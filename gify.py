import imageio
import numpy as np
from PIL import Image
import subprocess
import pandas as pd
trans = str.maketrans('ąćęłńóśźżĄĆĘŁŃÓŚŹŻ', 'acelnoszzACELNOSZZ')
shapes=np.array(Image.open('./img/pola.png')).shape
#print(shapes[19,31])
numery=0
#(20, 32, 4)
def create_page(page,t,y=None,x=None,wym=None,obrazek=None):
    page=page.copy()
    if t==True:
        wym = (int(wym[0]), int(wym[1]))
        y = int(y * wym[0])
        x = int(x * wym[1])
        page[y:y+wym[0],x:x+wym[1]]= page[y:y+wym[0],x:x+wym[1],:]*np.repeat((obrazek[:,:,3]!=255)[:,:,np.newaxis], 4, axis=2)+obrazek*np.repeat((obrazek[:,:,3]==255)[:,:,np.newaxis], 4, axis=2)
    else:
        return page
    return page
def create_gif():
    # Wczytaj obraz wynikowy z poprzedniego programu
    obraz_wynikowy = np.array(Image.open('./img/obraz_wynikowy.png'))
    wymiary=np.array(obraz_wynikowy).shape
    wymiary=(wymiary[0]/shapes[0], wymiary[1]/shapes[1])
    slownik_obiektow={}
    for i in ("kasy","wejścia"):
        df = pd.read_csv(f'./mapa/{i}.csv')
        df_unique = df.drop_duplicates(subset='Nazwa Pola')
        df_unique.loc[:, "Nazwa Pola"] = df_unique["Nazwa Pola"].apply(lambda a: a.translate(trans).lower().replace(" ", "_"))
        slownik_obiektow.update(df_unique.set_index('Nazwa Pola')['Pole Id'].to_dict())
    file=open("./pddl1/ostateczny.txt")
    file=list(map(lambda a: a.replace("\n",""), file.readlines()))
    file=list(map(lambda a: a.split(),file))
    td=lambda b:(lambda a: f"p_{int(a[:4])}_{a[4:]}" )(str(slownik_obiektow[b]).zfill(8)) if b in slownik_obiektow else b
    pages=[]
    obrazki=[np.array(Image.open('./img/koszyk.png')),np.array(Image.open('./img/money.png'))]
    for i in file:
        if i[0]=="in-region":
            k=td(i[1]).split("_")
            pages.append(create_page(obraz_wynikowy,True,int(k[1]),int(k[2]),wymiary,obrazki[0]))
        elif i[0]=="move-to-region":
            k = td(i[2]).split("_")
            pages.append(create_page(obraz_wynikowy, True, int(k[1]), int(k[2]), wymiary, obrazki[0]))
        elif i[0]=="take-to-backpack":
            k = td(i[1]).split("_")
            for i in range(3):
                pages.append(create_page(obraz_wynikowy,False))
                pages.append(create_page(obraz_wynikowy,True,int(k[1]),int(k[2]),wymiary,obrazki[0]))
        elif i[0]=="zaplac":
            k = td(i[1]).split("_")
            for i in range(3):
                pages.append(create_page(obraz_wynikowy,False))
                pages.append(create_page(obraz_wynikowy,True,int(k[1]),int(k[2]),wymiary,obrazki[1]))
    gif_path = './img/przejazd.gif'
    imageio.mimsave(gif_path, pages, duration=500)
    try:
        subprocess.run(f"magick {gif_path} -coalesce -duplicate 1,-1 -quiet -layers OptimizePlus -loop 0 {gif_path}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Błąd wykonania: {e}')
if __name__ == "__main__":
    create_gif()
