_Template for build guides. Agent rules and Source Map: ../AGENTS.md_

# Build Guide Template & Verification Framework

This file is the framework for producing build guides. It has two audiences, in this order:
1. **The player** — the top of every build file is a clean, human-readable guide. No file paths, no checkmarks, no grep commands.
2. **The verifying agent** — all verification work goes in the **Appendix** at the bottom. Every claim in the human section must have a matching evidence row there.

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

## A3. Stacking & Mechanics Notes
[Bonus-type analysis for the build's core buff stack; cite building/exploits.md where relevant.]
