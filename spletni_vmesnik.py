import bottle
from bottle import get, run, template, post, redirect, request
import modeli

moznosti = ['poglej skladišče','dodaj izdelek', 'novo narocilo', 'preglej neprejete pošiljke', 
            'vpisi prejeto posiljko', 'spremeni količino izdelka v skladišču', 
            'letni pregled porabe', 'najdi izdelek']

seznam_izdelkov_v_kosarici = list()

@get('/')
def glavna_stran():
    izbire = [
        (izbira, '/{}/'.format(izbira)) 
        for izbira in moznosti
    ]
    return template(
        'glavna_stran',
        izbire = izbire
    )

@get('/poglej skladišče/')
def poglej_skladisce():
    izdelki = modeli.podatki_skladisca()
    lastnosti = ['ID', 'Ime', 'Zaloga', 'Tip']
    return template(
        'pokazi_skladisce',
        lastnosti = lastnosti,
        izdelki = izdelki
    )

@get('/spremeni količino izdelka v skladišču/')
def spremeni_skladisce():
    izdelki = modeli.podatki_skladisca()
    lastnosti = ['ID', 'Ime', 'Zaloga', 'Tip']
    sporocilo = "<br>"
    return template(
        'spr_kolicino',
        lastnosti = lastnosti,
        izdelki = izdelki,
        id = "",
        kolicina = 0,
        sporocilo = sporocilo
    )

@post('/spremeni količino izdelka v skladišču/')
def spremenjanje_skladisce():
    izdelki = modeli.podatki_skladisca()
    lastnosti = ['ID', 'Ime', 'Zaloga', 'Tip']
    try:
        modeli.posodobitev_v_skladišču(request.forms.id,
                                       request.forms.kolicina)
    except:
        return template(
            'spr_kolicino',
            lastnosti = lastnosti,
            izdelki = izdelki,
            id=request.forms.id,
            kolicina=request.forms.kolicina,
            sporocilo="Nekaj ni šlo skozi! <br>"
            )
    redirect('/spremeni količino izdelka v skladišču/')

@get('/najdi izdelek/')
def poglej_skladisce():
    lastnosti = ['ID', 'Ime', 'Zaloga', 'Tip']
    izdelki = list()
    return template(
        'najdi_izdelek',
        lastnosti = lastnosti,
        izdelki = izdelki,
        ime = ""
    )

@post('/najdi izdelek/')
def poglejte_skladisce():
    lastnosti = ['ID', 'Ime', 'Zaloga', 'Tip']
    izdelki2 = modeli.izdelki_podatki(modeli.poisci_izdelek(request.forms.ime))
    izdelki = [[lastn for lastn, st in zip(izdelek, [0, 1, 2, 3, 4, 5]) if st in [0, 1, 2, 4] ] for izdelek in izdelki2]
    return template(
        'najdi_izdelek',
        lastnosti = lastnosti,
        izdelki = izdelki,
        ime = request.forms.ime
    )

@get('/novo narocilo/')
def dodaj_narocilo():
    seznam_izdelki=seznam_izdelkov_v_kosarici
    lastnosti=["sifra","ime","kolicina","cena","popust"]
    imena_izdelkov = modeli.imena_izdelkov()
    st_zadnjega_narocila=modeli.vrni_sifra_zadnje_narocilo()
    return template('novo_narocilo',
                    imena= imena_izdelkov,
                    sifra="",
                    ime="",
                    kolicina="",
                    cena=None,
                    popust=None
    )
                    
@post('/novo narocilo/')
def dodajanje_narocilo():
    seznam_izdelkov=seznam_izdelkov_v_kosarici
    sifra_izbranega=request.forms.izbran
    nov_izdelek=(sifra_izbranega,modeli.ime_izdelka_iz_sifre(sifra_izbranega)[0],request.forms.kolicina,request.forms.cena,request.forms.popust)
    seznam_izdelkov.append(nov_izdelek)
    print(seznam_izdelkov)
    lastnosti=["sifra","ime","kolicina","cena","popust"]
    imena_izdelkov = modeli.imena_izdelkov()
    st_zadnjega_narocila=modeli.vrni_sifra_zadnje_narocilo()
    return template('novo_narocilo2',
                    lastnosti=lastnosti,
                    sez_izdelkov=seznam_izdelkov,
                    imena= imena_izdelkov,
                    sifra="",
                    ime="",
                    kolicina="",
                    cena=None,
                    popust=None
                    )
    


@get('/novo narocilo2/')
def dodaj_narocilo():
    seznam_izdelki=seznam_izdelkov_v_kosarici
    lastnosti=["sifra","ime","kolicina","cena","popust"]
    imena_izdelkov = modeli.imena_izdelkov()
    st_zadnjega_narocila=modeli.vrni_sifra_zadnje_narocilo()
    return template('novo_narocilo2',
                    lastnosti=lastnosti,
                    sez_izdelkov=seznam_izdelki,
                    imena= imena_izdelkov,
                    sifra="",
                    ime="",
                    kolicina="",
                    cena=None,
                    popust=None
    )
                    
@post('/novo narocilo2/')
def dodajanje_narocilo():
    redirect('/koncaj narocilo/')

@get('/koncaj narocilo/')
def koncaj_narocilo():
    lastnosti=["sifra","ime","kolicina","cena","popust"]
    seznam_izdelkov=seznam_izdelkov_v_kosarici
    return template('koncaj_narocilo',
                    lastnosti = lastnosti,
                    sez_izdelkov=seznam_izdelkov)

@post('/koncaj narocilo/')
def koncaj_narocilo():
    lastnosti=["sifra","ime","kolicina","cena","popust"]
    seznam_izdelkov=seznam_izdelkov_v_kosarici
    print(seznam_izdelkov)
    sifra_narocila=modeli.vrni_sifra_zadnje_narocilo()+1
    for izdelek in seznam_izdelkov_v_kosarici:
        try: 
            modeli.nov_izdelek_v_kosarico(sifra_narocila,izdelek[0],izdelek[3],izdelek[2],izdelek[4])
            seznam_izdelkov_v_kosarici=list()
        except:
            seznam_izdelkov_v_kosarici=list()
            return template('koncaj_narocilo',
                    lastnosti = lastnosti,
                    sez_izdelkov=seznam_izdelkov)
    redirect('/')



@get('/dodaj izdelek/')
def dodaj_izdelek():
    tipi = modeli.tipi_izdelkov()
    return template('dodaj_izdelek',
                    ime="",
                    kolicina=0,
                    tip_izdelka="",
                    tipi_izdelkov=tipi,
                    opis="",
                    opomnik=0)

@post('/dodaj izdelek/')
def dodaj_izdelek():
    try:
        modeli.nov_izdelek(request.forms.ime,
                                request.forms.kolicina,
                                request.forms.opis,
                                request.forms.tip_izdelka,
                                request.forms.opomnik)
    except:
        tipi = modeli.tipi_izdelkov()
        return template('dodaj_izdelek',
                        ime="",
                        kolicina=0,
                        tip_izdelka="",
                        tipi_izdelkov=tipi,
                        opis="",
                        opomnik=0)
    redirect('/')

@get('/letni pregled porabe/')
def letni_pregled():
    leta = modeli.vrni_leta()
    
    return template(
        'letni_pregled',
        leta=leta,

    )

@post('/letni pregled porabe/')
def letni_pregled_podatkov():
    kateri_podatki = ["ID", "Ime", "Letna poraba za nabavo", "Povprečna cena na 1 izdelek"]
    podatki = 
    leto = int(request.forms.value)

    return template(
        'najdi_izdelek',
        lastnosti = lastnosti,
        izdelki = izdelki,
        ime = request.forms.ime
    )

run(reloader=True, debug=True)