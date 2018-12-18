import modeli
import datetime


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
    vnos_ime_partnerja = input("Vnesi ime parnerja: ")
    moznosti_partner = modeli.partnerji_podatki(modeli.poisci_partner(vnos_ime_partnerja))
    izbira_partner = izberi_moznost(moznosti_partner)
    if izbira_partner is None:
        modeli.nov_partner(vnos_ime_partnerja)
        sifra = modeli.poisci_partner(vnos_ime_partnerja)
        izbrani_partner = modeli.partnerji_podatki(sifra)
    else:
        izbrani_partner = moznosti_partner[izbira_partner]
    sifra_partner = izbrani_partner[0]


    vnos_datum_narocila = input('Vnesi datum narocila (mm/dd/yy) ali pritisni enter za današnji dan: ')
    if vnos_datum_narocila =='':
        vnos_datum_narocila = datetime.datetime.now().strftime("%m/%d/%Y")
    vnos_komentar = input('Vnesi komentar naročila: ')
    if vnos_komentar == '':
        vnos_komentar = None
    modeli.novo_narocilo(vnos_datum_narocila, sifra_partner, vnos_komentar)
    st_narocila = modeli.vrni_sifra_zadnje_narocilo()
    print('---------------{}'.format(st_narocila))


    
    ali_nadaljujem = 1
    while ali_nadaljujem:
        vnos_ime_izdelka = input("Vnesi ime izdelka: ")
        moznosti_izdelek = modeli.izdelki_podatki(modeli.poisci_izdelek(vnos_ime_izdelka))
        izbira_izdelka = izberi_moznost(moznosti_izdelek)
        if izbira_izdelka is None:
            v_skladisce = izberi_moznost(['Izdelek bo v skaldišču.', 'Izdelka ne bo v skladišču.'])
            if v_skladisce == 0:
                kolicina = 0
            else:
                kolicina = None
            opis = input('Dodaj opis izdelka: ')
            tip_izdelka = input('Dodaj tip izdelka: ')
            opomnik = input('Dodaj opomnik: ')
            modeli.nov_izdelek(vnos_ime_izdelka, None, None, kolicina, opis, tip_izdelka, opomnik)
            sifra = modeli.poisci_izdelek(vnos_ime_izdelka)
            izbrani_izdelek = modeli.izdelki_podatki(sifra)[0]
        else:
            izbrani_izdelek = moznosti_izdelek[izbira_izdelka]
        sifra_izdelka = izbrani_izdelek[0]
        print('---------------{}'.format(sifra_izdelka))

        kolicina = input('Koliko paketov izdelka bomo kupili: ')
        cena = input('Kolikšna je cena enega paketa: ')
        popust = input('Popust v procentih: ')
        datum_prejetja = input('Vnesi datum prejetja (mm/dd/yy) ali pritisni enter če izdelka še nisi prejel: ')
        if datum_prejetja == '':
            datum_prejetja = None
        modeli.nov_izdelek_v_kosarico(st_narocila,sifra_izdelka,cena,popust,kolicina,datum_prejetja)


        ali_nadaljujem = izberi_moznost(['Nimam več izdelkov.', 'Dodaj nov izdelek.'])

    return

def iz_skladisca():
    """
    Odšteje količino izdelka, ki smo ga vzeli iz skladišča
    """
    iskani = input('Vnesi ime izdelka, ki si vzel iz skladisca: \n')
    izbira = izberi_moznost(moznosti)
    izbrani = moznosti[izbira]
    print("spremenili boste količino izdelka: " + str(izbrani))
    v_skladiscu = izbrani[4]
    koliko = int(input('Koliko pakiranj si vzel iz skladišča: '))
    if koliko > v_skladiscu:
        print("Toliko izdelkov ni nikoli bilo v skladišču!! V skladišču je bilo toliko izdelkov: {}.".format(v_skladiscu))
        return
    nova_kolicina = v_skladiscu-koliko
    modeli.posodobitev_v_skladišču(izbrani[0], nova_kolicina)
    opomnik = izbrani[-1]
    if nova_kolicina < opomnik:
        print("OPOMNIK: Količina vašega izdelka vam je padla pod {}. Imate samo še {} paketov izdelka.\n Naroči si izdelek.".format(opomnik, nova_kolicina))
    return
    

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

