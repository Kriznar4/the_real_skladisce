import bottle
from bottle import get, run, template
import modeli

moznosti = ['poglej-skladišče', 'novo narocilo', 'preglej neprejete pošiljke', 
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

@get('/poglej-skladišče/')
def poglej_skladisce():
    izdelki = modeli.podatki_skladisca()
    lastnosti = ['ID', 'Ime', 'Zaloga', 'Tip']
    return template(
        'pokazi_skladisce',
        lastnosti = lastnosti,
        izdelki = izdelki
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

@get(/spr-kolicino/)    
def spremeni_kolicino():
    return template(
        'spr-kolicino'
    )
    
    








run(reloader=True, debug=True)