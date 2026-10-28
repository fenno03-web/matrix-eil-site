#!/usr/bin/env python3
"""Bouwt de HTML-pagina's van de site uit gedeelde onderdelen. Draai: python3 build.py"""
import hashlib
import json
import math
from pathlib import Path

from src.showlog import SHOWLOG, HIGHLIGHTS, press_for
from src.stories import STORIES

ROOT = Path(__file__).parent
MAIL = 'info@matrixeventsupport.nl'
TEL = '+31630971404'
TEL_TXT = '+31 6 30971404'
INSTA = 'https://www.instagram.com/matrix.eil/'
WHATSAPP = 'https://wa.me/31630971404'
# Zet op 'https://matrixeil.nl/' zodra het domein aan GitHub Pages hangt
BASE = 'https://fenno03-web.github.io/matrix-eil-site/'
CURRENT = 'index.html'

QUOTES = [
    ('Niemand stapt twee keer in dezelfde rivier.', 'Heraclitus'),
    ('Alles stroomt.', 'Heraclitus'),
    ('De weg omhoog en de weg omlaag zijn één en dezelfde.', 'Heraclitus'),
    ('Karakter is lotsbestemming.', 'Heraclitus'),
    ('De verborgen harmonie is sterker dan de zichtbare.', 'Heraclitus'),
    ('Wie het onverwachte niet verwacht, zal het niet vinden.', 'Heraclitus'),
    ('De zon is elke dag nieuw.', 'Heraclitus'),
    ('Execution is the chariot of genius.', 'William Blake'),
]

FONTS = ('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500'
         '&family=Space+Grotesk:wght@300;400;500;600;700&display=swap')

def ver(path):
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


NAV = [('diensten.html', 'Diensten'), ('projecten.html', 'Projecten'), ('operators.html', 'Operators'), ('over.html', 'Over'), ('argus.html', 'Argus')]
PORTAL = '<div class="portal" aria-hidden="true"><div class="void"></div><div class="ring"></div></div>'


ORG = {
    '@context': 'https://schema.org', '@type': 'ProfessionalService', '@id': BASE + '#matrix',
    'name': 'MATRIX E.I.L.', 'url': BASE, 'logo': BASE + 'assets/img/logo-matrix.png', 'image': BASE + 'assets/img/hero.jpg',
    'description': 'Stage- en lichtontwerp, lichtprogrammering en live operation, VJ en visual content en LED-infrastructuur voor festivals en evenementen.',
    'email': MAIL, 'telephone': TEL, 'areaServed': {'@type': 'Country', 'name': 'Nederland'},
    'sameAs': [INSTA], 'knowsAbout': ['Lichtontwerp', 'Stage design', 'Lichtprogrammering', 'Live operation', 'VJ', 'Visual content', 'LED-schermen'],
}


def crumbs(*items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': BASE + (u if u != 'index.html' else '')} for i, (n, u) in enumerate((('Home', 'index.html'),) + items)]}


def head(title, desc, image='assets/img/hero.jpg', icon='assets/img/favicon.png', ld=None):
    url = BASE + ('' if CURRENT == 'index.html' else CURRENT)
    ld = ld if ld is not None else [ORG]
    ld_html = ''.join(f'\n<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f'''<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="MATRIX E.I.L.">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{BASE}{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#050505">
<link rel="icon" href="{icon}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/css/style.css?v={ver('assets/css/style.css')}">{ld_html}
</head>'''


def header(current):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{href}"{cur if href == current else ""}>{label}</a>' for href, label in NAV)
    portal_in = '<div class="portal-in" aria-hidden="true"></div>\n' if current == 'argus.html' else ''
    return f'''{portal_in}{PORTAL}
<div class="standby" aria-hidden="true"><div class="sb">Standby<b class="go">GO</b></div></div>
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
    <p class="foot-quote" title="Klik voor een nieuwe quote"><span>{QUOTES[0][0]}</span> <cite>{QUOTES[0][1]}</cite></p>
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="assets/img/logo-matrix.png" alt="MATRIX E.I.L." width="600" height="179" loading="lazy">
        <p>Execution is the chariot of genius.</p>
      </div>
      <div>
        <h4>Diensten</h4>
        <ul>{''.join(f'<li><a href="{d["slug"]}.html">{d["short"]}</a></li>' for d in DIENSTEN)}</ul>
      </div>
      <div>
        <h4>Pagina's</h4>
        <ul><li><a href="projecten.html">Projecten</a></li><li><a href="over.html">Over</a></li><li><a href="operators.html">Operators</a></li><li><a href="voor-festivals.html">Festivals</a></li><li><a href="voor-carnaval.html">Carnaval</a></li><li><a href="voor-verenigingen.html">Verenigingen</a></li><li><a href="faq.html">FAQ</a></li><li><a href="woordenlijst.html">Woordenlijst</a></li><li><a href="argus.html">Argus Systems</a></li></ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul><li><a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li><a href="tel:{TEL}">{TEL_TXT}</a></li><li><a href="{INSTA}" target="_blank" rel="noopener">Instagram</a></li></ul>
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
<script src="assets/js/main.js?v={ver('assets/js/main.js')}"></script>{extra_js}
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
      <h2 class="display">Plan je volgende<br><em>editie met ons.</em></h2>
      <p class="lead contact-lead">Werk je aan een festival of evenement en zoek je één partij voor het complete visuele plaatje? Stuur een app of mail, dan denken we vrijblijvend mee.</p>
      <div class="contact-links">
        <a class="wa" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp · {TEL_TXT}</a>
        <a href="mailto:{MAIL}">{MAIL}</a>
        <a class="ig" href="{INSTA}" target="_blank" rel="noopener">Instagram · @matrix.eil</a>
      </div>
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- Home
WORK = [
    ('proj/woeesj-stock/01.jpg', 1600, 1067, 'Woeësj-Stock', 'Simpelveld, 2026', 'woeesj-stock',
     'Stage design · Lighting design<br>Programming · Live operation<br>Commissioned by GTF Franzen Sound Light Vision'),
    ('electrisize.jpg', 1345, 745, 'Electrisize', 'Main Stage &amp; Tapuya, 2026', 'electrisize',
     'LED systems · Infrastructure<br>Setup &amp; commissioning<br>For Djem LED Screens'),
    ('proj/parkcity-live/01.jpg', 1600, 1067, 'ParkCity Live', 'Dance tent, 2026', 'parkcity-live',
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
        <a class="work-media unveil rm" href="project-{slug}.html"><img src="assets/img/{img}" alt="{t}" width="{w}" height="{h}" loading="lazy"></a>
        <div class="work-copy reveal">
          <span class="cueno">Q2.{i + 1}</span>
          <h3>{t}</h3>
          <span class="meta">{meta}</span>
          <p class="disc">{disc}</p>
          <a class="link-arrow" href="project-{slug}.html">Bekijk project</a>
        </div>
      </article>''' for i, (img, w, h, t, meta, slug, disc) in enumerate(WORK))
    ticks = ''.join(f'<span>{n}</span>' for n in ['+10', '0', '-10', '-20', '-∞'])
    desk = ''.join(f'''
      <a class="ch reveal" href="{DIENSTEN[i]['slug']}.html" style="--v:{v}%">
        <div class="ph" aria-hidden="true"><img src="assets/img/{img}" alt="" loading="lazy"></div>
        <div class="top"><span>CH <b>{i + 1:02d}</b></span><span>{v}%</span></div>
        <div class="fader" aria-hidden="true"><div class="ticks">{ticks}</div><div class="lvl"></div><div class="knob"></div></div>
        <h3>{t}</h3>
        <p>{d}</p>
        <span class="ch-more">Meer over {DIENSTEN[i]['short'].lower()} →</span>
      </a>''' for i, (img, t, d, v) in enumerate(EXPERTISE))
    ticker = ''.join(f'<span>{t}</span><i>GO</i>' for _, t, _, _ in EXPERTISE) * 2
    steps = ''.join(f'''
      <li class="reveal"><span class="sn">0{i + 1}</span><h3>{t}</h3><p>{d}</p></li>''' for i, (t, d) in enumerate(STEPS))
    clients = ''.join(f'<li>{c}</li>' for c in CLIENTS)
    names = ''.join(f'<li>{n}</li>' for n in HIGHLIGHTS)
    strip = ''.join(f'<img src="assets/img/galerij/{n:02d}.jpg" alt="" width="1400" height="933" loading="lazy">' for n in [2, 3, 6, 7, 8, 9, 11, 12])
    return f'''{head("MATRIX E.I.L. | Stage, licht, visuals en LED", "MATRIX E.I.L. verzorgt stage- en lichtontwerp, programmering, live operation, VJ en LED-techniek voor live producties.")}
<body class="home">
<span class="visually-hidden">MATRIX E.I.L.: lichtontwerp, lichtprogrammering, VJ en LED voor festivals en evenementen.</span>
{header('index.html')}
<main>
<section class="hero" data-cue="Q1" data-cue-name="Opening">
  <img class="hero-bg" src="assets/img/hero.jpg" alt="" fetchpriority="high">
  <img class="hero-lit" src="assets/img/hero.jpg" alt="" aria-hidden="true">
  <h1 class="hero-h1"><img class="hero-tekst" src="assets/img/hero-tekst.png" alt="Execution is the chariot of genius." width="1600" height="518"><span class="blake" aria-hidden="true">— William Blake</span></h1>
  <div class="hud">
    <span class="tl">Q1 · <b>Opening</b></span>
    <span class="tr">Scene <b>01</b> / 06</span>
  </div>
  <div class="hero-pitch wrap">
    <p>Het complete visuele plaatje voor festivals en evenementen. Van lichtontwerp tot laatste cue.</p>
    <div class="btns"><a class="btn fill" href="#contact">Plan een gesprek</a><a class="btn" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a></div>
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

<section class="section" style="padding-top:0">
  <div class="wrap">
    {cue_head('Q3.5', 'Zo werken we', 'Voor organisaties')}
    <div class="intro-line">
      <h2 class="title reveal">Eén partij,<br><em>één beeld.</em></h2>
      <p class="lead reveal">Ontwerp, programmering, visuals en LED in één hand. Dat scheelt afstemming, en het beeld op je podium vertelt één verhaal.</p>
    </div>
    <ol class="steps">{steps}
    </ol>
    <div class="clients names reveal">
      <span class="tag">Gewerkt op o.a.</span>
      <ul>{names}</ul>
      <a class="link-arrow" href="projecten.html#showlog">{len(SHOWLOG)} producties sinds 2022</a>
    </div>
    <div class="clients reveal">
      <span class="tag">Ingehuurd door en samengewerkt met</span>
      <ul>{clients}</ul>
    </div>
  </div>
</section>

<section class="photo-break" data-cue="Q4" data-cue-name="Manifest">
  <img src="assets/img/saloon.jpg" alt="Festivalpodium met licht, rook en publiek" width="2400" height="1600" loading="lazy">
  <canvas class="embers" aria-hidden="true"></canvas>
  <div class="wrap"><span class="tag reveal"><b>Q4</b> · Manifest</span><h2 class="reveal">Het bestaat<br>maar <em>even.</em></h2>
    <p class="fire-quote reveal">“Zij was altijd, is en zal zijn: een eeuwig levend vuur.”<cite>Heraclitus</cite></p></div>
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
        <p>ARGUS Systems is de softwaretak van MATRIX, vernoemd naar Argus Panoptes, de wachter met honderd ogen. Elf tools voor licht, video en productie, gebouwd op de vloer en getest waar het telt: live, in het veld.</p>
        <div class="chips"><span>CHRONOS</span><span>BIFROST</span><span>IRIS</span><span class="t">AXIS</span><span class="t">METRON</span><span class="t">HOROS</span><span class="t">KANON</span><span class="t">+4</span></div>
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
    ('woeesj-stock', 'Woeësj-Stock', 'Simpelveld, 2026', 'Stage design · Lighting design · Programming · Live operation', 'Commissioned by GTF Franzen Sound Light Vision', None),
    ('sportclub-jubileum', 'Sportclub’25', '100 jaar jubileum, Bocholtz, 2025', 'Stage &amp; lighting design · Visuals · Programming · Live operation · VJ', 'Commissioned by GTF Franzen Sound Light Vision', None),
    ('parkcity-live', 'ParkCity Live', 'Dance tent, 2026', 'Custom visual content · VJ', 'For WE-AV', None),
    ('electrisize', 'Electrisize', 'Main Stage &amp; Tapuya, 2026', 'LED systems · Infrastructure · Setup &amp; commissioning', 'For Djem LED Screens', 'electrisize.jpg'),
    ('carnaval-radio', 'Carnaval Radio', '', 'VJ · Programming · Live operation (licht)', 'For Heijnens Audio - Light - Vision', None),
    ('paul-elstak', 'Complex × Paul Elstak', '', 'Programming · Live operation', 'For Stod', None),
    ('usc-lustrum', 'USC Lustrum', '2026', 'Programming · Live operation', 'For Spectrum AV', None),
    ('outrageous', 'Outrageous Festival', 'Mainstage, 2025', 'Programming · Live operation (licht)', 'For Bongers BLG', None),
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
        <tr class="row" id="{slug}" data-title="{t}" data-cover="{cover}" data-href="project-{slug}.html" tabindex="0">
          <td class="no">{i + 1:03d}<span class="thumb"><img src="{cover}" alt="" loading="lazy"></span></td>
          <td class="show"><a href="project-{slug}.html"><strong>{t}</strong></a>{small}</td>
          <td class="role">{role}</td>
          <td class="client{'' if client else ' empty'}">{client or '—'}</td>
          <td class="yr">{year_of(meta)}</td>
          <td class="go"><span class="btnlike">{label} →</span></td>
        </tr>'''
    pages = {slug for slug, *_ in PROJECTS}
    years = []
    for span, show, role, client, slug in SHOWLOG:
        y = span[:4]
        url = press_for(y, show)
        if url:
            role += f' <a class="sl-press" href="{url}" target="_blank" rel="noopener">Artikel op Highlite ↗</a>'
        if len(span) > 4:
            show += f' <small>({span})</small>'
        if not years or years[-1][0] != y:
            years.append((y, []))
        years[-1][1].append((show, role, client, slug))
    log = ''
    for y, items in reversed(years):
        lis = ''
        for show, role, client, slug in items:
            name = f'<a href="project-{slug}.html">{show} <span aria-hidden="true">→</span></a>' if slug in pages else show
            lis += f'''
          <li><span class="sl-show">{name}</span><span class="sl-role">{role}</span><span class="sl-client">{client or '—'}</span></li>'''
        log += f'''
      <div class="sl-year reveal">
        <h3><b>{y}</b><span>{len(items)} {'productie' if len(items) == 1 else 'producties'}</span></h3>
        <ul>{lis}
        </ul>
      </div>'''
    sheet = '\n'.join(f'      <figure><img src="assets/img/galerij/{i:02d}.jpg" alt="" width="1400" height="933" loading="lazy"><figcaption><b>▸ {i:02d}A</b><span>Uit het veld</span></figcaption></figure>' for i in range(1, 13))
    return f'''{head("Projecten | MATRIX E.I.L.", f"Het logboek van MATRIX E.I.L.: {len(SHOWLOG)} producties sinds 2022, van Paaspop en Pinkpop tot Decibel Outdoor en Electrisize. Lichtontwerp, programmering, visuals en LED.", "assets/img/electrisize.jpg")}
<body class="page-log">
{header('projecten.html')}
<main>
<section class="section page-top" data-cue="Q1" data-cue-name="Show log">
  <div class="wrap">
    {cue_head('Q1', 'Show log', '2022 – 2026')}
    <div class="log-head">
      <h1 class="display reveal">Show<br><em>log.</em></h1>
      <div class="reveal">
        <p class="lead">Elke regel een productie, elke productie een eigen opdracht. Hieronder een selectie met foto's, daarna het volledige logboek sinds 2022.</p>
        <div class="log-stats"><div><b>{len(SHOWLOG)}</b><span>Producties</span></div><div><b>{total}</b><span>Foto's</span></div><div><b>’22–’26</b><span>Seizoenen</span></div></div>
      </div>
    </div>
    <table class="log reveal">
      <thead><tr><th>No.</th><th>Show</th><th>Rol</th><th>Voor</th><th>Jaar</th><th></th></tr></thead>
      <tbody>{rows}
      </tbody>
    </table>
  </div>
</section>

<section class="section" id="showlog" style="padding-top:0" data-cue="Q1.5" data-cue-name="Volledig log">
  <div class="wrap">
    {cue_head('Q1.5', 'Volledig log', f'{len(SHOWLOG)} producties')}
    <div class="intro-line">
      <h2 class="title reveal">Het hele<br><em>logboek.</em></h2>
      <p class="lead reveal">Van ontwerp tot een avond achter de tafel: alles wat we sinds 2022 draaiden, per seizoen. Per productie staat erbij wat onze rol was.</p>
    </div>
    <div class="showlog">{log}
    </div>
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
      <defs><radialGradient id="irisG"><stop offset="0" stop-color="#3ccbe0" stop-opacity=".9"/><stop offset=".45" stop-color="#d9ad4f" stop-opacity=".85"/><stop offset="1" stop-color="#1a140a"/></radialGradient><clipPath id="lidClip"><path d="M120,300 Q300,140 480,300 Q300,460 120,300 Z"/></clipPath></defs>
      <circle class="ring dash" cx="300" cy="300" r="292"/>
      <circle class="ring" cx="300" cy="300" r="250"/>
      <circle class="ring dash2" cx="300" cy="300" r="214"/>
      {''.join(dots)}
      <path class="lid" d="M120,300 Q300,140 480,300 Q300,460 120,300 Z"/>
      <g clip-path="url(#lidClip)"><g class="pupil-g"><circle class="iris" cx="300" cy="300" r="74"/><circle class="pupil" cx="300" cy="300" r="30"/><circle class="glint" cx="314" cy="286" r="6"/></g></g>
    </svg>'''


# ---------------------------------------------------------------- ARGUS OS
# (slug, naam, logo, status, statusklasse, kernzin, uitleg, punten, accentkleur, demo-markup of None)
ARGUS_TOOLS = [
    ('chronos', 'CHRONOS', 'chronos.png', 'Alpha · in het veld', 'field', 'Eén klok voor de hele productie.',
     'Regie, backstage, kleedkamers en FOH zien live dezelfde tijd, op elk scherm en zonder internet.',
     ['Alle stages naast elkaar, met uitloop en curfew', 'Schermen voor backstage en kleedkamers', 'Volledig offline'], 'petrol', None),
    ('axis', 'AXIS', 'axis.png', 'In test', 'test', 'Planning, magazijn en show in één systeem.',
     'Een modulair platform voor de evenementenbranche: van planning en materiaal tot schermen en accreditatie.',
     ['Planning &amp; magazijn', 'LIVE: schermen en zones aansturen', 'Accreditatie, ook voor kleinere events'], 'gold', None),
    ('metron', 'METRON', 'metron.jpg', 'In test', 'test', 'Licht dat de beat kent.',
     'Tempo en positie in de track rechtstreeks van de DJ-set naar je licht, zodat effecten en drops vanzelf kloppen.',
     ['BPM en beatpositie live binnen', 'Tempo naar je speedmasters', 'Markers voor drops en breaks'], 'gold', None),
    ('horos', 'HOROS', 'horos.png', 'In test', 'test', 'Navigatie die weet hoe hoog je truck is.',
     'Op basis van RDW-data waarschuwt HOROS voor milieuzones en bruggen of viaducten waar je niet onderdoor past.',
     ['Milieuzones op je route', 'Doorrijhoogte per brug en viaduct', 'Live route, locatiecheck en routecheck'], 'gold', None),
    ('bifrost', 'BIFROST', 'bifrost.webp', 'In ontwikkeling · live testing', 'live', 'De brug tussen consoles, met een wachter die meekijkt.',
     'BIFROST verbindt lichttafels met elkaar en houdt tijdens de show alles in de gaten. Heimdall, de ingebouwde AI-assistent, ziet afwijkingen meteen en helpt je op het moment dat het telt.',
     ['Console bridge tussen tafels', 'Wachter die de show bewaakt', 'Heimdall AI als hulp naast de tafel'], 'petrol', 'bifrost'),
    ('visual', 'VISUAL INTELLIGENCE', 'visual-intelligence.webp', 'In ontwikkeling', 'dev', 'Richt je lampen vanaf de vloer.',
     'Positioneer lampen op locatie draadloos met een handheld, zoals een MSI Claw. Je wijst aan waar het licht moet komen en de lampen volgen. Dat maakt programmeren sneller en preciezer.',
     ['Draadloos vanaf een handheld', 'Lampen richten door aan te wijzen', 'Sneller posities en focus programmeren'], 'petrol', 'visual'),
    ('hyperion', 'HYPERION', 'hyperion.webp', 'Concept', 'concept', 'Een lichttafel in je laptop.',
     'Voor kleine evenementen zonder budget voor een echte lichttafel of lichtontwerper. HYPERION leest MVR-bestanden en maakt van een pc of laptop een overzichtelijke lichttool.',
     ['MVR-bestanden inlezen', 'Draait op een gewone pc of laptop', 'Gemaakt voor kleine events'], 'magenta', 'hyperion'),
    ('treehouse', 'TREEHOUSE', 'treehouse.webp', 'Vroege ontwikkeling', 'dev', 'Macro’s voor de Infinity Chimp.',
     'Een macrotool voor de Infinity Chimp G2 en G3 van Highlite. Bouw een reeks handelingen één keer op en roep die daarna aan met één druk.',
     ['Voor Infinity Chimp G2 en G3', 'Macro’s overzichtelijk in een boom', 'Eén druk in plaats van tien'], 'petrol', 'treehouse'),
    ('tartarus', 'TARTARUS', 'tartarus.webp', 'Vroege ontwikkeling', 'dev', 'De kluis voor je showfiles.',
     'TARTARUS spoort showfiles op, zet ze veilig weg en sorteert en filtert ze, zodat je altijd de nieuwste versie pakt. Volledig offline.',
     ['Vindt showfiles op al je schijven', 'Sorteert per show en filtert op nieuwste versie', 'Volledig offline'], 'red', 'tartarus'),
    ('kanon', 'KANON', 'kanon.webp', 'Vroege ontwikkeling · binnenkort live testing', 'dev', 'Volgspots die zelf volgen.',
     'Tracking op basis van camerabeeld voor live events. KANON herkent waar de artiest staat en laat het licht meebewegen.',
     ['Tracking op basis van camerabeeld', 'Lampen volgen de artiest live', 'Gemaakt voor podium en tent'], 'petrol', 'kanon'),
    ('iris', 'IRIS', 'iris.webp', 'Vroege ontwikkeling · live testing', 'live', 'Stream Deck en Resolume, direct verbonden.',
     'Een directe koppeling van Stream Deck naar Resolume. Veel sneller en overzichtelijker dan een tussenlaag, met thumbnails die live terugkomen uit Resolume op je knoppen.',
     ['Directe koppeling, geen tussenlaag', 'Live thumbnails uit Resolume op de knoppen', 'Overzichtelijk ingedeeld per laag'], 'petrol', 'iris'),
]
DEMO_HINT = '<p class="aw-hint">Impressie · geen echte software</p>'


def aos_demo(kind):
    if kind == 'bifrost':
        return '''<div class="bf">
          <canvas class="bf-cv" width="560" height="170" aria-hidden="true"></canvas>
          <ol class="bf-log" aria-live="polite"></ol>
          <form class="bf-ask"><label class="visually-hidden" for="bf-q">Vraag Heimdall</label><input id="bf-q" autocomplete="off" placeholder="Vraag Heimdall iets, bijv. “hoe staat de backup?”"><button>Vraag</button></form>
          <div class="bf-ans"></div>
        </div>'''
    if kind == 'visual':
        return '''<div class="vi"><canvas class="vi-cv" width="560" height="300" aria-label="Bovenaanzicht van een podium: tik om de lampen te richten"></canvas>
          <div class="vi-read"><span>Doel <b class="vi-xy">—</b></span><span>Lampen <b>6 / 6</b></span><span>Verbinding <b class="ok">draadloos</b></span></div></div>'''
    if kind == 'hyperion':
        return '''<div class="hy"><div class="hy-file">showfile.mvr <b>· 24 fixtures · 3 trussen</b></div>
          <canvas class="hy-cv" width="560" height="250" aria-hidden="true"></canvas>
          <div class="hy-scenes"><button data-s="warm" class="on">Warm</button><button data-s="koel">Koel</button><button data-s="chase">Chase</button><button data-s="blind">Blinders</button></div></div>'''
    if kind == 'treehouse':
        return '''<div class="th"><ul class="th-tree">
            <li><span>Show</span><ul><li><button data-m="Opening">Opening</button></li><li><button data-m="Drop">Drop</button></li><li><button data-m="Blackout">Blackout</button></li></ul></li>
            <li><span>Programmeren</span><ul><li><button data-m="Kleurpalet">Kleurpalet</button></li><li><button data-m="Fan-out">Fan-out</button></li><li><button data-m="Wis alles">Wis alles</button></li></ul></li>
          </ul><pre class="th-out">Kies een macro.</pre></div>'''
    if kind == 'tartarus':
        return '''<div class="ta"><div class="ta-bar"><button class="ta-go">Scan opnieuw</button><span class="ta-st">Klaar</span></div>
          <div class="ta-cols"><ul class="ta-found"></ul><div class="ta-vault"></div></div></div>'''
    if kind == 'kanon':
        return '''<div class="ka"><canvas class="ka-cv" width="560" height="280" aria-hidden="true"></canvas>
          <div class="ka-bar"><button class="on" data-mode="auto">Volgen</button><button data-mode="hand">Handmatig</button><span>Lock <b class="ka-conf">98%</b></span></div></div>'''
    if kind == 'iris':
        keys = ''.join(f'<button class="ir-k" data-i="{i}" style="--h:{(i * 37) % 360}"><i></i><span>{n}</span></button>'
                       for i, n in enumerate(['Intro', 'Tunnel', 'Strobe', 'Logo', 'Nebula', 'Glitch', 'Lines', 'Fire', 'Drop', 'Smoke', 'Grid', 'Out', 'BPM', 'Flash', 'Black']))
        return f'''<div class="ir"><div class="ir-deck">{keys}</div>
          <div class="ir-out"><div class="ir-prev"><i></i><span class="ir-name">Black</span></div><div class="ir-read"><span>Resolume <b class="ok">verbonden</b></span><span>Reactietijd <b class="ir-ms">—</b></span></div></div></div>'''
    return ''


def aos_templates():
    out = ''
    for slug, name, logo, status, cls, line, desc, pts, acc, demo in ARGUS_TOOLS:
        lis = ''.join(f'<li>{p}</li>' for p in pts)
        body = (aos_demo(demo) + DEMO_HINT) if demo else f'<ul class="aw-pts">{lis}</ul><a class="btn aw-go" href="#{slug}">Naar de live demo ↓</a>'
        out += f'''
<template id="tpl-{slug}"><section class="win tool-win acc-{acc}" data-win="{slug}" aria-label="{name}">
  <div class="win-bar"><span class="win-dots"><button class="win-x" aria-label="Sluit {name}"></button><i></i><i></i></span><b>{name}</b><span class="st st-{cls}">{status}</span></div>
  <div class="win-body"><img class="aw-logo" src="assets/img/argus/{logo}" alt="ARGUS {name}" loading="lazy"><p class="aw-line">{line}</p>{body}</div>
</section></template>'''
    return out


def aos_html():
    dock = ''.join(f'<button class="dk acc-{acc}" data-open="{slug}" title="{name} · {status}"><span class="dk-g">{name[0]}</span><span class="dk-n">{name.title() if len(name) > 8 else name}</span><i class="dot st-{cls}"></i></button>'
                   for slug, name, logo, status, cls, *_ , acc, demo in ARGUS_TOOLS)
    return f'''<div class="aos reveal" id="os">
      <div class="aos-top"><img src="assets/img/argus/favicon.png" alt="" width="18" height="18"><b>ARGUS OS</b><span class="aos-v">build 0.11 · {len(ARGUS_TOOLS)} tools</span><span class="aos-sp"></span><span class="aos-eyes">ogen <b>100</b>/100</span><span class="aos-clock">--:--:--</span></div>
      <div class="aos-body">
        <nav class="aos-dock" aria-label="Tools in ARGUS OS">{dock}<button class="dk dk-t" data-open="terminal"><span class="dk-g">&gt;_</span><span class="dk-n">Terminal</span></button></nav>
        <div class="aos-desk">
          <img class="aos-mark" src="assets/img/argus/argus-embleem.png" alt="" aria-hidden="true">
          <section class="win term" data-win="terminal" aria-label="ARGUS terminal">
            <div class="win-bar"><span class="win-dots"><button class="win-x" aria-label="Sluit terminal"></button><i></i><i></i></span><b>argus — terminal</b><span class="st">tty1</span></div>
            <div class="win-body term-body"><div class="term-out" aria-live="polite"></div><form class="term-line"><label for="term-in">argus@matrix:~$</label><input id="term-in" autocomplete="off" spellcheck="false" aria-label="Typ een commando"></form></div>
          </section>
        </div>
      </div>
      <div class="aos-task"><span class="aos-hint">Klik op een tool, of typ <b>help</b> in de terminal</span><span class="aos-wins"></span></div>
    </div>
    {aos_templates()}'''


def argus_cards():
    cards = ''
    for slug, name, logo, status, cls, line, desc, pts, acc, demo in ARGUS_TOOLS[4:]:
        lis = ''.join(f'<li>{p}</li>' for p in pts)
        cards += f'''
      <article class="ac acc-{acc} reveal" id="{slug}">
        <div class="ac-logo"><img src="assets/img/argus/{logo}" alt="ARGUS {name}" loading="lazy"></div>
        <span class="st st-{cls}">{status}</span>
        <h3>{line}</h3>
        <p>{desc}</p>
        <ul>{lis}</ul>
        <button class="btn ac-open" data-open="{slug}">Open in ARGUS OS</button>
      </article>'''
    return cards + '''
      <article class="ac ac-next reveal">
        <div class="ac-logo"><img src="assets/img/argus/argus-embleem.png" alt="" loading="lazy"></div>
        <span class="st">Volgende</span>
        <h3>Het twaalfde oog?</h3>
        <p>Loop je op de vloer tegen iets aan waar nog geen goede tool voor is? Vertel het ons. De beste ideeën komen uit het veld.</p>
        <a class="btn" href="#contact">Deel je idee</a>
      </article>'''


def argus():
    tools = (ROOT / 'src' / 'argus-tools.html').read_text()
    return f'''{head("ARGUS Systems | MATRIX E.I.L.", "ARGUS Systems is de softwaretak van MATRIX E.I.L.: CHRONOS, AXIS, METRON, HOROS, BIFROST, VISUAL INTELLIGENCE, HYPERION, TREEHOUSE, TARTARUS, KANON en IRIS. Software voor licht, video en productie, gebouwd vanuit de praktijk.", "assets/img/chronos-overzicht.jpg", "assets/img/argus/favicon.png")}
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

<section class="section" style="padding-top:clamp(40px,6vw,90px)" data-cue="Q2" data-cue-name="ARGUS OS">
  <div class="wrap">
    {cue_head('Q2', 'ARGUS OS', 'argus://desktop')}
    <div class="intro-line">
      <h2 class="title reveal">Elf tools.<br><em>Eén wachter.</em></h2>
      <p class="lead reveal">ARGUS Systems bouwt de software die we op de vloer zelf misten, tussen de cases en op echte producties. Open hieronder een tool, sleep de vensters rond of typ een commando in de terminal.</p>
    </div>
    {aos_html()}
  </div>
</section>

<section class="section" style="padding-top:0" data-cue="Q3" data-cue-name="Roadmap">
  <div class="wrap">
    {cue_head('Q3', 'Ontwikkeling', 'Status 2026')}
    <h2 class="title reveal">Van idee<br>naar <em>het veld.</em></h2>
    <div class="roadmap reveal">
      <span class="prog"></span>
      <div class="stage done"><div class="pt"></div><h4>Concept</h4><p>Een probleem dat we op de vloer zelf tegenkwamen.</p><div class="who"><span>HYPERION</span></div></div>
      <div class="stage done"><div class="pt"></div><h4>Ontwikkeling</h4><p>Eerste versies, gebouwd rond hoe een productie echt loopt.</p><div class="who"><span>TREEHOUSE</span><span>TARTARUS</span><span>KANON</span><span>VISUAL INTELLIGENCE</span></div></div>
      <div class="stage now"><div class="pt"></div><h4>Test</h4><p>Intern en met operators uittesten en bijschaven.</p><div class="who"><span>AXIS</span><span>METRON</span><span>HOROS</span></div></div>
      <div class="stage now"><div class="pt"></div><h4>Live testing</h4><p>Draaien op echte evenementen, onder echte druk.</p><div class="who"><span class="f">CHRONOS</span><span class="f">BIFROST</span><span class="f">IRIS</span></div></div>
      <div class="stage"><div class="pt"></div><h4>Release</h4><p>Beschikbaar voor andere producties en operators.</p></div>
    </div>
  </div>
</section>

{tools}
<section class="section" data-cue="Q8" data-cue-name="Werkplaats">
  <div class="wrap">
    {cue_head('Q8', 'De werkplaats', 'Nieuw in ontwikkeling')}
    <div class="intro-line">
      <h2 class="title reveal">Wat er nog<br><em>aan komt.</em></h2>
      <p class="lead reveal">Zeven nieuwe tools, van een kluis voor showfiles tot volgspots die zelf volgen. Elk ontstaan uit een probleem dat we op de vloer tegenkwamen.</p>
    </div>
    <div class="acards">{argus_cards()}
    </div>
  </div>
</section>
<section class="section argus-cta" id="contact" data-cue="Q9" data-cue-name="Meedoen">
  <div class="wrap">
    <div class="reveal">
      {cue_head('Q9', 'Meedoen', 'Testers gezocht')}
      <h2 class="title">Zet ARGUS in op<br><em>jouw productie.</em></h2>
    </div>
    <div class="reveal">
      <p>Wil je een van onze tools testen op jouw evenement, of heb je een idee dat hier past? Operators en producties die mee willen bouwen, horen we graag.</p>
      <a class="btn" href="mailto:{MAIL}?subject=ARGUS%20Systems">Neem contact op</a>
    </div>
  </div>
</section>
</main>
{footer(chr(10) + '<script src="assets/js/argus.js?v=' + ver('assets/js/argus.js') + '"></script>' + chr(10) + '<script src="assets/js/argus-os.js?v=' + ver('assets/js/argus-os.js') + '"></script>')}'''


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


# ---------------------------------------------------------------- Diensten
STEPS = [
    ('Kennismaking', 'We bespreken je evenement: de plek, het publiek, het programma en wat je wilt dat mensen voelen.'),
    ('Ontwerp', 'Een plan voor stage, licht, visuals en LED dat past bij de ruimte, de tijd en het budget.'),
    ('Voorbereiding', 'Programmeren, content maken en afstemmen met je productie en technische partners.'),
    ('Show', 'We staan zelf achter de tafel, zodat het ontwerp op het podium ook echt zo staat.'),
]
CLIENTS = ['GTF Franzen Sound Light Vision', 'WE-AV', 'Djem LED Screens', 'Heijnens Audio - Light - Vision', 'Stod', 'Spectrum AV', 'Bongers BLG', 'T.Y.S. Productions', 'Hoedemakers.PRO', 'SL Productions', 'Cowanzo', 'ROOT Productions', 'Demo Productions']

DIENSTEN = [
    dict(slug='lichtontwerp', short='Stage- en lichtontwerp', img='proj/woeesj-stock/01.jpg', match=('design',),
         title='Stage- en lichtontwerp voor festivals en evenementen',
         seo='Stage- en lichtontwerp voor festivals | MATRIX E.I.L.',
         desc='Stage- en lichtontwerp voor festivals en evenementen. Van eerste schets tot complete rig, afgestemd op plek, publiek en muziek.',
         h1='Stage- &amp;<br><em>lichtontwerp.</em>',
         lead='Een ontwerp dat past bij de plek, het publiek en de muziek. Van eerste schets tot complete rig.',
         body=['Een vertrouwde opstelling is snel gekozen. Toch verdient iedere productie opnieuw de vraag: waarom past dit hier? We kijken naar de ruimte, de zichtlijnen, het programma en de beschikbare tijd en middelen, en vertalen dat naar een ontwerp waarin elk onderdeel een reden heeft.',
               'Omdat programmering en live operation bij ons in dezelfde hand liggen, weten we hoe een ontwerp zich straks gedraagt tijdens de show. Zo staat wat op papier is bedacht ook echt zo op het podium.'],
         points=['Concept en sfeer voor stage en licht', 'Ontwerp van de rig, afgestemd op ruimte, tijd en budget', 'Afstemming met productie en verhuurpartners', 'Programmering en bediening door hetzelfde team']),
    dict(slug='lichtprogrammeur', short='Programmering en live operation', img='proj/paul-elstak/01.jpg', match=('programming',),
         title='Lichtprogrammeur en live operator voor je show',
         seo='Lichtprogrammeur en live operator | MATRIX E.I.L.',
         desc='Een lichtprogrammeur en live operator voor festivals, clubs en evenementen. De show voorbereiden en live bedienen, zodat licht en muziek samenvallen.',
         h1='Programmering &amp;<br><em>live operation.</em>',
         lead='De show programmeren en live bedienen, zodat licht en muziek op elk moment samenvallen.',
         body=['Een goede show begint lang voordat de eerste act op het podium staat. We bereiden de show voor op de lichttafel, bouwen looks en cues op die passen bij de artiesten en het programma, en zorgen dat alles klaarstaat als de deuren opengaan.',
               'Tijdens de show staan we zelf achter de tafel. We spelen in op wat er gebeurt: op een DJ die anders draait dan gepland, op een publiek dat meer wil, op het moment dat net iets meer of juist minder vraagt.'],
         points=['Show voorbereiden en programmeren op de lichttafel', 'Live bediening tijdens de show', "Inspelen op DJ's, live acts en het publiek", 'Ingehuurd door producties en verhuurbedrijven']),
    dict(slug='vj-visuals', short='VJ en visual content', img='proj/parkcity-live/01.jpg', match=('vj', 'visual'),
         title='VJ en visuals op maat voor je podium',
         seo='VJ en visual content op maat | MATRIX E.I.L.',
         desc='Live VJ en custom visual content voor festivals en evenementen. Visuals gemaakt voor het podium, de schermen en de artiesten van jouw productie.',
         h1='VJ &amp;<br><em>visual content.</em>',
         lead='Eigen visuals en live VJ, gemaakt voor het podium en de artiesten van jouw productie.',
         body=['Een scherm kan diepte geven aan een podium, maar ook alle aandacht opeisen. Daarom maken we content die past bij de stage, het licht en de muziek, in plaats van losse clips die toevallig voorbijkomen.',
               'Live sturen we de visuals mee met de show, zodat beeld en licht samen één geheel vormen.'],
         points=['Custom visual content voor jouw schermen en stage', 'Live VJ tijdens de show', 'Beeld afgestemd op licht, muziek en artiesten', 'Content en licht uit één hand']),
    dict(slug='led-schermen', short='LED-schermen en infrastructuur', img='electrisize.jpg', match=('led',),
         title='LED-schermen en infrastructuur voor evenementen',
         seo='LED-schermen en infrastructuur voor evenementen | MATRIX E.I.L.',
         desc='Opbouw, signaal en inregelen van LED-schermen voor festivals en evenementen: LED systems, infrastructuur en setup &amp; commissioning.',
         h1='LED-schermen &amp;<br><em>infrastructuur.</em>',
         lead='LED-schermen en de techniek erachter: opbouw, signaal en inregelen.',
         body=['Achter elk scherm zit een systeem: processors, signaalverdeling, voeding en een opbouw die moet kloppen voordat er ook maar één beeld verschijnt.',
               'We helpen bij de opbouw en het inregelen van LED-systemen, zodat het beeld scherp, stabiel en op tijd staat. Ook als onderdeel van een groter team of voor een LED-leverancier.'],
         points=['LED systems en infrastructuur', 'Setup &amp; commissioning op locatie', 'Signaal en inregelen van schermen', 'Samenwerking met LED-leveranciers']),
]


def project_photos(slug, single):
    if single:
        return f'assets/img/{single}', [f'assets/img/{single}']
    return f'assets/img/proj/{slug}/cover.jpg', [f'assets/img/proj/{slug}/{f}' for f, _, _ in SETS[slug]]


def projects_for(d):
    return [p for p in PROJECTS if any(m in p[3].lower() for m in d['match'])]


def steps_html():
    return ''.join(f'''
      <li class="reveal"><span class="sn">0{i + 1}</span><h3>{t}</h3><p>{d}</p></li>''' for i, (t, d) in enumerate(STEPS))


def dienst_cards(projects):
    out = ''
    for slug, t, meta, role, client, single in projects:
        cover, _ = project_photos(slug, single)
        out += f'''
      <a class="mini reveal" href="project-{slug}.html"><span class="mini-img rm"><img src="{cover}" alt="{t}" loading="lazy"></span><span class="mini-t"><b>{t}</b><small>{role}</small></span></a>'''
    return out


def diensten():
    rows = ''.join(f'''
    <a class="svc reveal" href="{d['slug']}.html">
      <span class="svc-no">0{i + 1}</span>
      <span class="svc-img rm"><img src="assets/img/{d['img']}" alt="{d['short']}" loading="lazy"></span>
      <span class="svc-copy"><h2>{d['short']}</h2><p>{d['lead']}</p><span class="link-arrow">Lees meer</span></span>
    </a>''' for i, d in enumerate(DIENSTEN))
    ld = [ORG, crumbs(('Diensten', 'diensten.html'))]
    return f'''{head("Diensten: lichtontwerp, programmering, VJ en LED | MATRIX E.I.L.", "MATRIX E.I.L. levert stage- en lichtontwerp, lichtprogrammering en live operation, VJ en visual content en LED-infrastructuur voor festivals en evenementen.", ld=ld)}
<body class="page-svc">
{header('diensten.html')}
<main>
<section class="section page-top" data-cue="Q1" data-cue-name="Diensten">
  <div class="wrap">
    {cue_head('Q1', 'Diensten', '4 disciplines')}
    <div class="intro-line">
      <h1 class="display reveal">Het complete<br><em>plaatje.</em></h1>
      <p class="lead reveal">Vier disciplines die samen het beeld van je evenement maken. Los in te huren, en het sterkst als één geheel.</p>
    </div>
    <div class="svc-list">{rows}
    </div>
  </div>
</section>
<section class="section" style="padding-top:0" data-cue="Q2" data-cue-name="Zo werken we">
  <div class="wrap">
    {cue_head('Q2', 'Zo werken we', 'Voor organisaties')}
    <ol class="steps">{steps_html()}
    </ol>
  </div>
</section>
{contact_block('Q3')}
</main>
{footer()}'''


def dienst_page(d):
    i = DIENSTEN.index(d)
    projs = projects_for(d)
    others = ''.join(f'<a href="{o["slug"]}.html">{o["short"]} →</a>' for o in DIENSTEN if o is not d)
    q, src = QUOTES[(i + 2) % len(QUOTES)]
    svc_ld = {'@context': 'https://schema.org', '@type': 'Service', 'name': d['short'], 'serviceType': d['short'],
              'description': d['desc'].replace('&amp;', '&'), 'provider': {'@id': BASE + '#matrix'}, 'areaServed': 'Nederland'}
    ld = [ORG, svc_ld, crumbs(('Diensten', 'diensten.html'), (d['short'], d['slug'] + '.html'))]
    body = ''.join(f'<p>{b}</p>' for b in d['body'])
    points = ''.join(f'<li>{pt}</li>' for pt in d['points'])
    return f'''{head(d['seo'], d['desc'], 'assets/img/' + d['img'], ld=ld)}
<body class="page-svc">
{header(d['slug'] + '.html')}
<main>
<section class="section page-top" data-cue="Q1" data-cue-name="{d['short']}">
  <div class="wrap">
    <nav class="crumb tag" aria-label="Kruimelpad"><a href="diensten.html">Diensten</a> / <b>{d['short']}</b></nav>
    {cue_head('Q1', d['short'], f'Dienst 0{i + 1} / 04')}
    <div class="intro-line">
      <h1 class="display reveal"><span class="visually-hidden">{d['title']}: </span>{d['h1']}</h1>
      <p class="lead reveal">{d['lead']}</p>
    </div>
    <div class="svc-hero unveil rm"><img src="assets/img/{d['img']}" alt="{d['title']}" loading="lazy"></div>
  </div>
</section>
<section class="section" style="padding-top:0" data-cue="Q2" data-cue-name="Wat we doen">
  <div class="wrap">
    {cue_head('Q2', 'Wat we doen')}
    <div class="svc-body">
      <div class="body-text reveal">{body}</div>
      <ul class="svc-points reveal">{points}</ul>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0" data-cue="Q3" data-cue-name="Projecten">
  <div class="wrap">
    {cue_head('Q3', 'Projecten', f'{len(projs)} shows')}
    <div class="minis">{dienst_cards(projs)}
    </div>
  </div>
</section>
<section class="section quote-block" style="padding-top:0">
  <div class="wrap reveal"><blockquote>{q}</blockquote><cite>{src}</cite></div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap others reveal"><span class="tag">Andere diensten</span>{others}</div>
</section>
{contact_block('Q4')}
</main>
{footer()}'''


# ---------------------------------------------------------------- Projectpagina's
def story_html(slug):
    st = STORIES.get(slug)
    if not st:
        return ''
    body = ''.join(f'<p>{b}</p>' for b in st['body'])
    facts = ''.join(f'<div><b>{v}</b><span>{l}</span></div>' for v, l in st['facts'])
    return f'''<section class="section story" style="padding-top:0" data-cue="Q2.5" data-cue-name="Het verhaal">
  <div class="wrap">
    {cue_head('Q2.5', 'Het verhaal')}
    <div class="story-grid">
      <h2 class="title reveal">{st['title']}</h2>
      <div class="body-text reveal">{body}</div>
    </div>
    <div class="story-facts reveal">{facts}</div>
    <blockquote class="story-quote reveal">“{st['quote']}”</blockquote>
  </div>
</section>'''

def project_page(idx):
    slug, t, meta, role, client, single = PROJECTS[idx]
    cover, photos = project_photos(slug, single)
    prev_p, next_p = PROJECTS[idx - 1], PROJECTS[(idx + 1) % len(PROJECTS)]
    svcs = [d for d in DIENSTEN if any(m in role.lower() for m in d['match'])]
    svc_links = ''.join(f'<a href="{d["slug"]}.html">{d["short"]}</a>' for d in svcs)
    grid = ''.join(f'<button class="pp-ph reveal" type="button" data-i="{k}" aria-label="Foto {k + 1} groot bekijken"><img src="{ph}" alt="{t}, foto {k + 1}" loading="lazy"></button>' for k, ph in enumerate(photos))
    plain = t.replace('&amp;', '&')
    meta_plain = meta.replace('&amp;', '&')
    role_plain = role.replace('&amp;', '&')
    desc = f'{plain}{", " + meta_plain if meta else ""}: {role_plain}{". " + client if client else ""}. Een project van MATRIX E.I.L.'
    work_ld = {'@context': 'https://schema.org', '@type': 'CreativeWork', 'name': plain, 'description': desc,
               'image': BASE + cover, 'creator': {'@id': BASE + '#matrix'}}
    ld = [ORG, work_ld, crumbs(('Projecten', 'projecten.html'), (plain, f'project-{slug}.html'))]
    meta_html = f'<span>{meta}</span>' if meta else ''
    client_html = f'<div><span class="tag">Voor</span><b>{client}</b></div>' if client else ''
    log = next((r for r in SHOWLOG if r[4] == slug), None)
    url = log and press_for(log[0][:4], log[1])
    if url:
        client_html += f'<div><span class="tag">In de pers</span><a class="link-arrow" href="{url}" target="_blank" rel="noopener">Artikel op Highlite</a></div>'
    n = len(photos)
    count = f"{n} foto's" if n > 1 else '1 foto'
    return f'''{head(f"{plain} | Project | MATRIX E.I.L.", desc, cover, ld=ld)}
<body class="page-project">
{header(f'project-{slug}.html')}
<main>
<section class="pp-hero" data-cue="Q1" data-cue-name="{plain}">
  <img class="pp-bg" src="{cover}" alt="" fetchpriority="high">
  <div class="wrap">
    <nav class="crumb tag" aria-label="Kruimelpad"><a href="projecten.html">Projecten</a> / <b>{t}</b></nav>
    <h1 class="display">{t}</h1>
    <div class="pp-meta">{meta_html}<span>{count}</span></div>
  </div>
</section>
<section class="section" data-cue="Q2" data-cue-name="De opdracht">
  <div class="wrap pp-facts">
    <div><span class="tag">Rol van MATRIX</span><b>{role}</b></div>
    {client_html}
    <div><span class="tag">Disciplines</span><span class="pp-svcs">{svc_links or '—'}</span></div>
  </div>
</section>
{story_html(slug)}
<section class="section" style="padding-top:0" data-cue="Q3" data-cue-name="Foto's">
  <div class="wrap">
    {cue_head('Q3', "Foto's", f'{n} frames')}
    <div class="pp-grid{' single' if n == 1 else ''}" data-title="{t}" data-gallery='{json.dumps(photos)}'>{grid}</div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap pp-nav">
    <a href="project-{prev_p[0]}.html"><span class="tag">← Vorige show</span><b>{prev_p[1]}</b></a>
    <a href="projecten.html" class="all"><span class="tag">Overzicht</span><b>Alle projecten</b></a>
    <a href="project-{next_p[0]}.html" class="nx"><span class="tag">Volgende show →</span><b>{next_p[1]}</b></a>
  </div>
</section>
{contact_block('Q4')}
</main>
{footer()}'''


# ---------------------------------------------------------------- 404
def not_found():
    return f'''{head("Cue niet gevonden | MATRIX E.I.L.", "Deze pagina bestaat niet (meer).")}
<body class="page-404">
{header('404.html')}
<main>
<section class="section page-top lost" data-cue="Q404" data-cue-name="Cue niet gevonden">
  <div class="wrap">
    {cue_head('Q404', 'Cue niet gevonden', 'Error')}
    <h1 class="display reveal">Deze cue<br><em>bestaat niet.</em></h1>
    <p class="lead reveal" style="max-width:640px;margin-top:30px">“Wie het onverwachte niet verwacht, zal het niet vinden.” Heraclitus had gelijk, maar ergens tussen de tafel en deze pagina is de DMX-lijn doorgeknipt.</p>
    <div class="dmx reveal" aria-hidden="true"><svg viewBox="0 0 1000 150" preserveAspectRatio="none">
      <path class="cable" d="M0,110 C150,110 250,60 420,80 L470,86"/><path class="core" d="M0,110 C150,110 250,60 420,80 L470,86"/>
      <path class="cable" d="M520,70 C620,40 760,120 900,60"/><path class="core dead" d="M520,70 C620,40 760,120 900,60"/>
      <circle class="spark" cx="474" cy="84" r="4"/><circle class="spark" cx="482" cy="78" r="2" style="animation-delay:.3s"/>
      <rect class="fix" x="900" y="30" width="60" height="60" rx="6"/><circle class="lens" cx="930" cy="60" r="18"/>
    </svg>
    <div class="dmx-cap"><span>Universe <b>404</b></span><span>Signaal <b>verloren</b></span><span>Fixture <b>geen data</b></span></div></div>
    <div class="btns reveal" style="margin-top:40px"><a class="btn fill" href="index.html">Terug naar Q1</a><a class="btn" href="projecten.html">Projecten</a><a class="btn" href="diensten.html">Diensten</a></div>
  </div>
</section>
</main>
{footer()}'''


# ---------------------------------------------------------------- Operators
CONSOLES = [
    ('grandMA3', 'Lichttafel', 'Voor grote shows en complexe rigs: van programmeren tot live busking.'),
    ('Infinity Chimp', 'Lichttafel', 'Snel en flexibel, ook voor kleinere podia en tours. Met eigen macro’s uit ARGUS TREEHOUSE in ontwikkeling.'),
    ('Resolume', 'Video', 'Visuals en content live op het ritme van de show, op LED-wanden en schermen.'),
    ('Capture', 'Visualisatie', 'Shows vooraf in 3D opbouwen en programmeren, zodat je op locatie tijd wint.'),
]
RIDER = [
    ('Plek aan FOH', 'Met vrij zicht op het podium en op de schermen.'),
    ('Stroom', 'Een eigen, schone groep voor tafel en laptop.'),
    ('Data', 'Netwerk of DMX tot aan FOH, liefst met een reservelijn.'),
    ('Info vooraf', 'Timetable, rigplot, patch en het contact van de productie, een paar dagen voor de show.'),
    ('Tijd om te focussen', 'Een donker moment in de opbouw om posities en focus te zetten.'),
    ('Crewcatering', 'Eten en drinken. Een operator op een lege maag mist cues.'),
]


def operators():
    con = ''.join(f'<article class="con reveal"><span class="tag">{k}</span><h3>{n}</h3><p>{d}</p></article>' for n, k, d in CONSOLES)
    rider = ''.join(f'<li class="reveal"><span class="sn">{i + 1:02d}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(RIDER))
    ld = [ORG, crumbs(('Operators', 'operators.html'))]
    return f'''{head("Licht- en video-operator inhuren | MATRIX E.I.L.", "Een ervaren lichtoperator, programmeur of VJ nodig op grandMA3, Infinity Chimp of Resolume? Of ben je zelf operator en wil je met MATRIX werken? Lees hier hoe.", ld=ld)}
<body class="page-svc page-ops">
{header('operators.html')}
<main>
<section class="section page-top" data-cue="Q1" data-cue-name="Operators">
  <div class="wrap">
    {cue_head('Q1', 'Operators', 'Achter de tafel')}
    <div class="intro-line">
      <h1 class="display reveal">Achter<br><em>de tafel.</em></h1>
      <p class="lead reveal">Een show is zo goed als de persoon die hem draait. Of je nu een operator zoekt voor je podium, of zelf achter de tafel staat en met ons wilt werken: hier lees je hoe dat gaat.</p>
    </div>
    <div class="ops-split">
      <a class="ops-card reveal" href="#inhuren"><span class="tag">Voor producties</span><h2>Operator inhuren</h2><p>Licht programmeren en draaien, of visuals live op je schermen.</p><span class="link-arrow">Lees meer</span></a>
      <a class="ops-card reveal" href="#aanmelden"><span class="tag">Voor operators</span><h2>Werken met MATRIX</h2><p>Freelance operator, programmeur of VJ? Meld je.</p><span class="link-arrow">Lees meer</span></a>
    </div>
  </div>
</section>

<section class="section" id="inhuren" style="padding-top:0" data-cue="Q2" data-cue-name="Inhuren">
  <div class="wrap">
    {cue_head('Q2', 'Operator inhuren', 'Licht · Video')}
    <div class="svc-body">
      <div class="body-text reveal">
        <p>MATRIX levert lichtprogrammeurs, lichtoperators en VJ’s voor festivals, evenementen en tours. We stappen in op jouw rig en jouw ontwerp, of nemen het ontwerp zelf mee.</p>
        <p>We komen voorbereid: de showfile staat vooraf klaar waar dat kan, de timetable is doorgenomen en we weten wie je productiecontact is. Op de dag zelf draaien we de show op het moment, met oog voor de artiest en het publiek.</p>
        <p>Van een enkele avond op een stage tot meerdere dagen festival: <a href="lichtprogrammeur.html">lees meer over lichtprogrammering</a> of <a href="vj-visuals.html">over VJ en visuals</a>.</p>
      </div>
      <div class="cons">{con}</div>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0" data-cue="Q3" data-cue-name="Rider">
  <div class="wrap">
    {cue_head('Q3', 'Operator rider', 'Wat we nodig hebben')}
    <h2 class="title reveal">De rider<br><em>van de tafel.</em></h2>
    <ol class="rider-list">{rider}
    </ol>
  </div>
</section>

<section class="section" id="aanmelden" style="padding-top:0" data-cue="Q4" data-cue-name="Aanmelden">
  <div class="wrap">
    {cue_head('Q4', 'Werken met MATRIX', 'Freelancers')}
    <div class="intro-line">
      <h2 class="title reveal">Sta jij<br><em>achter de tafel?</em></h2>
      <div class="reveal">
        <p class="lead">We werken graag met operators, programmeurs en VJ’s die hun vak verstaan en rustig blijven als het spannend wordt.</p>
        <p style="margin-top:18px;color:var(--muted)">Stuur een mail met wie je bent, op welke tafels en software je werkt, een paar shows die je draaide en waar je woont. Een showreel of Instagram helpt.</p>
        <div class="btns" style="margin-top:26px"><a class="btn fill" href="mailto:{MAIL}?subject=Operator%20bij%20MATRIX">Meld je aan</a><a class="btn" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a></div>
      </div>
    </div>
  </div>
</section>
{contact_block('Q5')}
</main>
{footer()}'''


# ---------------------------------------------------------------- Voor wie
DOELGROEPEN = [
    dict(slug='voor-festivals', short='Festivals', h1='Licht voor<br><em>festivals.</em>',
         seo='Lichtontwerp en lichtoperator voor festivals | MATRIX E.I.L.',
         desc='Lichtontwerp, programmering, operators en LED voor festivals en stages. MATRIX werkte op o.a. Paaspop, Pinkpop, Essential, Decibel Outdoor en Electrisize.',
         lead='Meerdere stages, wisselende acts en een strakke timetable. Wij zorgen dat elk podium een eigen gezicht heeft en dat de show op elke stage staat.',
         body=['Op een festival komt alles samen: veel artiesten achter elkaar, korte changeovers en weinig tijd om te programmeren. Daarom bereiden we de show vooraf voor waar het kan, en weten we op de dag precies wat er per act nodig is.',
               'We leveren het lichtontwerp voor een stage, programmeren en draaien de shows, of stappen in als operator op een bestaande rig. Ook visuals en LED nemen we mee, zodat licht en beeld één geheel vormen.'],
         points=['Lichtontwerp per stage', 'Programmering vooraf, in 3D waar het kan', 'Operators voor elke act', 'Visuals en LED in dezelfde lijn'],
         keys=['Festival', 'Paaspop', 'Pinkpop', 'Decibel', 'Electrisize', 'Soenda', 'Lake Dance', 'Groove Garden', 'Harmony', 'ParkCity', 'Woeësj', 'Power Weekend']),
    dict(slug='voor-carnaval', short='Carnaval', h1='Licht voor<br><em>carnaval.</em>',
         seo='Licht en visuals voor carnaval | MATRIX E.I.L.',
         desc='Licht, visuals en programmering voor carnavalsfeesten, pleinfeesten, carnavalsfinales en carnavalsradio in Limburg. Van Groëte Gulpener Vastelaoves Finale tot Carnaval Radio.',
         lead='Carnaval is in Limburg geen feestje, het is een seizoen. Van finale op het marktplein tot pleinfeest en live radio: wij zorgen dat het er groot uitziet.',
         body=['Carnaval vraagt om licht dat feest uitstraalt en toch strak loopt. Optredens, uitreikingen en live uitzendingen wisselen elkaar snel af, en alles moet in één keer goed.',
               'We werkten op onder meer de Groëte Gulpener Vastelaoves Finale, Carnaval Radio, Koning Carnaval en Halfvasten. We weten hoe zo’n avond loopt en wat er op het juiste moment moet gebeuren.'],
         points=['Licht voor zalen, tenten en pleinen', 'Programmering voor live tv en radio', 'Visuals op schermen', 'Ervaring met het Limburgse carnavalsseizoen'],
         keys=['Carnaval', 'Gulpener', 'Halfvasten', 'Pleinfeest', 'Gulden Humor']),
    dict(slug='voor-verenigingen', short='Scholen en verenigingen', h1='Licht voor<br><em>verenigingen.</em>',
         seo='Licht en stage voor jubilea, scholen en verenigingen | MATRIX E.I.L.',
         desc='Stage- en lichtontwerp voor jubilea, talentenshows, schuttersfeesten en verenigingsfeesten. Zoals 100 jaar Sportclub’25, 90 jaar G.V. Wilhelmina en ZLF 2025.',
         lead='Een jubileum, een talentenshow of een schuttersfeest verdient net zo goed een show om nooit te vergeten. Wij maken het groot, binnen jullie mogelijkheden.',
         body=['Bij verenigingen en scholen draait het om de mensen op het podium: leden, leerlingen, vrijwilligers. Wij zorgen dat zij er op hun mooist uitzien, met licht dat het verhaal van de avond vertelt.',
               'We denken mee vanaf het eerste idee, ontwerpen het podium en het licht, en draaien de show zelf. Zo hoeft de organisatie zich alleen nog druk te maken over het feest.'],
         points=['Stage- en lichtontwerp op maat', 'Meedenken vanaf het eerste idee', 'Show op muziek of timecode', 'Eén aanspreekpunt van begin tot eind'],
         keys=['Sportclub', 'Wilhelmina', 'Talentenshow', 'ZLF', 'USC', 'Gulden Humor']),
]


def doelgroep_page(d):
    rows = [r for r in SHOWLOG if any(k.lower() in r[1].lower() for k in d['keys'])]
    pages = {slug for slug, *_ in PROJECTS}
    lis = ''.join(f'<li><span class="sl-show">{f"<a href=\'project-{r[4]}.html\'>{r[1]}</a>" if r[4] in pages else r[1]}</span><span class="sl-role">{r[2]}</span><span class="sl-client">{r[0]}</span></li>' for r in reversed(rows))
    others = ''.join(f'<a href="{o["slug"]}.html">{o["short"]} →</a>' for o in DOELGROEPEN if o is not d)
    svc_ld = {'@context': 'https://schema.org', '@type': 'Service', 'name': f"Licht en visuals voor {d['short'].lower()}", 'description': d['desc'],
              'provider': {'@id': BASE + '#matrix'}, 'areaServed': 'Nederland'}
    ld = [ORG, svc_ld, crumbs((d['short'], d['slug'] + '.html'))]
    body = ''.join(f'<p>{b}</p>' for b in d['body'])
    points = ''.join(f'<li>{p}</li>' for p in d['points'])
    return f'''{head(d['seo'], d['desc'], ld=ld)}
<body class="page-svc">
{header(d['slug'] + '.html')}
<main>
<section class="section page-top" data-cue="Q1" data-cue-name="{d['short']}">
  <div class="wrap">
    {cue_head('Q1', 'Voor ' + d['short'].lower())}
    <div class="intro-line">
      <h1 class="display reveal">{d['h1']}</h1>
      <p class="lead reveal">{d['lead']}</p>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0" data-cue="Q2" data-cue-name="Aanpak">
  <div class="wrap">
    {cue_head('Q2', 'Aanpak')}
    <div class="svc-body">
      <div class="body-text reveal">{body}</div>
      <ul class="svc-points reveal">{points}</ul>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0" data-cue="Q3" data-cue-name="Gedraaid">
  <div class="wrap">
    {cue_head('Q3', 'Uit het logboek', f'{len(rows)} producties')}
    <div class="sl-year reveal"><h3><b>Gedraaid</b><span>selectie uit het <a href="projecten.html#showlog">showlog</a></span></h3><ul>{lis}</ul></div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap others reveal"><span class="tag">Ook voor</span>{others}<a href="operators.html">Operators →</a></div>
</section>
{contact_block('Q4')}
</main>
{footer()}'''


# ---------------------------------------------------------------- FAQ
FAQ = [
    ('Wat doet MATRIX E.I.L. precies?', 'We verzorgen het visuele plaatje van live producties: stage- en lichtontwerp, lichtprogrammering, live operation, VJ en visuals, en LED-techniek. Dat kan los, of alles in één hand.'),
    ('Wat kost een lichtontwerp of een operator?', 'Dat hangt af van de grootte van het podium, het aantal showdagen en hoeveel voorbereiding er nodig is. Stuur ons je datum, locatie en wat je in gedachten hebt, dan krijg je snel een voorstel op maat.'),
    ('Hoe ver van tevoren moet ik boeken?', 'Hoe eerder, hoe beter, zeker in het festival- en carnavalsseizoen. Voor een ontwerp hebben we graag een paar weken tot maanden voorbereiding. Voor een operator op een bestaande rig kan het soms ook op korte termijn, vraag het gerust.'),
    ('Leveren jullie ook het materiaal?', 'Dat verschilt per productie. Vaak werken we samen met verhuur- en techniekbedrijven die het materiaal leveren, terwijl wij het ontwerp, de programmering en de show verzorgen. We denken graag mee over de beste oplossing.'),
    ('Op welke lichttafels werken jullie?', 'Vooral op grandMA3 en Infinity Chimp. Voor video werken we met Resolume, en shows bouwen we vooraf op in Capture. <a href="operators.html">Lees meer over onze operators</a>.'),
    ('Werken jullie alleen in Limburg?', 'We werken veel in Limburg, maar draaien net zo goed shows in de rest van het land, van Paaspop en Pinkpop tot Decibel Outdoor.'),
    ('Kunnen jullie ook alleen programmeren, zonder ontwerp?', 'Zeker. We stappen in op een bestaand ontwerp of rig, programmeren de show en draaien hem live. Of we programmeren vooraf en geven de showfile door aan jullie eigen operator.'),
    ('Wat is ARGUS Systems?', 'ARGUS Systems is de softwaretak van MATRIX. We bouwen tools voor productie en showoperators, ontstaan uit problemen die we op de vloer zelf tegenkwamen. <a href="argus.html">Bekijk ARGUS</a>.'),
    ('Hoe neem ik contact op?', f'Het snelst via <a href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a> of mail naar <a href="mailto:{MAIL}">{MAIL}</a>. Je kunt ons ook vinden op <a href="{INSTA}" target="_blank" rel="noopener">Instagram</a>.'),
]


def faq():
    import re as _re
    items = ''.join(f'<details class="qa reveal"><summary><span class="qn">Q{i + 1:02d}</span>{q}</summary><div><p>{a}</p></div></details>' for i, (q, a) in enumerate(FAQ))
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': _re.sub('<[^>]+>', '', a)}} for q, a in FAQ]}
    return f'''{head("Veelgestelde vragen | MATRIX E.I.L.", "Antwoorden op veelgestelde vragen over lichtontwerp, lichtoperators, VJ en LED: wat het kost, hoe ver vooruit je boekt en op welke tafels we werken.", ld=[ORG, faq_ld, crumbs(('FAQ', 'faq.html'))])}
<body class="page-svc">
{header('faq.html')}
<main>
<section class="section page-top" data-cue="Q1" data-cue-name="FAQ">
  <div class="wrap">
    {cue_head('Q1', 'Veelgestelde vragen', f'{len(FAQ)} vragen')}
    <div class="intro-line">
      <h1 class="display reveal">Vragen<br><em>uit de zaal.</em></h1>
      <p class="lead reveal">De vragen die we het vaakst krijgen, met een eerlijk antwoord. Staat jouw vraag er niet bij? Stuur hem gerust.</p>
    </div>
    <div class="faq">{items}</div>
  </div>
</section>
{contact_block('Q2')}
</main>
{footer()}'''


# ---------------------------------------------------------------- Woordenlijst
TERMEN = [
    ('Art-Net', 'Een protocol om DMX-data over een gewoon netwerk te sturen. Zo gaan veel universes over één kabel.'),
    ('Beam', 'Een lamp met een smalle, strakke lichtbundel. Goed zichtbaar in rook, voor scherpe lijnen in de lucht.'),
    ('Blinder', 'Een felle lamp die op het publiek is gericht, voor korte momenten van verblinding bij een drop of climax.'),
    ('Busking', 'Live licht draaien zonder vaste cues, op gevoel en op de muziek. Veel gebruikt bij dance-acts.'),
    ('Capture', 'Software om een lichtshow vooraf in 3D te bouwen en te programmeren, zodat je op locatie tijd wint.'),
    ('Changeover', 'De ombouw tussen twee acts op hetzelfde podium.'),
    ('Cue', 'Een opgeslagen moment in de show: welke lampen aan staan, in welke kleur, positie en intensiteit.'),
    ('Cuelijst', 'Een reeks cues achter elkaar, die je met GO één voor één afspeelt.'),
    ('DMX', 'Het standaard stuursignaal voor licht. Eén DMX-universe stuurt tot 512 kanalen aan.'),
    ('FOH', 'Front of house: de plek in de zaal waar licht, geluid en video worden bediend.'),
    ('Fixture', 'Een lamp of apparaat dat je vanaf de lichttafel aanstuurt.'),
    ('grandMA3', 'Een veelgebruikte lichttafel voor grote shows en festivals.'),
    ('Haze', 'Fijne nevel die de lichtbundels zichtbaar maakt in de lucht.'),
    ('Infinity Chimp', 'Een lichttafel van Highlite, snel en flexibel voor podia en tours.'),
    ('LD', 'Lighting designer: de lichtontwerper die bepaalt hoe de show eruitziet.'),
    ('LED-wand', 'Een groot scherm opgebouwd uit LED-panelen, voor visuals en live beeld.'),
    ('Moving head', 'Een lamp met een draaiende kop die je op afstand kunt richten, kleuren en laten bewegen.'),
    ('MVR', 'My Virtual Rig: een bestandsformaat om een complete rig met posities en patch uit te wisselen tussen programma’s.'),
    ('Operator', 'De persoon die tijdens de show de lichttafel of video bedient.'),
    ('Patch', 'De koppeling tussen de lampen en hun DMX-adressen, zodat de tafel weet welke lamp waar zit.'),
    ('Pixel pitch', 'De afstand tussen de pixels van een LED-scherm. Hoe kleiner, hoe scherper het beeld van dichtbij.'),
    ('Pixelmapping', 'Video of effecten over losse lampen of LED-strips verdelen alsof het pixels van een scherm zijn.'),
    ('Programmeur', 'Degene die de show in de lichttafel bouwt: cues, effecten en paletten.'),
    ('Resolume', 'Software voor live visuals en VJ, veel gebruikt op festivals en in clubs.'),
    ('sACN', 'Een netwerkprotocol voor DMX-data, net als Art-Net.'),
    ('Speedmaster', 'Een regelaar op de lichttafel die de snelheid van effecten op het tempo van de muziek zet.'),
    ('Strobe', 'Een lamp die zeer kort en fel flitst.'),
    ('Timecode', 'Een tijdsignaal waarmee licht, video en muziek precies synchroon lopen.'),
    ('Truss', 'De aluminium constructie waaraan lampen, schermen en speakers hangen.'),
    ('VJ', 'Video jockey: maakt en mixt live visuals op het ritme van de muziek.'),
    ('Volgspot', 'Een lamp die een artiest over het podium volgt, met de hand of automatisch.'),
    ('Wash', 'Een lamp met een brede, zachte lichtbundel om vlakken en mensen in te kleuren.'),
]


def woordenlijst():
    letters = sorted({t[0][0].upper() for t in TERMEN})
    idx = ''.join(f'<a href="#l-{l}">{l}</a>' for l in letters)
    groups = ''
    for l in letters:
        items = ''.join(f'<div class="term" id="t-{t.lower().replace(" ", "-")}"><dt>{t}</dt><dd>{d}</dd></div>' for t, d in TERMEN if t[0].upper() == l)
        groups += f'<section class="tg reveal" id="l-{l}"><h2>{l}</h2><dl>{items}</dl></section>'
    term_ld = {'@context': 'https://schema.org', '@type': 'DefinedTermSet', 'name': 'Woordenlijst licht en video', 'hasDefinedTerm': [
        {'@type': 'DefinedTerm', 'name': t, 'description': d} for t, d in TERMEN]}
    return f'''{head("Woordenlijst licht en video: van DMX tot volgspot | MATRIX E.I.L.", "Wat is een cue, DMX, haze of pixel pitch? De woordenlijst van MATRIX E.I.L. legt de belangrijkste termen uit licht, video en LED kort en helder uit.", ld=[ORG, term_ld, crumbs(('Woordenlijst', 'woordenlijst.html'))])}
<body class="page-svc">
{header('woordenlijst.html')}
<main>
<section class="section page-top" data-cue="Q1" data-cue-name="Woordenlijst">
  <div class="wrap">
    {cue_head('Q1', 'Woordenlijst', f'{len(TERMEN)} termen')}
    <div class="intro-line">
      <h1 class="display reveal">Vaktaal,<br><em>vertaald.</em></h1>
      <p class="lead reveal">Op de vloer praten we in afkortingen. Hier staat wat ze betekenen, van Art-Net tot wash.</p>
    </div>
    <nav class="az reveal" aria-label="Letters">{idx}</nav>
    <div class="terms">{groups}</div>
  </div>
</section>
{contact_block('Q2')}
</main>
{footer()}'''


PAGES = {'index.html': home, 'diensten.html': diensten, 'projecten.html': projecten, 'over.html': over,
         'argus.html': argus, 'privacy.html': privacy, '404.html': not_found,
         'operators.html': operators, 'faq.html': faq, 'woordenlijst.html': woordenlijst}
for _g in DOELGROEPEN:
    PAGES[_g['slug'] + '.html'] = (lambda g: lambda: doelgroep_page(g))(_g)
for _d in DIENSTEN:
    PAGES[_d['slug'] + '.html'] = (lambda d: lambda: dienst_page(d))(_d)
for _i, _p in enumerate(PROJECTS):
    PAGES[f'project-{_p[0]}.html'] = (lambda i: lambda: project_page(i))(_i)

if __name__ == '__main__':
    import datetime
    for name, fn in PAGES.items():
        CURRENT = name
        (ROOT / name).write_text(fn())
    today = datetime.date.today().isoformat()
    urls = ''.join(f'  <url><loc>{BASE}{"" if n == "index.html" else n}</loc><lastmod>{today}</lastmod></url>\n'
                   for n in PAGES if n != '404.html')
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
    print('gebouwd:', len(PAGES), "pagina's + sitemap.xml + robots.txt")
