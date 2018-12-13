import sqlite3
import baza

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

