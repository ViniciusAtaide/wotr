# Agent Optimization Plan — WotR Knowledge Base

*Goal: best agent outcome per token. Audited 2026-06-09 against repo state (163 md files, ~490k tokens total). Verification spot-check results in §3.*

## 1. Current state

| Area | Size (est. tokens) | Agent cost problem |
| :--- | :--- | :--- |
| `classes/` (27 files) | 219k | Biggest files (9–12k each); archetypes buried inline; agent must read or grep blind |
| `spells/` (16 dirs) | 111k | Well sharded (per class, per level); 441 `_See` pointers dedupe well |
| `mythic/` | 48k | OK |
| `items/items.md` | 38k | Single monolith; weapons/armor/uniques mixed |
| `character-creation.md` | 30k | Monolith: races + backgrounds + attributes + skills + domains + bloodlines |
| `character-building.md` | 15k | Monolith: prereqs + exploits + sample builds |
| `feats/` (12 files) | 14k | Good: small files, `##` per feat, greppable |
| `wotr-guide.md` | 1.5k | Mixes two jobs: agent rules/source map + build template |
| No root README/index | — | Discovery costs `find`/`ls` round-trips every session |

What already works well (keep): per-class/per-level spell sharding, compact one-line spell format, `_See X spell list_` pointer dedup, oracle/sorcerer alias READMEs, evidence-table verification framework.

## 2. Enhancements (priority order)

### P1 — Navigation layer (highest ROI, ~2k tokens added, saves 5–10k per query)
- **Root `README.md` manifest**: one line per file/dir — what's in it, when to open it. An agent should route any lookup in one ≤1k-token read.
- **Per-directory `INDEX.md` for `classes/`**: for each class file, list its archetypes and major sections with line numbers (e.g. `oracle.md — Dual-Cursed L210, Purifier L387 …`). Lets agents `Read(offset, limit)` instead of consuming 12k tokens. Regenerate via a small script (`grep -n '^###'`).
- **Split `wotr-guide.md`** into `AGENTS.md` (agent rules, source map, quirks, alias table — read every session) and `builds/_template.md` (read only when writing a build).

### P2 — Greppability & aliases
- **`aliases.md`**: one table of name variants — British↔US spellings (armour/armor, manoeuvre/maneuver, Neutralise/Neutralize), known typos (e.g. "Swatooth Saber" → Sawtooth Sabre), and in-game vs guide naming. One grep target instead of N failed greps.
- **Heading discipline**: every archetype, revelation, curse, and mystery as `### Name` exactly matching in-game spelling, so `grep -n "^#.*<name>"` always hits. Currently archetype headings vary in level and aren't tagged (the word "Archetype" never appears in oracle.md).
- **Frontmatter** on every file: `source_url`, `scraped`, `game_patch: 2.7.0` — makes freshness checkable and gives agents provenance without prose.

### P3 — Shard the monoliths
- `character-creation.md` → `chargen/races.md`, `backgrounds.md`, `attributes-skills.md`, `domains.md`, `bloodlines.md` (~5–8k each).
- `items/items.md` → `items/weapons.md`, `armor.md`, `accessories.md`, `unique-items.md`.
- `character-building.md` → `building/prereqs.md`, `exploits.md` (stacking rules — referenced by the build framework), `sample-builds.md`.
- `classes/prestige-classes.md` (12k) → one file per prestige class.
- Update the Source Map after each split.

### P4 — Dedup consistency audit
Pointer policy is inconsistent: `bloodrager-l1.md` points Magic Missile to the wizard list, but `magus-l1.md` carries the full duplicate text. Rule: full text lives on exactly one canonical list (wizard for arcane, cleric for divine, druid for nature); all other lists carry pointers. Sweep with a script that diffs duplicate spell names across lists. Est. savings: 10–20k tokens, plus eliminates drift risk when corrections land.

### P5 — Hygiene & freshness
- Delete stray `.DS_Store` files (already gitignored).
- **Scrape missing DLC content**: the upstream guide has *A Dance of Masks* pages (items/feats), but the repo stops at Lord of Nothing. Add `items/items-dance-of-masks.md` etc. via `wotr_scrapper`.
- Record `game_patch: 2.7.0` as the baseline in `AGENTS.md`; content development ended with A Dance of Masks (June 2024), final hotfix 2.7.0x (Sept 2025), so the data is stable — no recurring re-verification needed.

### Explicitly not recommended
- Converting tables to CSV/JSON: markdown tables parse fine for agents; conversion adds maintenance for no token win.
- Splitting spell files further: already optimally sized (1–3k tokens).

## 3. Online verification findings (spot-check, 2026-06-09)

| Claim (local file) | Verdict | Correction |
| :--- | :--- | :--- |
| Mythic rank timing table (`mythic/mythic-paths.md`) | Confirmed | Structure matches; R4 timing varies with Act 3 progress (~12–13) rather than strictly the Lexicon pickup |
| Oracle: **6 HP/level** (`classes/oracle.md`) | **Contradicted** | 8 HP at L1, **5/level** after (d8). Systemic risk: audit HP lines in all 26 class files — source may use a wrong convention throughout |
| Oracle 3 skill pts, Cha-based, 3/4 BAB, cleric list, spontaneous | Confirmed | — |
| Lame curse milestones 5/10/15 (`classes/oracle.md`) | Confirmed | — |
| Skill at Arms = martial weapons + heavy armor | Confirmed | — |
| Reviving Finale: no description upstream (`spells/bard/bard-l3.md`) | Resolved | Ends an active bardic performance; allies in area heal 2d6 + 1 per 2 caster levels. Add to file |
| Angel merged spellbook (`builds/*.md`) | Confirmed | Merged CL = class level + mythic rank (max 30); casting stat from main class |
| Mythic abilities odd ranks / feats even ranks | Confirmed | — |
| Wings = +3 dodge AC (`builds/oracle-angel-frontliner.md`) | **Partly wrong** | +3 dodge **vs melee only**, + immunity to ground effects. Add qualifier |
| Weapon Finesse weapon list (`feats/weapon-feats.md`) | Confirmed | Dueling Sword works despite not being in the in-game text; "Swatooth Saber" typo stands (→ aliases.md) |
| Spontaneous casters one spell level later | Confirmed | — |
| Game current? | Stable | Last DLC June 2024; last patch 2.7.0x (Sept 2025); nothing newer as of June 2026. **Repo gap: no Dance of Masks files** |

Sources: [Fextralife Oracle](https://pathfinderwrathoftherighteous.wiki.fextralife.com/Oracle), [Oracle's Curse](https://pathfinderwrathoftherighteous.wiki.fextralife.com/Oracle's+Curse), [Mythic Spellbook](https://pathfinderwrathoftherighteous.wiki.fextralife.com/Mythic+Spellbook), [Mythic Path](https://pathfinderwrathoftherighteous.wiki.fextralife.com/Mythic+Path), [Wings](https://pathfinderwrathoftherighteous.wiki.fextralife.com/Wings), [Weapon Finesse](https://pathfinderwrathoftherighteous.wiki.fextralife.com/Weapon+Finesse), [Neoseeker Mythic rankings](https://www.neoseeker.com/pathfinder-wrath-of-the-righteous/guides/Mythic_Path_rankings), [Steam 2.7.0W notes](https://store.steampowered.com/news/app/1184370/view/536595840131664074), [SteamDB 2.7.0x](https://steamdb.info/patchnotes/18475305/), [GameFAQs 80843 — A Dance of Masks](https://gamefaqs.gamespot.com/ps4/324475-pathfinder-wrath-of-the-righteous/faqs/80843/a-dance-of-masks).

## 4. Suggested execution order

1. P1 navigation layer + P2 aliases/frontmatter (one session, immediate payoff)
2. Fix the three content findings: Oracle HP (then audit all class HP lines), Wings qualifier, Reviving Finale description
3. Scrape Dance of Masks pages (P5)
4. P3 monolith splits + Source Map update
5. P4 dedup sweep script
