# WotR Knowledge Base — File Manifest

Pathfinder: Wrath of the Righteous (Owlcat) game data, scraped from [GameFAQs guide 80843](https://gamefaqs.gamespot.com/ps4/324475-pathfinder-wrath-of-the-righteous/faqs/80843). Game version baseline: 2.7.0 (final). Agent rules and Source Map: `AGENTS.md`. Name variants/typos: `aliases.md`.

Route any lookup from this table — open only what you need.

| Path | Contents | How to use |
| :--- | :--- | :--- |
| `AGENTS.md` | Agent rules, Source Map, data baseline, source quirks | Read every session before build work |
| `aliases.md` | British↔US spellings, known typos | Check before declaring a name missing |
| `classes/INDEX.md` | Line numbers of every archetype/section per class file | Read this, then `Read(file, offset, limit)` — class files are 200–1000 lines |
| `classes/<class>.md` | 26 base classes: stats, progression tables, features, archetypes | Big files — go through INDEX.md |
| `classes/prestige/<name>.md` | One file per prestige class (+ `_overview.md`) | Small, read whole |
| `feats/<category>.md` | 12 category files (weapon, magic, teamwork, …); one `##` per feat | `grep -ri "<name>" feats/` |
| `spells/<class>/<class>-l<level>.md` | One file per class per spell level; one bullet per spell | Duplicates are `_See X spell list._` pointers — follow one hop. Sorcerer→wizard, oracle→cleric (see their README.md) |
| `mythic/mythic-paths.md` | Mythic ranks, timing, generic abilities/feats | |
| `mythic/<path>.md` | One file per mythic path | |
| `chargen/races.md` | Races + heritages | |
| `chargen/backgrounds.md` | Backgrounds | |
| `chargen/attributes-skills.md` | Character level, attributes, point buy, skills | |
| `chargen/companions-familiars.md` | Animal companions, familiars | |
| `chargen/domains.md` | Deities + all domains/subdomains | |
| `chargen/bloodlines.md` | Sorcerer/bloodrager bloodlines | |
| `building/prereqs.md` | Feat prerequisite mechanics, essential feats | |
| `building/exploits.md` | Bonus-stacking rules and exploits | Cite in build stacking audits |
| `building/sample-builds.md` | The guide's own sample builds | Reference only — local builds live in `builds/` |
| `items/weapons.md` | Mundane + unique weapons, properties, Finnean/Radiance | |
| `items/armor-shields.md` | Mundane + unique armour and shields | |
| `items/accessories.md` | Belts, rings, cloaks, boots, consumables, … | |
| `items/artifacts-relics.md` | Artifacts (incl. component locations) + relics | |
| `items/boosts-and-misc.md` | Skill/CL/DC boost items, books, recipes | |
| `items/items-inevitable-excess.md`, `items-lord-of-nothing.md` | DLC items | A Dance of Masks not yet scraped — see scrape_all.sh |
| `builds/_template.md` | Build-guide template + verification appendix skeleton | |
| `builds/*.md` | Finished build guides | |
| `wotr_scrapper/` | Scraper (`scrape_all.sh`, macOS host only), `dedup_spells.py`, `gen_index.py` | Rerun gen_index.py after editing classes/ |
| `agent-optimization-plan.md` | The enhancement plan + online verification findings (2026-06-09) | |

All data files carry YAML frontmatter (`source`, `game_patch`). Corrections applied vs upstream: class HP/level values (Owlcat formula: max die at L1, die/2+1 after), Reviving Finale description, Wings +3 dodge AC is vs melee only.
