# Build Guide Template & Verification Framework

This file is the framework for producing build guides. It has two audiences, in this order:
1. **The player** — the top of every build file is a clean, human-readable guide. No file paths, no checkmarks, no grep commands.
2. **The verifying agent** — all verification work goes in the **Appendix** at the bottom. Every claim in the human section must have a matching evidence row there.

**Agent rules:**
- Verify BEFORE writing: grep every class feature, feat, revelation, spell, and mythic ability against the local files (see Source Map below) before it appears in the guide.
- The human-readable section must never contain file references, "✓" prereq notes, or "Verified" labels — that's appendix material.
- Prereqs are still *checked*, just reported in the appendix table only.
- If something can't be found locally, retry with name variants (the guide has British spellings and a few typos — e.g. "Neutralise/Neutralize"); follow `_See X spell list_` pointers one hop. If still missing, flag it in the appendix under **Unverified** — never invent.
- Oracle/Sorcerer-style spontaneous casters MUST get an explicit spells-known plan — picks per spell level, respecting the class's spells-known table.
- **Ask before assuming party context.** If a build choice's value depends on something only the user knows, ask BEFORE writing (use the AskUserQuestion tool if available; otherwise ask in plain text). Batch the questions, offer concrete options with a recommended default, and only ask when the answer would change a pick. Triggers:
  - **Capstone/feature nullified by a companion** — e.g. a Skald sharing Beast Totem pounce makes Battle Oracle's Final Revelation redundant
  - **Teamwork feats** — who is the partner? If none, swap the feat
  - **Role overlap** — is healing/buffing/tanking already covered by the party?
  - **Solo vs party / difficulty / mod context** if the user hasn't said
  Record the answers in the **Party Fit** row of At a Glance, and design around them. If the user can't be asked, state the assumption explicitly there instead — never silently depend on it.

---

# [Build Name]
**[Class & Archetype] — [one-line role description]**

## At a Glance
| | |
| :--- | :--- |
| **Race** | [race (heritage)] |
| **Attributes** | Str X, Dex X, Con X, Int X, Wis X, Cha X (level-ups → [stat]) |
| **Key class choices** | [curse/mystery/deity/bloodline/etc.] |
| **Weapon & armour** | [loadout] |
| **Mythic Path** | [path + the one-line reason] |
| **Party Fit** | [confirmed party assumptions: who partners teamwork feats, what roles this build must/needn't cover, known anti-synergies avoided] |

## Levelling Table
*Just the picks. One row per level where you choose something.*

| Level | Feat | Class Feature Choice | Notes |
| :--- | :--- | :--- | :--- |
| 1 | ... | ... | ... |

## Spell Selection
*For spontaneous casters: picks per spell level in the order to learn them. Mark which come free (mystery/curse/bloodline/"Additional Spells") so the player doesn't waste picks.*

- **Level 1 (X known):** ...
- **Level 2 (X known):** ...

**Free, don't pick:** [list of spells granted automatically and their source]

## Mythic Progression
| Rank | Ability/Feat Pick | Path Choice |
| :--- | :--- | :--- |
| 1 | ... | ... |

## How It Plays
[2-3 short paragraphs: early game, the power-spike moment, endgame loop. Plain language.]

## Variants & Trade-offs
[Picks deliberately rejected and why — one line each.]

---

# Appendix: Agent Verification

## A1. Data Integrity Checklist
- [ ] **Literal String Match:** every named ability grepped verbatim (or via documented name-variant) in the local files
- [ ] **Archetype Compatibility:** archetype trade-aways checked against required features
- [ ] **Spell/Ability Origin:** each spell confirmed on this class's list (or granted by curse/mystery/mythic source)
- [ ] **Prerequisite Chains:** every feat's prereqs satisfied at the level it's taken
- [ ] **Spells-Known Budget:** spontaneous casters' picks fit the class table
- [ ] **Stacking Audit:** bonus types listed; no same-type collisions among the build's core buffs
- [ ] **Party-Composition Audit:** party context asked (or assumption stated in Party Fit); no core pick duplicated or nullified by a stated party member; every teamwork feat has a named partner

## A2. Evidence Table
*One row per claim in the human section.*

| Claim | Source | Status |
| :--- | :--- | :--- |
| [ability — what it does / prereq met how] | file.md:line | Verified / Unverified |

## A3. Source Map (local verification hub)
All extracted from the [GameFAQs WotR Guide (80843)](https://gamefaqs.gamespot.com/ps4/324475-pathfinder-wrath-of-the-righteous/faqs/80843).

| Domain | Location | Notes |
| :--- | :--- | :--- |
| Classes & archetypes | `classes/<class>.md` (26 + prestige) | features by level, archetype trade-aways |
| Feats | `feats/*.md` (12 category files) | `grep -ri "<name>" feats/` |
| Spells | `spells/<class>/<class>-l<level>.md` | alchemist, bard, bloodrager, cleric, druid, hunter, inquisitor, magus, paladin, ranger, shaman, warpriest, witch, wizard/sorcerer |
| Spell aliases | `spells/sorcerer/`, `spells/oracle/` | sorcerer → wizard list; oracle → cleric list |
| Cross-refs | `_See X spell list._` entries | full text one hop away; annotated variants: `_See X spell list ("Actual Name")._` |
| Mythic | `mythic/*.md` | mythic-paths.md = ranks/abilities/feats; one file per path |
| Races, backgrounds, attributes, skills, bloodlines, domains | `character-creation.md` | |
| Build-craft, stacking exploits, sample builds | `character-building.md` | Exploits section = stacking rules |
| Items | `items/*.md` | base + 2 DLC files |

**Known source quirks:** British spellings throughout (armour, manoeuvre…); guide typos are annotated in place; Reviving Finale (bard 3) has no description upstream; Nature's Exile / Thirsting Entanglement flagged as upstream omissions.

## A4. Stacking & Mechanics Notes
[Bonus-type analysis for the build's core buff stack; cite character-building.md Exploits where relevant.]
