const LANG = document.documentElement.lang || 'nl';
const QUOTES = LANG === 'en' ? [
  ['No man ever steps in the same river twice.', 'Heraclitus'],
  ['Everything flows.', 'Heraclitus'],
  ['The way up and the way down are one and the same.', 'Heraclitus'],
  ['Character is destiny.', 'Heraclitus'],
  ['The hidden harmony is better than the obvious.', 'Heraclitus'],
  ['If you do not expect the unexpected, you will not find it.', 'Heraclitus'],
  ['The sun is new each day.', 'Heraclitus'],
  ['Execution is the chariot of genius.', 'William Blake'],
] : LANG === 'de' ? [
  ['Niemand steigt zweimal in denselben Fluss.', 'Heraklit'],
  ['Alles fließt.', 'Heraklit'],
  ['Der Weg hinauf und hinab ist ein und derselbe.', 'Heraklit'],
  ['Charakter ist Schicksal.', 'Heraklit'],
  ['Die verborgene Harmonie ist stärker als die offenbare.', 'Heraklit'],
  ['Wer das Unerwartete nicht erwartet, wird es nicht finden.', 'Heraklit'],
  ['Die Sonne ist jeden Tag neu.', 'Heraklit'],
  ['Execution is the chariot of genius.', 'William Blake'],
] : [
  ['Niemand stapt twee keer in dezelfde rivier.', 'Heraclitus'],
  ['Alles stroomt.', 'Heraclitus'],
  ['De weg omhoog en de weg omlaag zijn één en dezelfde.', 'Heraclitus'],
  ['Karakter is lotsbestemming.', 'Heraclitus'],
  ['De verborgen harmonie is sterker dan de zichtbare.', 'Heraclitus'],
  ['Wie het onverwachte niet verwacht, zal het niet vinden.', 'Heraclitus'],
  ['De zon is elke dag nieuw.', 'Heraclitus'],
  ['Execution is the chariot of genius.', 'William Blake'],
];
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

// Mobiel menu
const btn = document.querySelector('.menu-btn');
const nav = document.querySelector('.nav');
if (btn && nav) {
  const setMenu = open => {
    nav.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open);
    document.body.classList.toggle('menu-open', open);
    document.body.style.overflow = open ? 'hidden' : '';
  };
  btn.addEventListener('click', () => setMenu(!nav.classList.contains('open')));
  nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  addEventListener('keydown', e => { if (e.key === 'Escape') setMenu(false); });
}

// Jaartal in de footer
document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

// Header wordt donker na het scrollen; knop terug naar boven met voortgangsring
const header = document.querySelector('.site-header');
const toTop = document.querySelector('.to-top');
const bar = toTop && toTop.querySelector('.bar');
const breakImg = document.querySelector('.photo-break img');
let ticking = false;
function onScroll() {
  const y = window.scrollY;
  const max = document.documentElement.scrollHeight - innerHeight;
  if (header) header.classList.toggle('solid', y > 60);
  if (toTop) {
    toTop.classList.toggle('show', y > innerHeight * .6);
    if (bar) bar.style.strokeDashoffset = 157 - 157 * Math.min(1, y / Math.max(1, max));
  }
  if (breakImg && !reduce) {
    const r = breakImg.parentElement.getBoundingClientRect();
    if (r.bottom > 0 && r.top < innerHeight) {
      const p = (r.top + r.height / 2 - innerHeight / 2) / innerHeight;
      breakImg.style.transform = `translate3d(0, ${p * -6}%, 0)`;
    }
  }
  ticking = false;
}
window.addEventListener('scroll', () => { if (!ticking) { requestAnimationFrame(onScroll); ticking = true; } }, { passive: true });
onScroll();
if (toTop) toTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }));

// Elementen laten verschijnen tijdens het scrollen
const reveals = document.querySelectorAll('.reveal, .unveil');
if ('IntersectionObserver' in window && !reduce) {
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -10% 0px' });
  reveals.forEach(el => io.observe(el));
} else {
  reveals.forEach(el => el.classList.add('in'));
}

// Volgspot die de muis volgt
if (finePointer && !reduce) {
  const spot = document.createElement('div');
  spot.className = 'spot';
  document.body.appendChild(spot);
  let sx = -999, sy = -999, tx = -999, ty = -999;
  addEventListener('mousemove', e => { tx = e.clientX; ty = e.clientY; }, { passive: true });
  (function follow() {
    sx += (tx - sx) * .12; sy += (ty - sy) * .12;
    spot.style.transform = `translate3d(${sx}px, ${sy}px, 0)`;
    requestAnimationFrame(follow);
  })();
}

// Fotoreeksen groot bekijken (projecten en galerij)
const box = document.createElement('div');
box.className = 'lightbox';
box.setAttribute('role', 'dialog');
box.setAttribute('aria-modal', 'true');
box.innerHTML = '<button class="lb-close" aria-label="Sluiten">✕</button><figure><img alt=""></figure>' +
  '<div class="lb-bar"><button class="lb-prev" aria-label="Vorige">←</button><span class="lb-title"></span><span class="lb-count"></span><button class="lb-next" aria-label="Volgende">→</button></div>';
const lbImg = box.querySelector('img');
let lbList = [], lbIdx = 0;
function lbShow(i) {
  lbIdx = (i + lbList.length) % lbList.length;
  lbImg.src = lbList[lbIdx];
  box.querySelector('.lb-count').textContent = lbList.length > 1 ? `${lbIdx + 1} / ${lbList.length}` : '';
  box.querySelectorAll('.lb-prev, .lb-next').forEach(b => { b.style.visibility = lbList.length > 1 ? 'visible' : 'hidden'; });
  const next = new Image(); next.src = lbList[(lbIdx + 1) % lbList.length];
}
function lbOpen(list, i, title) {
  if (!box.isConnected) document.body.appendChild(box);
  lbList = list;
  box.querySelector('.lb-title').textContent = title || '';
  lbShow(i);
  box.classList.add('open');
  document.body.style.overflow = 'hidden';
}
function lbClose() { box.classList.remove('open'); document.body.style.overflow = ''; }
box.addEventListener('click', e => {
  if (e.target.closest('.lb-prev')) lbShow(lbIdx - 1);
  else if (e.target.closest('.lb-next')) lbShow(lbIdx + 1);
  else if (e.target === lbImg) lbShow(lbIdx + 1);
  else if (!e.target.closest('.lb-bar')) lbClose();
});
document.addEventListener('keydown', e => {
  if (!box.classList.contains('open')) return;
  if (e.key === 'Escape') lbClose();
  if (e.key === 'ArrowRight') lbShow(lbIdx + 1);
  if (e.key === 'ArrowLeft') lbShow(lbIdx - 1);
});
let touchX = null;
box.addEventListener('touchstart', e => { touchX = e.touches[0].clientX; }, { passive: true });
box.addEventListener('touchend', e => {
  if (touchX === null) return;
  const dx = e.changedTouches[0].clientX - touchX;
  if (Math.abs(dx) > 40) lbShow(lbIdx + (dx < 0 ? 1 : -1));
  touchX = null;
});
document.querySelectorAll('[data-gallery]:not(.pp-grid)').forEach(el => {
  el.addEventListener('click', () => lbOpen(JSON.parse(el.dataset.gallery), 0, el.dataset.title));
});
const gallery = document.querySelector('.gallery');
if (gallery) {
  const imgs = [...gallery.querySelectorAll('img')];
  imgs.forEach((img, i) => img.addEventListener('click', () => lbOpen(imgs.map(x => x.src), i, 'Uit het veld')));
}

// Logboek: foto zweeft mee met de muis, klik opent de reeks
const logRows = document.querySelectorAll('.log tr.row');
if (logRows.length) {
  let float = null;
  if (finePointer) {
    float = document.createElement('div');
    float.className = 'log-float rm';
    float.innerHTML = '<img alt=""><span></span>';
    document.body.appendChild(float);
  }
  logRows.forEach(row => {
    const open = () => { const l = row.querySelector('td.show a'); if (l) l.click(); else location.href = row.dataset.href; };
    row.addEventListener('click', open);
    row.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
    if (!float) return;
    row.addEventListener('mouseenter', () => {
      float.firstChild.src = row.dataset.cover;
      float.lastChild.textContent = row.querySelector('.no').firstChild.textContent + ' · ' + row.dataset.title.replace('&amp;', '&');
      float.classList.add('show');
    });
    row.addEventListener('mouseleave', () => float.classList.remove('show'));
    row.addEventListener('mousemove', e => {
      const x = Math.min(e.clientX + 36, innerWidth - 360);
      float.style.transform = `translate3d(${x}px, ${e.clientY - 120}px, 0)`;
    });
  });
}

// Timecode (tijd van de dag, 25 beelden per seconde) in de showbalk en op de monitor
const tcEls = document.querySelectorAll('.tc');
const pad = n => String(n).padStart(2, '0');
function tcNow() {
  const d = new Date();
  return `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}:${pad(Math.floor(d.getMilliseconds() / 40))}`;
}
const tcLive = [...tcEls].filter(el => el.closest('.showbar, .osd'));
if (tcLive.length) {
  let last = 0;
  (function loop(t) {
    if (t - last > 40) { const v = tcNow(); tcLive.forEach(el => { el.textContent = v; }); last = t; }
    requestAnimationFrame(loop);
  })(0);
}

// Cues: elke sectie met data-cue komt in de cuelijst; de actieve cue staat in de showbalk
const cues = [...document.querySelectorAll('[data-cue]')];
const cueNow = document.querySelector('.showbar .cue-now');
if (cues.length) {
  let list = null;
  if (cues.length > 1) {
    list = document.createElement('nav');
    list.className = 'cuelist';
    list.setAttribute('aria-label', 'Cuelijst');
    list.innerHTML = '<span class="lbl">Cuelijst</span>' + cues.map((c, i) => {
      if (!c.id) c.id = 'cue-' + (i + 1);
      return `<a href="#${c.id}"><span class="n">${c.dataset.cueName}</span><span class="q">${c.dataset.cue}</span></a>`;
    }).join('');
    document.body.appendChild(list);
  }
  const setCue = c => {
    if (cueNow) cueNow.textContent = `${c.dataset.cue} · ${c.dataset.cueName}`;
    if (list) list.querySelectorAll('a').forEach((a, i) => a.classList.toggle('on', cues[i] === c));
  };
  setCue(cues[0]);
  const pickCue = () => {
    const mid = innerHeight * .45;
    let cur = cues[0];
    cues.forEach(c => { if (c.getBoundingClientRect().top < mid) cur = c; });
    setCue(cur);
  };
  addEventListener('scroll', pickCue, { passive: true });
  pickCue();
}

// Uitlezing linksonder: pan en tilt volgen de muis, intensiteit de scroll
if (finePointer && !reduce) {
  const ro = document.createElement('div');
  ro.className = 'readout';
  ro.setAttribute('aria-hidden', 'true');
  ro.innerHTML = '<span>PAN <b class="p">270.0</b>°</span><span>TILT <b class="t">135.0</b>°</span><span>INT <b class="i">100</b>%</span>';
  document.body.appendChild(ro);
  const [p, t, i] = ['.p', '.t', '.i'].map(s => ro.querySelector(s));
  addEventListener('mousemove', e => {
    p.textContent = (e.clientX / innerWidth * 540).toFixed(1).padStart(5, '0');
    t.textContent = (e.clientY / innerHeight * 270).toFixed(1).padStart(5, '0');
  }, { passive: true });
  addEventListener('scroll', () => {
    const max = document.documentElement.scrollHeight - innerHeight;
    i.textContent = String(Math.round(100 - 70 * Math.min(1, scrollY / Math.max(1, max)))).padStart(3, '0');
  }, { passive: true });
}

// Manifest: de tekst licht woord voor woord op tijdens het scrollen
document.querySelectorAll('.scrub').forEach(el => {
  el.innerHTML = el.textContent.trim().split(/\s+/).map(w => `<span>${w}</span>`).join(' ');
  const words = [...el.children];
  const update = () => {
    const r = el.getBoundingClientRect();
    const p = reduce ? 1 : Math.min(1, Math.max(0, (innerHeight * .85 - r.top) / (r.height + innerHeight * .35)));
    const n = Math.round(p * words.length);
    words.forEach((w, k) => w.classList.toggle('lit', k < n));
  };
  addEventListener('scroll', update, { passive: true });
  update();
});

// Blackout en GO tussen pagina's; bij het eerste bezoek aan de home een korte intro
const standby = document.querySelector('.standby');
const sb = standby && standby.querySelector('.sb');
if (standby && !reduce) {
  let first = false;
  try { first = document.body.classList.contains('home') && !sessionStorage.getItem('matrix-intro'); sessionStorage.setItem('matrix-intro', '1'); } catch (e) { first = false; }
  if (first) {
    document.body.classList.add('intro');
    const steps = [[{ en: 'House lights out', de: 'Saallicht aus' }[LANG] || 'Zaallicht uit', '…'], ['Standby', 'Q1'], ['', 'GO']];
    steps.forEach(([small, big], k) => setTimeout(() => {
      sb.innerHTML = `${small}<b${big === 'GO' ? ' class="go"' : ''}>${big}</b>`;
    }, k * 650));
    setTimeout(() => document.body.classList.add('go'), steps.length * 650 + 150);
  }
  document.querySelectorAll('a[href$=".html"], a[href*=".html#"]').forEach(a => {
    a.addEventListener('click', e => {
      if (e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank') return;
      e.preventDefault();
      const target = a.getAttribute('href').split('#')[0];
      const portal = document.querySelector('.portal');
      if (portal && (target.endsWith('argus.html')) !== document.body.classList.contains('argus-page')) {
        portal.classList.add('go');
        setTimeout(() => { location.href = a.href; }, 950);
        return;
      }
      const page = { 'index.html': 'Home', 'projecten.html': 'Projecten', 'over.html': 'Over', 'argus.html': 'Argus', 'privacy.html': 'Privacy', 'diensten.html': 'Diensten' };
      const txt = a.textContent.replace(/[←→]/g, '').trim();
      const label = page[target] || (txt && txt.length < 26 ? txt : 'GO');
      const [q, who] = QUOTES[Math.floor(Math.random() * QUOTES.length)];
      sb.innerHTML = `Standby<b>${label}</b><i>“${q}” · ${who}</i>`;
      document.body.classList.remove('intro', 'go');
      document.body.classList.add('leaving');
      setTimeout(() => { location.href = a.href; }, 380);
    });
  });
  addEventListener('pageshow', e => { if (e.persisted) { document.body.classList.remove('leaving'); const pt = document.querySelector('.portal'); if (pt) pt.classList.remove('go'); } });
}

// Projectpagina: foto's groot bekijken
document.querySelectorAll('.pp-grid').forEach(grid => {
  const list = JSON.parse(grid.dataset.gallery);
  grid.querySelectorAll('.pp-ph').forEach(b => b.addEventListener('click', () => lbOpen(list, +b.dataset.i, grid.dataset.title)));
});

// Hero: de volgspot onthult het beeld; zonder muis zwerft hij zelf rond
const lit = document.querySelector('.hero-lit');
if (lit && !reduce) {
  const hero = lit.parentElement;
  let mx = 50, my = 40, tx = 50, ty = 40, lastMove = 0;
  hero.addEventListener('pointermove', e => {
    const r = hero.getBoundingClientRect();
    tx = (e.clientX - r.left) / r.width * 100; ty = (e.clientY - r.top) / r.height * 100; lastMove = performance.now();
  });
  (function sweep(t) {
    if (t - lastMove > 2500) { tx = 50 + Math.sin(t / 3100) * 32; ty = 42 + Math.sin(t / 2300) * 16; }
    mx += (tx - mx) * .06; my += (ty - my) * .06;
    lit.style.setProperty('--mx', mx.toFixed(2) + '%'); lit.style.setProperty('--my', my.toFixed(2) + '%');
    requestAnimationFrame(sweep);
  })(0);
}

// ---------------------------------------------------------------- Easter eggs
const toastEl = document.createElement('div');
toastEl.className = 'toast'; toastEl.setAttribute('role', 'status');
document.body.appendChild(toastEl);
let toastT;
function toast(html, ms = 3200) {
  toastEl.innerHTML = html; toastEl.classList.add('show');
  clearTimeout(toastT); toastT = setTimeout(() => toastEl.classList.remove('show'), ms);
}

// Footer-quote: elke keer een andere, klik voor de volgende
const fq = document.querySelector('.foot-quote');
if (fq) {
  let qi = Math.floor(Math.random() * QUOTES.length);
  const show = () => { fq.querySelector('span').textContent = QUOTES[qi][0]; fq.querySelector('cite').textContent = QUOTES[qi][1]; };
  show();
  fq.addEventListener('click', () => { fq.classList.add('swap'); setTimeout(() => { qi = (qi + 1) % QUOTES.length; show(); fq.classList.remove('swap'); }, 300); });
}

// Klik op LIVE: hoe lang je al meekijkt
const t0 = Date.now();
const liveDot = document.querySelector('.showbar .live');
if (liveDot) liveDot.addEventListener('click', () => {
  const s = Math.floor((Date.now() - t0) / 1000);
  toast(`Je kijkt al <b>${pad(Math.floor(s / 60))}:${pad(s % 60)}</b> mee. De show loopt.`);
});

// Toetsen zoals op een lichttafel: B = blackout, G = GO. Typ "argus" voor het oog, de Konami-code voor een toegift.
const black = document.createElement('div');
black.className = 'blackout-layer'; black.textContent = 'Blackout · druk B';
document.body.appendChild(black);
let typed = '';
const KONAMI = 'ArrowUp,ArrowUp,ArrowDown,ArrowDown,ArrowLeft,ArrowRight,ArrowLeft,ArrowRight,b,a';
let keys = [];
addEventListener('keydown', e => {
  if (e.target.closest('input, textarea, select') || e.metaKey || e.ctrlKey || e.altKey) return;
  keys = [...keys, e.key].slice(-10);
  if (keys.join(',') === KONAMI) { encore(); keys = []; return; }
  const k = e.key.toLowerCase();
  typed = (typed + k).slice(-5);
  if (typed === 'argus') { bigEye(); typed = ''; return; }
  if (k === 'b' && keys[keys.length - 2] !== 'ArrowRight') {
    document.body.classList.toggle('blackout');
    if (document.body.classList.contains('blackout')) toast('<b>Blackout.</b> Druk nog een keer op B voor licht.');
  }
  if (k === 'g' && !typed.endsWith('arg') && !document.body.classList.contains('blackout')) {
    document.body.classList.add('leaving');
    setTimeout(() => document.body.classList.remove('leaving'), 420);
    toast('<b>GO.</b> Volgende cue.', 1800);
  }
  if (k === 'f') fohPanel();
  if (k === 'h') hazer();
  if (k === 's' && !reduce) strobe();
  if (e.key === '?') cheatSheet();
});
black.addEventListener('click', () => document.body.classList.remove('blackout'));

function bigEye() {
  const wrap = document.createElement('div');
  wrap.className = 'big-eye';
  wrap.innerHTML = '<svg viewBox="0 0 600 600" aria-hidden="true"><defs><radialGradient id="beG"><stop offset="0" stop-color="#3fd8ee"/><stop offset=".5" stop-color="#d9ad4f"/><stop offset="1" stop-color="#1a140a"/></radialGradient><clipPath id="beClip"><path d="M60,300 Q300,80 540,300 Q300,520 60,300 Z"/></clipPath></defs>' +
    '<g class="lids"><path class="lid" d="M60,300 Q300,80 540,300 Q300,520 60,300 Z"/><g clip-path="url(#beClip)"><g class="pg"><circle cx="300" cy="300" r="96" fill="url(#beG)"/><circle cx="300" cy="300" r="40" fill="#030607"/><circle cx="318" cy="282" r="8" fill="#fff" opacity=".8"/></g></g></g></svg>' +
    '<p>Argus ziet je</p>';
  document.body.appendChild(wrap);
  requestAnimationFrame(() => wrap.classList.add('show'));
  const pg = wrap.querySelector('.pg');
  const look = e => {
    const dx = e.clientX - innerWidth / 2, dy = e.clientY - innerHeight / 2, d = Math.hypot(dx, dy) || 1, k = Math.min(1, d / 300);
    pg.setAttribute('transform', `translate(${dx / d * 90 * k} ${dy / d * 50 * k})`);
  };
  addEventListener('mousemove', look);
  setTimeout(() => wrap.classList.add('blink'), 1600); setTimeout(() => wrap.classList.remove('blink'), 1780);
  setTimeout(() => wrap.classList.add('blink'), 3100); setTimeout(() => wrap.classList.remove('blink'), 3280);
  const close = () => { wrap.classList.remove('show'); removeEventListener('mousemove', look); setTimeout(() => wrap.remove(), 700); };
  setTimeout(close, 4600); wrap.addEventListener('click', close);
}

function encore() {
  const el = document.createElement('div');
  el.className = 'encore';
  const [q, who] = QUOTES[Math.floor(Math.random() * QUOTES.length)];
  el.innerHTML = `<div><h2>Toe<br><em>gift.</em></h2><p>Je vond de verborgen cue. “${q}” · ${who}</p></div>`;
  document.body.appendChild(el);
  requestAnimationFrame(() => el.classList.add('show'));
  const close = () => { el.classList.remove('show'); setTimeout(() => el.remove(), 600); };
  el.addEventListener('click', close); setTimeout(close, 5000);
}

// Logo vijf keer snel aanklikken
const logoEl = document.querySelector('.site-header .logo');
if (logoEl) {
  let clicks = 0, ct;
  logoEl.addEventListener('click', e => {
    clicks++; clearTimeout(ct); ct = setTimeout(() => { clicks = 0; }, 900);
    if (clicks >= 3 && document.body.classList.contains('home')) e.preventDefault();
    if (clicks === 5) { clicks = 0; e.preventDefault(); toast('<b>Encore!</b> Druk ↑↑↓↓←→←→BA voor meer.', 4000); }
  });
}

// Wie lang stilstaat, krijgt een pauzescherm
if (!reduce) {
  const ss = document.createElement('div');
  ss.className = 'screensaver';
  ss.innerHTML = `<div><img src="${document.querySelector('.logo img').getAttribute('src')}" alt=""><p>${{ en: 'Changeover between two acts', de: 'Umbaupause zwischen zwei Acts' }[LANG] || 'Pauze tussen twee acts'}</p><q></q></div>`;
  document.body.appendChild(ss);
  let idle;
  const wake = () => {
    ss.classList.remove('show'); clearTimeout(idle);
    idle = setTimeout(() => { ss.querySelector('q').textContent = QUOTES[Math.floor(Math.random() * QUOTES.length)][0]; ss.classList.add('show'); }, 120000);
  };
  ['mousemove', 'keydown', 'scroll', 'touchstart', 'click'].forEach(ev => addEventListener(ev, wake, { passive: true }));
  wake();
}

// FOH-modus: faders voor kleur, licht en rook
function fohPanel() {
  let p = document.querySelector('.foh');
  if (p) { p.classList.toggle('show'); document.body.classList.toggle('foh-open', p.classList.contains('show')); return; }
  p = document.createElement('div');
  p.className = 'foh show';
  document.body.classList.add('foh-open');
  p.innerHTML = '<div class="foh-head"><b>FOH</b><span>Jij hebt nu de tafel</span><button aria-label="Sluit">×</button></div>' +
    ['Kleur', 'Master', 'Haze', 'Strobe'].map((n, i) => `<label class="fdr"><input type="range" min="0" max="100" value="${[0, 100, 30, 0][i]}" data-f="${i}" orient="vertical"><span>${n}</span><b>${[0, 100, 30, 0][i]}</b></label>`).join('');
  document.body.appendChild(p);
  const root = document.documentElement, base = getComputedStyle(root).getPropertyValue('--accent');
  let strobeId = null;
  p.querySelector('button').addEventListener('click', () => { p.classList.remove('show'); document.body.classList.remove('foh-open'); });
  p.querySelectorAll('input').forEach(inp => inp.addEventListener('input', () => {
    const v = +inp.value; inp.nextElementSibling.nextElementSibling.textContent = v;
    if (inp.dataset.f === '0') root.style.setProperty('--accent', v ? `hsl(${(325 + v * 3.6) % 360} 90% 55%)` : base);
    if (inp.dataset.f === '1') document.querySelector('main').style.filter = v < 100 ? `brightness(${.15 + v / 117})` : '';
    if (inp.dataset.f === '2') { const sm = document.querySelector('.smoke'); if (sm) sm.style.opacity = .3 + v / 30; }
    if (inp.dataset.f === '3') {
      clearInterval(strobeId); document.body.classList.remove('flash-on');
      if (v > 0 && !reduce) strobeId = setInterval(() => document.body.classList.toggle('flash-on'), 600 - v * 3.5);
      if (v === 0) document.body.classList.remove('flash-on');
    }
  }));
  toast('<b>FOH-modus.</b> Niet aan de master komen. Grapje, ga je gang.');
}

// Rookmachine: de pagina loopt even vol haze
function hazer() {
  if (document.querySelector('.haze-burst')) return;
  const h = document.createElement('div');
  h.className = 'haze-burst';
  h.innerHTML = '<i></i><i></i><i></i><i></i>';
  document.body.appendChild(h);
  setTimeout(() => h.remove(), 9000);
  toast(['<b>Hazer aan.</b> Hopelijk heeft iemand de rookmelders overbrugd.', '<b>Hazer aan.</b> Nu zie je pas wat de beams doen.', '<b>Hazer op 100%.</b> De fotograaf is blij, de brandweer minder.'][Math.floor(Math.random() * 3)]);
}

// Strobe: kort, en onder de drie flitsen per seconde
function strobe() {
  if (document.body.classList.contains('strobing')) return;
  document.body.classList.add('strobing');
  let n = 0;
  const id = setInterval(() => { document.body.classList.toggle('flash-on'); if (++n >= 6) { clearInterval(id); document.body.classList.remove('flash-on', 'strobing'); } }, 360);
  toast('<b>Strobe.</b> Even kort. Epilepsiewaarschuwing staat op de flyer.', 2200);
}

// Spiekbriefje met de sneltoetsen
function cheatSheet() {
  toast('<b>Tafeltoetsen</b> · B blackout · G go · F FOH · H hazer · S strobe · typ “argus”', 6000);
}

// Knoppen die je niet mag indrukken
const NOPE = [
  ['Dat was de clear-knop. De programmer is leeg. Succes.', 'shake'],
  ['Grand master op 0. Het publiek klapt alvast.', 'dim'],
  ['Je hebt net de intro van de headliner gestart. Tien minuten te vroeg.', ''],
  ['Fixture 101 zit nu op adres 1. En adres 1 is weg.', 'shake'],
  ['Timecode kwijt. De DJ draait toch een andere track.', ''],
  ['Dat was de noodstop van de kinetics. Grapje. Toch?', 'shake'],
  ['Highlight aan. Iedereen ziet er nu slecht uit.', 'bright'],
  ['Je hebt de showfile overschreven met “test_final_echt_v2”. TARTARUS heeft hem gelukkig nog.', ''],
  ['De rookmelder gaat af. De zaal staat buiten.', 'haze'],
  ['Changeover gestart. De drummer staat nog op het podium.', ''],
  ['Alle moving heads kijken nu naar de bar.', 'shake'],
  ['Strobe op 100% tijdens de ballad. De zanger kijkt je aan.', 'strobe'],
  ['Je hebt de productieleider gebeld. Om 04:00.', ''],
  ['Universe 1 ging net offline. Universe 2 doet solidair mee.', 'dim'],
  ['Niet indrukken, stond er. Hier is een quote als straf: “Karakter is lotsbestemming.” · Heraclitus', ''],
];
let nopeBag = [];
function nope() {
  if (!nopeBag.length) nopeBag = NOPE.map((_, i) => i).sort(() => Math.random() - .5);
  const [txt, fx] = NOPE[nopeBag.pop()];
  if (fx === 'shake') { document.body.classList.remove('shake'); void document.body.offsetWidth; document.body.classList.add('shake'); }
  if (fx === 'dim') { document.body.classList.add('dim'); setTimeout(() => document.body.classList.remove('dim'), 1600); }
  if (fx === 'bright') { document.body.classList.add('bright'); setTimeout(() => document.body.classList.remove('bright'), 1400); }
  if (fx === 'haze') hazer();
  if (fx === 'strobe' && !reduce) strobe();
  toast(txt, 3600);
}
document.querySelectorAll('.foot-bottom').forEach(fb => {
  const b = document.createElement('button');
  b.className = 'nope'; b.type = 'button'; b.innerHTML = '<i></i>Niet indrukken';
  b.addEventListener('click', nope);
  fb.appendChild(b);
});

// Load-out: wie de site met de muis bovenaan verlaat, krijgt een vrachtwagen te zien
if (finePointer) {
  let shown = false;
  try { shown = sessionStorage.getItem('matrix-loadout') === '1'; } catch (e) {}
  document.addEventListener('mouseout', e => {
    if (shown || e.relatedTarget || e.clientY > 8) return;
    shown = true;
    try { sessionStorage.setItem('matrix-loadout', '1'); } catch (err) {}
    const t = document.createElement('div');
    t.className = 'loadout';
    t.innerHTML = '<span class="truck" aria-hidden="true"><b>MATRIX</b></span>';
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 5200);
    toast('<b>Load-out?</b> Vergeet de gaffa niet. En ons nummer: wa.me/31630971404', 4800);
  });
}

// Voor wie in de console kijkt
console.log('%cMATRIX E.I.L.%c\nExecution is the chariot of genius.\n\nZelfstandige specialist met een eigen blik? info@matrixeventsupport.nl\nTip: typ "argus" op de site, of druk op ? voor de tafeltoetsen.', 'font: 700 28px sans-serif; color: #ec0a8c', 'font: 13px monospace; color: #9a938a');

// ---------------------------------------------------------------- Organisch: rook, stof, vuur en hittetrilling
const SVGNS = 'http://www.w3.org/2000/svg';

// Rook en stof: een dunne laag haze die traag door de pagina drijft, met stofjes die oplichten in het licht van de cursor
(function smoke() {
  if (reduce) return;
  const cv = document.createElement('canvas');
  cv.className = 'smoke'; cv.setAttribute('aria-hidden', 'true');
  document.body.appendChild(cv);
  const ctx = cv.getContext('2d');
  const small = innerWidth < 700;
  let w, h, mx = -999, my = -999, lx = -999, ly = -999, t = 0, running = true;
  const size = () => { const dpr = Math.min(1.5, devicePixelRatio || 1); w = innerWidth; h = innerHeight; cv.width = w * dpr; cv.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
  size(); addEventListener('resize', size);
  addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; }, { passive: true });
  document.addEventListener('mouseleave', () => { mx = my = -999; });
  // Rookwolken: grote zachte vlekken die langzaam zijwaarts drijven en ademen
  const clouds = Array.from({ length: small ? 4 : 7 }, (_, i) => ({
    x: Math.random(), y: Math.random(), r: .35 + Math.random() * .35,
    vx: (.00004 + Math.random() * .00008) * (i % 2 ? 1 : -1), ph: Math.random() * 6.28,
    warm: Math.random() < .35,
  }));
  // Stofjes: klein, traag, zwevend
  const motes = Array.from({ length: small ? 34 : 110 }, () => ({
    x: Math.random(), y: Math.random(), z: .3 + Math.random() * .7,
    vx: (Math.random() - .5) * .00006, vy: -(.00002 + Math.random() * .00008), ph: Math.random() * 6.28,
  }));
  let lastY = scrollY;
  function tick() {
    if (!running) return;
    t++;
    const dy = (scrollY - lastY) / h; lastY = scrollY;
    lx += ((mx < 0 ? -999 : mx) - lx) * (lx < -900 ? 1 : .06); ly += ((my < 0 ? -999 : my) - ly) * (ly < -900 ? 1 : .06);
    ctx.clearRect(0, 0, w, h);
    const R = Math.max(w, h);
    clouds.forEach(c => {
      c.x += c.vx; if (c.x > 1.4) c.x = -.4; if (c.x < -.4) c.x = 1.4;
      c.y -= dy * .25; if (c.y < -.4) c.y += 1.8; if (c.y > 1.4) c.y -= 1.8;
      const breathe = .5 + .5 * Math.sin(t / 420 + c.ph);
      const x = c.x * w, y = c.y * h, r = c.r * R * (.9 + breathe * .2);
      const g = ctx.createRadialGradient(x, y, 0, x, y, r);
      const col = c.warm ? '236, 190, 160' : '170, 200, 190';
      g.addColorStop(0, `rgba(${col}, ${.035 + breathe * .02})`);
      g.addColorStop(.6, `rgba(${col}, .012)`);
      g.addColorStop(1, `rgba(${col}, 0)`);
      ctx.fillStyle = g; ctx.fillRect(x - r, y - r, r * 2, r * 2);
    });
    motes.forEach(m => {
      m.x += m.vx + Math.sin(t / 160 + m.ph) * .00012 * m.z;
      m.y += m.vy - dy * m.z * .6;
      if (m.y < -.02) { m.y = 1.02; m.x = Math.random(); }
      if (m.y > 1.02) { m.y = -.02; m.x = Math.random(); }
      if (m.x < -.02) m.x = 1.02; if (m.x > 1.02) m.x = -.02;
      const x = m.x * w, y = m.y * h;
      const d = lx > -900 ? Math.hypot(x - lx, y - ly) : 999;
      const lit = Math.max(0, 1 - d / 280) ** 1.5;
      const tw = .5 + .5 * Math.sin(t / 50 + m.ph * 3);
      const a = (.12 + tw * .1) * m.z + lit * .8;
      ctx.beginPath(); ctx.arc(x, y, (.6 + m.z * 1.1) * (1 + lit * .8), 0, 6.283);
      ctx.fillStyle = `rgba(255, 236, 214, ${a.toFixed(3)})`;
      ctx.fill();
    });
    requestAnimationFrame(tick);
  }
  document.addEventListener('visibilitychange', () => { running = !document.hidden; if (running) tick(); });
  tick();
})();

// Vonken die opstijgen boven het manifest
document.querySelectorAll('canvas.embers').forEach(cv => {
  if (reduce) return;
  const ctx = cv.getContext('2d');
  let w, h, parts = [], running = false;
  const size = () => { const dpr = Math.min(2, devicePixelRatio || 1); w = cv.clientWidth; h = cv.clientHeight; cv.width = w * dpr; cv.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); };
  const spawn = () => ({ x: Math.random() * w, y: h + 10, vx: (Math.random() - .5) * .4, vy: -(.4 + Math.random() * 1.2), r: .6 + Math.random() * 1.8, life: 0, max: 260 + Math.random() * 260, hue: Math.random() < .15 ? 320 : 18 + Math.random() * 22 });
  size(); addEventListener('resize', size);
  for (let i = 0; i < 70; i++) { const p = spawn(); p.y = Math.random() * h; p.life = Math.random() * p.max; parts.push(p); }
  function tick() {
    if (!running) return;
    ctx.clearRect(0, 0, w, h);
    parts.forEach((p, i) => {
      p.life++; p.x += p.vx + Math.sin((p.life + i * 30) / 40) * .35; p.y += p.vy;
      const a = Math.sin(Math.PI * p.life / p.max) * (.55 + Math.random() * .45);
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `hsla(${p.hue}, 100%, ${60 + Math.random() * 15}%, ${Math.max(0, a)})`;
      ctx.shadowBlur = 8; ctx.shadowColor = `hsla(${p.hue}, 100%, 55%, .8)`;
      ctx.fill();
      if (p.life > p.max || p.y < -10) parts[i] = spawn();
    });
    requestAnimationFrame(tick);
  }
  new IntersectionObserver(es => es.forEach(e => { running = e.isIntersecting; if (running) tick(); })).observe(cv);
});

// Hittetrilling: foto's trillen even als lucht boven een podium
if (finePointer && !reduce) {
  const defs = document.createElementNS(SVGNS, 'svg');
  defs.setAttribute('width', 0); defs.setAttribute('height', 0); defs.style.position = 'absolute';
  defs.innerHTML = '<filter id="heat" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.008 0.03" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="0" xChannelSelector="R" yChannelSelector="G"/></filter>';
  document.body.appendChild(defs);
  const turb = defs.querySelector('feTurbulence'), disp = defs.querySelector('feDisplacementMap');
  let target = null, amt = 0, t = 0, raf = null;
  const loop = () => {
    t += 1; amt += ((target ? 16 : 0) - amt) * .08;
    turb.setAttribute('baseFrequency', `0.008 ${(0.03 + Math.sin(t / 30) * .006).toFixed(4)}`);
    turb.setAttribute('seed', String(4 + Math.floor(t / 6) % 3));
    disp.setAttribute('scale', amt.toFixed(2));
    if (target || amt > .2) raf = requestAnimationFrame(loop); else { document.querySelectorAll('.heat-on').forEach(x => x.classList.remove('heat-on')); raf = null; }
  };
  document.querySelectorAll('.work-media img, .mini-img img, .svc-img img, .proj-img img, .strip-track img').forEach(img => {
    img.addEventListener('mouseenter', () => { document.querySelectorAll('.heat-on').forEach(x => x.classList.remove('heat-on')); img.classList.add('heat-on'); target = img; if (!raf) loop(); });
    img.addEventListener('mouseleave', () => { target = null; });
  });
}
