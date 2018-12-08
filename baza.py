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
        sifra              INTEGER PRIMARY KEY AUTOINCREMENT,
        ime                STRING  NOT NULL,
        velikost_pakiranja INTEGER CHECK (kolicina >= 0),
        enota              STRING  DEFAULT X,
        kolicina           INTEGER CHECK (kolicina >= 0),
        opis               STRING,
        tip_izdelka        STRING,
        opomnik            INTEGER DEFAULT (3),
        UNIQUE (
            ime,
            velikost_pakiranja
        )
    );
    """)

    cur.execute("""
    CREATE TABLE narocila (
        st_narocila    INTEGER PRIMARY KEY AUTOINCREMENT,
        datum_narocila DATE    NOT NULL,
        partner        INTEGER NOT NULL
                            REFERENCES partnerji (sifra),
        komentar       STRING
    );
    """)

    cur.execute("""
    CREATE TABLE partnerji (
        sifra   INTEGER PRIMARY KEY AUTOINCREMENT,
        ddv     INTEGER UNIQUE,
        ime     STRING,
        naslov  STRING,
        telefon,
        email   STRING
);
    """)

    cur.execute("""
    CREATE TABLE kosarica (
        st_narocila    INTEGER REFERENCES narocila (st_narocila),
        sifra_izdelka  INTEGER REFERENCES narocila (st_narocila),
        cena           DOUBLE  NOT NULL,
        popust         DOUBLE,
        kolicina       DOUBLE  NOT NULL,
        datum_prejetja DATE,
        PRIMARY KEY (
            st_narocila,
            sifra_izdelka
        )
    );
    """)

    cur.execute("""
    CREATE TABLE ponudba (
        partner INTEGER REFERENCES partnerji (sifra),
        izdelek INTEGER REFERENCES izdelki (sifra),
        PRIMARY KEY (
            partner,
            izdelek
        )
    );
    """)

def uvozi_izdelke(cur):
    """
    Uvozi podatke o izdelkih.
    """
    cur.execute("DELETE FROM izdelki;")
    with open('podatki/izdelki.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO izdelki VALUES ({})
        """.format(', '.join(["?"] * len(stolpci))) 
        for vrstica in podatki:
            cur.execute(poizvedba, vrstica)

def uvozi_kosarico(cur):
    #TODO: popravi to funkcijo
    """
    Uvozi podatke o kosarici.
    """
    cur.execute("DELETE FROM kosarica;")
    pari_ponudbe = cur.execute("""
        SELECT * FROM ponudba
        """)
    with open('podatki/kosarica.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        ind_sifra_izdelka = stolpci.index('sifra_izdelka')
        ind_st_narocila = stolpci.index('st_narocila')
        ind_stolpci_narocila = cur.execute("""PRAGMA table_info(narocila);""").index('partner')
        poizvedba = """
            INSERT INTO izdelki VALUES ({})
        """.format(', '.join(["?"] * len(stolpci))) 
        poizvedba_ponudba = """
            INSERT INTO ponudba (?, ?)
        """
        poizvedba_narocilo = """
            SELECT partner 
            FROM narocila 
            WHERE st_narocila == ?
        """
        ponudba = cur.execute(poizvedba_ponudba)
        for vrstica in podatki:
            sifra_izdelka = vrstica[ind_sifra_izdelka]
            st_narocila = vrstica[ind_st_narocila]
            narocilo = 

            if ()
            # TODO: preveri če so izdelki v že ponudbi in če niso jih dodaj

            cur.execute(poizvedba, vrstica)

def uvozi_partnerje(cur):
    """
    Uvozi podatke o partnerjih.
    """
    cur.execute("DELETE FROM partnerji;")
    with open('podatki/partnerji.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO izdelki VALUES ({})
        """.format(', '.join(["?"] * len(stolpci))) 
        for vrstica in podatki:
            cur.execute(poizvedba, vrstica)

def uvozi_ponudbo(cur):
    """
    Uvozi podatke o ponudbi.
    """
    cur.execute("DELETE FROM ponudba;")
    with open('podatki/ponudba.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO izdelki VALUES ({})
        """.format(', '.join(["?"] * len(stolpci))) 
        for vrstica in podatki:
            cur.execute(poizvedba, vrstica)

def uvozi_narocila(cur):
    """
    uvozi podatke o narocilih.
    """
    cur.execute("DELETE FROM naroila;")
    with open('podatki/ponudba.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO narocila VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            cur.execute(poizvedba, vrstica)

def ustvari_bazo(cur):
    """
    Opravi celoten postopek postavitve baze.
    """
    pobrisi_tabele(cur)
    ustvari_tabele(cur)
    uvozi_izdelke(cur)
    uvozi_partnerje(cur)
    uvozi_ponudbo(cur)
    uvozi_narocila(cur)
    uvozi_kosarico(cur)

def ustvari_bazo_ce_ne_obstaja(cur):
    """
    Ustvari bazo, če ta še ne obstaja.
    """
    cur = conn.execute("SELECT COUNT(*) FROM sqlite_master")
    if cur.fetchone() == (0, ):
        ustvari_bazo(cur)
