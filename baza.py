import csv
import sqlite3

def pobrisi_tabele(cur):
    """
    Pobriše tabele iz baze.
    """
    cur.execute("DROP TABLE IF EXISTS izdelki;")
    cur.execute("DROP TABLE IF EXISTS narocila;")
    cur.execute("DROP TABLE IF EXISTS partnerji;")
    cur.execute("DROP TABLE IF EXISTS ponudba;")
    cur.execute("DROP TABLE IF EXISTS kosarica;")

def ustvari_tabele(cur):
    """
    Ustvari tabele v bazi.
    """
    cur.execute("""
    CREATE TABLE izdelki (
        sifra              INTEGER PRIMARY KEY AUTOINCREMENT,
        ime                STRING  NOT NULL,
        kolicina           INTEGER CHECK (kolicina >= 0),
        opis               STRING,
        tip_izdelka        STRING,
        opomnik            INTEGER DEFAULT (3)
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
        ddv     STRING,
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
            cur.execute(poizvedba, vnesi_none(vrstica))

def uvozi_kosarico(cur):
    """
    Uvozi podatke o kosarici. Če ni izdelka še v ponudbi s tem partnerjem naj bi ga dodali.
    """
    cur.execute("DELETE FROM kosarica;")
    with open('podatki/kosarica.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        ind_sifra_izdelka = stolpci.index('sifra_izdelka')
        ind_st_narocila = stolpci.index('st_narocila')
        ind_partner_iz_narocila = [r[1] for r in cur.execute("""PRAGMA table_info(narocila);""")].index('partner')
        poizvedba = """
            INSERT INTO kosarica VALUES ({})
        """.format(', '.join(["?"] * len(stolpci))) 
        poizvedba_ponudba = """
            INSERT INTO ponudba VALUES (?, ?)
        """
        poizvedba_narocilo = """
            SELECT partner 
            FROM narocila 
            WHERE st_narocila = ?
        """
        poizvedba_pari_ponudbe = """
            SELECT partner, izdelek 
            FROM ponudba
        """
        ponudba = cur.execute(poizvedba_pari_ponudbe).fetchall()
        for vrstica in podatki:
            sifra_izdelka = vrstica[ind_sifra_izdelka]
            st_narocila = vrstica[ind_st_narocila]
            partner = cur.execute(poizvedba_narocilo, [st_narocila]).fetchone()[0]
            par = (partner, int(sifra_izdelka))
            if par not in ponudba:
                cur.execute(poizvedba_ponudba, par)
                ponudba.append(par)
            cur.execute(poizvedba, vnesi_none(vrstica))

def uvozi_partnerje(cur):
    """
    Uvozi podatke o partnerjih.
    """
    cur.execute("DELETE FROM partnerji;")
    with open('podatki/partnerji.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO partnerji VALUES ({})
        """.format(', '.join(["?"] * len(stolpci))) 
        for vrstica in podatki:
            cur.execute(poizvedba, vnesi_none(vrstica))

def uvozi_ponudbo(cur):
    """
    Uvozi podatke o ponudbi.
    """
    cur.execute("DELETE FROM ponudba;")
    with open('podatki/ponudba.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO ponudba VALUES ({})
        """.format(', '.join(["?"] * len(stolpci))) 
        for vrstica in podatki:
            cur.execute(poizvedba, vnesi_none(vrstica))

def uvozi_narocila(cur):
    """
    uvozi podatke o narocilih.
    """
    cur.execute("DELETE FROM narocila;")
    with open('podatki/narocila.csv') as datoteka:
        podatki = csv.reader(datoteka)
        stolpci = next(podatki)
        poizvedba = """
            INSERT INTO narocila VALUES ({})
        """.format(', '.join(["?"] * len(stolpci)))
        for vrstica in podatki:
            cur.execute(poizvedba, vnesi_none(vrstica))

def vnesi_none(tab):
    """
    Elemente, kjer nastopa prazen niz zamenja z None in vrne novo popravljeno tabelo.
    """
    nova_tab = [el if el != '' else None for el in tab]
    return nova_tab

def ustvari_bazo(cur):
    """
    Opravi celoten postopek
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
    with cur:
        cur = cur.execute("SELECT COUNT(*) FROM sqlite_master")
        if cur.fetchone() == (0, ):
            ustvari_bazo(cur)


