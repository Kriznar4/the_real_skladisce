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

def poisci_izdelek_ime(ime_vnos):
    """
    Poišče izdelke le na podlagi imena.
    """
    poizvedba = """
        SELECT sifra, ime, velikost_pakiranja, enota, tip_izdelka
        FROM izdelki
        WHERE ime LIKE ?
    """
    return conn.execute(poizvedba, ['%' + ime_vnos + '%']).fetchall()

def poisci_partner_ime(ime_vnos):
    """
    Poišče izdelke le na podlagi imena.
    """
    poizvedba = """
        SELECT sifra
        FROM partnerji
        WHERE ime LIKE ?
    """
    sifra, = conn.execute(poizvedba, ['%' + ime_vnos + '%']).fetchone()
    return sifra

def v_narocila(partner, komentar = None, datum_narocila = datetime.datetime.now().strftime("%d/%m/%Y")):
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

def posodobitev_v_skladišču(sifra,ime,velikost_pakiranja,enota,kolicina,opis,tip_izdelka,opomnik):
    """
    Spremeni vrednosti za obstoječ izdelek v skladišču.
    """
    poizvedba = """
        UPDATE izdelki
        SET ime=?,velikost_pakiranja=?,enota=?,kolicina=?,opis=?,tip_izdelka=?,opomnik=?
    """
    with conn:
        conn.execute(poizvedba, [sifra,ime,velikost_pakiranja,enota,kolicina,opis,tip_izdelka,opomnik])

print(poisci_izdelek_ime('li'))
