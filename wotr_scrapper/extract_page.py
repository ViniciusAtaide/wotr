#!/usr/bin/env python3
"""Convert a saved GameFAQs WotR guide page to markdown (generic: headings, tables, lists, paragraphs)."""
import html as H
import re
import sys

SRC, OUT = sys.argv[1], sys.argv[2]
src = open(SRC).read()

# main FAQ content lives in <div class="ffaq ..."> after the ftoc; take from first <h2 to the share/footer
start = src.find('<h2')
end = src.find('faq_bot_wrap')
if end == -1:
    end = len(src)
body = src[start:end]
body = re.sub(r'<div class="ftoc">.*?</div>', '', body, flags=re.S)


def text(s):
    s = re.sub(r'<br ?/?>', '\n', s)
    s = re.sub(r'<sup>(\d+)</sup>', r'^\1', s)
    s = re.sub(r'<(b|strong)>(.*?)</\1>', r'**\2**', s, flags=re.S)
    s = re.sub(r'<(i|em)>(.*?)</\1>', r'*\2*', s, flags=re.S)
    s = re.sub(r'<[^>]+>', '', s)
    return H.unescape(s).strip()


out = []
# tokenize block-level elements in order
for m in re.finditer(
        r'<h([2-6])[^>]*>(.*?)</h\1>|<table[^>]*>(.*?)</table>|<p[^>]*>(.*?)</p>|<[ou]l[^>]*>(.*?)</[ou]l>',
        body, re.S):
    h_lvl, h_txt, tbl, para, lst = m.groups()
    if h_lvl:
        t = text(h_txt)
        if t and t.lower() != 'table of contents':
            out.append('#' * int(h_lvl) + ' ' + t)
    elif tbl is not None:
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tbl, re.S)
        md_rows = []
        for r in rows:
            cells = re.findall(r'<t[hd][^>]*(?: colspan="(\d+)")?[^>]*>(.*?)</t[hd]>', r, re.S)
            vals = []
            for span, c in cells:
                vals.append(text(c).replace('\n', ' ').replace('|', '/'))
                for _ in range(int(span or 1) - 1):
                    vals.append('')
            md_rows.append(vals)
        if not md_rows:
            continue
        width = max(len(r) for r in md_rows)
        # key-value table (2 cols, many rows where first col is a label) renders better as list
        for r in md_rows:
            r += [''] * (width - len(r))
        out.append('| ' + ' | '.join(md_rows[0]) + ' |')
        out.append('|' + ' --- |' * width)
        for r in md_rows[1:]:
            out.append('| ' + ' | '.join(r) + ' |')
        out.append('')
    elif para is not None:
        t = text(para)
        if t:
            out.append(t + '\n')
    elif lst is not None:
        for li in re.findall(r'<li[^>]*>(.*?)</li>', lst, re.S):
            t = text(li)
            if t:
                out.append('- ' + t)
        out.append('')

# drop the guide byline + prev/next nav: start at the second h2 (the page title)
h2s = [i for i, l in enumerate(out) if l.startswith('## ')]
if len(h2s) > 1:
    out = out[h2s[1]:]
# drop everything from the trailing prev/next nav onward (page footer junk)
cut = next((i for i, l in enumerate(out) if l.startswith('- Previous: ') or l.startswith('- Next: ')), None)
if cut is not None:
    out = out[:cut]
title = out[0][3:] if out and out[0].startswith('## ') else ''
out.insert(1, '*Source: GameFAQs WotR Guide (80843).*\n')
md = '\n'.join(out).replace('## ', '# ', 1)
md = re.sub(r'\n{3,}', '\n\n', md)
open(OUT, 'w').write(md + '\n')
print(f'{OUT}: {title}: {len(md)} chars')
