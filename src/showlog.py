# Volledig showlog van MATRIX E.I.L., aangeleverd door Fenno (28-10-2026).
# (jaar, show, rol, opdrachtgever, slug van de projectpagina of None)
SHOWLOG = [
    ('2022–2023', 'Pinkpop · De Stille Jan', 'Licht programming, operating', 'Demo Productions', None),
    ('2023', 'Groëte Gulpener Vastelaoves Finale (GGVF)', 'Licht design, programming, operating', 'Hoedemakers.PRO', None),
    ('2023', 'Deviate Festival · Area 2', 'Licht design, programming, operating', 'SL Productions', None),
    ('2023', 'Essential Festival', 'Licht design Mainstage, Crossover en Harddance stage; programming en operating Harddance stage', '', None),
    ('2023', 'Gulden Humor', 'Licht design, programming, operating', 'GTF Franzen Sound Light Vision', None),
    ('2024', 'Carnaval Radio', 'Licht design, programming, operating', 'Heijnens Audio - Light - Vision', 'carnaval-radio'),
    ('2024', 'Groëte Gulpener Vastelaoves Finale (GGVF)', 'Licht design, programming, operating', 'Hoedemakers.PRO', None),
    ('2024', 'Soenda Indoor · Solor stage', 'Licht programming, operating', 'T.Y.S. Productions', None),
    ('2024', 'Koning Carnaval Brunssum', 'Licht design, programming, operating', 'Heijnens Audio - Light - Vision', None),
    ('2024', 'Duikboot Lente Festival · House stage', 'Licht programming, operating', 'T.Y.S. Productions', None),
    ('2024', 'Paaspop · Pixl Stage', 'Licht en pixelstrips, programming, operating', 'T.Y.S. Productions', None),
    ('2024', 'Talentenshow Brandenberg College', 'Stage- en lichtdesign, programming, operating', 'GTF Franzen Sound Light Vision', None),
    ('2024', '90 jaar G.V. Wilhelmina', 'Stage- en lichtdesign, programming, operating', 'GTF Franzen Sound Light Vision', 'wilhelmina-90'),
    ('2024', 'Knaltibal Festival · Mainstage', 'Licht design, programming, operating', 'Heijnens Audio - Light - Vision', None),
    ('2024', 'Lake Dance Winterpark', 'Licht programming, operating', 'T.Y.S. Productions', None),
    ('2024', 'Power Weekend Gulpen', 'Licht programming, operating', 'Hoedemakers.PRO', None),
    ('2024', 'Essential Festival · Harddance stage', 'Licht design, programming, operating', 'Heijnens Audio - Light - Vision', None),
    ('2024–2026', 'The Notorious IBE · Cypher 1', 'Licht programming, operating', 'Demo Productions', None),
    ('2025', 'ZLF 2025 · Zuid-Limburgs Federatiefestival, Ubachsberg', 'Licht- en stagedesign, programming, operating en video', 'GTF Franzen Sound Light Vision', 'zlf-2025'),
    ('2025', 'Groëte Gulpener Vastelaoves Finale (GGVF)', 'Licht design, programming, operating', 'Hoedemakers.PRO', None),
    ('2025', 'Soenda Presents', 'Licht programming, operating', 'T.Y.S. Productions', None),
    ('2025', 'Sportclub’25 Bocholtz · 100 jaar', 'Stage- en lichtdesign; programming en operating van licht, video en special FX; technische ondersteuning', 'GTF Franzen Sound Light Vision', 'sportclub-jubileum'),
    ('2025', 'Outrageous Festival · Mainstage', 'Licht programming, operating', 'Bongers BLG', 'outrageous'),
    ('2025', 'Ohm Herfstfestival · Mainstage / De Kathedraal', 'Licht programming, operating', 'T.Y.S. Productions', None),
    ('2026', 'Pleinfeest Echt', 'Licht programming, operating', 'Cowanzo', None),
    ('2026', 'Koning Carnaval', 'Licht programming, operating', 'Heijnens Audio - Light - Vision', None),
    ('2026', 'Diverse carnavalsprojecten', 'Licht design, programming, operating', 'GTF Franzen Sound Light Vision', None),
    ('2026', 'Carnaval Radio', 'Licht programming, operating, video operating', 'Heijnens Audio - Light - Vision', 'carnaval-radio'),
    ('2026', 'Halfvasten Pleinfeest', 'Licht programming, operating', 'Heijnens Audio - Light - Vision', None),
    ('2026', 'Groove Garden Festival · Techno Area', 'Licht programming, operating', 'ROOT Productions', None),
    ('2026', 'Harmony of Hardcore / 7th Sunday', 'LED-systeemtechniek en opbouwploeg', 'DJEM LED', 'harmony'),
    ('2026', 'Beachparty Brunssum', 'Licht programming, operating, video operating', 'Heijnens Audio - Light - Vision', None),
    ('2026', 'ParkCity Live · Dance tent', 'Custom content en LED operating', 'WE-AV', 'parkcity-live'),
    ('2026', 'Brabants Verbond Festival · Mainstage', 'Licht programming, operating', 'Spectrum AV', None),
    ('2026', 'USC Lustrum · Stelz Vriendendag, Ongemengde dag, Reünistendag, Familiedag, La Grande Finale', 'Licht programming, operating', 'Spectrum AV', 'usc-lustrum'),
    ('2026', 'Electrisize · Tapuya & Mainstage', 'LED-infratechniek, load-in en load-out', 'DJEM LED', 'electrisize'),
    ('2026', 'Decibel Outdoor · Area 11 City Hall', 'Licht programming, operating', 'Spectrum AV', None),
    ('2026', 'Woeësj-Stock Festival', 'Stage- en lichtdesign, programming, operating', 'GTF Franzen Sound Light Vision', 'woeesj-stock'),
]

# Grote namen voor de highlightstrip op de home
HIGHLIGHTS = ['Paaspop', 'Pinkpop', 'Essential Festival', 'Decibel Outdoor', 'Electrisize', 'Soenda', 'Lake Dance', 'Ohm', 'Groove Garden', 'Harmony of Hardcore']

# Artikelen van Highlite over producties uit het showlog: (jaar, begin van de shownaam) -> url
HL = 'https://www.highlite.com/nl/news/base/'
PRESS = {
    ('2025', 'Sportclub'): HL + 'sportsclub-bocholtz.html',
    ('2025', 'ZLF'): HL + 'zlf-2025.html',
    ('2025', 'Groëte'): HL + 'ggvf-2025.html',
    ('2024', 'Essential Festival'): HL + 'showtec-and-infinity-shine-on-essential-festival-2024.html',
    ('2024', '90 jaar'): HL + '90th-anniversary-of-the-gymnastics-club-wilhelmina.html',
}


def press_for(year, show):
    return next((u for (y, start), u in PRESS.items() if y == year and show.startswith(start)), None)
