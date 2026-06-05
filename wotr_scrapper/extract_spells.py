#!/usr/bin/env python3
"""Extract per-level spell markdown from a saved GameFAQs WotR guide spell page."""
import html
import os
import re
import sys

SRC = sys.argv[1]
OUT_DIR = sys.argv[2]      # e.g. ../spells/druid
PREFIX = sys.argv[3]       # e.g. druid
TITLE = sys.argv[4]        # e.g. "Druid Spells"

src = open(SRC).read()
os.makedirs(OUT_DIR, exist_ok=True)


def clean(s):
    s = re.sub(r'<br ?/?>', '', s)
    s = re.sub(r'<[^>]+>', '', s)
    return html.unescape(s).strip()


# ---- parse h5 detail entries: name -> formatted line tail ----
details = {}
for m in re.finditer(r'<h5>([^<(]+?)\s*\(?(\w+)\)<a [^>]*></a></h5>(<table class="ffaq">.*?</table>)', src, re.S):
    name, school, body = m.group(1).strip(), m.group(2).strip(), m.group(3)
    fields = dict(re.findall(r'<th[^>]*>([^<]+)</th><td>(.*?)</td>', body))
    desc_m = re.search(r'<td colspan="2">(.*?)</td>', body, re.S)
    desc = clean(desc_m.group(1)) if desc_m else ''
    parts = []
    t = clean(fields.get('Target', ''))
    if t and t != 'N/A':
        parts.append(f'T: {t}')
    dur = clean(fields.get('Duration', ''))
    if dur and dur != 'N/A':
        parts.append(f'Dur: {dur}')
    save = clean(fields.get('Saving Throw', ''))
    if save and save != 'N/A':
        parts.append(f'Save: {save}')
    if '✓' in fields.get('Spell Resistance', ''):
        parts.append('SR')
    d = clean(fields.get('Spell Descriptors', ''))
    if d and d not in ('N/A', '-'):
        parts.append(f'Desc: {d}')
    cast = clean(fields.get('Casting Time', ''))
    if cast and cast not in ('N/A', 'Standard Action'):
        cast = re.sub(r' Action$', '', cast)
        cast = cast[0] + cast[1:].lower()  # "Full Round" -> "Full round"
        parts.append(f'Cast: {cast}')
    details[name] = (school, ' | '.join(parts), desc)

# ---- parse per-level summary tables ----
levels = re.split(r'<h4>Level (\d+)<a [^>]*></a></h4>', src)
# levels: [pre, '0', chunk, '1', chunk, ...]
for i in range(1, len(levels), 2):
    lvl, chunk = levels[i], levels[i + 1]
    # footnote definitions in this chunk, e.g. <p><sup>1</sup> Primal Druid only</p>
    notes = dict(re.findall(r'<p><sup>(\d+)</sup>\s*(.*?)</p>', chunk))
    rows = re.findall(
        r'<tr><td>(?:<a href="([^"]*)"[^>]*>)?([^<]+)(?:</a>)?(?:<sup>(\d+)</sup>)?</td>'
        r'<td>([^<]+)</td></tr>', chunk)
    lines = []
    for href, name, sup, school in rows:
        name, school = html.unescape(name).strip(), school.strip()
        note = f' *({notes[sup]})*' if sup and sup in notes else ''
        if name in details:
            school2, fields_str, desc = details[name]
            tail = (f'{fields_str} — {desc}' if fields_str else desc)
            lines.append(f'- **{name}** *({school2})* — {tail}{note}')
        elif href:
            ref = 'Wizard' if 'wizard' in href else 'Cleric' if 'cleric' in href else 'other'
            lines.append(f'- **{name}** *({school})* — _See {ref} spell list._{note}')
        else:
            lines.append(f'- **{name}** *({school})* —{note}')
            print(f'WARN: no detail/link for {name} (L{lvl})')
    out = os.path.join(OUT_DIR, f'{PREFIX}-l{lvl}.md')
    with open(out, 'w') as f:
        f.write(f'# {TITLE} — Level {lvl}\n')
        f.write(f'*{len(lines)} spells. Source: GameFAQs WotR Guide (80843).*\n')
        f.write('*Format: **Name** *(School)* — T: target | Dur | Save | SR | Desc | Cast — '
                'Description. Fields omitted if empty/default.*\n\n')
        f.write('\n'.join(lines) + '\n')
    print(f'{out}: {len(lines)} spells')
