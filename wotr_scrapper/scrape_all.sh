#!/bin/zsh
# Scrape WotR guide pages via Safari and convert to markdown.
set -u
cd "$(dirname "$0")"
BASE="https://gamefaqs.gamespot.com/ps4/324475-pathfinder-wrath-of-the-righteous/faqs/80843"

scrape() {  # scrape <slug> <outfile>
  local slug=$1 out=$2
  osascript -e "tell application \"Safari\" to set URL of document 1 to \"$BASE/$slug\"" || return 1
  sleep 10
  osascript -e 'tell application "Safari" to get source of document 1' > "$slug.html"
  # retry once if capture looks like a challenge page (tiny)
  if [ "$(wc -c < "$slug.html")" -lt 60000 ]; then
    sleep 8
    osascript -e 'tell application "Safari" to get source of document 1' > "$slug.html"
  fi
  python3 extract_page.py "$slug.html" "$out" && rm "$slug.html"
}

mkdir -p ../classes ../mythic ../items

CLASSES=(alchemist arcanist barbarian bard bloodrager cavalier cleric druid hunter inquisitor kineticist magus monk oracle paladin ranger rogue shaman shifter skald slayer sorcerer warpriest witch wizard prestige-classes)
for c in $CLASSES; do scrape "$c" "../classes/$c.md"; done
# fighter already done

MYTHIC=(mythic-paths aeon angel azata demon gold-dragon lich trickster other-mythic-paths appendix-ascension)
for m in $MYTHIC; do scrape "$m" "../mythic/$m.md"; done

scrape character-creation ../character-creation.md
scrape character-building ../character-building.md

ITEMS=(items items-inevitable-excess items-lord-of-nothing)
for i in $ITEMS; do scrape "$i" "../items/$i.md"; done

echo ALL DONE

# A Dance of Masks DLC (missing from repo — run on macOS host):
#   scrape a-dance-of-masks ../items/items-dance-of-masks.md
# NOTE: sub-page slugs should be checked on the guide's TOC at
# gamefaqs.gamespot.com/ps4/324475-pathfinder-wrath-of-the-righteous/faqs/80843
# before running — the slug above is a guess until verified there.
