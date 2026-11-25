---
name: broll-picker
description: "Find B-roll in the user's iCloud Photos, meaning clips and photos of places and scenes without the user or close-up people. Filter by length, place and scene labels (city, sunset, office, food), rank by Apple's aesthetic scores, keep variety across moments, review visually and download originals. Use for video edits, reels, and post backgrounds."
---

# B-roll picker

Needs `icloud-photos-bridge` set up (its `setup.sh` saves where its scripts live).
```bash
PY=$(cat ~/.config/icloud-photos/python 2>/dev/null); B=$(cat ~/.config/icloud-photos/bridge_dir 2>/dev/null)
[ -x "$PY" ] && [ -d "$B" ] || echo "icloud-photos-bridge is not set up: run its scripts/setup.sh first"
```
`scripts/pick.py` below is in this skill's own folder.

## Steps

1. **Catalog:** `$PY $B/catalog.py --out catalog.jsonl --since <date> --kind all`
2. **Rank:**
   ```bash
   $PY scripts/pick.py catalog.jsonl --owner $($PY $B/owner.py get) --kind video --top 48 \
       [--min-sec 3 --max-sec 30] [--label city --label sunset] [--place "Lisbon"]
   ```
   - Leaves out selfies, anything with the owner in it, and by default anything with faces or people labels.
     `--people small` allows small background people (street scenes).
   - At most one pick per 10 minutes (`--window-min`), so you get different scenes.
   - `--kind photo|all` for stills. Labels are Apple's scene labels; look at a few catalog lines to see the vocabulary.
3. **Look before you pick.** `$PY $B/montage.py broll_picks.json m.jpg --n 48` (videos show their poster frame).
   Drop: tilted horizons, blown-out sky, screens or documents showing private info, license plates up close,
   anything where a person ends up as the subject. Keep a mix: wide establishing shots, details, motion.
4. **Show the user** `$PY $B/sheet.py final.json broll.html --title "B-roll"` with duration and labels per item.
5. **Download originals:** `$PY $B/fetch.py ./broll-<date> --from uuids.txt`. Videos can be large; check free disk first.
