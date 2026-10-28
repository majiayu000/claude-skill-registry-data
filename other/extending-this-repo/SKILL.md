---
name: extending-this-repo
description: Add a new lead source, enrichment step, or output format to this repo, following its existing conventions. Use when the user wants to scrape a site this repo doesn't cover, add a step to the pipeline, or asks how to extend or customize the system.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# Extending This Repo

## Goal
Add a new source or step without breaking the ones that work.

## The shape everything follows

Every script in `scripts/` is the same shape, and a new one should be too:

```python
#!/usr/bin/env python3
"""What this does, and one runnable example."""
import os, sys, argparse

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", ".."))
from scripts.lib.env import load_env, require      # NEVER bare load_dotenv()
from scripts.lib.windows_compat import fix_encoding
from scripts.lib.output import read_any, write_csv, write_json

fix_encoding()
load_env()
```

Then: argparse with `--input` / `--output` / `--out-csv`, do the work, write both formats, print the next command.

## Non-negotiables

1. **`load_env()`, never bare `load_dotenv()`.** The bare version walks up the directory tree and will silently pick up a `.env` from a parent folder. Works locally, fails for everyone else. `scripts/lib/env.py` explains it.
2. **CSV output, always.** Google Sheets stays behind an explicit `--sheet-url`.
3. **Write through `scripts/lib/output.py`** so the Windows/Excel encoding is handled once.
4. **Checkpoint anything that loops over leads** — `scripts/lib/checkpoint.py`. Runs get interrupted.
5. **Print a cost estimate before spending money.** Then print what was actually spent.
6. **Cap the loops.** Anything agentic gets a `--max-tool-calls`-style ceiling.

## The canonical lead shape
Emit these keys so downstream steps read your source without special-casing:

`first_name`, `last_name`, `name`, `job_title`, `company`, `company_website`, `email`, `phone`, `linkedin`, `location`, `_source`

Missing fields should be `""`, not absent.

## Adding a new Apify actor

Check the store before writing anything — this repo replaced two of the course's actors because better ones exist now:

```bash
curl -s -H "Authorization: Bearer $APIFY_API_TOKEN" \
  "https://api.apify.com/v2/store?search=YOUR+TERM&limit=10&sortBy=popularity" \
  | python -X utf8 -c "import json,sys; [print(f\"{a['username']}/{a['name']:<44} {a.get('actorReviewRating') or 0:.2f}\") for a in json.load(sys.stdin)['data']['items']]"
```

Rate below ~4.0 usually means stale data or breakage. Check `modifiedAt` too — an actor untouched for a year is a liability.

Then read its input schema:
```bash
curl -s -H "Authorization: Bearer $APIFY_API_TOKEN" "https://api.apify.com/v2/acts/USERNAME~NAME"
```

## Adding a skill
Copy an existing `.claude/skills/*/SKILL.md`. The `description` line is what Claude Code matches against user intent — write it as the situations it applies to, not as a summary of the file.

Then verify: open Claude Code in the repo and phrase a request the way a user would. If your skill doesn't trigger, rewrite the description.
