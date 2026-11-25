// ARGUS Metron beta-aanmelding: post het formulier als JSON naar de Supabase-functie metron-apply.
// Antwoord: {ok:true[, repeat:true]} -> bedankt-scherm; {ok:false, code} -> melding per code.
(() => {
  const ENDPOINT = 'https://nxlozepwjjfxxxmcadnq.supabase.co/functions/v1/metron-apply';
  const KEY = 'sb_publishable_ZWzmO6NzE8zTTEnlgp1-lQ_LhdUFKpY'; // publieke sleutel, hoort in de site
  const form = document.querySelector('.mb-form');
  if (!form) return;
  const lang = form.dataset.lang === 'en' ? 'en' : 'nl';
  const L = (nl, en) => (lang === 'en' ? en : nl);
  const MSG = {
    invalid: L('Vul je naam en een geldig e-mailadres in.', 'Please enter your name and a valid email address.'),
    consent: L('Vink het akkoord aan.', 'Please tick the consent box.'),
    rate: L('Te veel aanmeldingen, probeer het later.', 'Too many sign-ups, please try again later.'),
    server: L('Er ging iets mis, probeer het later opnieuw.', 'Something went wrong, please try again later.'),
  };
  const btn = form.querySelector('button[type="submit"]');
  const msg = form.querySelector('.bf-msg');
  const thanks = form.parentElement.querySelector('.mb-thanks');
  const count = form.querySelector('.mb-count');
  const motivation = form.elements.motivation;
  const btnText = btn.textContent;
  let busy = false;

  motivation.addEventListener('input', () => { count.textContent = `${motivation.value.length} / 2000`; });

  const val = name => (form.elements[name] && form.elements[name].value || '').trim();
  const fail = (code, field) => {
    msg.className = 'bf-msg er';
    msg.textContent = MSG[code] || MSG.server;
    const el = field || (code === 'consent' ? form.elements.consent : code === 'invalid' ? (val('name').length < 2 ? form.elements.name : form.elements.email) : null);
    if (el) el.focus();
  };

  form.addEventListener('submit', async e => {
    e.preventDefault();
    if (busy) return;
    // Eerst zelf controleren, dan hoeft de server het niet af te keuren
    if (val('name').length < 2 || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(val('email'))) return fail('invalid');
    if (!form.elements.consent.checked) return fail('consent');

    const body = {
      name: val('name'), email: val('email'), company: val('company'), role: val('role'),
      console: val('console'), dj_gear: val('dj_gear'), os: (form.querySelector('input[name="os"]:checked') || {}).value || '',
      country: val('country'), motivation: val('motivation').slice(0, 2000), source: val('source'),
      lang, consent: true,
      website: form.elements.website.value, // honeypot: mensen laten dit leeg
    };

    busy = true;
    btn.disabled = true;
    btn.textContent = L('Versturen…', 'Sending…');
    form.classList.add('sending');
    msg.className = 'bf-msg';
    msg.textContent = '';
    try {
      const res = await fetch(ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', apikey: KEY },
        body: JSON.stringify(body),
      });
      const json = await res.json().catch(() => ({}));
      if (json.ok === true) {
        form.hidden = true;
        thanks.hidden = false;
        thanks.focus({ preventScroll: true });
        thanks.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return; // knop blijft uit: geen tweede aanmelding
      }
      fail(json.code || 'server');
    } catch (err) {
      fail('server');
    }
    busy = false;
    btn.disabled = false;
    btn.textContent = btnText;
    form.classList.remove('sending');
  });
})();
