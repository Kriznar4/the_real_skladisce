import sqlite3
import baza
import datetime

conn = sqlite3.connect('evidenca_narocil.db')
baza.ustvari_bazo_ce_ne_obstaja(conn)
conn.execute('PRAGMA foreign_keys = ON')

def commit(fun):
    """
    Dekorator, ki ustvari kurzor, ga poda dekorirani funkciji,
    in nato zapiše spremembe v bazo.

    Originalna funkcija je na voljo pod atributom nocommit.
    """
    def funkcija(*largs, **kwargs):
        ret = fun(conn.cursor(), *largs, **kwargs)
        conn.commit()
        return ret
    funkcija.__doc__ = fun.__doc__
    funkcija.__name__ = fun.__name__
    funkcija.__qualname__ = fun.__qualname__
    fun.__qualname__ += '.nocommit'
    funkcija.nocommit = fun
    return funkcija

def koliko_izdelkov_v_skladiscu():
    """
    Vrne stevilo razlicnih izdelkov v skladiscu.

    >>> koliko_izdelkov_v_skladiscu()
    18
    """
    poizvedba = """
        SELECT COUNT(*)
        FROM izdelki
        WHERE kolicina IS NOT null
    """
    st, = conn.execute(poizvedba).fetchone()
    return st

def podatki_skladisca():
    """
    Vrne podatke o izdelkih v skladišču.
    
    """
    poizvedba = """
        SELECT sifra, ime, velikost_pakiranja, enota, kolicina, tip_izdelka
        FROM izdelki
        WHERE kolicina IS NOT null
    """
    return conn.execute(poizvedba).fetchall()

def poisci_izdelek(ime_vnos):
    """
    Poišče izdelke le na podlagi imena. Vrne seznam šifer.
    """
    poizvedba = """
        SELECT sifra
        FROM izdelki
        WHERE ime LIKE ?
    """
    return [sifra for sifra, in conn.execute(poizvedba, ['%' + ime_vnos + '%']).fetchall()]

def poisci_partner(ime_vnos):
    """
    Poišče izdelke le na podlagi imena. Vrne seznam šifer.
    """
    poizvedba = """
        SELECT sifra
        FROM partnerji
        WHERE ime LIKE ?
    """
    return [sifra for sifra, in conn.execute(poizvedba, ['%' + ime_vnos + '%']).fetchall()]

def izdelek_podatki(sifra):
    """
    Vrne podatke o izdelku z dano šifro.

    [sifra, ime, velikost_pakiranja, enota, kolicina, opis, tip_izdelka, opomnik]
    """
    poizvedba = """
        SELECT sifra, 
               ime, 
               velikost_pakiranja, 
               enota, 
               kolicina, 
               opis, 
               tip_izdelka, 
               opomnik
        FROM izdelki
        WHERE sifra = ?
    """
    return conn.execute(poizvedba, [sifra]).fetchone()


def izdelki_podatki(tab_sifr):
    """
    Vrne podatke o izdelku z dane šifre.

    [sifra, ime, velikost_pakiranja, enota, kolicina, opis, tip_izdelka, opomnik]
    """
    podatki=list()
    for sifra in tab_sifr:
        poizvedba = """
            SELECT sifra, 
                ime, 
                velikost_pakiranja, 
                enota, 
                kolicina, 
                opis, 
                tip_izdelka, 
                opomnik
            FROM izdelki
            WHERE sifra = ?
        """
        podatki.append(conn.execute(poizvedba, [sifra]).fetchone())
    return podatki


def partner_podatki(sifra):
    """
    Vrne podatke o partnerju z dano šifro.

    [sifra, ddv, ime, naslov, telefon, email]
    """
    poizvedba = """
        SELECT sifra, 
               ddv, 
               ime, 
               naslov, 
               telefon, 
               email
        FROM partnerji
        WHERE sifra = ?
    """
    return conn.execute(poizvedba, [sifra]).fetchone()

def partnerji_podatki(tab_sifr):
    """
    Vrne podatke o partnerju z dano šifro.

    [sifra, ddv, ime, naslov, telefon, email]
    """
    podatki=list()
    for sifra in tab_sifr:
        poizvedba = """
            SELECT sifra, 
                ddv, 
                ime, 
                naslov, 
                telefon, 
                email
            FROM partnerji
            WHERE sifra = ?
        """
        podatki.append(conn.execute(poizvedba, [sifra]).fetchone())
    return podatki


def v_narocila(partner, komentar = None, datum_narocila = datetime.datetime.now().strftime("%m/%d/%Y")):
    """
    Vstavi podatke samo v naročila.
    """
    poizvedba = """
        INSERT INTO narocila
        (datum_narocila, partner, komentar)
        VALUES (?, ?, ?)
    """
    with conn:
        conn.execute(poizvedba, [datum_narocila, partner, komentar])

def v_kosarico(st_narocila, sifra_izdelka, cena, popust = 0, kolicina = None, datum_prejetja = None):
    """
    Vstavi v košarico.
    """
    return

def posodobitev_v_skladišču(sifra, kolicina):
    """
    Spremeni vrednosti za obstoječ izdelek v skladišču.
    """
    poizvedba = """
        UPDATE izdelki
        SET kolicina=?
        WHERE sifra = ?
    """
    with conn:
        conn.execute(poizvedba, [kolicina, sifra])

def nov_partner(ime,ddv=None,naslov=None,telefon=None,email=None):
    poizvedba = """
        INSERT INTO partnerji 
        (ddv,ime,naslov,telefon,email)
        VALUES (?, ?, ?, ?, ?)
    """
    with conn:
        conn.execute(poizvedba, [ddv,ime,naslov,telefon,email])

def nov_izdelek(ime,velikost_pakiranja=None,enota=None,kolicina=None,opis=None,tip_izdelka=None,opomnik=None):
    poizvedba = """
        INSERT INTO izdelki
        (ime,velikost_pakiranja,enota,kolicina,opis,tip_izdelka,opomnik)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    with conn:
        conn.execute(poizvedba, [ime,velikost_pakiranja,enota,kolicina,opis,tip_izdelka,opomnik])

def nov_izdelek_v_kosarico(st_narocila, sifra_izdelka, cena, kolicina, popust = None, datum_prejetja = None):
    poizvedba = """
        INSERT INTO kosarica
        (st_narocila,sifra_izdelka,cena,popust,kolicina,datum_prejetja)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    with conn:
        conn.execute(poizvedba, [st_narocila,sifra_izdelka,cena,popust,kolicina,datum_prejetja])
    
def novo_narocilo(datum_narocila,partner,komentar):
    poizvedba = """
        INSERT INTO narocila
        (datum_narocila,partner,komentar)
        VALUES (?, ?, ?)
    """
    with conn:
        conn.execute(poizvedba, [datum_narocila,partner,komentar])

def vrni_sifra_zadnje_narocilo():
    poizvedba = """
        SELECT max(st_narocila)
        FROM narocila
    """
    return conn.execute(poizvedba).fetchone()[0]
