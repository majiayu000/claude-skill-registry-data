---
name: example-portal
description: "TEMPLATE — a CareerForge example job-portal adapter (ADR-0004). Copy this directory to add structured search for a real job board. Not auto-loaded by Claude Code."
---

# Example Portal Adapter — TEMPLATE (copy me)

> ⚠️ **This is a template, not a working portal.** Its `cli/` returns clearly-labelled
> **example** data so you can run it end-to-end and see the contract. To add a real
> portal, **copy this whole directory** to `.agents/skills/<portal-name>/` and implement
> real fetching in `cli/index.ts`.

## Why `.agents/skills/` and not `.claude/skills/`?

Per **ADR-0004**, structured portal adapters are a **Plane-2** extension: each portal is a
self-contained CLI tool that the country-agnostic [`job-scraper`](../../../.claude/skills/job-scraper/SKILL.md)
skill calls out to, with web search (`site:<portal>`) as the universal fallback. They live
under `.agents/skills/` deliberately — that path is **not** the Claude Code skill
auto-load directory (`.claude/skills/`), so an adapter is invoked as a CLI (via `bun run`),
never silently activated as a chat skill. This keeps the core framework clean and lets any
market contribute an adapter without changing core code.

## Directory contract (ADR-0004)

```
.agents/skills/<portal-name>/
├── SKILL.md           # this file — trigger keywords + contract
├── cli/
│   ├── package.json   # dependencies + start script (Bun/TypeScript)
│   └── index.ts       # CLI entry point implementing the contract below
└── url-reference.md   # optional — the portal's search-URL patterns
```

## CLI contract

| | |
|---|---|
| **Runtime** | Bun (TypeScript). `node`/`npx tsx` also work for this template. |
| **Input** | CLI flags: `--keywords "<terms>"`, `--location "<place>"`, `--date-range <days>` |
| **Output** | A JSON array on stdout, one object per posting: `{ title, company, location, url, date, snippet }` |
| **Exit code** | `0` on success (even with zero results — emit `[]`), `1` on error (message on stderr) |

The `job-scraper` skill runs the adapter like:

```bash
bun run .agents/skills/<portal-name>/cli/index.ts \
  --keywords "data engineer" --location "Remote" --date-range 14
```

…then parses the JSON array, dedupes against `seen_jobs.json`, quick-rates fit, and
presents results exactly as it does for web-search hits.

## How to add a real portal

1. Copy this directory to `.agents/skills/<portal-name>/`.
2. In `cli/index.ts`, replace the example data with a real fetch (the portal's public
   search/API, or HTML parsing) that honours the input/output/exit-code contract.
3. Record the portal's search-URL patterns in `url-reference.md`.
4. Add the portal to your `search-queries.md` so `job-scraper` knows to use it.
5. **No core change is required** — that is the whole point of ADR-0004.

## Constraints

- **No fabrication (ARCH-0007):** a real adapter must return only postings it actually
  found, with real URLs. This template clearly labels its output as example data.
- Keep dependencies minimal; each adapter installs independently (`bun install`).
