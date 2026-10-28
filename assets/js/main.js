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

// Expertise: foto beweegt mee met de muis
const expList = document.querySelector('.exp-list');
if (expList && finePointer) {
  const float = document.createElement('div');
  float.className = 'exp-float';
  float.innerHTML = '<img alt="">';
  document.body.appendChild(float);
  const img = float.firstChild;
  expList.querySelectorAll('li').forEach(li => {
    li.addEventListener('mouseenter', () => { img.src = li.dataset.img; float.classList.add('show'); });
    li.addEventListener('mouseleave', () => float.classList.remove('show'));
    li.addEventListener('mousemove', e => {
      float.style.transform = `translate3d(${e.clientX + 30}px, ${e.clientY - 200}px, 0) rotate(${(e.clientX / innerWidth - .5) * 6}deg)`;
    });
  });
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

// Zachte overgang bij het wisselen van pagina
if (!reduce) {
  document.querySelectorAll('a[href$=".html"]').forEach(a => {
    a.addEventListener('click', e => {
      if (e.metaKey || e.ctrlKey || e.shiftKey || a.target === '_blank') return;
      e.preventDefault();
      document.body.classList.add('leaving');
      setTimeout(() => { location.href = a.href; }, 320);
    });
  });
  addEventListener('pageshow', e => { if (e.persisted) document.body.classList.remove('leaving'); });
}
