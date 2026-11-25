---
name: selfie-picker
description: "Pick the user's nicest selfies from their iCloud Photos. Ranks by Apple's own aesthetic and face scores (sharp, well framed, good light, eyes open, smile), keeps one shot per moment, then a visual pass picks the final set and downloads originals. Use for 'find good selfies of me', profile/post/thumbnail photos, or a photo dump."
---

# Selfie picker

Needs `icloud-photos-bridge` set up (its `setup.sh` saves where its scripts live), with the owner saved
(`$PY $B/owner.py set`).
```bash
PY=$(cat ~/.config/icloud-photos/python 2>/dev/null); B=$(cat ~/.config/icloud-photos/bridge_dir 2>/dev/null)
[ -x "$PY" ] && [ -d "$B" ] || echo "icloud-photos-bridge is not set up: run its scripts/setup.sh first"
```
`scripts/pick.py` below is in this skill's own folder.

## Steps

1. **Catalog the period** the user cares about (default: last 60 days):
   `$PY $B/catalog.py --out catalog.jsonl --since <date> --kind photo`
2. **Rank:**
   `$PY scripts/pick.py catalog.jsonl --owner $($PY $B/owner.py get) --top 48`
   - Keeps photos where the owner is the main face, front camera or Photos' Selfies album.
   - `--allow-others 1` lets one other person in; `--include-portraits` adds photos others took of the owner.
   - One shot per 10 minutes by default (`--burst-seconds`), so the list is varied rather than 20 takes of one moment.
3. **Look before you pick.** `$PY $B/montage.py selfie_picks.json m.jpg --n 48`, read it, and choose the final
   set (default 12). Drop:
   - eyes half closed, motion blur, odd angles from below, heavy shadows on the face
   - anything stuck on the face or a stray object in front of it (a patch, a straw, a hand covering it)
   - near-duplicates of a shot already chosen, other people's faces up close, private screens or documents
   Prefer: natural smile, eye contact, soft light, a background that says where they are (city, office, nature).
4. **Show the user** the HTML sheet of the final set: `$PY $B/sheet.py final.json final.html --title "Best selfies"`.
5. **Download originals** of the ones they keep: `$PY $B/fetch.py ./selfies-<date> --from uuids.txt`.

Say how many photos were looked at and the date range. Never post or share anything; hand over the files.
