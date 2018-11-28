import csv
import sqlite3

conn = sqlite3.connect('filmi.db')

#osnovne operacije nad bazamai


#def pobrisi_tabele(cur):
#    """
#    Pobriše tabele iz baze
#    """
#    cur.execute('DROP TABLE IF EXISTS')
#    cur.execute('DROP TABLE IF EXISTS')
#    cur.execute('DROP TABLE IF EXISTS')
#    cur.execute('DROP TABLE IF EXISTS')
#    cur.execute('DROP TABLE IF EXISTS')
#    cur.execute('DROP TABLE IF EXISTS')
#    cur.execute('DROP TABLE IF EXISTS')
#    cur.execute('DROP TABLE IF EXISTS')  
# 
# poglej si cur.lastrowid  
# cur = conn.cursor()