# Engelse vertalingen voor de rest van de site (alles buiten de hoofdpagina's in i18n.py).
# (Nederlands, Engels). build.py vervangt deze teksten in de Nederlandse HTML na TR, langste eerst.
TR_EN = [
]

# Losse stukken tekst (exact), uit i18n_en_seg.json: {Nederlands: Engels}.
import json as _json
from pathlib import Path as _Path
SEG_EN = _json.loads((_Path(__file__).parent / 'i18n_en_seg.json').read_text())

# Patronen voor herhalende teksten (fotobijschriften e.d.).
RE_EN = [
    (r'^(.+), foto (\d+)$', r'\1, photo \2'),
    (r'^Foto (\d+) groot bekijken$', r'View photo \1 large'),
    (r"^(\d+) foto's$", r'\1 photos'),
    (r'^1 foto$', '1 photo'),
    (r'Een project van MATRIX E\.I\.L\. voor ', 'A project by MATRIX E.I.L. for '),
    (r'Een project van MATRIX E\.I\.L\.', 'A project by MATRIX E.I.L.'),
]
