import sqlite3
#--------------------------------------------------------------še ni spremenjeno------------------------------------------------------------
conn = sqlite3.connect('filmi.db')
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

#TODO: napiši funkcije za dodajanje v tabele
def dodaj_vlogo(id_osebe, id_filma, id_vloge):
    poizvedba = """
        INSERT INTO nastopa
        (oseba, film, vloga)
        VALUES (?, ?, ?)
    """
    with conn:
        conn.execute(poizvedba, [id_osebe, id_filma, id_vloge])