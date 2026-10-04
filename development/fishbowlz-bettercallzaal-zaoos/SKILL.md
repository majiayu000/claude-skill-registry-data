---
name: fishbowlz
description: FISHBOWLZ is a standalone product — it no longer lives in ZAOOS. Development and deployment happen in the bettercallzaal/fishbowlz repo, deployed at fishbowlz.com. Use this skill when asked to work on FISHBOWLZ; it points you at the right repo and explains why the code is not in ZAOOS.
---

# FISHBOWLZ — Standalone Product

**FISHBOWLZ graduated out of ZAOOS.** As of 2026-06 the FISHBOWLZ code was removed
from this monorepo (decommissioned-from-lab per `research/agents/601-agent-stack-cleanup-decision/`
and the "graduate → own repo, delete from ZAOOS" pattern in CLAUDE.md). It now
stands alone:

- **Repo:** `github.com/bettercallzaal/fishbowlz` (canonical — build here)
- **Site:** https://fishbowlz.com
- **DB:** its own Supabase project + `fishbowl_*` tables (no longer shared with ZAOOS)

## How to work on FISHBOWLZ

Do **not** rebuild FISHBOWLZ inside ZAOOS. There is no `src/app/fishbowlz/`,
`src/app/api/fishbowlz/`, `src/components/fishbowlz/`, or `src/lib/fishbowlz/`
here anymore, and there is no sync-from-ZAOOS workflow. Instead:

```bash
git clone https://github.com/bettercallzaal/fishbowlz
cd fishbowlz
npm install
npm run dev
```

The standalone repo stands alone (clone, no deps) — that is the ZAO sharing
model for graduates. Open the feature there, ship there; Vercel deploys to
fishbowlz.com on push to `main`.

## If someone asks to add FISHBOWLZ back to ZAOOS

Don't, without an explicit decision from Zaal that reverses the graduation. The
"no new bots / no re-adding decommissioned surfaces without a doc" rule in
CLAUDE.md applies. Point them at this skill and the standalone repo first.
