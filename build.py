#!/usr/bin/env python3
"""Bouwt de HTML-pagina's van de site uit gedeelde onderdelen. Draai: python3 build.py"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent
MAIL = 'info@matrixeventsupport.nl'
TEL = '+31630971404'
TEL_TXT = '+31 6 30971404'
WHATSAPP = 'https://wa.me/31630971404'
INSTA = 'https://www.instagram.com/matrix.eil/'

FONTS = 'https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap'


def ver(path):
    return hashlib.md5((ROOT / path).read_bytes()).hexdigest()[:8]


NAV = [('projecten.html', 'Projecten'), ('over.html', 'Over')]
ARGUS_NAV = [('#chronos', 'Chronos'), ('#axis', 'Axis'), ('#metron', 'Metron'), ('#horos', 'Horos')]


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
<meta name="theme-color" content="#0a0a09">
<link rel="icon" href="{icon}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/css/style.css?v={ver('assets/css/style.css')}">
</head>'''


def skeleton():
    return '<div class="columns" aria-hidden="true"><div class="wrap"><span></span><span></span><span></span><span></span></div></div>'


def header(current):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{href}"{cur if href == current else ""}>{label}</a>' for href, label in NAV)
    return f'''{skeleton()}
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="MATRIX E.I.L. home"><img src="assets/img/logo-matrix.png" alt="MATRIX E.I.L." width="600" height="179"></a>
    <button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="Hoofdmenu">{links}<a class="door" href="argus.html">Argus</a><a class="nav-cta" href="#contact">Contact</a></nav>
  </div>
</header>'''


def argus_header():
    links = ''.join(f'<a href="{href}">{label}</a>' for href, label in ARGUS_NAV)
    return f'''<div class="portal-in" aria-hidden="true"></div>
{skeleton()}
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="#top" aria-label="ARGUS Systems"><img src="assets/img/argus/argus-systems.png" alt="ARGUS Systems" width="1200" height="390"></a>
    <button class="menu-btn" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="ARGUS-menu">{links}<a class="back" href="index.html">Matrix</a><a class="nav-cta" href="#contact">Contact</a></nav>
  </div>
</header>'''


def footer():
    return f'''<footer class="site-footer">
  <div class="wrap">
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
<button class="to-top" aria-label="Terug naar boven"><span aria-hidden="true">↑</span><i class="bar"></i></button>
<script src="assets/js/main.js?v={ver('assets/js/main.js')}"></script>
</body>
</html>
'''


def contact_block(title='Plan je volgende<br><span class="soft">editie met ons.</span>',
                  lead='Werk je aan een festival of evenement en zoek je één partij voor het visuele plaatje? Stuur een app of mail, dan denken we vrijblijvend mee.'):
    return f'''<section class="section contact" id="contact">
  <div class="wrap grid">
    <span class="eyebrow reveal" style="grid-column:1/-1;margin-bottom:34px">Contact</span>
    <h2 class="huge reveal">{title}</h2>
    <p class="lead reveal">{lead}</p>
    <div class="contact-ways reveal">
      <a href="{WHATSAPP}" target="_blank" rel="noopener"><small>WhatsApp</small><b>{TEL_TXT}</b></a>
      <a href="mailto:{MAIL}"><small>Mail</small><b>{MAIL}</b></a>
      <a href="{INSTA}" target="_blank" rel="noopener"><small>Instagram</small><b>@matrix.eil</b></a>
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- Home
# (foto, b, h, titel, plaats/jaar, slug, rol, layout)
WORK = [
    ('proj/woeesj-stock/01.jpg', 1600, 1067, 'Woeësj-Stock', 'Simpelveld, 2026', 'woeesj-stock',
     'Stage design · Lighting design · Programming · Live operation · Commissioned by GTF Franzen', 'w-full'),
    ('electrisize.jpg', 1345, 745, 'Electrisize', 'Main Stage &amp; Tapuya, 2026', 'electrisize',
     'LED systems · Infrastructure · Setup &amp; commissioning · For Djem LED Screens', 'w-left'),
    ('proj/parkcity-live/01.jpg', 1600, 1067, 'Parkcity Live', 'Dance tent, 2026', 'parkcity-live',
     'Custom visual content · VJ · For WE-AV', 'w-right'),
    ('boiler-room.jpg', 704, 481, 'Boiler Room', 'Complex Maastricht, 2026', 'boiler-room',
     'Programming · Live operation', 'w-mid'),
]

EXPERTISE = [
    ('proj/woeesj-stock/01.jpg', 'Stage &amp; lighting design',
     'Van eerste schets tot complete rig: een ontwerp dat past bij de plek, het publiek en de muziek.'),
    ('proj/paul-elstak/01.jpg', 'Programming &amp; live operation',
     'De show programmeren en live bedienen, zodat licht en muziek op elk moment samenvallen.'),
    ('proj/parkcity-live/01.jpg', 'VJ &amp; visual content',
     'Eigen visuals en live VJ, gemaakt voor het podium en de artiesten van jouw productie.'),
    ('electrisize.jpg', 'LED systems &amp; infrastructure',
     'LED-schermen en de techniek erachter: opbouw, signaal en inregelen.'),
]


def home():
    work = ''.join(f'''
      <a class="work {cls} reveal" href="projecten.html#{slug}">
        <span class="media unveil"><img src="assets/img/{img}" alt="{t}" width="{w}" height="{h}" loading="lazy"></span>
        <span class="cap"><h3>{t}</h3><span class="meta">{meta}</span><span class="role">{role}</span></span>
      </a>''' for img, w, h, t, meta, slug, role, cls in WORK)
    disc = ''.join(f'''
      <li class="reveal"><div class="ph" aria-hidden="true"><img src="assets/img/{img}" alt="" loading="lazy"></div><span class="n">0{i + 1}</span><h3>{t}</h3><p>{d}</p></li>''' for i, (img, t, d) in enumerate(EXPERTISE))
    return f'''{head("MATRIX E.I.L. | Licht, video, content en ontwerp voor festivals", "MATRIX E.I.L. verzorgt het complete visuele plaatje voor festivals en evenementen: lichtontwerp, programmering, live operation, VJ, content en LED.")}
<body class="home" data-seed="1">
{header('index.html')}
<main>
<section class="hero">
  <img class="hero-bg" src="assets/img/hero.jpg" alt="" fetchpriority="high">
  <h1><img class="hero-tekst" src="assets/img/hero-tekst.png" alt="Execution is the chariot of genius." width="1600" height="518"></h1>
  <div class="wrap hero-foot">
    <p>Licht, video, content en ontwerp voor festivals en evenementen. Eén partij voor het complete visuele plaatje.</p>
    <div class="btns"><a class="btn fill" href="#contact">Plan een gesprek <i>→</i></a><a class="btn" href="#werk">Bekijk werk <i>↓</i></a></div>
  </div>
</section>

<section class="section">
  <div class="wrap statement">
    <span class="eyebrow reveal">MATRIX E.I.L.</span>
    <h2 class="huge reveal">Het beeld van<br>jouw festival,<br><span class="soft">van schets tot<br>laatste cue.</span></h2>
    <div class="body-text reveal">
      <p>MATRIX geeft vorm aan de voorwaarden voor dat ene moment. Lichtontwerp, programmering, visuals en LED komen bij ons samen, zodat alles op het podium één verhaal vertelt.</p>
      <p>We denken mee vanaf het eerste idee en staan er zelf achter de tafel als het zover is.</p>
    </div>
  </div>
</section>

<section class="section tight">
  <div class="wrap">
    <span class="eyebrow reveal" style="margin-bottom:40px">Wat we doen</span>
    <ul class="disc-list">{disc}
    </ul>
  </div>
</section>

<section class="section" id="werk">
  <div class="wrap">
    <div class="page-head" style="margin-bottom:clamp(60px,7vw,100px)">
      <span class="eyebrow reveal">Geselecteerd werk · 2024 – 2026</span>
      <h2 class="huge reveal">Op de<br><span class="soft">vloer.</span></h2>
      <p class="lead reveal">Een greep uit producties waar we licht, beeld en LED neerzetten. <a href="projecten.html" style="color:var(--fg)">Alle projecten →</a></p>
    </div>
    <div class="work-grid">{work}
    </div>
  </div>
</section>

<section class="photo-break">
  <img src="assets/img/saloon.jpg" alt="Festivalpodium met licht, rook en publiek" width="2400" height="1600" loading="lazy">
  <div class="wrap"><span class="eyebrow reveal">Manifest</span><h2 class="mega reveal" style="margin-top:24px">Het bestaat<br>maar <span class="soft">even.</span></h2></div>
</section>

<section class="section" style="padding-top:clamp(50px,6vw,90px)">
  <div class="wrap manifest">
    <p class="lead reveal">Maanden voorbereiding voor een moment dat zich nooit precies laat herhalen. Dezelfde ruimte, dezelfde muziek, dezelfde techniek, en toch iedere keer iets anders.</p>
    <div class="body-text reveal">
      <p>Dat fascineert ons aan liveproducties. Je kunt alles voorbereiden, maar pas met mensen in de ruimte ontdek je wat het wordt.</p>
      <p>MATRIX geeft vorm aan de voorwaarden voor dat moment. Met ideeën, techniek en mensen die hun vak verstaan. Wat het uiteindelijk betekent, ontstaat tussen het podium en het publiek.</p>
    </div>
  </div>
  <div class="wrap quote reveal">
    <blockquote>Niemand stapt twee keer in dezelfde rivier.</blockquote>
    <cite>Heraclitus</cite>
  </div>
</section>

<section class="door-sec">
  <div class="wrap door-grid">
    <div class="door-copy reveal">
      <span class="eyebrow">Achter de deur</span>
      <h2 class="big" style="margin-top:28px">Argus<br><span class="soft">Systems.</span></h2>
      <p>De softwaretak van MATRIX, vernoemd naar Argus Panoptes, de wachter met honderd ogen. Tools voor productie en showoperators, gebouwd op de vloer en getest waar het telt: live, in het veld.</p>
      <a class="btn" href="argus.html">Betreed Argus <i>→</i></a>
    </div>
    <a class="door reveal" href="argus.html" aria-label="Naar ARGUS Systems"><img src="assets/img/argus/argus-embleem.png" alt="" width="400" height="399" loading="lazy"><span class="lbl">Argus</span></a>
  </div>
</section>

{contact_block()}
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


def projecten():
    cards = ''
    for slug, t, meta, role, client, single in PROJECTS:
        if single:
            cover, photos = f'assets/img/{single}', [f'assets/img/{single}']
        else:
            cover = f'assets/img/proj/{slug}/cover.jpg'
            photos = [f'assets/img/proj/{slug}/{f}' for f, _, _ in SETS[slug]]
        count = f'<span class="count">{len(photos)} foto\'s</span>' if len(photos) > 1 else ''
        client_html = f'<span class="client">{client}</span>' if client else ''
        cards += f'''
      <article class="proj reveal" id="{slug}">
        <button class="proj-img" type="button" data-title="{t}" data-gallery='{json.dumps(photos)}' aria-label="Bekijk foto's van {t}"><img src="{cover}" alt="{t}" loading="lazy">{count}</button>
        <div class="info"><h3>{t}</h3><span class="meta">{meta}</span><span class="role">{role}</span>{client_html}</div>
      </article>'''
    gal = '\n'.join(f'      <img src="assets/img/galerij/{i:02d}.jpg" alt="" width="1400" height="933" loading="lazy">' for i in range(1, 13))
    return f'''{head("Projecten | MATRIX E.I.L.", "Producties waar MATRIX E.I.L. licht, visuals en LED verzorgde.", "assets/img/electrisize.jpg")}
<body data-seed="2">
{header('projecten.html')}
<main>
<section class="section page-top">
  <div class="wrap">
    <div class="page-head">
      <span class="eyebrow reveal">Projecten · 2024 – 2026</span>
      <h1 class="mega reveal">Pro<br><span class="soft">jecten.</span></h1>
      <p class="lead reveal">Van stage- en lichtontwerp tot programmering, live operation, visuals en LED-infrastructuur. Klik op een project voor de foto's.</p>
    </div>
    <div class="proj-grid">{cards}
    </div>
  </div>
</section>

<section class="wrap quote reveal">
  <blockquote>The hidden attunement is better than the open.</blockquote>
  <cite>Heraclitus</cite>
</section>

<section class="section tight">
  <div class="wrap">
    <span class="eyebrow reveal" style="margin-bottom:40px">Uit het veld</span>
    <div class="gallery-grid gallery">
{gal}
    </div>
  </div>
</section>
{contact_block()}
</main>
{footer()}'''


# ---------------------------------------------------------------- Over
def over():
    return f'''{head("Over | MATRIX E.I.L.", "Over MATRIX E.I.L.: stage- en lichtontwerp, programmering, visuals en LED-techniek met aandacht voor het idee en de uitvoering.", "assets/img/over-matrix.jpg")}
<body data-seed="3">
{header('over.html')}
<main>
<section class="section page-top">
  <div class="wrap over-hero">
    <h1 class="huge reveal">Ieder moment<br>verdient een<br><span class="soft">eigen verhaal.</span></h1>
    <div class="ph unveil"><img src="assets/img/over-matrix.jpg" alt="Operator aan de lichttafel in een MATRIX-shirt" width="822" height="637" loading="lazy"></div>
    <p class="lead reveal">MATRIX E.I.L. verbindt stage- en lichtontwerp, programmering, visuals en LED-techniek. Met aandacht voor het idee én voor de uitvoering.</p>
  </div>
</section>

<section class="wrap chapter">
  <div class="side"><div class="num"><b>01</b><span>Oorsprong</span></div></div>
  <div class="main">
    <h2 class="big reveal">Waar het<br><span class="soft">begon.</span></h2>
    <div class="body-text reveal">
      <p>MATRIX E.I.L. begon vanuit de wens om zelfstandig te werken en als freelancer te groeien. Onderweg werd steeds duidelijker welke manier van werken daarbij hoort, en welke overtuiging daarachter zit.</p>
      <p>Ieder evenement verdient aandacht voor zijn eigen karakter. De plek, het publiek en de aanleiding vragen telkens om nieuwe afwegingen. Daar hoort een ontwerp bij waar gedachte en moeite in zitten.</p>
    </div>
  </div>
</section>

<section class="wrap chapter">
  <div class="side"><div class="num"><b>02</b><span>Werkwijze</span></div></div>
  <div class="main">
    <h2 class="big reveal">Een ontwerp moet<br><span class="soft">ergens over gaan.</span></h2>
    <div class="body-text reveal">
      <p>Een vertrouwde opstelling is snel gekozen. Toch verdient iedere productie opnieuw de vraag: waarom past dit hier?</p>
      <p>Voor MATRIX hoort die vraag bij het vak. Kijken naar de ruimte, mogelijkheden onderzoeken en verder denken dan de eerste oplossing. De beschikbare tijd en middelen geven grenzen aan; daarbinnen blijft ruimte voor bewuste keuzes.</p>
      <p>Een eenvoudige set kan precies goed zijn. Het verschil zit in de gedachte erachter. Waarom staat iets daar? Waar gaat de aandacht naartoe? Wat draagt het bij aan de ervaring?</p>
      <p>Licht, beeld en ruimte beïnvloeden elkaar. Duisternis kan een beweging betekenis geven. Een scherm kan diepte creëren, maar ook alle aandacht opeisen. De betekenis van een onderdeel ontstaat in samenhang met de rest.</p>
    </div>
    <p class="pull reveal">Die samenhang verdient zorg, van de eerste schets tot de laatste cue.</p>
  </div>
</section>

<section class="wrap reveal" style="padding-bottom:clamp(80px,10vw,150px)">
  <figure class="reel-full unveil" style="margin:0"><video src="assets/video/showreel.mp4" autoplay muted loop playsinline preload="auto" poster="assets/img/reel-poster.jpg" aria-label="Showreel met beelden van MATRIX-producties"></video></figure>
  <p class="eyebrow" style="margin-top:18px">Showreel · beelden uit het veld</p>
</section>

<section class="wrap chapter">
  <div class="side"><div class="num"><b>03</b><span>Samenwerking</span></div></div>
  <div class="main">
    <h2 class="big reveal">Een eigen signatuur.<br><span class="soft">Meerdere perspectieven.</span></h2>
    <div class="body-text reveal">
      <p>MATRIX heeft een persoonlijk begin. De ambitie is om vanuit die basis verder te bouwen met zelfstandige specialisten die hun eigen kennis, ideeën en oordeel meenemen.</p>
      <p>Een gedeelde overtuiging hoeft geen identieke blik op te leveren. Juist iemand die een andere vraag stelt, kan een ontwerp verder brengen. Daarvoor zijn vertrouwen, heldere afspraken en ruimte voor inhoudelijke discussie nodig.</p>
    </div>
    <p class="pull reveal">Wat we willen delen, is betrokkenheid bij het resultaat. Begrijpen waarom een keuze wordt gemaakt. Aandacht hebben voor elkaars werk. En de moeite nemen om een idee zorgvuldig uit te voeren.</p>
  </div>
</section>
{contact_block()}
</main>
{footer()}'''


# ---------------------------------------------------------------- ARGUS
TOOLS = [
    ('chronos', 'CHRONOS', 'Eén klok voor de hele productie', True),
    ('axis', 'AXIS', 'Planning, magazijn en show in één systeem', False),
    ('metron', 'METRON', 'Timing en tempo voor lichtoperators', False),
    ('horos', 'HOROS', 'Navigatie voor productietransport', False),
]


def argus():
    chambers = (ROOT / 'src' / 'argus-tools.html').read_text()
    index = ''.join(f'''
      <a href="#{slug}"><span class="nm">{name}</span><span class="ds">{ds}</span><span class="status{' field' if field else ''}">{'Alpha · in het veld' if field else 'In test'}</span></a>''' for slug, name, ds, field in TOOLS)
    return f'''{head("ARGUS Systems | Software uit de praktijk van live producties", "ARGUS Systems is de softwaretak van MATRIX E.I.L.: CHRONOS, AXIS, METRON en HOROS, tools gebouwd vanuit de praktijk van live producties.", "assets/img/chronos-overzicht.jpg", "assets/img/argus/favicon.png")}
<body class="argus-page" data-seed="4" id="top">
{argus_header()}
<main>
<section class="ar-hero">
  <div class="rings" aria-hidden="true"><i></i><i></i><i></i><i></i></div>
  <div class="wrap">
    <img class="emblem" src="assets/img/argus/argus-embleem.png" alt="" width="400" height="399">
    <h1>Argus<span>Systems</span></h1>
    <p class="lead">Software uit de praktijk van live producties. Gebouwd door de mensen die er zelf elke week mee werken.</p>
  </div>
</section>

<section class="section">
  <div class="wrap ar-intro">
    <h2 class="big reveal">Honderd ogen.<br><span class="soft">Eén show.</span></h2>
    <div class="body-text reveal">
      <p class="myth">Argus Panoptes, de wachter met honderd ogen, sliep nooit met alle ogen tegelijk. Er keek er altijd wel één.</p>
      <p>Op de vloer zien we elke week waar het schuurt: timetables die niet meer kloppen, planningen verspreid over losse lijstjes, informatie die net te laat aankomt.</p>
      <p>ARGUS Systems ontwikkelt de software die we zelf misten. Niet achter een bureau, maar op echte producties, getest door de mensen die er elke dag mee werken.</p>
    </div>
  </div>
</section>

<section class="section tight">
  <div class="wrap">
    <span class="eyebrow reveal" style="margin-bottom:40px">De tools · status 2026</span>
    <nav class="ar-index reveal" aria-label="Tools">{index}
    </nav>
  </div>
</section>

{chambers}
<section class="section ar-cta" id="contact">
  <div class="wrap grid">
    <span class="eyebrow reveal" style="grid-column:1/-1;margin-bottom:34px">Meebouwen</span>
    <h2 class="huge reveal">Zet Argus in op<br><span class="soft">jouw productie.</span></h2>
    <div class="side reveal">
      <p>Wil je een van onze tools testen op jouw evenement, of heb je een idee dat hier past? Operators en producties die mee willen bouwen, horen we graag.</p>
      <div class="btns"><a class="btn fill" href="mailto:{MAIL}?subject=ARGUS%20Systems">Mail ons <i>→</i></a><a class="btn" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp <i>→</i></a></div>
    </div>
  </div>
</section>
</main>
{footer()}'''


# ---------------------------------------------------------------- Privacy
def privacy():
    return f'''{head("Privacy | MATRIX E.I.L.", "Privacyverklaring van MATRIX E.I.L.")}
<body data-seed="5">
{header('privacy.html')}
<main>
<section class="section page-top" id="contact">
  <div class="wrap prose">
    <span class="eyebrow">Privacy</span>
    <h1 class="big">Privacy</h1>
    <p>MATRIX E.I.L. verzamelt via deze website geen persoonsgegevens. Er worden geen tracking- of advertentiecookies gebruikt. Neem je contact op via WhatsApp, e-mail of telefoon, dan gebruiken we je gegevens alleen om je bericht te beantwoorden.</p>
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
