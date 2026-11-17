"""Knipt HTML in vertaalbare stukken: lopende tekst (met inline-tags erin), attributen en JSON-LD-teksten."""
import json
import re

INLINE = {'b', 'em', 'strong', 'br', 'code', 'cite', 'q', 'abbr', 'sup', 'sub', 'mark', 'u', 's', 'kbd', 'wbr'}
ATTRS = r'(alt|title|aria-label|content|placeholder|data-[\w-]+)'
_TOK = re.compile(r'(<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<[^>]+>)', re.S)
_TAG = re.compile(r'</?([a-zA-Z0-9]+)')
_ATTR = re.compile(r'\b' + ATTRS + r'="([^"]*)"')
_LD = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


def _is_inline(tok):
    m = _TAG.match(tok)
    return bool(m) and m.group(1).lower() in INLINE


def _texty(s):
    return bool(re.search(r'[A-Za-zÀ-ÿ]', re.sub(r'<[^>]+>', '', s)))


def walk(html, fn, attrs=True):
    """Roept fn(stuk) aan voor elk vertaalbaar stuk en vervangt het door de uitkomst (None = laten staan)."""
    toks = _TOK.split(html)
    out, group = [], []

    def flush():
        if not group:
            return
        raw = ''.join(group)
        core = raw.strip()
        if _texty(core):
            new = fn(core)
            if new is not None:
                lead = raw[:len(raw) - len(raw.lstrip())]
                trail = raw[len(raw.rstrip()):]
                raw = lead + new + trail
        out.append(raw)
        group.clear()

    for t in toks:
        if not t:
            continue
        if t.startswith('<') and (t.startswith('<script') or t.startswith('<style') or t.startswith('<!--') or not _is_inline(t)):
            flush()
            if attrs and not t.startswith(('<script', '<style', '<!--')):
                t = _ATTR.sub(lambda m: f'{m.group(1)}="{_attr(fn, m.group(1), m.group(2))}"', t)
            elif t.startswith('<script type="application/ld+json">'):
                t = _LD.sub(lambda m: m.group(1) + _ld(fn, m.group(2)) + m.group(3), t)
            out.append(t)
        else:
            if t.startswith('<') and attrs:
                t = _ATTR.sub(lambda m: f'{m.group(1)}="{_attr(fn, m.group(1), m.group(2))}"', t)
            group.append(t)
    flush()
    return ''.join(out)


def _attr(fn, name, val):
    if not _texty(val) or name in ('data-href', 'data-cover', 'data-src') or val.startswith(('http', 'width=')):
        return val
    new = fn(val)
    return val if new is None else new


def _ld(fn, src):
    try:
        data = json.loads(src)
    except ValueError:
        return src

    def rec(x, key=''):
        if isinstance(x, dict):
            return {k: rec(v, k) for k, v in x.items()}
        if isinstance(x, list):
            return [rec(v, key) for v in x]
        if isinstance(x, str) and key in ('name', 'description', 'text', 'headline', 'alternateName', 'jobTitle',
                                            'serviceType', 'about', 'caption', 'acceptedAnswer') and _texty(x):
            new = fn(x)
            return x if new is None else new
        return x
    return json.dumps(rec(data), ensure_ascii=False)
