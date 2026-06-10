_Template for build guides. Agent rules and Source Map: ../AGENTS.md_

# Build Guide Template & Verification Framework

This file is the framework for producing build guides. The shipped guide is written for **the player only** — no file paths, no checkmarks, no grep commands, no evidence tables. Verification still happens in full while writing (see the process below); its bookkeeping just stays out of the final file. What *does* ship is the player-relevant residue of that work: the **Fine Print** section at the end of every guide.

## Verification process (do this while writing — don't ship it)
- **Literal String Match:** every named ability grepped verbatim (or via documented name-variant) in the local files
- **Archetype Compatibility:** archetype trade-aways checked against required features
- **Spell/Ability Origin:** each spell confirmed on this class's list (or granted by curse/mystery/bloodline/mythic source)
- **Prerequisite Chains:** every feat's prereqs satisfied at the level it's taken
- **Spells-Known Budget:** spontaneous casters' picks fit the class table
- **Stacking Audit:** bonus types listed; no same-type collisions among the build's core buffs
- **Party-Composition Audit:** party context asked (or assumption stated in Party Fit); no core pick duplicated or nullified by a stated party member; every teamwork feat has a named partner

Anything that can't be verified locally must not be silently included: either cut it, or keep it and flag it in **Fine Print** as an unverified/play-confirmed assumption *with its in-game fallback*.

---

# [Build Name]
**[Class & Archetype] — [one-line role description]**

## At a Glance
| | |
| :--- | :--- |
| **Race** | [race (heritage)] |
| **Attributes** | Str X, Dex X, Con X, Int X, Wis X, Cha X (level-ups → [stat]) |
| **Key class choices** | [curse/mystery/deity/bloodline/etc.] |
| **Weapon & armor** | [loadout] |
| **Mythic Path** | [path + the one-line reason] |
| **Party Fit** | [confirmed party assumptions: who partners teamwork feats, what roles this build must/needn't cover, known anti-synergies avoided] |

## Leveling Table
*Just the picks. One row per level where you choose something.*

| Level | Feat | Class Feature Choice | Notes |
| :--- | :--- | :--- | :--- |
| 1 | ... | ... | ... |

## Spell Selection
*For spontaneous casters: picks per spell level in the order to learn them. For prepared casters: the staples worth preparing. Mark which come free (mystery/curse/bloodline/"Additional Spells") so the player doesn't waste picks.*

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

## Fine Print
[Player-relevant residue of verification, in plain language with no file references:
- bonus-type collisions among the build's core buffs and with common gear (what supersedes what, what to sell)
- mechanics quirks that change play (action-economy notes, targeting rules)
- any assumption the build leans on that isn't documented locally — flagged as such, with its fallback if a patch changes it]
