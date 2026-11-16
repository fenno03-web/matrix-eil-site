// Bèta-aanmelding op de ARGUS-productpagina's.
// Verstuurt via FormSubmit naar info@; lukt dat niet, dan opent een ingevulde mail als terugval.
document.querySelectorAll('.beta-form').forEach(form => {
  const msg = form.querySelector('.bf-msg');
  const btn = form.querySelector('button[type="submit"]');
  const mailto = data => {
    const lines = [...data.entries()].filter(([k]) => !k.startsWith('_')).map(([k, v]) => `${k}: ${v}`);
    return `mailto:info@matrixeventsupport.nl?subject=${encodeURIComponent('Bèta-aanmelding ' + form.dataset.tool)}&body=${encodeURIComponent(lines.join('\n'))}`;
  };
  form.addEventListener('submit', async e => {
    e.preventDefault();
    const data = new FormData(form);
    if (data.get('_honey')) return;
    btn.disabled = true;
    form.classList.add('sending');
    msg.className = 'bf-msg';
    msg.textContent = 'Versturen…';
    try {
      const res = await fetch(form.action.replace('formsubmit.co/', 'formsubmit.co/ajax/'), {
        method: 'POST', headers: { Accept: 'application/json' }, body: data,
      });
      const json = await res.json().catch(() => ({}));
      if (!res.ok || String(json.success) === 'false') throw new Error(json.message || res.status);
      form.classList.remove('sending');
      form.classList.add('sent');
      msg.classList.add('ok');
      msg.innerHTML = `<b>Aangemeld.</b> Bedankt! We nemen contact op zodra er een plek vrij is voor ${form.dataset.tool}.`;
      form.reset();
    } catch (err) {
      form.classList.remove('sending');
      msg.classList.add('er');
      msg.innerHTML = `Versturen lukte niet. <a href="${mailto(data)}">Stuur je aanmelding per mail</a>, dan staat alles er al in.`;
    } finally {
      btn.disabled = false;
    }
  });
});
