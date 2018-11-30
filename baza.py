import csv
from modeli import conn, commit

@commit
def pobrisi_tabele(cur):
    """
    Pobriše tabele iz baze.
    """
    cur.execute("DROP TABLE IF EXISTS izdelki;")
    cur.execute("DROP TABLE IF EXISTS narocila;")
    cur.execute("DROP TABLE IF EXISTS partnerji;")
    cur.execute("DROP TABLE IF EXISTS ponudba;")
    cur.execute("DROP TABLE IF EXISTS kosarica;")

@commit
def ustvari_tabele(cur):
    """
    Ustvari tabele v bazi.
    """
    cur.execute("""
        CREATE TABLE izdelki (
        sifra         INTEGER PRIMARY KEY AUTOINCREMENT,
        ime           STRING  NOT NULL
                              UNIQUE,
        zaloga        INTEGER NOT NULL
                              CHECK (zaloga >= 0),
        opis          STRING,
        trenutna_cena DOUBLE
    );
    """)
    cur.execute("""
    CREATE TABLE narocila (
        st_narocila    INTEGER PRIMARY KEY AUTOINCREMENT,
        datum_narocila DATE,
        datum_prejetja DATE,
        partner        STRING
    );

    """)
    cur.execute("""
    CREATE TABLE partnerji (
        ddv    INTEGER PRIMARY KEY,
        ime    STRING,
        naslov STRING,
        drzava STRING
    );

    """)
    cur.execute("""
    CREATE TABLE kosarica (
        st_narocila   INTEGER,
        sifra_izdelka INTEGER,
        cena          DOUBLE  NOT NULL,
        popust        DOUBLE,
        kolicina      DOUBLE  NOT NULL,
        PRIMARY KEY (
            st_narocila,
            sifra_izdelka
        )
    );

    """)
    cur.execute("""
    CREATE TABLE ponudba (
        partner INTEGER,
        izdelek INTEGER,
        PRIMARY KEY (
            partner,
            izdelek
        )
    );
    """)
#------------------------------------------------------------do sem spremenjeno------------------------------------------------------------------------------
@commit
def uvozi_filme(cur):
    """
    Uvozi podatke o filmih.
    """
    cur.execute("DELETE FROM film;")
    with open('podatki/film.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO film VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            cur.execute(poizvedba, vrstica)

@commit
def uvozi_osebe(cur):
    """
    Uvozi podatke o osebah.
    """
    cur.execute("DELETE FROM oseba;")
    with open('podatki/oseba.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO oseba VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            cur.execute(poizvedba, vrstica)

@commit
def uvozi_vloge(cur):
    """
    Uvozi podatke o vlogah.
    """
    cur.execute("DELETE FROM nastopa;")
    cur.execute("DELETE FROM vloga;")
    vloge = {}
    with open('podatki/vloge.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        v = stolpci.index('vloga')
        poizvedba = """
            INSERT INTO nastopa VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        poizvedba_vloga = "INSERT INTO vloga (naziv) VALUES (?);"
        for vrstica in podatki:
            vloga = vrstica[v]
            if vloga not in vloge:
                cur.execute(poizvedba_vloga, [vloga])
                vloge[vloga] = cur.lastrowid
            vrstica[v] = vloge[vloga]
            cur.execute(poizvedba, vrstica)

@commit
def uvozi_zanre(cur):
    """
    Uvozi podatke o žanrih.
    """
    cur.execute("DELETE FROM pripada;")
    cur.execute("DELETE FROM zanr;")
    zanri = {}
    with open('podatki/zanri.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        z = stolpci.index('zanr')
        poizvedba = """
            INSERT INTO pripada VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        poizvedba_zanr = "INSERT INTO zanr (naziv) VALUES (?);"
        for vrstica in podatki:
            zanr = vrstica[z]
            if zanr not in zanri:
                cur.execute(poizvedba_zanr, [zanr])
                zanri[zanr] = cur.lastrowid
            vrstica[z] = zanri[zanr]
            cur.execute(poizvedba, vrstica)

@commit
def ustvari_bazo(cur):
    """
    Opravi celoten postopek postavitve baze.
    """
    pobrisi_tabele.nocommit(cur)
    ustvari_tabele.nocommit(cur)
    uvozi_filme.nocommit(cur)
    uvozi_osebe.nocommit(cur)
    uvozi_vloge.nocommit(cur)
    uvozi_zanre.nocommit(cur)

def ustvari_bazo_ce_ne_obstaja():
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
    if cur.fetchone() == (0, ):
        ustvari_bazo()
