# -*- coding: utf-8 -*-
# corrige de la question 5 du TD1

import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as pltd
import sqlite3

# ouverture d'une connexion avec la base de données
conn = sqlite3.connect('ter.sqlite')
c = conn.cursor()

# Definition des régions et des couleurs de tracé
regions = [("Rhône Alpes","blue"), ("Auvergne","green"), ("Auvergne-Rhône Alpes","cyan"), ('Bourgogne',"red"), 
           ('Franche Comté','orange'), ('Bourgogne-Franche Comté','olive') ]

# configuration du tracé
plt.figure(figsize=(18,6))
plt.ylim(80,100)
plt.grid(which='major', color='#888888', linestyle='-')
plt.grid(which='minor',axis='x', color='#888888', linestyle=':')

ax = plt.subplot(111)
loc_major = pltd.YearLocator()
loc_minor = pltd.MonthLocator()
ax.xaxis.set_major_locator(loc_major)
ax.xaxis.set_minor_locator(loc_minor)
format_major = pltd.DateFormatter('%B %Y')
ax.xaxis.set_major_formatter(format_major)
ax.xaxis.set_tick_params(labelsize=10)

# boucle sur les régions
for l in (regions) :
    c.execute("SELECT * FROM 'regularite-mensuelle-ter' WHERE Région=? ORDER BY Date",l[:1])  # ou (l[0],)
    r = c.fetchall()
    # recupération de la date (2e colonne) et transformation dans le format de pyplot
    x = [pltd.date2num(dt.date(int(a[1][:4]),int(a[1][5:]),1)) for a in r if not a[7] == '']
    # récupération de la régularité (8e colonne)
    y = [float(a[7]) for a in r if not a[7] == '']
    # tracé de la courbe
    plt.plot_date(x,y,linewidth=1, linestyle='-', marker='o', color=l[1], label=l[0])
    
# légendes
plt.legend(loc='lower left')
plt.title('Régularité des TER (en %)',fontsize=16)
plt.ylabel('% de régularité')
plt.xlabel('Date')

# affichage des courbes
plt.show()

# fermeture de la base de données
conn.close()
