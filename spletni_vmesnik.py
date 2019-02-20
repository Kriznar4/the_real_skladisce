import bottle
from bottle import get, run, template, post, redirect, request
import modeli

moznosti = ['poglej skladišče', 'novo narocilo', 'preglej neprejete pošiljke', 
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

#@post('/poglej-skladišče/')
#def dodajanje_filma():
#    try:
#        id = modeli.dodaj_film(naslov=request.forms.naslov,
#                               dolzina=request.forms.dolzina,
#                               leto=request.forms.leto,
#                               ocena=request.forms.ocena,
#                               metascore=request.forms.metascore,
#                               glasovi=request.forms.glasovi,
#                               zasluzek=request.forms.zasluzek,
#                               opis=request.forms.opis,
#                               zanri=request.forms.getall('zanri'),
#                               igralci=request.forms.getall('igralci'),
#                               reziserji=request.forms.getall('reziserji'))
#    except:
#        zanri = modeli.seznam_zanrov()
#        osebe = modeli.seznam_oseb()
#        return template('dodaj_film',
#                        naslov=request.forms.naslov,
#                        dolzina=request.forms.dolzina,
#                        leto=request.forms.leto,
#                        ocena=request.forms.ocena,
#                        metascore=request.forms.metascore,
#                        glasovi=request.forms.glasovi,
#                        zasluzek=request.forms.zasluzek,
#                        opis=request.forms.opis,
#                        zanri=request.forms.getall('zanri'),
#                        igralci=request.forms.getall('igralci'),
#                        reziserji=request.forms.getall('reziserji'),
#                        vsi_zanri=zanri,
#                        vse_osebe=osebe,
#                        napaka=True)
#    redirect('/film/{}/'.format(id))

    
    








run(reloader=True, debug=True)