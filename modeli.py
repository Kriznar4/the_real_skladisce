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
        SELECT sifra, ime, kolicina, tip_izdelka
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

def poisci_v_skladiscu(ime_vnos):
    """
    Poišče izdelke le na podlagi imena. Vrne seznam šifer.
    """
    poizvedba = """
        SELECT sifra
        FROM izdelki
        WHERE ime LIKE ?
        AND kolicina IS NOT null
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

    [sifra, ime, kolicina, opis, tip_izdelka, opomnik]
    """
    poizvedba = """
        SELECT sifra, 
               ime,  
               kolicina, 
               opis, 
               tip_izdelka, 
               opomnik
        FROM izdelki
        WHERE sifra = ?
    """
    return conn.execute(poizvedba, [sifra]).fetchone()

def izdelki_podatki(tab_sifer:list):
    """
    Vrne podatke o izdelkih iz tabele šifer.
    """

    poizvedba = ("""
        SELECT sifra, 
               ime,  
               kolicina, 
               opis, 
               tip_izdelka, 
               opomnik
        FROM izdelki
        WHERE sifra IN (""" + ('?, '*len(tab_sifer)))[:-2] + ')'
    return conn.execute(poizvedba, tab_sifer).fetchall()


def izdelki_podatki_vsi():
    """
    Vrne podatke o vseh izdelkih.
    """
    podatki=list()
    for sifra in tab_sifr:
        poizvedba = """
            SELECT sifra, 
                ime,  
                kolicina, 
                opis, 
                tip_izdelka, 
                opomnik
            FROM izdelki
        """
    return conn.execute(poizvedba).fetchall()


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

    Prištevanje česarkoli nullu vren null.
    """
    poizvedba = """
        UPDATE izdelki
        SET kolicina= (SELECT kolicina FROM izdelki WHERE sifra = ?) + ?
        WHERE sifra = ?
    """
    with conn:
        conn.execute(poizvedba, [sifra, kolicina, sifra])

def nov_partner(ime,ddv=None,naslov=None,telefon=None,email=None):
    poizvedba = """
        INSERT INTO partnerji 
        (ddv,ime,naslov,telefon,email)
        VALUES (?, ?, ?, ?, ?)
    """
    with conn:
        conn.execute(poizvedba, [ddv,ime,naslov,telefon,email])

def nov_izdelek(ime,kolicina=None,opis=None,tip_izdelka=None,opomnik=None):
    poizvedba = """
        INSERT INTO izdelki
        (ime,kolicina,opis,tip_izdelka,opomnik)
        VALUES (?, ?, ?, ?, ?)
    """
    with conn:
        conn.execute(poizvedba, [ime,kolicina,opis,tip_izdelka,opomnik])

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

def imena_partnerjev():
    poizvedba = """
        SELECT sifra,ime
        FROM partnerji
    """
    return conn.execute(poizvedba).fetchall()

def imena_izdelkov():
    poizvedba = """
        SELECT sifra,ime
        FROM izdelki
       """
    return conn.execute(poizvedba).fetchall()

def tipi_izdelkov():
    poizvedba = """
        SELECT sifra,tip_izdelka
        FROM izdelki
        GROUP BY tip_izdelka
    """
    return conn.execute(poizvedba).fetchall()

def ime_izdelka_iz_sifre(stevilo):
    poizvedba = """
        SELECT ime
        FROM izdelki
        WHERE sifra=?
        """
    return conn.execute(poizvedba, [stevilo]).fetchone()

def vrni_leta():
    """Vrne seznam z leti v katerih smo nakupovali izdelke"""
    poizvedba = """
        SELECT DISTINCT SUBSTR(datum_narocila, -4, 4) AS leto
        FROM narocila
        ORDER BY leto
    """
    return [el[0] for el in conn.execute(poizvedba).fetchall()]

def vrni_letno(leto: str):
    """Vrne ["ID", "Ime", "Letna poraba za nabavo", 
    "Povprečna cena na 1 izdelek"] za leto za vse izdelke v tem letu."""
    poizvedba = """
        SELECT izdelki.sifra,
            izdelki.ime,
            ROUND(SUM(kosarica.cena - kosarica.cena * kosarica.popust/100), 2),
            ROUND(SUM(kosarica.cena - kosarica.cena * kosarica.popust/100) / SUM(kosarica.kolicina), 2) 
        FROM kosarica
            JOIN
            narocila ON kosarica.st_narocila = narocila.st_narocila
            JOIN
            izdelki ON kosarica.sifra_izdelka = izdelki.sifra
        WHERE narocila.datum_narocila LIKE ?
        GROUP BY izdelki.sifra,
                izdelki.ime
        ORDER BY izdelki.ime
        """
    return conn.execute(poizvedba, ["%" + leto]).fetchall()

def neprejete():
    """Vrne seznam neprejetih pošiljk oblike [(st_narocila, 
    sifra_izdelka, ime_izdelka, kolicina, sifra_partnerja, ime_partnerja, datum_narocila), ...]"""
    poizvedba = """
        SELECT kosarica.st_narocila, kosarica.sifra_izdelka, izdelki.ime, kosarica.kolicina, partnerji.sifra, partnerji.ime, narocila.datum_narocila
        FROM kosarica
            JOIN
            narocila ON kosarica.st_narocila = narocila.st_narocila
            JOIN
            izdelki ON kosarica.sifra_izdelka = izdelki.sifra
            JOIN
            partnerji ON partnerji.sifra = narocila.partner
        WHERE kosarica.datum_prejetja IS NULL
        ORDER BY kosarica.st_narocila desc, kosarica.sifra_izdelka asc
        """
    return conn.execute(poizvedba).fetchall()

def datum_prejetja(dan, mesec, leto, sifra_izdelka, sifra_narocila):
    """Vstavi datum v kosarico"""
    datum = mesec + "/" + dan + "/" + leto
    print(datum)
    poizvedba = """
        UPDATE kosarica
        SET datum_prejetja = ?
        WHERE sifra_izdelka = ?
        AND st_narocila = ?
    """
    with conn:
        conn.execute(poizvedba, [datum, int(sifra_izdelka), int(sifra_narocila)])

def dodaj_v_ponudbo_partnerja(partner,izdelek):
    poizvedba="""
        INSERT INTO ponudba
        (partner, izdelek)
        VALUES (?,?)
    """
    with conn:
        conn.execute(poizvedba,[partner,izdelek])


def ponudba_partnerja(partner):
    """vrne ID-je produktov, ki jih partner ponuja"""
    poizvedba="""
        SELECT izdelek
        FROM ponudba
        where partner = ?
    """
    return conn.execute(poizvedba,[partner]).fetchall()


def posodobitev_ponudbe(partner, seznam_produktov):
    ponudba=ponudba_partnerja(partner)
    prava_ponudba=set()
    for izdelek in ponudba:
        prava_ponudba.add(izdelek[0])
    seznam_prod=set(seznam_produktov)
    for izdelek in seznam_prod-prava_ponudba:
        dodaj_v_ponudbo_partnerja(partner,izdelek)
