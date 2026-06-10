#!/usr/bin/env python3
"""Deduplicate spell descriptions across class spell lists.

Finds spells whose FULL description text appears in 2+ class lists and
replaces the non-canonical copies with a pointer:

    - **Name** *(School)* — _See <CanonicalClass> spell list._

Canonical priority: wizard > cleric > druid > bard > alphabetical-first
remaining class.

Safety: a copy is only replaced when its description is essentially
identical to the canonical one (whitespace-normalized difflib ratio
>= 0.95). Genuinely differing texts are kept and reported.

Usage:
    python3 dedup_spells.py [--dry-run] [--spells-dir PATH]
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

SIMILARITY_THRESHOLD = 0.95
CANONICAL_PRIORITY = ["wizard", "cleric", "druid", "bard"]

# - **Name** *(School)* — rest
ENTRY_RE = re.compile(r"^- \*\*(?P<name>.+?)\*\* \*\((?P<school>[^)]+)\)\* — (?P<rest>.*)$")
POINTER_RE = re.compile(r"^_See .+?spell list")
# trailing italic-parenthetical annotation, e.g. *(Beast Tamer only)* or
# *(Listed as "Flamestrike" in the guide's cleric table.)* — these are meta
# notes, not part of the description, so they are excluded from similarity
# comparison and preserved on the replacement pointer line.
ANNOTATION_RE = re.compile(r"\s*(\*\([^)]*\)\*)\s*$")
COUNT_LINE_RE = re.compile(r"^\*(\d+) spells?\.(.*)$")


class Entry:
    def __init__(self, path, line_idx, line, name, school, rest):
        self.path = path
        self.line_idx = line_idx
        self.line = line
        self.name = name
        self.school = school
        self.rest = rest
        m = ANNOTATION_RE.search(rest)
        self.annotation = m.group(1) if m else None
        self.body = ANNOTATION_RE.sub("", rest).strip()
        self.is_pointer = bool(POINTER_RE.match(self.body))
        # placeholder / meta entries start with "_" (e.g. "_No description...")
        self.is_full = not self.body.startswith("_")

    @property
    def cls(self):
        return self.path.parent.name


def normalize(text):
    return re.sub(r"\s+", " ", text).strip()


def similarity(a, b):
    return difflib.SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def canonical_sort_key(cls):
    if cls in CANONICAL_PRIORITY:
        return (CANONICAL_PRIORITY.index(cls), "")
    return (len(CANONICAL_PRIORITY), cls)


def parse_files(spells_dir):
    files = {}  # path -> list of lines
    entries = []
    for path in sorted(spells_dir.glob("*/*.md")):
        if path.name.lower() == "readme.md":
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        files[path] = lines
        for i, line in enumerate(lines):
            m = ENTRY_RE.match(line)
            if m:
                entries.append(Entry(path, i, line, m.group("name"),
                                     m.group("school"), m.group("rest")))
    return files, entries


def count_entries(lines):
    return sum(1 for ln in lines if ENTRY_RE.match(ln))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="print planned changes without writing files")
    ap.add_argument("--spells-dir", default=None,
                    help="path to the spells/ directory "
                         "(default: ../spells relative to this script)")
    args = ap.parse_args()

    spells_dir = (Path(args.spells_dir) if args.spells_dir
                  else Path(__file__).resolve().parent.parent / "spells")
    if not spells_dir.is_dir():
        sys.exit(f"spells dir not found: {spells_dir}")

    files, entries = parse_files(spells_dir)
    pre_counts = {p: count_entries(ls) for p, ls in files.items()}

    # group FULL-text entries by spell name
    by_name = {}
    for e in entries:
        if e.is_full:
            by_name.setdefault(e.name, []).append(e)

    replacements = []   # (entry, canonical_class, new_line)
    kept_differs = []   # (entry, canonical_entry, ratio)

    for name, group in sorted(by_name.items()):
        classes = {e.cls for e in group}
        if len(classes) < 2:
            continue
        group.sort(key=lambda e: canonical_sort_key(e.cls))
        canon = group[0]
        canon_cls_title = canon.cls.capitalize()
        for dup in group[1:]:
            if dup.cls == canon.cls:
                continue  # same class, different file/level — leave alone
            ratio = similarity(canon.body, dup.body)
            if ratio >= SIMILARITY_THRESHOLD:
                new_line = (f"- **{dup.name}** *({dup.school})* — "
                            f"_See {canon_cls_title} spell list._")
                if dup.annotation:
                    new_line += f" {dup.annotation}"
                replacements.append((dup, canon, ratio, new_line))
            else:
                kept_differs.append((dup, canon, ratio))

    chars_saved = sum(len(d.line) - len(new) for d, _, _, new in replacements)

    print(f"Spell entries parsed: {len(entries)}")
    print(f"Full-text duplicates to convert to pointers: {len(replacements)}")
    print(f"Estimated savings: {chars_saved} chars (~{chars_saved // 4} tokens)\n")

    for dup, canon, ratio, new_line in replacements:
        rel = dup.path.relative_to(spells_dir)
        print(f"[{'DRY' if args.dry_run else 'EDIT'}] {rel}:{dup.line_idx + 1} "
              f"**{dup.name}** -> See {canon.cls.capitalize()} "
              f"(sim {ratio:.3f}, -{len(dup.line) - len(new_line)} chars)")

    if kept_differs:
        print("\nKept — differs (similarity < "
              f"{SIMILARITY_THRESHOLD}):")
        for dup, canon, ratio in kept_differs:
            print(f"  **{dup.name}**: {dup.path.relative_to(spells_dir)} vs "
                  f"{canon.path.relative_to(spells_dir)} (sim {ratio:.3f})")
    else:
        print("\nKept — differs: none")

    if args.dry_run:
        print("\nDry run: no files written.")
        return

    # apply edits
    touched = set()
    for dup, _canon, _ratio, new_line in replacements:
        files[dup.path][dup.line_idx] = new_line
        touched.add(dup.path)

    for path in sorted(touched):
        lines = files[path]
        new_count = count_entries(lines)
        if new_count != pre_counts[path]:
            # entry count changed (should not happen — pointers still match
            # the entry pattern); update the "*N spells.*" header line
            print(f"WARNING: entry count changed in {path.name}: "
                  f"{pre_counts[path]} -> {new_count}; updating header")
            for i, ln in enumerate(lines):
                m = COUNT_LINE_RE.match(ln)
                if m:
                    lines[i] = f"*{new_count} spells.{m.group(2)}"
                    break
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\nWrote {len(touched)} files.")


if __name__ == "__main__":
    main()
