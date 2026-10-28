const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

// Mobiel menu
const btn = document.querySelector('.menu-btn');
const nav = document.querySelector('.nav');
if (btn && nav) {
  btn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
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
document.querySelectorAll('[data-gallery]').forEach(el => {
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
    const open = () => lbOpen(JSON.parse(row.dataset.gallery), 0, row.dataset.title);
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
      const page = { 'index.html': 'Home', 'projecten.html': 'Projecten', 'over.html': 'Over', 'argus.html': 'Argus', 'privacy.html': 'Privacy' };
      sb.innerHTML = `Standby<b>${page[a.getAttribute('href').split('#')[0]] || 'GO'}</b>`;
      document.body.classList.remove('intro', 'go');
      document.body.classList.add('leaving');
      setTimeout(() => { location.href = a.href; }, 380);
    });
  });
  addEventListener('pageshow', e => { if (e.persisted) { document.body.classList.remove('leaving'); const pt = document.querySelector('.portal'); if (pt) pt.classList.remove('go'); } });
}
