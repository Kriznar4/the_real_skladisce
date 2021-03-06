import bottle
from bottle import get, run, template, post, redirect, request, response
import modeli

moznosti = ['poglej skladišče',
            'dodaj izdelek', 
            'novo narocilo', 
            'preglej neprejete pošiljke', 
            'spremeni količino izdelka v skladišču', 
            'letni pregled porabe', 
            'najdi izdelek']


@get('/')
def glavna_stran():
    izbire = [
        (izbira, '/{}/'.format(izbira)) 
        for izbira in moznosti
    ]
    return template(
        'glavna_stran',
        izbire = izbire,
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
    imena_izdelkov=modeli.imena_izdelkov()
    izdelki = modeli.podatki_skladisca()
    lastnosti = ['ID', 'Ime', 'Zaloga', 'Tip']
    sporocilo = "<br>"
    return template(
        'spr_kolicino',
        imena=imena_izdelkov,
        lastnosti = lastnosti,
        izdelki = izdelki,
        id = "",
        kolicina = 0,
        sporocilo = sporocilo
    )

@post('/spremeni količino izdelka v skladišču/')
def spremenjanje_skladisce():
    imena_izdelkov=modeli.imena_izdelkov()
    izdelki = modeli.podatki_skladisca()
    lastnosti = ['ID', 'Ime', 'Zaloga', 'Tip']
    try:
        modeli.posodobitev_v_skladišču(request.forms.id,
                                       request.forms.kolicina)
    except:
        return template(
            'spr_kolicino',
            imena=imena_izdelkov,
            lastnosti = lastnosti,
            izdelki = izdelki,
            id=request.forms.id,
            kolicina=request.forms.kolicina,
            sporocilo="V skladišču ni bilo toliko izdelkov! <br>"
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
    try:
        izdelki2 = modeli.izdelki_podatki(modeli.poisci_izdelek(request.forms.ime))
        izdelki = [[lastn for lastn, st in zip(izdelek, [0, 1, 2, 3, 4, 5]) if st in [0, 1, 2, 4] ] for izdelek in izdelki2]
        return template(
        'najdi_izdelek',
        lastnosti = lastnosti,
        izdelki = izdelki,
        ime = request.forms.ime
    )
    except:
        redirect('/najdi izdelek/')

def zapakiraj(tab):
    return '$$$'.join(['###'.join(str(l) for l in el) for el in tab])

def razpakiraj(niz):
    return [niz2.split('###') for niz2 in niz.split('$$$')]

@get('/novo narocilo/')
def dodaj_narocilo():
    if request.get_cookie("kosarica") == None:
        response.set_cookie("kosarica", "", path='/')
        niz = ""
    else:
        niz = request.get_cookie("kosarica")
    seznam_izdelki=razpakiraj(niz)
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

@post('/novo narocilo/')
def dodajanje_narocilo():
    if request.get_cookie("kosarica") == None:
        response.set_cookie("kosarica", "", path='/')
        niz = ""
    else:
        niz = request.get_cookie("kosarica")
    seznam_izdelki=razpakiraj(niz)
    sifra_izbranega=request.forms.izbran
    nov_izdelek=(sifra_izbranega,modeli.ime_izdelka_iz_sifre(sifra_izbranega)[0],request.forms.kolicina,request.forms.cena,request.forms.popust)
    seznam_izdelki.append(nov_izdelek)
    response.set_cookie("kosarica", zapakiraj(seznam_izdelki), path='/')
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

@post('/ne oddaj narocila/')
def ne_oddaj():
    response.set_cookie("kosarica", "", path='/')
    redirect('/')

@post('/novo narocilo2/')
def dodajanje_narocilo():
    redirect('/koncaj narocilo/')

@post('/vrnime na prvo stran/')
def vrni():
    redirect('/')

@get('/koncaj narocilo/')
def koncaj_narocilo():
    if request.get_cookie("kosarica") == None:
        response.set_cookie("kosarica", "", path='/')
        niz = ""
    else:
        niz = request.get_cookie("kosarica")
    seznam_izdelki=razpakiraj(niz)
    lastnosti=["sifra","ime","kolicina","cena","popust"]
    partnerji=modeli.imena_partnerjev()
    return template('koncaj_narocilo',
                    part=partnerji,
                    izbran_partner="",
                    lastnosti = lastnosti,
                    sez_izdelkov=seznam_izdelki,
                    opis="")

@post('/koncaj narocilo/')
def dokoncaj_narocilo():
    izbran_partner=request.forms.izbran_partner
    opis=request.forms.opis

    modeli.v_narocila(izbran_partner,opis)
    lastnosti=["sifra","ime","kolicina","cena","popust"]
    if request.get_cookie("kosarica") == None:
        response.set_cookie("kosarica", "", path='/')
        niz = ""
    else:
        niz = request.get_cookie("kosarica")
    seznam_izdelki=razpakiraj(niz)[1:]
    seznam_idjev=list()

    st_naro=modeli.vrni_sifra_zadnje_narocilo()
    for izdelek in seznam_izdelki:
        seznam_idjev.append(int(izdelek[0]))
        modeli.nov_izdelek_v_kosarico(st_naro,izdelek[0],izdelek[3],izdelek[4],izdelek[2])
    modeli.posodobitev_ponudbe(izbran_partner,seznam_idjev)
    response.set_cookie("kosarica", "", path='/')

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
        kolicina = request.forms.kolicina
        if not kolicina:
            kolicina = None
        modeli.nov_izdelek(request.forms.ime,
                                kolicina,
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
    leto = request.forms.leto
    izdelki = modeli.vrni_letno(leto)

    return template(
        'pokazi_porabo',
        tip_lastnosti = kateri_podatki,
        izdelki = izdelki,
        leto = leto
    )

@get('/preglej neprejete pošiljke/')
def neprejete_posiljke():
    izdelki = modeli.neprejete()
    tipi_lastnosti = ["Nastavi enak datum", "Številka naročila", "Šifra izdelka", "Ime izdelka", 
    "Količina", "Šifra partnerja", "Ime partnerja", "Datum naročila"]
    
    return template(
        'neprejete', 
        tipi_lastnosti = tipi_lastnosti,
        izdelki = izdelki,
        dan = None,
        mesec = None,
        leto = None

    )

@post('/preglej neprejete pošiljke/')
def neprejete_posiljke_post():
    izdelki = modeli.neprejete()
    tipi_lastnosti = ["Nastavi enak datum", "Številka naročila", "Šifra izdelka", "Ime izdelka", 
    "Količina", "Šifra partnerja", "Ime partnerja", "Datum naročila"]
    obklukani = list()
    dan = request.forms.dan
    mesec = request.forms.mesec
    leto = request.forms.leto
    for i in range(len(izdelki)):
        if request.forms.get(str(i)) == 'on':
            modeli.datum_prejetja(dan, mesec, leto, izdelki[i][1], izdelki[i][0])
    return template(
        'neprejete', 
        tipi_lastnosti = tipi_lastnosti,
        izdelki = modeli.neprejete(),
        dan = None,
        mesec = None,
        leto = None

    )

run(reloader=True, debug=True)