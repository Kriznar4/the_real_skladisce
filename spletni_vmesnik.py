import bottle
from bottle import get, run, template, post, redirect, request
import modeli

moznosti = ['poglej skladišče','dodaj izdelek', 'novo narocilo', 'preglej neprejete pošiljke', 
            'vpisi prejeto posiljko', 'spremeni količino izdelka v skladišču', 
            'letni pregled porabe', 'najdi izdelek']

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
    imena_izdelkov = modeli.imena_izdelkov()
    st_zadnjega_narocila=modeli.vrni_sifra_zadnje_narocilo()
    return template('novo_narocilo',
                    imena= imena_izdelkov,
                    st_narocila=st_zadnjega_narocila+1,
                    sifra=None,
                    kolicina=0,
                    cena=None,
                    popust=None
                    )


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

run(reloader=True, debug=True)