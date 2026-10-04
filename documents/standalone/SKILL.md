---
name: coc7-keeper-lite
description: "CoC 7e Keeper standalone — no pip install needed. File-based persistence, zero dependencies."
---

# CoC 7e Keeper (Standalone)

Standalone mode uses **Python stdlib only** (`tools/portable.py`) + plain Markdown files.
No `sagasmith-coc` runtime required.

## Quick Start

```powershell
python portable.py doctor
python portable.py campaign start --name "Arkham"
python portable.py character create --campaign <id> --name "Herbert" --sheet '{"str":50}'
python portable.py module ingest --campaign <id> --path "scenario.md" --title "Lightless Beacon"
python portable.py module current --campaign <id> --scope party
python portable.py roll d100 --score 65
```

Data lives in `~/.sagasmith/`. Create a campaign first.

## Keeper Turn

1. Resolve scope (`party`/`group:<id>`/`player:<id>`). Run `module current`.
2. Read that scope's scene and player-visible discoveries.
3. Clarify investigator intent.
4. Retrieve a reference when uncertain.
5. Roll d100 openly and resolve the success level.
6. Apply SAN, combat, or chase mechanics.
7. Narrate consequences without revealing hidden info.
8. Merge clues, handouts, and triggers into progress.
9. Record durable clues, events, and saves.

Before play read `skills/coc7-keeper/references/KEEPER_RULES.md`. Load
`skills/coc7-keeper/references/SCENARIO_INDEX.md` for scenario validation.

## Commands

### Campaign

```powershell
python portable.py campaign start --name "Arkham"
python portable.py campaign list
python portable.py campaign get --campaign <id>
```

### Characters

```powershell
python portable.py character create --campaign <id> --name "Herbert West" --sheet '{"str":50,"con":60,"siz":65,"dex":55,"int":80,"pow":70,"edu":75}'
python portable.py character list --campaign <id>
python portable.py character get --campaign <id> --name "Herbert West"
```

### Scenarios

```powershell
python portable.py module ingest --campaign <id> --path "scenario.md" --title "Scenario"
python portable.py module index --campaign <id>
python portable.py module current --campaign <id> --scope party
python portable.py module read-scene --campaign <id> --scene <id>
python portable.py module search --campaign <id> --query "<situation>" --limit 5
python portable.py module set-progress --campaign <id> --scope party --scene <id> --progress 50 --state '{"discovered_clues":["letter"]}'
```

Import Markdown only. Convert PDF first.

### Dice (d100)

```powershell
python portable.py roll d100 --score 65
# → {"roll": 39, "score": 65, "level": "regular", "success": true}
# Levels: critical (01) > extreme (≤score/5) > hard (≤score/2) > regular (≤score) > failure

python portable.py roll dice --expression "1D6"
```

### Events & Memory

```powershell
python portable.py event add --campaign <id> --type clue --summary "Found torn letter"
python portable.py memory add --campaign <id> --type clue --subject "Letter" --content "Mentions the church"
python portable.py memory search --campaign <id> --query "letter"
```

### Save / Restore

```powershell
python portable.py save create --campaign <id> --label "Before the ritual"
python portable.py save list --campaign <id>
python portable.py save restore --campaign <id> --slot 3
```

## Reference Docs

- `skills/coc7-keeper/references/KEEPER_RULES.md`
- `skills/coc7-keeper/references/SCENARIO_INDEX.md`
- `skills/coc7-keeper/references/INVESTIGATOR_CREATION.md`
- `skills/coc7-keeper/references/KEEPER_TEMPLATES.md`
- `skills/coc7-keeper/references/COMBAT_CHASE.md`
- `skills/coc7-keeper/references/SANITY.md`
- `skills/coc7-keeper/references/INVESTIGATION.md`

## Data Location

```
~/.sagasmith/
  campaigns.json                  # campaign index
  <campaign_id>/
    campaign.json                 # metadata
    characters/<name>.json        # investigator sheets
    modules/<source_key>.md       # imported scenarios
    progress.json                 # scoped scene progress
    events.jsonl                  # event log
    memories.jsonl                # campaign memory
    saves/<slot>/                 # snapshot copies
```

## Limitations

- No PDF import — convert to Markdown first
- No commercial rulebook search
- No SQL FTS5 — lexical scoring with CJK query expansion
- No ChromaDB vector search
- No built-in SAN loss or combat melee — roll d100 and apply rules manually
