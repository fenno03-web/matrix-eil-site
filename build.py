#!/usr/bin/env python3
"""Bouwt de HTML-pagina's van de site uit gedeelde onderdelen. Draai: python3 build.py"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).parent
MAIL = 'info@matrixeventsupport.nl'
TEL = '+31630971404'
TEL_TXT = '+31 6 30971404'
INSTA = 'https://www.instagram.com/matrix.eil/'

FONTS = ('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500'
         '&family=Space+Grotesk:wght@300;400;500;600;700&display=swap')

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
    return f'''<div class="standby" aria-hidden="true"><div class="sb">Standby<b class="go">GO</b></div></div>
<div class="haze" aria-hidden="true"><i></i><i></i></div>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="MATRIX E.I.L. home"><img src="assets/img/logo-matrix.png" alt="MATRIX E.I.L." width="600" height="179"></a>
    <div class="showbar" aria-hidden="true"><span class="live">Live</span><span class="sep"></span><span class="tc-wrap">TC <span class="tc">00:00:00:00</span></span><span class="sep s2"></span><span class="cue-now"></span></div>
    <button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="Hoofdmenu">{links}<a class="nav-cta" href="#contact">Contact</a></nav>
  </div>
</header>'''


def footer(extra_js=''):
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="eoc">Einde cuelijst · bedankt voor het kijken</div>
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="assets/img/logo-matrix.png" alt="MATRIX E.I.L." width="600" height="179" loading="lazy">
        <p>Execution is the chariot of genius.</p>
      </div>
      <div>
        <h4>Pagina's</h4>
        <ul><li><a href="index.html">Home</a></li><li><a href="projecten.html">Projecten</a></li><li><a href="over.html">Over</a></li><li><a href="argus.html">Argus Systems</a></li></ul>
      </div>
      <div>
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
    <div class="foot-bottom">
      <span>&copy; <span data-year>2026</span> MATRIX E.I.L.</span>
      <a href="privacy.html">Privacy</a>
    </div>
  </div>
</footer>
<button class="to-top" aria-label="Terug naar boven"><svg viewBox="0 0 54 54" aria-hidden="true"><circle class="track" cx="27" cy="27" r="25"/><circle class="bar" cx="27" cy="27" r="25"/></svg><span aria-hidden="true">↑</span></button>
<script src="assets/js/main.js"></script>{extra_js}
</body>
</html>
'''


def cue_head(q, name, tc=''):
    tc_html = f'<span class="tc">{tc}</span>' if tc else ''
    return f'<div class="cue-head reveal"><span class="q">{q}</span><span class="nm">{name}</span><span class="ln"></span>{tc_html}</div>'


def contact_block(q='Q6'):
    return f'''<section class="contact-block" id="contact" data-cue="{q}" data-cue-name="Contact">
  <div class="wrap">
    {cue_head(q, 'Contact', 'Standby for your call')}
    <div class="reveal">
      <div class="standby-line">Standby</div>
      <h2 class="display">Een productie in<br><em>voorbereiding?</em></h2>
      <div class="contact-links">
        <a href="mailto:{MAIL}">{MAIL}</a>
        <a href="tel:{TEL}">{TEL_TXT}</a>
        <a class="ig" href="{INSTA}" target="_blank" rel="noopener">Instagram · @matrix.eil</a>
      </div>
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- Home
WORK = [
    ('proj/woeesj-stock/01.jpg', 1600, 1067, 'Woeësj-Stock', 'Simpelveld, 2026', 'woeesj-stock',
     'Stage design · Lighting design<br>Programming · Live operation<br>Commissioned by GTF Franzen'),
    ('electrisize.jpg', 1345, 745, 'Electrisize', 'Main Stage &amp; Tapuya, 2026', 'electrisize',
     'LED systems · Infrastructure<br>Setup &amp; commissioning<br>For Djem LED Screens'),
    ('proj/parkcity-live/01.jpg', 1600, 1067, 'Parkcity Live', 'Dance tent, 2026', 'parkcity-live',
     'Custom visual content · VJ<br>For WE-AV'),
    ('boiler-room.jpg', 704, 481, 'Boiler Room', 'Complex Maastricht, 2026', 'boiler-room',
     'Programming · Live operation'),
]

# (foto, titel, tekst, faderstand)
EXPERTISE = [
    ('proj/woeesj-stock/01.jpg', 'Stage &amp; lighting design',
     'Van eerste schets tot complete rig: een ontwerp dat past bij de plek, het publiek en de muziek.', 86),
    ('proj/paul-elstak/01.jpg', 'Programming &amp; live operation',
     'De show programmeren en live bedienen, zodat licht en muziek op elk moment samenvallen.', 72),
    ('proj/parkcity-live/01.jpg', 'VJ &amp; custom visual content',
     'Eigen visuals en live VJ, gemaakt voor het podium en de artiesten van jouw productie.', 93),
    ('electrisize.jpg', 'LED systems &amp; infrastructure',
     'LED-schermen en de techniek erachter: opbouw, signaal en inregelen.', 64),
]


def home():
    rows = ''.join(f'''
      <article class="work-row">
        <a class="work-media unveil rm" href="projecten.html#{slug}"><img src="assets/img/{img}" alt="{t}" width="{w}" height="{h}" loading="lazy"></a>
        <div class="work-copy reveal">
          <span class="cueno">Q2.{i + 1}</span>
          <h3>{t}</h3>
          <span class="meta">{meta}</span>
          <p class="disc">{disc}</p>
          <a class="link-arrow" href="projecten.html#{slug}">Open in logboek</a>
        </div>
      </article>''' for i, (img, w, h, t, meta, slug, disc) in enumerate(WORK))
    ticks = ''.join(f'<span>{n}</span>' for n in ['+10', '0', '-10', '-20', '-∞'])
    desk = ''.join(f'''
      <div class="ch reveal" style="--v:{v}%">
        <div class="ph" aria-hidden="true"><img src="assets/img/{img}" alt="" loading="lazy"></div>
        <div class="top"><span>CH <b>{i + 1:02d}</b></span><span>{v}%</span></div>
        <div class="fader" aria-hidden="true"><div class="ticks">{ticks}</div><div class="lvl"></div><div class="knob"></div></div>
        <h3>{t}</h3>
        <p>{d}</p>
      </div>''' for i, (img, t, d, v) in enumerate(EXPERTISE))
    ticker = ''.join(f'<span>{t}</span><i>GO</i>' for _, t, _, _ in EXPERTISE) * 2
    strip = ''.join(f'<img src="assets/img/galerij/{n:02d}.jpg" alt="" width="1400" height="933" loading="lazy">' for n in [2, 3, 6, 7, 8, 9, 11, 12])
    return f'''{head("MATRIX E.I.L. | Stage, licht, visuals en LED", "MATRIX E.I.L. verzorgt stage- en lichtontwerp, programmering, live operation, VJ en LED-techniek voor live producties.")}
<body class="home">
{header('index.html')}
<main>
<section class="hero" data-cue="Q1" data-cue-name="Opening">
  <img class="hero-bg" src="assets/img/hero.jpg" alt="" fetchpriority="high">
  <div class="beams" aria-hidden="true"><i></i><i></i><i></i></div>
  <h1><img class="hero-tekst" src="assets/img/hero-tekst.png" alt="Execution is the chariot of genius." width="1600" height="518"></h1>
  <div class="hud">
    <span class="tl">Q1 · <b>Opening</b></span>
    <span class="tr">Scene <b>01</b> / 06</span>
    <span class="bl">Licht · Video · LED · Content</span>
    <a href="#werk" class="bc">GO<i></i></a>
    <span class="br">Stage &amp; show design</span>
  </div>
</section>

<div class="ticker" aria-hidden="true"><div class="ticker-track">{ticker}</div></div>

<section class="section" id="werk" data-cue="Q2" data-cue-name="Selected work">
  <div class="wrap">
    {cue_head('Q2', 'Selected work', '2024 – 2026')}
    <div class="intro-line">
      <h2 class="title reveal">Selected<br><em>work.</em></h2>
      <p class="lead reveal">MATRIX geeft vorm aan de voorwaarden voor dat moment. Een greep uit de producties waar we licht, beeld en LED neerzetten.</p>
    </div>
    <div class="work-list">{rows}
    </div>
  </div>
</section>

<section class="section" style="padding-top:0" data-cue="Q3" data-cue-name="Disciplines">
  <div class="wrap">
    {cue_head('Q3', 'Disciplines', '4 kanalen · 1 beeld')}
    <div class="intro-line">
      <h2 class="title reveal">Vier disciplines,<br><em>één beeld.</em></h2>
      <p class="lead reveal">Vier kanalen op dezelfde tafel. Pas als ze samen omhoog gaan, ontstaat het beeld.</p>
    </div>
    <div class="desk">{desk}
    </div>
  </div>
</section>

<section class="photo-break" data-cue="Q4" data-cue-name="Manifest">
  <img src="assets/img/saloon.jpg" alt="Festivalpodium met licht, rook en publiek" width="2400" height="1600" loading="lazy">
  <div class="wrap"><span class="tag reveal"><b>Q4</b> · Manifest</span><h2 class="reveal">Het bestaat<br>maar <em>even.</em></h2></div>
</section>

<section class="section" style="padding-top:clamp(40px,6vw,80px)">
  <div class="wrap manifest-grid">
    <p class="scrub">Maanden voorbereiding voor een moment dat zich nooit precies laat herhalen. Dezelfde ruimte, dezelfde muziek, dezelfde techniek, en toch iedere keer iets anders.</p>
    <div class="side reveal">
      <p>Dat fascineert ons aan liveproducties. Je kunt alles voorbereiden, maar pas met mensen in de ruimte ontdek je wat het wordt.</p>
      <p>MATRIX geeft vorm aan de voorwaarden voor dat moment. Met ideeën, techniek en mensen die hun vak verstaan. Wat het uiteindelijk betekent, ontstaat tussen het podium en het publiek.</p>
    </div>
  </div>
</section>

<section class="section quote-block" style="padding-top:0">
  <div class="wrap reveal">
    <blockquote>Niemand stapt twee keer in dezelfde rivier.</blockquote>
    <cite>Heraclitus</cite>
  </div>
</section>

<div class="strip" aria-hidden="true"><div class="strip-track">{strip}{strip}</div></div>

<section class="argus-teaser" style="margin-top:clamp(80px,10vw,140px)" data-cue="Q5" data-cue-name="Argus">
  <div class="wrap">
    <div class="copy">
      {cue_head('Q5', 'Argus Systems', 'In ontwikkeling')}
      <div class="reveal">
        <h2 class="title">Honderd ogen<br>op <em>de show.</em></h2>
        <p>ARGUS Systems is de softwaretak van MATRIX, vernoemd naar Argus Panoptes, de wachter met honderd ogen. Vier tools voor productie en showoperators, gebouwd op de vloer en getest waar het telt: live, in het veld.</p>
        <div class="chips"><span>CHRONOS</span><span class="t">AXIS</span><span class="t">METRON</span><span class="t">HOROS</span></div>
        <a class="btn" href="argus.html">Open de regiekamer</a>
      </div>
    </div>
    <div class="teaser-eye reveal"><img src="assets/img/argus/argus-embleem.png" alt="ARGUS Systems embleem" width="400" height="399" loading="lazy"></div>
  </div>
</section>

{contact_block('Q6')}
</main>
{footer()}'''


# ---------------------------------------------------------------- Projecten
# (slug, titel, plaats/jaar, rol, opdrachtgever, losse foto als er geen set is)
PROJECTS = [
    ('woeesj-stock', 'Woeësj-Stock', 'Simpelveld, 2026', 'Stage design · Lighting design · Programming · Live operation', 'Commissioned by GTF Franzen', None),
    ('sportclub-jubileum', 'Sportclub ’25 Jubileum', '2025', 'Stage &amp; lighting design · Visuals · Programming · Live operation · VJ', '', None),
    ('parkcity-live', 'Parkcity Live', 'Dance tent, 2026', 'Custom visual content · VJ', 'For WE-AV', None),
    ('electrisize', 'Electrisize', 'Main Stage &amp; Tapuya, 2026', 'LED systems · Infrastructure · Setup &amp; commissioning', 'For Djem LED Screens', 'electrisize.jpg'),
    ('carnaval-radio', 'Carnaval Radio', '', 'VJ · Programming · Live operation (licht)', 'For Heijnens Audio Light', None),
    ('paul-elstak', 'Complex × Paul Elstak', '', 'Programming · Live operation', 'For Stod', None),
    ('usc-lustrum', 'USC Lustrum', '', 'Programming · Live operation', 'For Spectrum AV', None),
    ('outrageous', 'Outrageous Festival', '2025', 'Programming · Live operation (licht)', 'For Bongers BLG', None),
    ('oranjeroes', 'OranjeRoes Festival', '', 'Programming · Live operation', 'With and for T.Y.S. Productions', None),
    ('fissafari', 'Fissafari', '2026', 'Programming · Live operation (licht)', 'For Bongers BLG', None),
    ('k3', 'K3', '2026', 'Programming · Live operation (licht)', 'For Bongers BLG', None),
    ('boiler-room', 'Boiler Room', 'Complex Maastricht, 2026', 'Programming · Live operation', '', 'boiler-room.jpg'),
    ('harmony', 'Harmony of Hardcore &amp; 7th Sunday', 'Hardnature · The High · Losjes, 2026', 'LED systems &amp; infrastructure', '', 'harmony-of-hardcore.jpg'),
]
SETS = json.loads((ROOT / 'src' / 'projects.json').read_text())


def year_of(meta):
    digits = [w.strip(',') for w in meta.split() if w.strip(',').isdigit() and len(w.strip(',')) == 4]
    return digits[-1] if digits else '—'


def projecten():
    rows, total = '', 0
    for i, (slug, t, meta, role, client, single) in enumerate(PROJECTS):
        if single:
            cover, photos = f'assets/img/{single}', [f'assets/img/{single}']
        else:
            cover = f'assets/img/proj/{slug}/cover.jpg'
            photos = [f'assets/img/proj/{slug}/{f}' for f, _, _ in SETS[slug]]
        total += len(photos)
        place = ', '.join(p for p in meta.split(', ') if not p.isdigit()) if meta else ''
        small = f'<small>{place}</small>' if place else ''
        label = f"{len(photos)} foto's" if len(photos) > 1 else '1 foto'
        rows += f'''
        <tr class="row" id="{slug}" data-title="{t}" data-cover="{cover}" data-gallery='{json.dumps(photos)}' tabindex="0">
          <td class="no">{i + 1:03d}<span class="thumb"><img src="{cover}" alt="" loading="lazy"></span></td>
          <td class="show"><strong>{t}</strong>{small}</td>
          <td class="role">{role}</td>
          <td class="client{'' if client else ' empty'}">{client or '—'}</td>
          <td class="yr">{year_of(meta)}</td>
          <td class="go"><button type="button" aria-label="Bekijk foto's van {t}">{label} →</button></td>
        </tr>'''
    sheet = '\n'.join(f'      <figure><img src="assets/img/galerij/{i:02d}.jpg" alt="" width="1400" height="933" loading="lazy"><figcaption><b>▸ {i:02d}A</b><span>Uit het veld</span></figcaption></figure>' for i in range(1, 13))
    return f'''{head("Projecten | MATRIX E.I.L.", "Het logboek van MATRIX E.I.L.: producties waar we licht, visuals en LED verzorgden.", "assets/img/electrisize.jpg")}
<body class="page-log">
{header('projecten.html')}
<main>
<section class="section page-top" data-cue="Q1" data-cue-name="Show log">
  <div class="wrap">
    {cue_head('Q1', 'Show log', '2024 – 2026')}
    <div class="log-head">
      <h1 class="display reveal">Show<br><em>log.</em></h1>
      <div class="reveal">
        <p class="lead">Elke regel een productie, elke productie een eigen opdracht. Klik op een show voor de foto's.</p>
        <div class="log-stats"><div><b>{len(PROJECTS)}</b><span>Producties</span></div><div><b>{total}</b><span>Foto's</span></div><div><b>’24–’26</b><span>Seizoenen</span></div></div>
      </div>
    </div>
    <table class="log reveal">
      <thead><tr><th>No.</th><th>Show</th><th>Rol</th><th>Voor</th><th>Jaar</th><th></th></tr></thead>
      <tbody>{rows}
      </tbody>
    </table>
  </div>
</section>

<section class="section quote-block" style="padding-top:0">
  <div class="wrap reveal">
    <blockquote>The hidden attunement is better than the open.</blockquote>
    <cite>Heraclitus</cite>
  </div>
</section>

<section class="section" style="padding-top:0" data-cue="Q2" data-cue-name="Contactvel">
  <div class="wrap">
    {cue_head('Q2', 'Uit het veld', 'Contactvel · 12 frames')}
    <div class="sheet gallery reveal">
{sheet}
    </div>
  </div>
</section>
{contact_block('Q3')}
</main>
{footer()}'''


# ---------------------------------------------------------------- Over
def over():
    return f'''{head("Over | MATRIX E.I.L.", "Over MATRIX E.I.L.: stage- en lichtontwerp, programmering, visuals en LED-techniek met aandacht voor het idee en de uitvoering.", "assets/img/over-matrix.jpg")}
<body class="page-rider">
{header('over.html')}
<main>
<section class="section page-top" data-cue="Q1" data-cue-name="Rider">
  <div class="wrap">
    {cue_head('Q1', 'Rider', 'Lees voor de show')}
    <article class="rider reveal">
      <div class="rider-head">
        <div><span>Productie</span><b>MATRIX E.I.L.</b></div>
        <div><span>Document</span><b>Rider · over ons</b></div>
        <div><span>Versie</span><b>2026 · rev. 3</b></div>
        <div><span>Pagina</span><b>1 / 1</b></div>
      </div>
      <div class="rider-title">
        <h1 class="title">Ieder moment verdient een <em>eigen verhaal.</em></h1>
        <div class="stamp">Gelezen<br>voor de show</div>
      </div>

      <div class="clause" data-cue="Q2" data-cue-name="§1 Oorsprong">
        <div class="no">Artikel<b>§1</b></div>
        <div class="body">
          <h2>Oorsprong</h2>
          <p>MATRIX E.I.L. begon vanuit de wens om zelfstandig te werken en als freelancer te groeien. Onderweg werd steeds duidelijker welke manier van werken daarbij hoort, en welke overtuiging daarachter zit.</p>
          <p>Ieder evenement verdient aandacht voor zijn eigen karakter. De plek, het publiek en de aanleiding vragen telkens om nieuwe afwegingen. Daar hoort een ontwerp bij waar gedachte en moeite in zitten.</p>
          <p>Vanuit die overtuiging verbindt MATRIX stage- en lichtontwerp, programmering, visuals en LED-techniek. Met aandacht voor het idee én voor de uitvoering.</p>
          <figure class="att unveil rm" style="margin:40px 0 0;max-width:620px"><img src="assets/img/over-matrix.jpg" alt="Operator aan de lichttafel in een MATRIX-shirt" width="822" height="637" loading="lazy"></figure>
          <p class="tag" style="margin-top:14px">Bijlage A · Aan de tafel</p>
        </div>
        <p class="note"><b>NB</b>De plek, het publiek en de aanleiding bepalen het ontwerp. Niet andersom.</p>
      </div>

      <div class="clause" data-cue="Q3" data-cue-name="§2 Werkwijze">
        <div class="no">Artikel<b>§2</b></div>
        <div class="body">
          <h2>Een ontwerp moet ergens <em>over gaan.</em></h2>
          <p>Een vertrouwde opstelling is snel gekozen. Toch verdient iedere productie opnieuw de vraag: waarom past dit hier?</p>
          <p>Voor MATRIX hoort die vraag bij het vak. Kijken naar de ruimte, mogelijkheden onderzoeken en verder denken dan de eerste oplossing. De beschikbare tijd en middelen geven grenzen aan; daarbinnen blijft ruimte voor bewuste keuzes.</p>
          <p>Een eenvoudige set kan precies goed zijn. Het verschil zit in de gedachte erachter. Waarom staat iets daar? Waar gaat de aandacht naartoe? Wat draagt het bij aan de ervaring?</p>
          <p>Licht, beeld en ruimte beïnvloeden elkaar. Duisternis kan een beweging betekenis geven. Een scherm kan diepte creëren, maar ook alle aandacht opeisen. De betekenis van een onderdeel ontstaat in samenhang met de rest.</p>
          <p class="big">Die samenhang verdient zorg, van de eerste schets tot de laatste cue.</p>
        </div>
        <p class="note"><b>Checklist</b>Waarom staat het daar?<br>Waar gaat de aandacht heen?<br>Wat voegt het toe?</p>
      </div>

      <div class="clause" data-cue="Q4" data-cue-name="Bijlage B · Reel">
        <div class="no">Bijlage<b>B</b></div>
        <div class="body">
          <div class="monitor">
            <video class="reel" src="assets/video/showreel.mp4" autoplay muted loop playsinline preload="auto" poster="assets/img/reel-poster.jpg" aria-label="Showreel met beelden van MATRIX-producties"></video>
            <div class="osd" aria-hidden="true"><span class="safe"></span><span class="rec">REC</span><span class="pgm">PGM</span><span class="tc">00:00:00:00</span><span class="src">CAM 1 · Showreel</span></div>
          </div>
          <div class="monitor-cap"><span>Programma-uitgang</span><span>Zonder geluid · 18 s loop</span></div>
        </div>
        <p class="note"><b>Monitor</b>Beelden uit het veld, van opbouw tot show.</p>
      </div>

      <div class="clause" data-cue="Q5" data-cue-name="§3 Samenwerking">
        <div class="no">Artikel<b>§3</b></div>
        <div class="body">
          <h2>Een eigen signatuur. <em>Meerdere perspectieven.</em></h2>
          <p>MATRIX heeft een persoonlijk begin. De ambitie is om vanuit die basis verder te bouwen met zelfstandige specialisten die hun eigen kennis, ideeën en oordeel meenemen.</p>
          <p>Een gedeelde overtuiging hoeft geen identieke blik op te leveren. Juist iemand die een andere vraag stelt, kan een ontwerp verder brengen. Daarvoor zijn vertrouwen, heldere afspraken en ruimte voor inhoudelijke discussie nodig.</p>
          <p class="big">Wat we willen delen, is betrokkenheid bij het resultaat. Begrijpen waarom een keuze wordt gemaakt. Aandacht hebben voor elkaars werk. En de moeite nemen om een idee zorgvuldig uit te voeren.</p>
        </div>
        <p class="note"><b>Open call</b>Zelfstandige specialist met een eigen blik? Neem contact op.</p>
      </div>
    </article>
  </div>
</section>
{contact_block('Q6')}
</main>
{footer()}'''


# ---------------------------------------------------------------- ARGUS
def eye_svg():
    """Het oog van Argus: honderd ogen in drie ringen rond een iris die de cursor volgt."""
    dots = []
    for radius, count, size in [(268, 44, 3.4), (232, 32, 2.8), (196, 24, 2.3)]:
        for k in range(count):
            a = 2 * math.pi * k / count + (radius % 7) * .1
            dots.append(f'<circle class="dot" cx="{300 + radius * math.cos(a):.1f}" cy="{300 + radius * math.sin(a):.1f}" r="{size}"/>')
    return f'''<svg class="eye" viewBox="0 0 600 600" aria-hidden="true">
      <defs><radialGradient id="irisG"><stop offset="0" stop-color="#3ccbe0" stop-opacity=".9"/><stop offset=".45" stop-color="#d9ad4f" stop-opacity=".85"/><stop offset="1" stop-color="#1a140a"/></radialGradient></defs>
      <circle class="ring dash" cx="300" cy="300" r="292"/>
      <circle class="ring" cx="300" cy="300" r="250"/>
      <circle class="ring dash2" cx="300" cy="300" r="214"/>
      {''.join(dots)}
      <path class="lid" d="M120,300 Q300,140 480,300 Q300,460 120,300 Z"/>
      <g class="pupil-g"><circle class="iris" cx="300" cy="300" r="74"/><circle class="pupil" cx="300" cy="300" r="30"/><circle class="glint" cx="314" cy="286" r="6"/></g>
    </svg>'''


def argus():
    tools = (ROOT / 'src' / 'argus-tools.html').read_text()
    return f'''{head("ARGUS Systems | MATRIX E.I.L.", "ARGUS Systems is de softwaretak van MATRIX E.I.L.: CHRONOS, AXIS, METRON en HOROS, tools gebouwd vanuit de praktijk van live producties.", "assets/img/chronos-overzicht.jpg", "assets/img/argus/favicon.png")}
<body class="argus-page">
{header('argus.html')}
<main>
<section class="ar-hero" data-cue="Q1" data-cue-name="Het oog">
  <div class="wrap">
    <div>
      <img class="logo-ar reveal" src="assets/img/argus/argus-systems.png" alt="ARGUS Systems" width="1200" height="390">
      <h1 class="reveal">Honderd ogen.<br><em>Eén show.</em></h1>
      <p class="myth reveal">Argus Panoptes, de wachter met honderd ogen, sliep nooit met alle ogen tegelijk. Er keek er altijd wel één. Dat is precies wat een productie nodig heeft.</p>
    </div>
    <div class="eye-wrap reveal">
      {eye_svg()}
      <div class="eye-cap"><b>100</b> ogen · <span class="open-count">100</span> open</div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:clamp(40px,6vw,90px)" data-cue="Q2" data-cue-name="Systeemstart">
  <div class="wrap">
    {cue_head('Q2', 'Systeemstart', 'argus://boot')}
    <div class="why">
      <div class="boot reveal" aria-label="Status van de ARGUS-tools">
        <div class="bar"><i></i><i></i><i></i><span>argus — regie</span></div>
        <pre class="boot-out"></pre>
      </div>
      <div class="reveal">
        <p class="lead">Op de vloer zien we elke week waar het schuurt.</p>
        <p>Timetables die niet meer kloppen. Planningen verspreid over losse lijstjes. Informatie die net te laat aankomt. Tappen op een knop terwijl je eigenlijk de show wilt vormgeven.</p>
        <p>ARGUS Systems bouwt de software die we zelf misten. Niet achter een bureau, maar tussen de cases, op echte producties, door de mensen die er elke dag mee werken. Elke tool wordt eerst in het veld getest voordat hij verder gaat.</p>
      </div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0" data-cue="Q3" data-cue-name="Roadmap">
  <div class="wrap">
    {cue_head('Q3', 'Ontwikkeling', 'Status 2026')}
    <h2 class="title reveal">Van idee<br>naar <em>het veld.</em></h2>
    <div class="roadmap reveal">
      <span class="prog"></span>
      <div class="stage done"><div class="pt"></div><h4>Concept</h4><p>Een probleem dat we op de vloer zelf tegenkwamen.</p></div>
      <div class="stage done"><div class="pt"></div><h4>Bouw</h4><p>Eerste versies, gebouwd rond hoe een productie echt loopt.</p></div>
      <div class="stage now"><div class="pt"></div><h4>Test</h4><p>Intern en met operators uittesten en bijschaven.</p><div class="who"><span>AXIS</span><span>METRON</span><span>HOROS</span></div></div>
      <div class="stage now"><div class="pt"></div><h4>Alpha in het veld</h4><p>Draaien op echte evenementen, onder echte druk.</p><div class="who"><span class="f">CHRONOS</span></div></div>
      <div class="stage"><div class="pt"></div><h4>Release</h4><p>Beschikbaar voor andere producties en operators.</p></div>
    </div>
  </div>
</section>

{tools}
<section class="section argus-cta" id="contact" data-cue="Q8" data-cue-name="Meedoen">
  <div class="wrap">
    <div class="reveal">
      {cue_head('Q8', 'Meedoen', 'Testers gezocht')}
      <h2 class="title">Zet ARGUS in op<br><em>jouw productie.</em></h2>
    </div>
    <div class="reveal">
      <p>Wil je een van onze tools testen op jouw evenement, of heb je een idee dat hier past? Operators en producties die mee willen bouwen, horen we graag.</p>
      <a class="btn" href="mailto:{MAIL}?subject=ARGUS%20Systems">Neem contact op</a>
    </div>
  </div>
</section>
</main>
{footer(chr(10) + '<script src="assets/js/argus.js"></script>')}'''


# ---------------------------------------------------------------- Privacy
def privacy():
    return f'''{head("Privacy | MATRIX E.I.L.", "Privacyverklaring van MATRIX E.I.L.")}
<body>
{header('privacy.html')}
<main>
<section class="section page-top" data-cue="Q1" data-cue-name="Privacy">
  <div class="wrap narrow prose">
    <span class="tag"><b>§</b> Privacy</span>
    <h2>Privacy</h2>
    <p>MATRIX E.I.L. verzamelt via deze website geen persoonsgegevens. Er worden geen tracking- of advertentiecookies gebruikt. Neem je contact op via e-mail of telefoon, dan gebruiken we je gegevens alleen om je bericht te beantwoorden.</p>
    <p>Lettertypen worden geladen via Google Fonts. Daarbij wordt je IP-adres door Google verwerkt.</p>
    <p>Vragen over privacy? Mail naar <a href="mailto:{MAIL}">{MAIL}</a>.</p>
  </div>
</section>
<div id="contact"></div>
</main>
{footer()}'''


PAGES = {'index.html': home, 'projecten.html': projecten, 'over.html': over, 'argus.html': argus, 'privacy.html': privacy}

if __name__ == '__main__':
    for name, fn in PAGES.items():
        (ROOT / name).write_text(fn())
        print('gebouwd:', name)
