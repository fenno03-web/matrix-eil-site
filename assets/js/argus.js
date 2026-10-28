// ARGUS: het oog, de systeemstart en de werkende demo's van de vier tools
const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const two = n => String(n).padStart(2, '0');
const mmss = s => `${two(Math.floor(Math.abs(s) / 60))}:${two(Math.abs(s) % 60)}`;
const onView = (el, fn) => {
  if (!el) return;
  const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { fn(); io.disconnect(); } }), { threshold: .25 });
  io.observe(el);
};

// Het oog: de pupil volgt de cursor, de honderd ogen knipperen om beurten
const eye = document.querySelector('.eye');
if (eye) {
  const pupil = eye.querySelector('.pupil-g');
  const dots = [...eye.querySelectorAll('.dot')];
  const openCount = document.querySelector('.open-count');
  let tx = 0, ty = 0, px = 0, py = 0;
  addEventListener('mousemove', e => {
    const r = eye.getBoundingClientRect();
    const dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
    const d = Math.hypot(dx, dy) || 1, k = Math.min(1, d / 400);
    tx = dx / d * 46 * k; ty = dy / d * 26 * k;
  }, { passive: true });
  if (!still) {
    (function look() {
      px += (tx - px) * .08; py += (ty - py) * .08;
      pupil.setAttribute('transform', `translate(${px.toFixed(1)} ${py.toFixed(1)})`);
      requestAnimationFrame(look);
    })();
    setInterval(() => {
      const shut = new Set();
      const n = 1 + Math.floor(Math.random() * 4);
      for (let k = 0; k < n; k++) shut.add(dots[Math.floor(Math.random() * dots.length)]);
      shut.forEach(d => d.classList.add('shut'));
      if (openCount) openCount.textContent = dots.length - shut.size;
      setTimeout(() => { shut.forEach(d => d.classList.remove('shut')); if (openCount) openCount.textContent = dots.length; }, 260);
    }, 700);
  }
}

// Systeemstart: de statusregels worden uitgetypt
const out = document.querySelector('.boot-out');
const BOOT = [
  ['pr', '> argus --status'],
  ['di', 'ARGUS Systems · softwaretak van MATRIX E.I.L.'],
  ['di', 'honderd ogen geladen ......................... 100/100'],
  ['', ''],
  ['ok', '[ VELD ] CHRONOS   alpha · draait op echte producties'],
  ['wa', '[ TEST ] AXIS      planning · magazijn · LIVE · accreditatie'],
  ['wa', '[ TEST ] METRON    Pro DJ Link · BPM · speedmasters'],
  ['wa', '[ TEST ] HOROS     RDW-data · bruggen · milieuzones'],
  ['', ''],
  ['pr', '> wachter actief. de show wordt bewaakt.'],
];
if (out) {
  const render = (lines, partial) => {
    out.innerHTML = lines.map(([c, t]) => `<span class="${c}">${t}</span>`).join('\n') + (partial !== undefined ? partial : '') + '<span class="cur"></span>';
  };
  if (still) render(BOOT);
  else onView(out, () => {
    const done = [];
    let li = 0, ci = 0;
    (function type() {
      if (li >= BOOT.length) { render(done); return; }
      const [c, t] = BOOT[li];
      if (ci <= t.length) {
        render(done, (done.length ? '\n' : '') + `<span class="${c}">${t.slice(0, ci)}</span>`);
        ci += c === 'pr' ? 1 : 3;
        setTimeout(type, c === 'pr' ? 32 : 8);
      } else {
        done.push(BOOT[li]); li++; ci = 0;
        setTimeout(type, t ? 160 : 60);
      }
    })();
  });
}

// Roadmap: de voortgangslijn loopt op als hij in beeld komt
const road = document.querySelector('.roadmap');
onView(road, () => road.classList.add('in'));

// CHRONOS: drie stages die live aftellen, met uitloop
const chronos = document.querySelector('.chronos-demo');
if (chronos) {
  const stages = [...chronos.querySelectorAll('.stg')].map(el => ({ el, left: +el.dataset.left, len: +el.dataset.len }));
  const cf = chronos.querySelector('.cf');
  let curfew = +cf.dataset.left;
  const draw = () => {
    stages.forEach(s => {
      const over = s.left < 0;
      s.el.querySelector('.cd span').textContent = (over ? '+' : '') + mmss(s.left);
      s.el.querySelector('.pb i').style.width = over ? '100%' : `${100 - s.left / s.len * 100}%`;
    });
    const h = Math.floor(curfew / 3600);
    cf.textContent = `${two(h)}:${mmss(curfew % 3600)}`;
  };
  draw();
  setInterval(() => {
    stages.forEach(s => { s.left = s.left <= 0 && s.el.classList.contains('over') ? s.left - 1 : (s.left > 0 ? s.left - 1 : s.len); });
    curfew = curfew > 0 ? curfew - 1 : 1120;
    draw();
  }, 1000);
}

// AXIS: modules aan en uit zetten
const axis = document.querySelector('.axis-demo');
if (axis) {
  const empty = axis.querySelector('.zones-empty'), zones = axis.querySelector('.zones');
  axis.querySelectorAll('.mod').forEach(btn => btn.addEventListener('click', () => {
    const on = btn.getAttribute('aria-pressed') !== 'true';
    btn.setAttribute('aria-pressed', on);
    axis.dataset[btn.dataset.mod] = on ? '1' : '0';
    const any = ['plan', 'live', 'acc'].some(m => axis.dataset[m] === '1');
    empty.style.display = any ? 'none' : 'block';
    zones.style.display = any ? '' : 'none';
  }));
}

// METRON: beat op het tempo, met tap tempo
const metron = document.querySelector('.metron-demo');
if (metron) {
  const beats = [...metron.querySelectorAll('.beats i')];
  const bpmV = metron.querySelector('.bpm-v'), srcV = metron.querySelector('.src');
  const barV = metron.querySelector('.bar-v'), dropV = metron.querySelector('.drop-v'), fadeV = metron.querySelector('.fade-v');
  const tap = metron.querySelector('.tap');
  let bpm = 128, beat = 0, bar = 1, drop = 32, timer = null, taps = [];
  const show = () => {
    bpmV.textContent = bpm.toFixed(1);
    fadeV.textContent = `${Math.round(60000 / bpm)} ms`;
  };
  const tick = () => {
    beats.forEach((b, k) => { b.classList.toggle('on', k === beat); b.classList.toggle('one', k === 0); });
    setTimeout(() => beats[beat] && beats[beat].classList.remove('on'), Math.min(140, 30000 / bpm));
    barV.textContent = `${bar}.${beat + 1}`;
    dropV.textContent = drop;
    beat = (beat + 1) % 4;
    if (beat === 0) bar = bar % 16 + 1;
    drop = drop > 1 ? drop - 1 : 32;
  };
  const run = () => { clearInterval(timer); timer = setInterval(tick, 60000 / bpm); };
  const hit = () => {
    const now = performance.now();
    taps = taps.filter(t => now - t < 2500);
    taps.push(now);
    tap.classList.add('hit'); setTimeout(() => tap.classList.remove('hit'), 90);
    if (taps.length > 1) {
      const gaps = taps.slice(1).map((t, k) => t - taps[k]);
      const avg = gaps.reduce((a, b) => a + b, 0) / gaps.length;
      bpm = Math.max(60, Math.min(200, 60000 / avg));
      srcV.textContent = 'Tap';
      beat = 0; show(); run();
    }
  };
  tap.addEventListener('click', hit);
  addEventListener('keydown', e => {
    if (e.code !== 'Space' || e.target.closest('input, textarea, button')) return;
    const r = metron.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight) return;
    e.preventDefault(); hit();
  });
  show();
  if (!still) onView(metron, run);
}

// HOROS: voertuig rijdt de route; bruggen kleuren rood als je er niet onderdoor past
const horos = document.querySelector('.horos-demo');
if (horos) {
  const route = horos.querySelector('#route');
  const len = route.getTotalLength();
  const grid = horos.querySelector('.grid');
  for (let x = 20; x < 520; x += 40) grid.insertAdjacentHTML('beforeend', `<line x1="${x}" y1="0" x2="${x}" y2="300"/>`);
  for (let y = 20; y < 300; y += 40) grid.insertAdjacentHTML('beforeend', `<line x1="0" y1="${y}" x2="520" y2="${y}"/>`);
  const bridges = [...horos.querySelectorAll('.br')].map(g => {
    const p = route.getPointAtLength(len * +g.dataset.at);
    g.setAttribute('transform', `translate(${p.x.toFixed(1)} ${(p.y - 26).toFixed(1)})`);
    return { g, h: +g.dataset.h, km: Math.round(+g.dataset.at * 42) };
  });
  const slider = horos.querySelector('input'), outV = horos.querySelector('output');
  const w = [horos.querySelector('.w1'), horos.querySelector('.w2')];
  const nl = v => v.toFixed(2).replace('.', ',');
  const check = () => {
    const h = +slider.value;
    outV.textContent = `${nl(h)} m`;
    bridges.forEach((b, k) => {
      const bad = h > b.h;
      b.g.classList.toggle('bad', bad);
      w[k].classList.toggle('bad', bad);
      w[k].textContent = bad
        ? `Viaduct · km ${b.km} · doorrijhoogte ${nl(b.h)} m · past niet, omrijden`
        : `Viaduct · km ${b.km} · doorrijhoogte ${nl(b.h)} m · vrij`;
    });
  };
  slider.addEventListener('input', check);
  check();
  const veh = horos.querySelector('.veh'), ring = horos.querySelector('.veh-ring');
  let t = 0;
  const place = () => {
    const p = route.getPointAtLength(len * t);
    [veh, ring].forEach(c => { c.setAttribute('cx', p.x.toFixed(1)); c.setAttribute('cy', p.y.toFixed(1)); });
  };
  place();
  if (!still) (function drive() { t = (t + .0016) % 1; place(); requestAnimationFrame(drive); })();
}
