# Agent Rules & Source Map

Repo-wide rules for agents working in this WotR knowledge base. The build-guide template lives in `builds/_template.md`.

**Data baseline:** Game version: 2.7.0 (final content DLC: A Dance of Masks, June 2024; last hotfix 2.7.0x, Sept 2025). Data scraped June 2026 from GameFAQs guide 80843.

Read README.md for the file manifest. All content is US English, matching in-game naming.

## Agent rules

- Verify BEFORE writing: grep every class feature, feat, revelation, spell, and mythic ability against the local files (see Source Map below) before it appears in a guide.
- The human-readable section of a build guide must never contain file references, "✓" prereq notes, or "Verified" labels — that's appendix material (see `builds/_template.md`).
- Prereqs are still *checked*, just reported in the appendix table only.
- If something can't be found locally, retry with close name variants (rare upstream typos are annotated in place); follow `_See X spell list_` pointers one hop. If still missing, flag it in the appendix under **Unverified** — never invent.
- Oracle/Sorcerer-style spontaneous casters MUST get an explicit spells-known plan — picks per spell level, respecting the class's spells-known table.
- **Ask before assuming party context.** If a build choice's value depends on something only the user knows, ask BEFORE writing (use the AskUserQuestion tool if available; otherwise ask in plain text). Batch the questions, offer concrete options with a recommended default, and only ask when the answer would change a pick. Triggers:
  - **Capstone/feature nullified by a companion** — e.g. a Skald sharing Beast Totem pounce makes Battle Oracle's Final Revelation redundant
  - **Teamwork feats** — who is the partner? If none, swap the feat
  - **Role overlap** — is healing/buffing/tanking already covered by the party?
  - **Solo vs party / difficulty / mod context** if the user hasn't said
  Record the answers in the **Party Fit** row of At a Glance, and design around them. If the user can't be asked, state the assumption explicitly there instead — never silently depend on it.

## Source Map (local verification hub)

All extracted from the [GameFAQs WotR Guide (80843)](https://gamefaqs.gamespot.com/ps4/324475-pathfinder-wrath-of-the-righteous/faqs/80843).

| Domain | Location | Notes |
| :--- | :--- | :--- |
| Classes & archetypes | `classes/<class>.md` (26 base classes) | features by level, archetype trade-aways |
| Prestige classes | `classes/prestige/<name>.md` | one file per prestige class |
| Archetype index | `classes/INDEX.md` | archetype line-number index |
| Feats | `feats/*.md` (12 category files) | `grep -ri "<name>" feats/` |
| Spells | `spells/<class>/<class>-l<level>.md` | alchemist, bard, bloodrager, cleric, druid, hunter, inquisitor, magus, paladin, ranger, shaman, warpriest, witch, wizard/sorcerer |
| Spell aliases | `spells/sorcerer/`, `spells/oracle/` | sorcerer → wizard list; oracle → cleric list |
| Cross-refs | `_See X spell list._` entries | full text one hop away; annotated variants: `_See X spell list ("Actual Name")._` |
| Mythic | `mythic/*.md` | mythic-paths.md = ranks/abilities/feats; one file per path |
| Races, backgrounds, attributes & skills, companions/familiars, domains, bloodlines | `chargen/{races,backgrounds,attributes-skills,companions-familiars,domains,bloodlines}.md` | replaces character-creation.md |
| Build-craft, stacking exploits, sample builds | `building/{prereqs,exploits,sample-builds}.md` | replaces character-building.md; exploits.md = stacking rules |
| Items | `items/{weapons,armor-shields,accessories,artifacts-relics,boosts-and-misc}.md` + `items/items-inevitable-excess.md`, `items/items-lord-of-nothing.md` | replaces items/items.md; unique weapons/armor live in weapons.md / armor-shields.md |
| Build template | `builds/_template.md` | build-guide structure + verification appendix skeleton |

**Known source quirks:** the source guide used British spellings — all content was converted to US English (2026-06-09) to match in-game naming (incl. the "Swatooth Saber" typo → Sawtooth Saber); remaining guide typos are annotated in place; Reviving Finale (bard 3) had no description upstream — local copy completed from the WotR wiki (2026-06-09); Nature's Exile / Thirsting Entanglement flagged as upstream omissions.
