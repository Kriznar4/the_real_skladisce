import modeli


MAX_REZULTATOV_ISKANJA = 15


def izberi_moznost(moznosti):
    """
    Funkcija, ki izpiše seznam možnosti in vrne indeks izbrane možnosti.

    Če na voljo ni nobene možnosti, izpiše opozorilo in vrne None.
    Če je na voljo samo ena možnost, vrne 0.

    >>> izberi_moznost(['jabolko', 'hruška', 'stol'])
    1) jabolko
    2) hruška
    3) stol
    Vnesite izbiro > 2
    1
    >>> izberi_moznost([])
    >>> izberi_moznost(['jabolko'])
    0
    """

    if len(moznosti) == 0:
        return
    elif len(moznosti) == 1:
        return 0
    else:
        for i, moznost in enumerate(moznosti, 1):
            print('{}) {}'.format(i, moznost))

        st_moznosti = len(moznosti)
        while True:
            izbira = input('Vnesite izbiro > ')
            if not izbira.isdigit():
                print('NAPAKA: vnesti morate število')
            else:
                n = int(izbira)
                if 1 <= n <= st_moznosti:
                    return n - 1
                else:
                    print('NAPAKA: vnesti morate število med 1 in {}!'.format(
                        st_moznosti))

def novo_narocilo():
    """
    """
    return

def iz_skladisca():
    """
    """
    iskani= input('Vnesi ime izdelka, ki si vzel iz skladisca: \n')
    izdelki = 



    return
def izberi_izdelek():
    """
    
    """



def skladisce():
    """
    Izpiše kaj imamo v skladišču
    """
    skladisce = modeli.podatki_skladisca()

    print('Vaše skladišče izgleda takole: \n')
    for izdelek in skladisce:
        sifra, ime, velikost_pakiranja, enota, kolicina, tip_izdelka = izdelek
        if velikost_pakiranja is None:
            enota = ''
            velikost_pakiranja = ''
        elif enota is None:
            enota = ''
        if tip_izdelka is None:
            tip_izdelka = 'Brez tipa'

        print('|  Šifra: {}  |  Izdelek: {} {}{}  |   Količina: {}  |   Tip izdelka: {}  |'.format(sifra, ime, velikost_pakiranja, enota, kolicina, tip_izdelka))
    return

def neprejete_posilke():
    """
    """
    return


def pokazi_moznosti():
    print(50 * '-')
    izbira = izberi_moznost([
        'Novo naročilo',
        'Porabil iz skladišča',
        'Pokaži skladišče',
        'Prikaži neprejete pošilke',
        'izhod',
    ])
    if izbira == 0:
        novo_narocilo()
    elif izbira == 1:
        iz_skladisca()
    elif izbira == 2:
        skladisce()
    elif izbira == 3:
        neprejete_posilke()
    else:
        print('Nasvidenje!')
        exit()
        


def main():
    print('Pozdravljeni v evidenci naročil!')
    while True:
        pokazi_moznosti()


main()
