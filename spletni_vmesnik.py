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
    lastnosti = ['ID: ', 'Ime: ', 'Količina pakiranja: ',  'Enota pakiranja: ', 'Zaloga: ', 'Tip: ']
    seznam_nizov = list()
    for izdelek in izdelki:
        niz = '|'
        for i in range(len(lastnosti)):
            niz = niz + str(lastnosti[i]) + str(izdelek[i]) + '|'
        seznam_nizov.append(niz)
    return template(
        'pokazi_skladisce',
        izdelki = seznam_nizov
    )

    









run(reloader=True, debug=True)