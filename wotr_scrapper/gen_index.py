#!/usr/bin/env python3
"""Regenerate classes/INDEX.md (heading line-number index). Run from repo root."""
import glob, re, os
out = ["---","source: generated index","game_patch: 2.7.0","---","",
"# Classes Index","",
"Line numbers for every major heading in each class file — use Read with offset/limit instead of reading whole files.",
"Regenerate after any edit: `python3 wotr_scrapper/gen_index.py`",""]
for f in sorted(glob.glob("classes/*.md")):
    if f.endswith("INDEX.md"): continue
    lines = open(f).read().splitlines()
    out.append(f"## {os.path.basename(f)} ({len(lines)} lines)")
    entries = [f"L{i+1} {re.sub('^#+ ','',l)}" for i,l in enumerate(lines) if re.match(r'^###? ',l)]
    out.append("; ".join(entries) if entries else "(no subsections)")
    out.append("")
out.append("## classes/prestige/")
out.append("One file per prestige class: " + ", ".join(sorted(os.path.basename(p) for p in glob.glob("classes/prestige/*.md"))))
open("classes/INDEX.md","w").write("\n".join(out)+"\n")
print("regenerated classes/INDEX.md")
