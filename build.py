#!/usr/bin/env python3
"""Bouwt de HTML-pagina's van de site uit gedeelde onderdelen. Draai: python3 build.py"""
from pathlib import Path

ROOT = Path(__file__).parent
MAIL = 'info@matrixeventsupport.nl'
TEL = '+31630971404'
TEL_TXT = '+31 6 30971404'
INSTA = 'https://www.instagram.com/'

FONTS = ('https://fonts.googleapis.com/css2?family=Archivo:wght@800;900'
         '&family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400'
         '&family=JetBrains+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;700&display=swap')

NAV = [('projecten.html', 'Projecten'), ('over.html', 'Over'), ('argus.html', 'Argus')]


def head(title, desc, image='assets/img/hero.jpg', icon='assets/img/favicon.png'):
    return f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{image}">
<meta name="theme-color" content="#050505">
<link rel="icon" href="{icon}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/css/style.css">
</head>'''


def header(current):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{href}"{cur if href == current else ""}>{label}</a>' for href, label in NAV)
    return f'''<header class="site-header">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="MATRIX E.I.L. home"><img src="assets/img/logo-matrix.png" alt="MATRIX E.I.L." width="600" height="179"></a>
    <button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="Hoofdmenu">{links}<a class="nav-cta" href="#contact">Contact</a></nav>
  </div>
</header>'''


def footer(contact_id=True):
    cid = ' id="contact"' if contact_id else ''
    return f'''<footer class="site-footer">
  <div class="wrap foot-grid">
    <div class="foot-brand">
      <img src="assets/img/logo-matrix.png" alt="MATRIX E.I.L." width="600" height="179" loading="lazy">
      <p>Execution is the chariot of genius.</p>
    </div>
    <div>
      <h4>Pagina's</h4>
      <ul><li><a href="index.html">Home</a></li><li><a href="projecten.html">Projecten</a></li><li><a href="over.html">Over</a></li><li><a href="argus.html">Argus Systems</a></li></ul>
    </div>
    <div{cid}>
      <h4>Contact</h4>
      <ul><li><a href="mailto:{MAIL}">{MAIL}</a></li><li><a href="tel:{TEL}">{TEL_TXT}</a></li><li><a href="{INSTA}" target="_blank" rel="noopener">Instagram</a></li></ul>
    </div>
    <div>
      <h4>Fotografie</h4>
      <div class="credits">
        <img src="assets/img/partner-eleven-media.png" alt="Eleven Media" loading="lazy">
        <img src="assets/img/partner-highlite.png" alt="Highlite" loading="lazy">
        <img class="voncken" src="assets/img/partner-voncken.png" alt="Voncken Media Solutions" loading="lazy">
      </div>
    </div>
  </div>
  <div class="wrap foot-bottom">
    <span>&copy; <span data-year>2026</span> MATRIX E.I.L.</span>
    <a href="privacy.html">Privacy</a>
  </div>
</footer>
<button class="to-top" aria-label="Terug naar boven"><svg viewBox="0 0 54 54" aria-hidden="true"><circle class="track" cx="27" cy="27" r="25"/><circle class="bar" cx="27" cy="27" r="25"/></svg><span aria-hidden="true">↑</span></button>
<script src="assets/js/main.js"></script>
</body>
</html>
'''


def contact_block():
    return f'''<section class="contact-block" id="contact">
  <div class="wrap reveal">
    <span class="label"><b>VI</b> Contact</span>
    <h2 class="title">Een productie in<br><em>voorbereiding?</em></h2>
    <div class="contact-links">
      <a href="mailto:{MAIL}">{MAIL}</a>
      <a href="tel:{TEL}">{TEL_TXT}</a>
    </div>
  </div>
</section>'''


ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']

# ---------------------------------------------------------------- Home
WORK = [
    ('woeesj-stock-wide.jpg', 1285, 559, 'Woeësj-Stock', 'Simpelveld, 2026',
     'Stage design · Lighting design<br>Programming · Live operation<br>Commissioned by GTF Franzen'),
    ('electrisize.jpg', 1345, 745, 'Electrisize', 'Main Stage &amp; Tapuya, 2026',
     'LED systems · Infrastructure<br>Setup &amp; commissioning<br>For Djem LED Screens'),
    ('parkcity.jpg', 1600, 1066, 'Parkcity Live', 'Dance Stage, 2026',
     'VJ · Custom visual content<br>Live visual operation<br>For WE-AV'),
    ('boiler-room.jpg', 704, 481, 'Boiler Room', 'Complex Maastricht, 2026',
     'Programming · Live operation'),
]

EXPERTISE = [
    ('woeesj-stock-wide.jpg', 'Stage &amp; lighting design',
     'Van eerste schets tot complete rig: een ontwerp dat past bij de plek, het publiek en de muziek.'),
    ('over-matrix.jpg', 'Programming &amp; live operation',
     'De show programmeren en live bedienen, zodat licht en muziek op elk moment samenvallen.'),
    ('parkcity.jpg', 'VJ &amp; custom visual content',
     'Eigen visuals en live VJ, gemaakt voor het podium en de artiesten van jouw productie.'),
    ('electrisize.jpg', 'LED systems &amp; infrastructure',
     'LED-schermen en de techniek erachter: opbouw, signaal en inregelen.'),
]


def home():
    rows = ''.join(f'''
      <article class="work-row">
        <a class="work-media unveil" href="projecten.html"><img src="assets/img/{img}" alt="{t}" width="{w}" height="{h}" loading="lazy"></a>
        <div class="work-copy reveal">
          <span class="numeral">{ROMAN[i]}.</span>
          <h3>{t}</h3>
          <span class="meta">{meta}</span>
          <p class="disc">{disc}</p>
          <a class="link-arrow" href="projecten.html">Bekijk project</a>
        </div>
      </article>''' for i, (img, w, h, t, meta, disc) in enumerate(WORK))
    exp = ''.join(f'''
      <li class="reveal" data-img="assets/img/{img}"><span class="numeral">{ROMAN[i]}.</span><h3>{t}</h3><p>{d}</p><div class="exp-img"><img src="assets/img/{img}" alt="" loading="lazy"></div></li>''' for i, (img, t, d) in enumerate(EXPERTISE))
    ticker = ''.join(f'<span>{t}</span><i>✦</i>' for _, t, _ in EXPERTISE) * 2
    strip = ''.join(f'<img src="assets/img/galerij/{n:02d}.jpg" alt="" width="1400" height="933" loading="lazy">' for n in [2, 3, 6, 7, 8, 9, 11, 12])
    return f'''{head("MATRIX E.I.L. | Stage, licht, visuals en LED", "MATRIX E.I.L. verzorgt stage- en lichtontwerp, programmering, live operation, VJ en LED-techniek voor live producties.")}
<body class="home">
{header('index.html')}
<main>
<section class="hero">
  <img class="hero-bg" src="assets/img/hero.jpg" alt="" fetchpriority="high">
  <h1><img class="hero-tekst" src="assets/img/hero-tekst.png" alt="Execution is the chariot of genius." width="1600" height="518"></h1>
  <div class="hero-foot wrap">
    <span>Licht · Video · LED · Content</span>
    <a href="#werk" class="scroll-cue">Scroll<i></i></a>
    <span>Stage &amp; show design</span>
  </div>
</section>

<div class="ticker" aria-hidden="true"><div class="ticker-track">{ticker}</div></div>

<section class="section" id="werk">
  <div class="wrap">
    <div class="head">
      <span class="label reveal"><b>I</b> Selected work · 2024 – 2026</span>
      <p class="intro-big reveal">MATRIX geeft vorm aan de voorwaarden voor <em>dat moment.</em></p>
    </div>
    <div class="work-list">{rows}
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="head">
      <span class="label reveal"><b>II</b> Expertise</span>
      <h2 class="title reveal">Vier disciplines,<br><em>één beeld.</em></h2>
    </div>
    <ol class="exp-list">{exp}
    </ol>
  </div>
</section>

<section class="photo-break">
  <img src="assets/img/saloon.jpg" alt="Festivalpodium met licht, rook en publiek" width="2400" height="1600" loading="lazy">
  <div class="wrap"><span class="label reveal"><b>III</b> Manifest</span><h2 class="reveal">Het bestaat<br>maar <em>even.</em></h2></div>
</section>

<section class="section" style="padding-top:clamp(40px,6vw,80px)">
  <div class="wrap manifest-grid">
    <p class="big reveal">Maanden voorbereiding voor een moment dat zich nooit precies laat herhalen. Dezelfde ruimte, dezelfde muziek, dezelfde techniek, en toch iedere keer iets anders.</p>
    <div class="reveal">
      <p>Dat fascineert ons aan liveproducties. Je kunt alles voorbereiden, maar pas met mensen in de ruimte ontdek je wat het wordt.</p>
      <p>MATRIX geeft vorm aan de voorwaarden voor dat moment. Met ideeën, techniek en mensen die hun vak verstaan. Wat het uiteindelijk betekent, ontstaat tussen het podium en het publiek.</p>
    </div>
  </div>
</section>

<section class="section quote-block" style="padding-top:0">
  <div class="wrap reveal">
    <span class="ornament">✦✦✦</span>
    <blockquote>Niemand stapt twee keer in dezelfde rivier.</blockquote>
    <cite>Heraclitus</cite>
  </div>
</section>

<div class="strip" aria-hidden="true"><div class="strip-track">{strip}{strip}</div></div>

<section class="argus-teaser" style="margin-top:clamp(80px,10vw,140px)">
  <div class="wrap">
    <div class="copy reveal">
      <span class="label"><b style="color:var(--gold)">IV</b> Argus Systems</span>
      <h2 class="title">Honderd ogen<br>op <em>de show.</em></h2>
      <p>ARGUS Systems is de softwaretak van MATRIX, vernoemd naar Argus Panoptes, de wachter met honderd ogen. We bouwen tools voor licht- en showoperators, getest waar het telt: live, in het veld.</p>
      <div class="chips"><span>CHRONOS</span><span>AXIS</span><span>METRON</span><span>HOROS</span></div>
      <a class="btn gold" href="argus.html">Ontdek ARGUS</a>
    </div>
    <img class="emblem" src="assets/img/argus/argus-embleem.png" alt="ARGUS Systems embleem" width="400" height="399" loading="lazy">
  </div>
</section>

{contact_block()}
</main>
{footer(contact_id=False)}'''


# ---------------------------------------------------------------- Projecten
PROJECTS = [
    ('woeesj-stock.jpg', 'Woeësj-Stock', 'Simpelveld, 2026', 'Stage &amp; lighting design · Programming · Live operation'),
    ('electrisize.jpg', 'Electrisize', 'Main Stage &amp; Tapuya, 2026', 'LED systems · Infrastructure · Setup &amp; commissioning'),
    ('parkcity.jpg', 'Parkcity Live', 'Dance Stage, 2026', 'VJ · Custom visual content · Live visual operation'),
    (None, 'Sportclub ’25 Jubileum', '2025', 'Stage &amp; lighting design · Visuals · Programming · Live operation · VJ'),
    ('boiler-room.jpg', 'Boiler Room', 'Complex Maastricht, 2026', 'Programming · Live operation'),
    ('harmony-of-hardcore.jpg', 'Harmony of Hardcore &amp; 7th Sunday', 'Hardnature · The High · Losjes, 2026', 'LED systems &amp; infrastructure'),
]


def projecten():
    cards = ''
    for i, (img, t, meta, disc) in enumerate(PROJECTS):
        media = (f'<div class="proj-img unveil"><img src="assets/img/{img}" alt="{t}" loading="lazy"></div>' if img
                 else f'<div class="proj-img empty reveal"><span>{ROMAN[i]}</span></div>')
        cards += f'''
      <article class="proj">
        {media}
        <span class="numeral">{ROMAN[i]}.</span>
        <h3>{t}</h3>
        <span class="meta">{meta}</span>
        <p class="disc">{disc}</p>
      </article>'''
    gal = '\n'.join(f'      <img src="assets/img/galerij/{i:02d}.jpg" alt="" width="1400" height="933" loading="lazy">' for i in range(1, 13))
    return f'''{head("Projecten | MATRIX E.I.L.", "Een selectie van producties waar MATRIX E.I.L. licht, visuals en LED verzorgde.", "assets/img/electrisize.jpg")}
<body>
{header('projecten.html')}
<main>
<section class="section page-top">
  <div class="wrap">
    <div class="head split-head">
      <div class="reveal"><span class="label"><b>I</b> Projecten</span><h1 class="title" style="margin-top:22px">Selected <em>work.</em></h1></div>
      <p class="lead reveal">Een selectie van producties uit 2024 tot 2026, van stage- en lichtontwerp tot LED-infrastructuur en live visuals.</p>
    </div>
    <div class="proj-grid">{cards}
    </div>
  </div>
</section>

<section class="section quote-block" style="padding-top:0">
  <div class="wrap reveal">
    <span class="ornament">✦✦✦</span>
    <blockquote>The hidden attunement is better than the open.</blockquote>
    <cite>Heraclitus</cite>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="head"><span class="label reveal"><b>II</b> Uit het veld</span></div>
    <div class="gallery">
{gal}
    </div>
  </div>
</section>
{contact_block()}
</main>
{footer(contact_id=False)}'''


# ---------------------------------------------------------------- Over
def over():
    return f'''{head("Over | MATRIX E.I.L.", "Over MATRIX E.I.L.: stage- en lichtontwerp, programmering, visuals en LED-techniek met aandacht voor het idee en de uitvoering.", "assets/img/over-matrix.jpg")}
<body>
{header('over.html')}
<main>
<section class="section page-top">
  <div class="wrap split">
    <div class="copy reveal">
      <span class="label"><b>I</b> Over MATRIX</span>
      <h1 class="title" style="font-size:clamp(42px,5.4vw,80px)">Ieder moment verdient een <em>eigen verhaal.</em></h1>
      <p>MATRIX E.I.L. begon vanuit de wens om zelfstandig te werken en als freelancer te groeien. Onderweg werd steeds duidelijker welke manier van werken daarbij hoort, en welke overtuiging daarachter zit.</p>
      <p>Ieder evenement verdient aandacht voor zijn eigen karakter. De plek, het publiek en de aanleiding vragen telkens om nieuwe afwegingen. Daar hoort een ontwerp bij waar gedachte en moeite in zitten.</p>
      <p>Vanuit die overtuiging verbindt MATRIX stage- en lichtontwerp, programmering, visuals en LED-techniek. Met aandacht voor het idee én voor de uitvoering.</p>
    </div>
    <div class="split-img unveil"><img src="assets/img/over-matrix.jpg" alt="Operator aan de lichttafel in een MATRIX-shirt" width="822" height="637" loading="lazy"></div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap narrow prose reveal">
    <span class="label"><b>II</b> Werkwijze</span>
    <h2>Een ontwerp moet ergens <em>over gaan.</em></h2>
    <p>Een vertrouwde opstelling is snel gekozen. Toch verdient iedere productie opnieuw de vraag: waarom past dit hier?</p>
    <p>Voor MATRIX hoort die vraag bij het vak. Kijken naar de ruimte, mogelijkheden onderzoeken en verder denken dan de eerste oplossing. De beschikbare tijd en middelen geven grenzen aan; daarbinnen blijft ruimte voor bewuste keuzes.</p>
    <p>Een eenvoudige set kan precies goed zijn. Het verschil zit in de gedachte erachter. Waarom staat iets daar? Waar gaat de aandacht naartoe? Wat draagt het bij aan de ervaring?</p>
    <p>Licht, beeld en ruimte beïnvloeden elkaar. Duisternis kan een beweging betekenis geven. Een scherm kan diepte creëren, maar ook alle aandacht opeisen. De betekenis van een onderdeel ontstaat in samenhang met de rest.</p>
    <p class="big">Die samenhang verdient zorg, van de eerste schets tot de laatste cue.</p>
  </div>
</section>

<section class="reel-wrap">
  <div class="wrap unveil"><video class="reel" src="assets/video/showreel.mp4" autoplay muted loop playsinline preload="auto" poster="assets/img/reel-poster.jpg" aria-label="Showreel met beelden van MATRIX-producties"></video></div>
</section>

<section class="section">
  <div class="wrap narrow prose reveal">
    <span class="label"><b>III</b> Samenwerking</span>
    <h2>Een eigen signatuur. <em>Meerdere perspectieven.</em></h2>
    <p>MATRIX heeft een persoonlijk begin. De ambitie is om vanuit die basis verder te bouwen met zelfstandige specialisten die hun eigen kennis, ideeën en oordeel meenemen.</p>
    <p>Een gedeelde overtuiging hoeft geen identieke blik op te leveren. Juist iemand die een andere vraag stelt, kan een ontwerp verder brengen. Daarvoor zijn vertrouwen, heldere afspraken en ruimte voor inhoudelijke discussie nodig.</p>
    <p class="big">Wat we willen delen, is betrokkenheid bij het resultaat. Begrijpen waarom een keuze wordt gemaakt. Aandacht hebben voor elkaars werk. En de moeite nemen om een idee zorgvuldig uit te voeren.</p>
  </div>
</section>
{contact_block()}
</main>
{footer(contact_id=False)}'''


# ---------------------------------------------------------------- ARGUS
def argus():
    tools = (ROOT / 'src' / 'argus-tools.html').read_text()
    return f'''{head("ARGUS Systems | MATRIX E.I.L.", "ARGUS Systems is de softwaretak van MATRIX E.I.L.: CHRONOS, AXIS, METRON en HOROS, tools gebouwd vanuit de praktijk van live producties.", "assets/img/chronos-overzicht.jpg", "assets/img/argus/favicon.png")}
<body class="argus-page">
{header('argus.html')}
<main>
<section class="argus-hero">
  <div class="wrap">
    <img class="argus-logo reveal" src="assets/img/argus/argus-systems.png" alt="ARGUS Systems" width="1200" height="390">
    <span class="label reveal">De softwaretak van MATRIX</span>
    <h1 class="reveal">Gebouwd vanuit<br><em>de praktijk.</em></h1>
    <p class="myth reveal">Argus Panoptes, de wachter met honderd ogen, sliep nooit met alle ogen tegelijk. Zo houden onze tools de show in de gaten.</p>
    <p class="reveal">Op de vloer zien we elke week waar het schuurt: timetables die niet meer kloppen, planningen verspreid over losse lijstjes, informatie die net te laat aankomt. ARGUS Systems ontwikkelt de software die we zelf misten. Getest op echte producties, door de mensen die er elke dag mee werken.</p>
  </div>
</section>

{tools}
<section class="section argus-cta" id="contact">
  <div class="wrap reveal">
    <span class="label">Meedenken of testen?</span>
    <h2 class="title">Zet ARGUS in op<br><em>jouw productie.</em></h2>
    <p>Wil je een van onze tools testen op jouw evenement, of heb je een idee dat hier past? We horen het graag.</p>
    <a class="btn gold" href="mailto:{MAIL}">Neem contact op</a>
  </div>
</section>
</main>
{footer(contact_id=False)}'''


# ---------------------------------------------------------------- Privacy
def privacy():
    return f'''{head("Privacy | MATRIX E.I.L.", "Privacyverklaring van MATRIX E.I.L.")}
<body>
{header('privacy.html')}
<main>
<section class="section page-top">
  <div class="wrap narrow prose">
    <span class="label"><b>§</b> Privacy</span>
    <h2>Privacy</h2>
    <p>MATRIX E.I.L. verzamelt via deze website geen persoonsgegevens. Er worden geen tracking- of advertentiecookies gebruikt. Neem je contact op via e-mail of telefoon, dan gebruiken we je gegevens alleen om je bericht te beantwoorden.</p>
    <p>Lettertypen worden geladen via Google Fonts. Daarbij wordt je IP-adres door Google verwerkt.</p>
    <p>Vragen over privacy? Mail naar <a href="mailto:{MAIL}">{MAIL}</a>.</p>
  </div>
</section>
</main>
{footer()}'''


PAGES = {'index.html': home, 'projecten.html': projecten, 'over.html': over, 'argus.html': argus, 'privacy.html': privacy}

if __name__ == '__main__':
    for name, fn in PAGES.items():
        (ROOT / name).write_text(fn())
        print('gebouwd:', name)
