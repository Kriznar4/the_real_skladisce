import bottle
from bottle import get, run, template, post, redirect, request
import modeli

moznosti = ['poglej skladišče', 'novo narocilo', 'preglej neprejete pošiljke', 
            'vpisi prejeto posiljko', 'spremeni količino izdelka v skladišču', 
            'letni pregled porabe']

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
        ime = "",
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
            ime=request.forms.ime,
            kolicina=request.forms.kolicina,
            sporocilo="Nekaj ni šlo skozi! Mogoče si želel iz skladišča vzeti več izdelkov kot jih imaš! <br>"
            )
    redirect('/spremeni količino izdelka v skladišču/')

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