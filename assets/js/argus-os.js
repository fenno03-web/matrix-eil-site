// ARGUS OS: een bureaublad in de pagina, met vensters, een terminal en een live impressie per tool
(() => {
  const os = document.querySelector('.aos');
  if (!os) return;
  const desk = os.querySelector('.aos-desk');
  const winsBar = os.querySelector('.aos-wins');
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const small = () => innerWidth < 760;
  const NAMES = {};
  os.querySelectorAll('.dk[data-open]').forEach(b => { NAMES[b.dataset.open] = b.querySelector('.dk-n').textContent; });
  let z = 10, cascade = 0;

  // Klok en ogen in de bovenbalk
  const clock = os.querySelector('.aos-clock'), eyes = os.querySelector('.aos-eyes b');
  setInterval(() => {
    clock.textContent = new Date().toLocaleTimeString('nl-NL');
    eyes.textContent = 100 - (Math.random() < .3 ? Math.ceil(Math.random() * 3) : 0);
  }, 1000);

  // ---------------------------------------------------------------- Vensterbeheer
  const focus = w => {
    w.style.zIndex = ++z;
    desk.querySelectorAll('.win').forEach(x => x.classList.toggle('front', x === w));
    winsBar.querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.w === w.dataset.win));
  };
  const taskBtn = w => {
    const b = document.createElement('button');
    b.type = 'button'; b.dataset.w = w.dataset.win;
    b.textContent = w.dataset.win === 'terminal' ? 'Terminal' : NAMES[w.dataset.win];
    b.addEventListener('click', () => focus(w));
    winsBar.appendChild(b);
  };
  const close = w => {
    (w._stop || []).forEach(f => f());
    winsBar.querySelector(`[data-w="${w.dataset.win}"]`)?.remove();
    w.remove();
  };
  const place = w => {
    if (small()) return;
    const d = desk.getBoundingClientRect();
    const ww = Math.min(w.offsetWidth, d.width - 20), wh = Math.min(w.offsetHeight, d.height - 20);
    const x = Math.max(10, Math.min(d.width - ww - 10, d.width - ww - 24 - cascade * 40));
    const y = Math.max(10, Math.min(d.height - wh - 10, 20 + cascade * 30));
    w.style.left = x + 'px'; w.style.top = y + 'px';
    cascade = (cascade + 1) % 6;
  };
  const wire = w => {
    w.addEventListener('pointerdown', () => focus(w));
    w.querySelector('.win-x').addEventListener('click', e => { e.stopPropagation(); close(w); });
    const bar = w.querySelector('.win-bar');
    bar.addEventListener('pointerdown', e => {
      if (small() || e.target.closest('button')) return;
      const d = desk.getBoundingClientRect(), r = w.getBoundingClientRect();
      const ox = e.clientX - r.left, oy = e.clientY - r.top;
      bar.setPointerCapture(e.pointerId);
      w.classList.add('drag');
      const move = ev => {
        w.style.left = Math.max(-r.width + 80, Math.min(d.width - 80, ev.clientX - d.left - ox)) + 'px';
        w.style.top = Math.max(0, Math.min(d.height - 40, ev.clientY - d.top - oy)) + 'px';
      };
      const up = () => { w.classList.remove('drag'); bar.removeEventListener('pointermove', move); bar.removeEventListener('pointerup', up); };
      bar.addEventListener('pointermove', move); bar.addEventListener('pointerup', up);
    });
    taskBtn(w);
    focus(w);
  };
  const open = slug => {
    const have = desk.querySelector(`.win[data-win="${slug}"]`);
    if (have) { focus(have); return have; }
    if (slug === 'terminal') { const t = makeTerminal(); return t; }
    const tpl = document.getElementById('tpl-' + slug);
    if (!tpl) return null;
    const w = tpl.content.firstElementChild.cloneNode(true);
    w._stop = [];
    desk.appendChild(w);
    place(w); wire(w);
    w.classList.add('pop');
    (DEMOS[slug] || (() => {}))(w.querySelector('.win-body'), w);
    return w;
  };
  os.querySelectorAll('.dk[data-open]').forEach(b => b.addEventListener('click', () => open(b.dataset.open)));
  document.querySelectorAll('.ac-open').forEach(b => b.addEventListener('click', () => {
    os.scrollIntoView({ behavior: still ? 'auto' : 'smooth', block: 'center' });
    setTimeout(() => open(b.dataset.open), still ? 0 : 450);
  }));

  // ---------------------------------------------------------------- Terminal
  const BOOT = [
    ['pr', 'argus --status'],
    ['di', 'ARGUS Systems · softwaretak van MATRIX E.I.L.'],
    ['di', 'honderd ogen geladen ......................... 100/100'],
    ['ok', '[ VELD ] CHRONOS   alpha · draait op echte producties'],
    ['ok', '[ LIVE ] BIFROST   console bridge · Heimdall AI'],
    ['ok', '[ LIVE ] IRIS      Stream Deck ⇄ Resolume'],
    ['wa', '[ TEST ] AXIS · METRON · HOROS'],
    ['wa', '[ BOUW ] VISUAL INTELLIGENCE · TREEHOUSE · TARTARUS · KANON'],
    ['di', '[ IDEE ] HYPERION'],
    ['pr', 'wachter actief. typ help voor commando’s.'],
  ];
  const HELP = [
    ['di', 'help                 deze lijst'],
    ['di', 'ls                   alle tools en hun status'],
    ['di', 'open <tool>          open een tool, bijv. open kanon'],
    ['di', 'heimdall <vraag>     vraag het de wachter'],
    ['di', 'status · whoami · date · clear'],
  ];
  const TOOLS = Object.keys(NAMES);
  let term = desk.querySelector('.win.term'), out, input, termReady = false;
  const say = (lines, delay = 0) => new Promise(res => {
    let i = 0;
    const next = () => {
      if (i >= lines.length) { res(); return; }
      const [c, t] = lines[i++];
      const p = document.createElement('div');
      p.className = 'tl ' + c;
      p.textContent = c === 'pr' ? '› ' + t : t;
      out.appendChild(p);
      out.scrollTop = out.scrollHeight;
      delay && !still ? setTimeout(next, delay) : next();
    };
    next();
  });
  const heimdall = q => {
    q = q.toLowerCase();
    if (/backup|sync/.test(q)) return 'Backup-tafel loopt synchroon. Laatste vergelijking 0,4 seconden geleden, geen verschillen.';
    if (/uitloop|tijd|curfew|chronos/.test(q)) return 'Main loopt 2 minuten uit. Curfew-marge is nog 18 minuten. Ik heb regie een seintje gegeven.';
    if (/universe|dmx|signaal|net/.test(q)) return 'Alle 12 universes ontvangen. Universe 7 had om 22:14 een korte onderbreking van 0,2 seconden, sindsdien stabiel.';
    if (/hallo|hoi|hey|wie/.test(q)) return 'Ik ben Heimdall. Ik kijk mee zodat jij naar de show kunt kijken.';
    if (/regen|weer/.test(q)) return 'Buienradar zegt over 40 minuten lichte regen. Misschien de hazers alvast terug?';
    return 'Daar heb ik nog geen antwoord op. In de echte BIFROST kijk ik mee met je show, deze impressie kent alleen een paar vragen.';
  };
  const run = async raw => {
    const cmd = raw.trim();
    if (!cmd) return;
    await say([['me', 'argus@matrix:~$ ' + cmd]]);
    const [c, ...rest] = cmd.split(/\s+/);
    const arg = rest.join(' ').toLowerCase();
    switch (c.toLowerCase()) {
      case 'help': return say(HELP);
      case 'ls': case 'tools':
        return say([...os.querySelectorAll('.dk[data-open]:not(.dk-t)')].map(b => ['di', b.dataset.open.padEnd(11) + b.title.split(' · ').slice(1).join(' · ')]));
      case 'status': return say(BOOT.slice(3, 9), 40);
      case 'open': {
        const hit = TOOLS.find(t => t === arg || NAMES[t].toLowerCase().startsWith(arg) && arg);
        if (!hit) return say([['er', `Onbekende tool: ${arg || '(leeg)'}. Probeer ls.`]]);
        open(hit); return say([['ok', `${NAMES[hit]} geopend.`]]);
      }
      case 'heimdall': return say([['hd', 'Heimdall: ' + heimdall(arg || 'hallo')]], 0);
      case 'whoami': return say([['di', 'gast · honderd ogen kijken mee']]);
      case 'date': return say([['di', new Date().toLocaleString('nl-NL')]]);
      case 'clear': out.innerHTML = ''; return;
      case 'sudo': return say([['er', 'Toegang geweigerd. Argus ziet alles.']]);
      case 'matrix': return say([['ok', 'Execution is the chariot of genius. · William Blake']]);
      case 'exit': close(term); return;
      case 'rm': return say([['er', 'TARTARUS zegt nee. Showfiles gooien we niet weg.']]);
      default:
        if (TOOLS.includes(c.toLowerCase())) { open(c.toLowerCase()); return say([['ok', `${NAMES[c.toLowerCase()]} geopend.`]]); }
        return say([['er', `Onbekend commando: ${c}. Typ help.`]]);
    }
  };
  const initTerm = (t, boot) => {
    term = t; out = t.querySelector('.term-out'); input = t.querySelector('input');
    t.querySelector('.term-body').addEventListener('click', () => input.focus({ preventScroll: true }));
    t.querySelector('form').addEventListener('submit', e => { e.preventDefault(); const v = input.value; input.value = ''; run(v); });
    if (boot) say(BOOT, 110).then(() => { termReady = true; });
  };
  function makeTerminal() {
    const t = document.createElement('section');
    t.className = 'win term'; t.dataset.win = 'terminal';
    t.innerHTML = `<div class="win-bar"><span class="win-dots"><button class="win-x" aria-label="Sluit terminal"></button><i></i><i></i></span><b>argus — terminal</b><span class="st">tty1</span></div>
      <div class="win-body term-body"><div class="term-out" aria-live="polite"></div><form class="term-line"><label>argus@matrix:~$</label><input autocomplete="off" spellcheck="false" aria-label="Typ een commando"></form></div>`;
    t._stop = [];
    desk.appendChild(t); place(t); wire(t); initTerm(t, false);
    say([['di', 'Terug. Typ help.']]);
    return t;
  }
  term._stop = [];
  wire(term);
  out = term.querySelector('.term-out');
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (!e.isIntersecting) return;
    io.disconnect();
    initTerm(term, true);
    // Na de systeemstart springt er vanzelf een tool open, zodat je ziet wat er kan
    setTimeout(() => { if (!desk.querySelector('.tool-win') && !small()) open('kanon'); }, still ? 0 : 1700);
  }), { threshold: .35 });
  io.observe(os);

  // ---------------------------------------------------------------- Hulpjes voor de demo's
  const loop = (w, fn) => {
    let on = true, raf;
    const vis = new IntersectionObserver(es => { on = es[0].isIntersecting; if (on) tick(); });
    const tick = () => { if (!on || !w.isConnected) return; fn(); raf = requestAnimationFrame(tick); };
    vis.observe(w);
    w._stop.push(() => { on = false; cancelAnimationFrame(raf); vis.disconnect(); });
    tick();
  };
  const every = (w, ms, fn) => { const id = setInterval(fn, ms); w._stop.push(() => clearInterval(id)); };
  const fit = cv => {
    const ctx = cv.getContext('2d');
    const W = cv.width, H = cv.height, dpr = Math.min(2, devicePixelRatio || 1);
    cv.width = W * dpr; cv.height = H * dpr; ctx.scale(dpr, dpr);
    return [ctx, W, H];
  };
  const css = v => getComputedStyle(os).getPropertyValue(v).trim();
  const GOLD = '#d9ad4f', CYAN = '#3fd8ee';
  const ptr = (cv, e) => { const r = cv.getBoundingClientRect(); return [(e.clientX - r.left) / r.width * cv.width / Math.min(2, devicePixelRatio || 1), (e.clientY - r.top) / r.height * cv.height / Math.min(2, devicePixelRatio || 1)]; };
  const beam = (ctx, x1, y1, x2, y2, col, width = 26, a = .5) => {
    const ang = Math.atan2(y2 - y1, x2 - x1), len = Math.hypot(x2 - x1, y2 - y1);
    ctx.save(); ctx.translate(x1, y1); ctx.rotate(ang);
    const g = ctx.createLinearGradient(0, 0, len, 0);
    g.addColorStop(0, col.replace('A', a)); g.addColorStop(1, col.replace('A', 0));
    ctx.fillStyle = g;
    ctx.beginPath(); ctx.moveTo(0, -2); ctx.lineTo(len, -width / 2); ctx.lineTo(len, width / 2); ctx.lineTo(0, 2); ctx.closePath(); ctx.fill();
    ctx.restore();
  };

  // ---------------------------------------------------------------- De demo's per tool
  const DEMOS = {
    // BIFROST: twee tafels, een regenboogbrug met datapakketjes en een wachter die meeleest
    bifrost(body, w) {
      const cv = body.querySelector('.bf-cv'), [ctx, W, H] = fit(cv);
      const log = body.querySelector('.bf-log'), ans = body.querySelector('.bf-ans');
      const packets = [];
      let t = 0, alert = 0;
      loop(w, () => {
        t++;
        ctx.clearRect(0, 0, W, H);
        // de brug
        for (let k = 0; k < 6; k++) {
          ctx.strokeStyle = `hsla(${180 + k * 30 + Math.sin(t / 40) * 10}, 90%, 60%, .35)`;
          ctx.lineWidth = 2;
          ctx.beginPath(); ctx.moveTo(110, 110 + k * 3); ctx.quadraticCurveTo(W / 2, 10 + k * 3, W - 110, 110 + k * 3); ctx.stroke();
        }
        // tafels
        [[20, 'FOH · MAIN'], [W - 110, 'BACKUP']].forEach(([x, l], i) => {
          ctx.fillStyle = '#0b1416'; ctx.strokeStyle = i ? GOLD : CYAN; ctx.lineWidth = 1;
          ctx.fillRect(x, 100, 90, 46); ctx.strokeRect(x, 100, 90, 46);
          for (let f = 0; f < 6; f++) { ctx.fillStyle = i ? GOLD : CYAN; ctx.globalAlpha = .4 + .4 * Math.sin(t / 15 + f); ctx.fillRect(x + 8 + f * 13, 112, 6, 26); }
          ctx.globalAlpha = 1; ctx.fillStyle = '#9aa'; ctx.font = '10px JetBrains Mono, monospace'; ctx.fillText(l, x, 162);
        });
        if (t % 8 === 0) packets.push({ p: 0, s: .006 + Math.random() * .006 });
        packets.forEach(pk => {
          pk.p += pk.s;
          const u = pk.p, x = (1 - u) * (1 - u) * 110 + 2 * (1 - u) * u * (W / 2) + u * u * (W - 110), y = (1 - u) * (1 - u) * 115 + 2 * (1 - u) * u * 15 + u * u * 115;
          ctx.fillStyle = '#fff'; ctx.shadowColor = CYAN; ctx.shadowBlur = 10;
          ctx.beginPath(); ctx.arc(x, y, 2.2, 0, 7); ctx.fill(); ctx.shadowBlur = 0;
        });
        while (packets.length && packets[0].p > 1) packets.shift();
        // Heimdalls oog boven de brug
        const ey = 40 + Math.sin(t / 50) * 3;
        ctx.strokeStyle = alert ? '#ff5a4d' : GOLD; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.ellipse(W / 2, ey, 22, 10, 0, 0, 7); ctx.stroke();
        ctx.fillStyle = alert ? '#ff5a4d' : CYAN; ctx.beginPath(); ctx.arc(W / 2 + Math.sin(t / 30) * 8, ey, 4.5, 0, 7); ctx.fill();
        if (alert) alert--;
      });
      const LINES = [
        ['ok', 'Bridge actief · 12 universes · 0 verschillen'],
        ['ok', 'Backup synchroon met FOH'],
        ['wa', 'Universe 7 · 0,2 s geen data · hersteld'],
        ['ok', 'Cuelist 3 · GO 47 bevestigd op beide tafels'],
        ['ok', 'Temperatuur tafel FOH normaal'],
        ['wa', 'Heimdall: Main loopt 2 min uit, regie ingelicht'],
      ];
      let li = 0;
      const add = () => {
        const [c, txt] = LINES[li++ % LINES.length];
        if (c === 'wa') alert = 90;
        const el = document.createElement('li'); el.className = c;
        el.innerHTML = `<time>${new Date().toLocaleTimeString('nl-NL')}</time>${txt}`;
        log.prepend(el);
        while (log.children.length > 4) log.lastChild.remove();
      };
      add(); every(w, 2200, add);
      body.querySelector('.bf-ask').addEventListener('submit', e => {
        e.preventDefault();
        const inp = body.querySelector('input');
        const q = inp.value.trim(); if (!q) return;
        ans.textContent = '…';
        setTimeout(() => { ans.textContent = 'Heimdall: ' + heimdall(q); }, 500);
        inp.value = '';
      });
    },

    // VISUAL INTELLIGENCE: tik op het podium en de lampen richten zich
    visual(body, w) {
      const cv = body.querySelector('.vi-cv'), [ctx, W, H] = fit(cv);
      const xy = body.querySelector('.vi-xy');
      const fx = [70, 150, 230, 330, 410, 490].map(x => ({ x, y: 40, a: Math.PI / 2, ta: Math.PI / 2 }));
      let tx = W / 2, ty = H * .6, t = 0, auto = true;
      cv.addEventListener('pointerdown', e => { [tx, ty] = ptr(cv, e); auto = false; });
      loop(w, () => {
        t++;
        if (auto) { tx = W / 2 + Math.sin(t / 70) * 160; ty = H * .62 + Math.cos(t / 55) * 50; }
        ctx.clearRect(0, 0, W, H);
        ctx.strokeStyle = 'rgba(63,216,238,.12)'; ctx.lineWidth = 1;
        for (let x = 20; x < W; x += 40) { ctx.beginPath(); ctx.moveTo(x, 70); ctx.lineTo(x, H - 10); ctx.stroke(); }
        for (let y = 70; y < H; y += 40) { ctx.beginPath(); ctx.moveTo(10, y); ctx.lineTo(W - 10, y); ctx.stroke(); }
        ctx.strokeStyle = 'rgba(217,173,79,.6)'; ctx.strokeRect(10, 70, W - 20, H - 80);
        ctx.fillStyle = '#2a2418'; ctx.fillRect(40, 34, W - 80, 12);
        fx.forEach((f, i) => {
          f.ta = Math.atan2(ty - f.y, tx - f.x);
          f.a += (f.ta - f.a) * (.05 + i * .006);
          const len = Math.hypot(tx - f.x, ty - f.y);
          beam(ctx, f.x, f.y, f.x + Math.cos(f.a) * len, f.y + Math.sin(f.a) * len, 'rgba(255,240,210,A)', 34, .32);
          ctx.fillStyle = GOLD; ctx.beginPath(); ctx.arc(f.x, f.y, 6, 0, 7); ctx.fill();
        });
        ctx.strokeStyle = CYAN; ctx.lineWidth = 1.4;
        ctx.beginPath(); ctx.arc(tx, ty, 14 + Math.sin(t / 8) * 2, 0, 7); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(tx - 22, ty); ctx.lineTo(tx + 22, ty); ctx.moveTo(tx, ty - 22); ctx.lineTo(tx, ty + 22); ctx.stroke();
        xy.textContent = `${((tx - 10) / (W - 20) * 12 - 6).toFixed(1)} m · ${((ty - 70) / (H - 80) * 8).toFixed(1)} m`;
      });
    },

    // HYPERION: een ingelezen MVR-podium in schuin perspectief, met scenes
    hyperion(body, w) {
      const cv = body.querySelector('.hy-cv'), [ctx, W, H] = fit(cv);
      let scene = 'warm', t = 0;
      body.querySelectorAll('.hy-scenes button').forEach(b => b.addEventListener('click', () => {
        scene = b.dataset.s;
        body.querySelectorAll('.hy-scenes button').forEach(x => x.classList.toggle('on', x === b));
      }));
      const iso = (x, y, zz) => [W / 2 + (x - y) * 1.1, 70 + (x + y) * .45 - zz];
      const truss = [[-140, -60], [-140, 20], [-140, 100]];
      loop(w, () => {
        t++;
        ctx.clearRect(0, 0, W, H);
        // vloer
        ctx.strokeStyle = 'rgba(236,10,140,.25)'; ctx.lineWidth = 1;
        for (let k = -150; k <= 150; k += 30) {
          let [a, b] = iso(k, -100, 0), [c, d] = iso(k, 140, 0); ctx.beginPath(); ctx.moveTo(a, b); ctx.lineTo(c, d); ctx.stroke();
          [a, b] = iso(-150, k, 0); [c, d] = iso(150, k, 0); ctx.beginPath(); ctx.moveTo(a, b); ctx.lineTo(c, d); ctx.stroke();
        }
        truss.forEach(([, y], ti) => {
          const [a, b] = iso(-130, y, 90), [c, d] = iso(130, y, 90);
          ctx.strokeStyle = '#c9a25a'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(a, b); ctx.lineTo(c, d); ctx.stroke();
          for (let i = 0; i < 8; i++) {
            const x = -120 + i * 34;
            const [px, py] = iso(x, y, 90);
            let hue = 30, on = 1;
            if (scene === 'koel') hue = 190 + i * 6;
            if (scene === 'chase') { hue = 300; on = (Math.floor(t / 6) % 8) === i ? 1 : .08; }
            if (scene === 'blind') { hue = 40; on = ti === 0 ? (Math.sin(t / 5) > 0 ? 1 : .15) : .1; }
            const sway = Math.sin(t / 40 + i * .6 + ti) * 18;
            const [fx2, fy2] = iso(x + sway, y + 40, 0);
            beam(ctx, px, py, fx2, fy2, `hsla(${hue},95%,62%,A)`, 22, .45 * on);
            ctx.fillStyle = `hsla(${hue},95%,${40 + 30 * on}%,1)`; ctx.beginPath(); ctx.arc(px, py, 3.2, 0, 7); ctx.fill();
          }
        });
      });
    },

    // TREEHOUSE: een macro uit de boom loopt toets voor toets op de tafel
    treehouse(body, w) {
      const outEl = body.querySelector('.th-out');
      const MACROS = {
        'Opening': ['Clear', 'Group 1 · Washes', 'Intensity 0 → 100 in 4 s', 'Color · Deep Blue', 'Playback 1 · Go'],
        'Drop': ['Group 3 · Beams', 'Effect · Fan wave', 'Speed → BPM 150', 'Strobe sync 1/2', 'Go'],
        'Blackout': ['Master 0', 'Hold'],
        'Kleurpalet': ['Store · Palette 1', 'Color · Amber', 'Store · Palette 2', 'Color · Cyan', 'Store · Palette 3', 'Color · Magenta'],
        'Fan-out': ['Select · Group 2', 'Pan · Fan Ø', 'Tilt · Fan V', 'Store · Position 4'],
        'Wis alles': ['Clear', 'Clear', 'Clear · Programmer leeg'],
      };
      let timer;
      body.querySelectorAll('[data-m]').forEach(b => b.addEventListener('click', () => {
        clearInterval(timer);
        body.querySelectorAll('[data-m]').forEach(x => x.classList.toggle('on', x === b));
        const steps = MACROS[b.dataset.m]; let i = 0;
        outEl.textContent = `▸ Macro “${b.dataset.m}” · Infinity Chimp\n`;
        timer = setInterval(() => {
          if (i >= steps.length) { outEl.textContent += `✓ Klaar · ${steps.length} handelingen in 1 druk`; clearInterval(timer); return; }
          outEl.textContent += `  ${String(i + 1).padStart(2, '0')}  ${steps[i++]}\n`;
        }, still ? 0 : 180);
      }));
      w._stop.push(() => clearInterval(timer));
      body.querySelector('[data-m]').click();
    },

    // TARTARUS: showfiles worden gevonden, gesorteerd en de nieuwste versie gaat de kluis in
    tartarus(body, w) {
      const found = body.querySelector('.ta-found'), vault = body.querySelector('.ta-vault'), st = body.querySelector('.ta-st');
      const FILES = [
        ['D:/Shows/Woeesj_2026_v3.chimp', 'Woeësj-Stock', 3], ['Bureaublad/woeesj FINAL.chimp', 'Woeësj-Stock', 4],
        ['USB/woeesj FINAL echt.chimp', 'Woeësj-Stock', 5], ['Downloads/sportclub_v1.show', 'Sportclub’25', 1],
        ['D:/Shows/sportclub_v2.show', 'Sportclub’25', 2], ['USB/carnaval_radio.show', 'Carnaval Radio', 1],
        ['Mail/carnaval_radio_v2.show', 'Carnaval Radio', 2], ['Bureaublad/kopie van kopie.show', 'Carnaval Radio', 1],
      ];
      let timers = [];
      const scan = () => {
        timers.forEach(clearTimeout); timers = [];
        found.innerHTML = ''; vault.innerHTML = ''; st.textContent = 'Zoeken…';
        FILES.forEach((f, i) => timers.push(setTimeout(() => {
          const li = document.createElement('li'); li.innerHTML = `<span>${f[0]}</span><b>v${f[2]}</b>`; found.appendChild(li);
        }, (still ? 0 : 160) * i)));
        timers.push(setTimeout(() => {
          st.textContent = `${FILES.length} gevonden · kluis bijgewerkt`;
          const shows = {};
          FILES.forEach(f => { (shows[f[1]] = shows[f[1]] || []).push(f); });
          vault.innerHTML = Object.entries(shows).map(([s, fs]) => {
            const top = fs.reduce((a, b) => (b[2] > a[2] ? b : a));
            return `<div class="ta-show"><h6>${s}</h6><p class="new">▲ v${top[2]} · nieuwste</p><p>${fs.length - 1} oudere versies veilig bewaard</p></div>`;
          }).join('');
          found.querySelectorAll('li').forEach((li, i) => {
            const f = FILES[i], top = Math.max(...FILES.filter(x => x[1] === f[1]).map(x => x[2]));
            li.classList.add(f[2] === top ? 'keep' : 'old');
          });
        }, (still ? 0 : 160) * FILES.length + 300));
      };
      body.querySelector('.ta-go').addEventListener('click', scan);
      w._stop.push(() => timers.forEach(clearTimeout));
      scan();
    },

    // KANON: de camera herkent de artiest en de spot volgt, of je stuurt zelf met de cursor
    kanon(body, w) {
      const cv = body.querySelector('.ka-cv'), [ctx, W, H] = fit(cv);
      const conf = body.querySelector('.ka-conf');
      let mode = 'auto', px = W / 2, tx = W / 2, sx = W / 2, sy = H * .7, mx = W / 2, my = H * .7, t = 0;
      body.querySelectorAll('[data-mode]').forEach(b => b.addEventListener('click', () => {
        mode = b.dataset.mode; body.querySelectorAll('[data-mode]').forEach(x => x.classList.toggle('on', x === b));
      }));
      cv.addEventListener('pointermove', e => { [mx, my] = ptr(cv, e); });
      cv.addEventListener('pointerdown', e => { [mx, my] = ptr(cv, e); });
      loop(w, () => {
        t++;
        if (Math.random() < .012) tx = 60 + Math.random() * (W - 120);
        px += (tx - px) * .018;
        const py = H * .74, bob = Math.sin(t / 6) * (Math.abs(tx - px) > 4 ? 2 : .4);
        const aimX = mode === 'auto' ? px : mx, aimY = mode === 'auto' ? py - 30 : my;
        sx += (aimX - sx) * .12; sy += (aimY - sy) * .12;
        ctx.clearRect(0, 0, W, H);
        // podiumvloer en truss
        ctx.fillStyle = '#0a0a0a'; ctx.fillRect(0, H * .82, W, H * .18);
        ctx.fillStyle = '#2a2418'; ctx.fillRect(0, 14, W, 8);
        // spot
        const g = ctx.createRadialGradient(sx, sy + 34, 4, sx, sy + 34, 70);
        g.addColorStop(0, 'rgba(255,245,225,.55)'); g.addColorStop(1, 'rgba(255,245,225,0)');
        beam(ctx, W / 2, 20, sx, sy + 20, 'rgba(255,245,225,A)', 90, .22);
        ctx.fillStyle = g; ctx.beginPath(); ctx.ellipse(sx, H * .84, 70, 16, 0, 0, 7); ctx.fill();
        // artiest
        ctx.fillStyle = '#e9e1d2';
        ctx.beginPath(); ctx.arc(px, py - 52 + bob, 9, 0, 7); ctx.fill();
        ctx.fillRect(px - 9, py - 42 + bob, 18, 34);
        ctx.fillRect(px - 8, py - 8 + bob, 6, 26); ctx.fillRect(px + 2, py - 8 + bob, 6, 26);
        // trackingkader
        if (mode === 'auto') {
          ctx.strokeStyle = CYAN; ctx.lineWidth = 1.3;
          const bx = px - 22, by = py - 66;
          [[bx, by, 1, 1], [bx + 44, by, -1, 1], [bx, by + 86, 1, -1], [bx + 44, by + 86, -1, -1]].forEach(([x, y, dx, dy]) => {
            ctx.beginPath(); ctx.moveTo(x, y + 10 * dy); ctx.lineTo(x, y); ctx.lineTo(x + 10 * dx, y); ctx.stroke();
          });
          ctx.fillStyle = CYAN; ctx.font = '10px JetBrains Mono, monospace';
          ctx.fillText('ARTIST_01', bx, by - 6);
          if (t % 20 === 0) conf.textContent = (95 + Math.random() * 4.5).toFixed(0) + '%';
        } else if (t % 20 === 0) conf.textContent = 'hand';
        // camerabeeld-rand
        ctx.strokeStyle = 'rgba(63,216,238,.4)'; ctx.strokeRect(4, 4, W - 8, H - 8);
        ctx.fillStyle = '#ff4d4d'; ctx.globalAlpha = t % 60 < 30 ? 1 : .2; ctx.beginPath(); ctx.arc(W - 18, 18, 4, 0, 7); ctx.fill(); ctx.globalAlpha = 1;
      });
    },

    // IRIS: knoppen met live thumbnails, en het beeld wisselt direct
    iris(body, w) {
      const prev = body.querySelector('.ir-prev'), name = body.querySelector('.ir-name'), ms = body.querySelector('.ir-ms');
      body.querySelectorAll('.ir-k').forEach(k => k.addEventListener('click', () => {
        body.querySelectorAll('.ir-k').forEach(x => x.classList.toggle('on', x === k));
        prev.style.setProperty('--h', k.style.getPropertyValue('--h'));
        prev.dataset.fx = k.dataset.i % 4;
        name.textContent = k.textContent.trim();
        ms.textContent = (1.2 + Math.random() * 1.6).toFixed(1).replace('.', ',') + ' ms';
        prev.classList.remove('hit'); void prev.offsetWidth; prev.classList.add('hit');
      }));
      const keys = [...body.querySelectorAll('.ir-k')];
      let n = 0;
      every(w, 1600, () => { if (!w.matches(':hover')) keys[[1, 4, 6, 8, 2][n++ % 5]].click(); });
    },
  };
})();
