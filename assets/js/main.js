const QUOTES = [
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
    const steps = [['Zaallicht uit', '…'], ['Standby', 'Q1'], ['', 'GO']];
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
      if (portal && (target === 'argus.html') !== document.body.classList.contains('argus-page')) {
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
  if (k === 'g' && !document.body.classList.contains('blackout')) {
    document.body.classList.add('leaving');
    setTimeout(() => document.body.classList.remove('leaving'), 420);
    toast('<b>GO.</b> Volgende cue.', 1800);
  }
});
black.addEventListener('click', () => document.body.classList.remove('blackout'));

function bigEye() {
  const wrap = document.createElement('div');
  wrap.className = 'big-eye';
  wrap.innerHTML = '<svg viewBox="0 0 600 600" aria-hidden="true"><defs><radialGradient id="beG"><stop offset="0" stop-color="#3fd8ee"/><stop offset=".5" stop-color="#d9ad4f"/><stop offset="1" stop-color="#1a140a"/></radialGradient></defs>' +
    '<g class="lids"><path class="lid" d="M60,300 Q300,80 540,300 Q300,520 60,300 Z"/><g class="pg"><circle cx="300" cy="300" r="96" fill="url(#beG)"/><circle cx="300" cy="300" r="40" fill="#030607"/><circle cx="318" cy="282" r="8" fill="#fff" opacity=".8"/></g></g></svg>' +
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
  ss.innerHTML = '<div><img src="assets/img/logo-matrix.png" alt=""><p>Pauze tussen twee acts</p><q></q></div>';
  document.body.appendChild(ss);
  let idle;
  const wake = () => {
    ss.classList.remove('show'); clearTimeout(idle);
    idle = setTimeout(() => { ss.querySelector('q').textContent = QUOTES[Math.floor(Math.random() * QUOTES.length)][0]; ss.classList.add('show'); }, 120000);
  };
  ['mousemove', 'keydown', 'scroll', 'touchstart', 'click'].forEach(ev => addEventListener(ev, wake, { passive: true }));
  wake();
}

// Voor wie in de console kijkt
console.log('%cMATRIX E.I.L.%c\nExecution is the chariot of genius.\n\nZelfstandige specialist met een eigen blik? info@matrixeventsupport.nl\nTip: typ "argus" op de site, of probeer B.', 'font: 700 28px sans-serif; color: #ec0a8c', 'font: 13px monospace; color: #9a938a');

// ---------------------------------------------------------------- Organisch: groei, vuur en hittetrilling
const SVGNS = 'http://www.w3.org/2000/svg';

// Groeiende lijnen: als wortels of kabels lopen ze door de pagina en groeien mee met het scrollen
(function growth() {
  if (innerWidth < 700) return;
  let seed = [...location.pathname].reduce((a, c) => a + c.charCodeAt(0), 7);
  const rnd = () => { seed = (seed * 9301 + 49297) % 233280; return seed / 233280; };
  const svg = document.createElementNS(SVGNS, 'svg');
  svg.setAttribute('class', 'growth'); svg.setAttribute('aria-hidden', 'true');
  document.body.appendChild(svg);
  let runs = [], nodes = [];
  function build() {
    seed = [...location.pathname].reduce((a, c) => a + c.charCodeAt(0), 7);
    svg.innerHTML = ''; runs = []; nodes = [];
    const H = document.documentElement.scrollHeight, W = document.documentElement.clientWidth;
    svg.setAttribute('width', W); svg.setAttribute('height', H); svg.style.height = H + 'px';
    const wrap = document.querySelector('main .wrap');
    const r = wrap ? wrap.getBoundingClientRect() : { left: 40, width: W - 80 };
    const pad = parseFloat(getComputedStyle(wrap || document.body).paddingLeft) || 40;
    const left = r.left + pad * .5, width = r.width - pad;
    const cols = [0, .25, .5, .75, 1].map(f => left + f * width);
    const strands = [0, 4, rnd() > .5 ? 2 : 1];
    strands.forEach((ci, si) => {
      let x = cols[ci], y = innerHeight * (.7 + rnd() * .5) + si * 180;
      let d = `M${x.toFixed(1)},${y.toFixed(1)}`, start = y;
      while (y < H - 200) {
        const step = 140 + rnd() * 220;
        let nx = cols[ci] + (rnd() - .5) * 46;
        if (rnd() < .16) { // tak naar een buurkolom
          const nci = Math.max(0, Math.min(4, ci + (rnd() < .5 ? -1 : 1)));
          const tx = cols[nci], ty = y + step * .6;
          const tw = `M${x.toFixed(1)},${y.toFixed(1)} C${x.toFixed(1)},${(y + step * .4).toFixed(1)} ${tx.toFixed(1)},${(ty - step * .3).toFixed(1)} ${tx.toFixed(1)},${(ty + step).toFixed(1)}`;
          runs.push({ d: tw, y0: y, y1: ty + step, twig: true });
          nodes.push({ x: tx, y: ty + step, hot: rnd() < .3 });
        }
        const cy1 = y + step * .35, cy2 = y + step * .7;
        d += ` C${(x + (rnd() - .5) * 60).toFixed(1)},${cy1.toFixed(1)} ${(nx + (rnd() - .5) * 60).toFixed(1)},${cy2.toFixed(1)} ${nx.toFixed(1)},${(y + step).toFixed(1)}`;
        x = nx; y += step;
        if (rnd() < .22) nodes.push({ x, y, hot: rnd() < .25 });
      }
      runs.push({ d, y0: start, y1: y, twig: false });
    });
    runs.forEach(run => {
      const p = document.createElementNS(SVGNS, 'path');
      p.setAttribute('d', run.d);
      if (run.twig) p.setAttribute('class', 'twig');
      svg.appendChild(p);
      run.el = p; run.len = p.getTotalLength();
      p.style.strokeDasharray = run.len; p.style.strokeDashoffset = run.len;
    });
    nodes.forEach(n => {
      const c = document.createElementNS(SVGNS, 'circle');
      c.setAttribute('cx', n.x.toFixed(1)); c.setAttribute('cy', n.y.toFixed(1)); c.setAttribute('r', n.hot ? 2.6 : 3.2);
      if (n.hot) c.setAttribute('class', 'hot');
      svg.appendChild(c); n.el = c;
    });
    draw();
  }
  function draw() {
    const front = scrollY + innerHeight * .8;
    runs.forEach(run => {
      const p = Math.max(0, Math.min(1, (front - run.y0) / (run.y1 - run.y0)));
      run.el.style.strokeDashoffset = reduce ? 0 : run.len * (1 - p);
    });
    nodes.forEach(n => n.el.classList.toggle('on', reduce || n.y < front));
  }
  let rt;
  addEventListener('scroll', () => requestAnimationFrame(draw), { passive: true });
  addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(build, 300); });
  addEventListener('load', build);
  build();
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
