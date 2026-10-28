// Mobiel menu
const btn = document.querySelector('.menu-btn');
const nav = document.querySelector('.nav');
if (btn && nav) {
  btn.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open);
  });
}

// Jaartal in de footer
document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });

// Elementen laten verschijnen tijdens het scrollen
const reveals = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px' });
  reveals.forEach(el => io.observe(el));
} else {
  reveals.forEach(el => el.classList.add('in'));
}

// Galerij groot bekijken
const gallery = document.querySelector('.gallery');
if (gallery) {
  const box = document.createElement('div');
  box.className = 'lightbox';
  box.innerHTML = '<img alt="">';
  document.body.appendChild(box);
  gallery.addEventListener('click', e => {
    if (e.target.tagName !== 'IMG') return;
    box.firstChild.src = e.target.src;
    box.classList.add('open');
  });
  box.addEventListener('click', () => box.classList.remove('open'));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') box.classList.remove('open'); });
}
