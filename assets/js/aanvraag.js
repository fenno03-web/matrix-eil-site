// Aanvraagwizard: stappen aanklikken, aan het eind een kant-en-klaar bericht
(() => {
  const form = document.querySelector('.wz');
  if (!form) return;
  const steps = [...form.querySelectorAll('.wz-step')];
  const cues = [...form.querySelectorAll('.wz-cues span')];
  const bar = form.querySelector('.wz-bar span');
  const next = form.querySelector('.wz-next');
  const back = form.querySelector('.wz-back');
  const wa = form.querySelector('.wz-wa');
  const mail = form.querySelector('.wz-mail');
  const sum = form.querySelector('.wz-sum');
  const picked = {};
  let at = 0;

  const value = step => {
    const key = step.dataset.key;
    if (key === 'info') return true;
    return (picked[key] || []).length > 0;
  };

  const message = () => {
    const f = n => form.elements[n].value.trim();
    const lines = ['Hoi MATRIX, ik wil graag een aanvraag doen.', ''];
    const add = (label, v) => { if (v) lines.push(`${label}: ${v}`); };
    add('Evenement', [f('event'), (picked.type || []).join('')].filter(Boolean).join(' · '));
    add('Nodig', (picked.need || []).join(', '));
    add('Omvang', (picked.size || []).join(''));
    add('Datum', f('date'));
    add('Plaats', f('place'));
    add('Organisatie', f('org'));
    if (f('note')) lines.push('', f('note'));
    if (f('name')) lines.push('', `Groet, ${f('name')}`);
    return lines.join('\n');
  };

  const show = () => {
    steps.forEach((s, i) => s.classList.toggle('on', i === at));
    cues.forEach((c, i) => { c.classList.toggle('on', i === at); c.classList.toggle('done', i < at); });
    bar.style.width = `${(at / (steps.length - 1)) * 100}%`;
    back.hidden = at === 0;
    const last = at === steps.length - 1;
    next.hidden = last;
    next.textContent = at === steps.length - 2 ? 'GO' : 'Volgende';
    next.disabled = !value(steps[at]);
    if (last) {
      const txt = message();
      sum.textContent = txt;
      wa.href = `https://wa.me/31630971404?text=${encodeURIComponent(txt)}`;
      mail.href = `mailto:info@matrixeventsupport.nl?subject=${encodeURIComponent('Aanvraag via de site')}&body=${encodeURIComponent(txt)}`;
    }
    const f = steps[at].querySelector('button, input');
    if (f && at) f.focus({ preventScroll: true });
  };

  steps.forEach(step => {
    const key = step.dataset.key;
    const multi = step.dataset.multi === '1';
    step.querySelectorAll('.wz-opt').forEach(b => b.addEventListener('click', () => {
      let list = picked[key] || [];
      const v = b.dataset.v;
      if (multi) list = list.includes(v) ? list.filter(x => x !== v) : [...list, v];
      else list = [v];
      picked[key] = list;
      step.querySelectorAll('.wz-opt').forEach(o => o.setAttribute('aria-pressed', list.includes(o.dataset.v)));
      next.disabled = !value(step);
      // Eén keuze: meteen door naar de volgende cue
      if (!multi) setTimeout(() => { if (at < steps.length - 1 && steps[at] === step) { at++; show(); } }, 260);
    }));
  });

  next.addEventListener('click', () => { if (value(steps[at]) && at < steps.length - 1) { at++; show(); } });
  back.addEventListener('click', () => { if (at > 0) { at--; show(); } });
  form.addEventListener('submit', e => e.preventDefault());
  show();
})();
