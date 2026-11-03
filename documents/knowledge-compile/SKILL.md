---
name: knowledge-compile
description: "Refreshes the repo-native compiled knowledge layer in knowledge/. Reads new research reports, transcripts, backbone docs, voice-corpus entries, and skill learnings, then updates short source-linked markdown pages used for ideation, scripting, and research synthesis. Triggers: update knowledge, compile knowledge, refresh repo memory, update the wiki, knowledge layer."
---

> **Video Studio:** this skill lives in `engines/content-os` (Content OS, inside this repo). Before running anything from it, `cd engines/content-os` and use that folder's copy (`.claude/skills/knowledge-compile/`), which has its scripts and reference files. Every path below is relative to that folder. This copy only lets Claude find the skill from the Video Studio folder.


# Knowledge Compile

Maintains the repo's lightweight compiled knowledge layer (plain markdown).

The goal is not to create another vault. The goal is to stop re-reading 100k+ words of scattered transcripts, reports, and playbooks every time the creator asks for strategy, ideas, or scripts.

## Folder Contract

```
knowledge/
├── index.md
├── current-content-opportunities.md
├── winning-hooks.md
├── competitor-patterns.md
├── creator-ai-positioning.md
└── reusable-script-formats.md
```

## Source Hierarchy

Authoritative sources, in priority order. This is the one canonical list; the refresh step below scans exactly these paths.

1. `backbone/` (offer, ICP, messaging, vision: the offer name, price, and proof numbers live here and are never hardcoded into `knowledge/`)
2. `voice-dna.md`
3. `voice-corpus/`
4. `research/`
5. `transcripts/{url,local,analysis}/`
6. `CLAUDE.md` Lab Notes / Gotchas section
7. `.claude/skills/*/SKILL.md`

Compiled outputs:

- `knowledge/`

Never treat `knowledge/` as the source of truth. It is a fast navigation and synthesis layer.

## When To Run

- After a new research report lands.
- After transcribing a high-signal competitor/video.
- After a major offer, positioning, or pipeline change.
- Before a big ideation block if the latest research is not reflected in `knowledge/`.

## Refresh Workflow

1. Read `knowledge/index.md`.
2. Check the newest files in every path from the Source Hierarchy: `backbone/`, `voice-dna.md`, `voice-corpus/`, `research/`, `transcripts/{url,local,analysis}/`, `CLAUDE.md` Lab Notes / Gotchas section, `.claude/skills/*/SKILL.md`. Research reports are self-contained HTML with embedded media (5-8 MB each), so never `Read` a raw `research/*.html`. List, then extract text (the one-liners below resolve the Python binary once, so they run as-is on macOS, Linux, and Windows Git Bash):
   ```bash
   ls -t research/ | head
   PY=$(command -v python3 || command -v python)
   "$PY" -c '
   import re,sys,html
   s=open(sys.argv[1],encoding="utf-8",errors="ignore").read()
   s=re.sub(r"data:[^\"'"'"')\s]+","",s)                       # drop data: URIs (embedded media)
   s=re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>","",s)
   s=re.sub(r"(?s)<[^>]+>"," ",s)
   s=re.sub(r"[ \t]+"," ",html.unescape(s)); s=re.sub(r"\n\s*\n+","\n",s)
   print(s[:int(sys.argv[2])])
   ' research/<report>.html 12000
   ```
   That turns an 8 MB report into about 30 KB of text; the summary + ranking sit at the top, so a 12k-char slice is usually enough.
3. Compare the latest source dates against each knowledge page's `last_updated`. Print the staleness warning first, so the gap is visible even if you only refresh one page:
   ```bash
   PY=$(command -v python3 || command -v python)
   "$PY" -c '
   import os,re,glob,datetime as d
   new=d.date.fromtimestamp(max(os.path.getmtime(p) for p in glob.glob("research/*.html")+glob.glob("backbone/*.md")))
   for p in sorted(glob.glob("knowledge/*.md")):
       m=re.search(r"last_updated:\s*(\d{4}-\d{2}-\d{2})",open(p,encoding="utf-8").read())
       lag=(new-d.date.fromisoformat(m.group(1))).days if m else "?"
       print(f"{p}: {lag} days behind newest source ({new}); run knowledge-compile" if lag!=0 else f"{p}: current")
   '
   ```
4. Update only pages affected by new signal.
5. Keep each page short. It should be faster to read than the raw source.
6. Include local source paths in frontmatter and inline where useful.
7. Do not add claims, numbers, or dates without a source path.
8. Before saving a page, confirm every path in its `sources:` frontmatter exists (`ls` each one). A missing path means re-source the claim to an existing `research/*.html` (or other live source) or drop the claim. Never leave a dangling source:
   ```bash
   PY=$(command -v python3 || command -v python)
   "$PY" -c '
   import re,glob,os
   for p in sorted(glob.glob("knowledge/*.md")):
       fm=open(p,encoding="utf-8").read().split("---")[1]
       for s in re.findall(r"^\s*-\s*(\S+)",fm,re.M):
           if not os.path.exists(s): print(f"MISSING {p}: {s}")
   '
   ```
9. Retired-tier sweep. Retired or excluded offer names must not leak into compiled pages; the live offer is whatever `backbone/offer.md` names (price per the same file). Build the grep pattern from the names listed under "What is NOT sold" in `backbone/offer.md` (or whatever that file marks as dead/retired); if it says "none", skip this step. Before saving, the sweep must return nothing:
   ```bash
   # pattern = the "What is NOT sold" names from backbone/offer.md, pipe-separated
   # e.g. a retired mastermind + a retired done-for-you tier -> 'Inner Circle|DFY Install'
   grep -rn -E '<name1>|<name2>' knowledge/
   ```
   Keep the pattern to the specific names. Do not widen it to bare `apply` or `install`, or to generic words a name might contain (a tier called "Standard" would match "standard format"): those false-positive constantly.

## Page Roles

- `current-content-opportunities.md`: latest actionable content angles.
- `winning-hooks.md`: reusable hook mechanics.
- `competitor-patterns.md`: what competitors are doing that keeps working.
- `creator-ai-positioning.md`: positioning page. The current market lane, offer, voice, and belief shifts, whatever the lane is this generation (compile it from `backbone/`, not from the filename). The filename is fixed because `scriptwriter` reads it by that name; do not rename it when the lane changes.
- `reusable-script-formats.md`: script shapes for the scripting step.

## Usage Rules For Other Skills

Ideation should read `knowledge/index.md` and `knowledge/current-content-opportunities.md` before opening raw reports.

Scripting should read `knowledge/creator-ai-positioning.md`, `knowledge/winning-hooks.md`, and `knowledge/reusable-script-formats.md` before opening full transcripts or long playbooks.

`hook-generator` reads `knowledge/winning-hooks.md` for proven shapes; keep that page's mechanics section stable and source-linked.

(`scriptwriter` follows this reading order, plus few-shot pulls from `voice-corpus/`. Ideation deliberately has no skill — it's the creator's job, done by hand in chat; this reading order applies to that step, or to any ideation skill if one is ever built.)

Research skills should continue writing raw reports to `research/`. They should not write directly into `knowledge/` unless explicitly running this skill afterward.
