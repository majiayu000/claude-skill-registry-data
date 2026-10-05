---
name: blog-flow
description: FLOW framework integration for bloggers. Evidence-led content workflow using the Find, Optimize, Win loop with stage-specific AI prompts from the FLOW knowledge base (30 blog-applicable prompts, CC BY 4.0). Use when user says "FLOW", "FLOW framework", "blog flow", "evidence-led blogging", "find optimize win", or wants stage-specific blog prompts.
user_invocable: true
argument-hint: "[stage] [url|topic]"
license: MIT
compatibility: Requires Claude Code. Prompts are vendored — no runtime fetch.
metadata:
  author: AgriciDaniel
  version: "1.9.1"
  category: blog
---

# FLOW Framework for Bloggers (Find, Optimize, Win)

> Framework and prompts (c) Daniel Agrici, CC BY 4.0. Source: github.com/AgriciDaniel/flow

FLOW is an evidence-led operating model built for the AI-search era. Claude Blog
integrates the FLOW prompt library so writers can drive their workflow with
structured, source-backed AI prompts instead of improvised queries.

This skill exposes the three blog-relevant stages (Find, Optimize, Win) and keeps
the single Leverage prompt available through the prompts index. The local-SEO
prompts (GBP, citations, local audits) are intentionally excluded because they
target brick-and-mortar work, not blogs.

**Runtime context.** Load `references/flow-framework.md` on every `/blog flow`
activation. Load prompt files on demand only, scoped to the stage the user
requests.

---

## Commands

| Command | What it does |
|---------|-------------|
| `/blog flow` | Show FLOW overview and stage menu |
| `/blog flow find [topic\|url]` | Find-stage: keyword discovery, intent mapping, gap analysis (5 prompts) |
| `/blog flow optimize [url]` | Optimize-stage: select 2 to 3 most relevant prompts of 21 based on context |
| `/blog flow win [url]` | Win-stage: BOFU, conversion, dual-surface scorecard (3 prompts) |
| `/blog flow prompts` | Full index of all 30 blog-applicable prompts (Find, Leverage, Optimize, Win) |
| `/blog flow sync` | Report vendor state and verify the lockfile — automatic sync is not implemented |

The single Leverage prompt (off-site authority) is reachable through
`/blog flow prompts` and is not promoted to a top-level command, since most
blog workflows route off-site work elsewhere.

---

## Orchestration Logic

### On `/blog flow` (no sub-command)
1. Read `references/flow-framework.md`.
2. Show the FLOW stage overview with a one-line description of each stage.
3. Ask the user which stage matches their current situation.

### On `/blog flow find [topic|url]`
1. Read all files in `references/prompts/find/`.
2. Apply each prompt to the topic or URL, capturing demand and intent signals.
3. Cross-reference: "For deeper briefs and outlines, see `/blog brief <topic>`,
   `/blog outline <topic>`, and `/blog cannibalization` to detect overlap with
   existing posts."

### On `/blog flow optimize [url]`
1. Read the file names in `references/prompts/optimize/`.
2. Read prior context (target URL, niche, any prior skill output in this
   conversation, scoring deltas from `/blog analyze`).
3. Select 2 to 3 most relevant prompts, then load only those files.
4. Apply the selected prompts; note that the rest are accessible via
   `/blog flow prompts`.
5. Cross-reference: "For deeper rewrites and validation, see `/blog rewrite
   <file>`, `/blog seo-check <file>`, `/blog geo <file>`, `/blog schema <file>`,
   and `/blog factcheck <file>`."

### On `/blog flow win [url]`
1. Read all files in `references/prompts/win/`.
2. Apply each prompt to the URL's conversion and BOFU context.
3. Cross-reference: "For repurposing, full-site health, and quality scoring,
   see `/blog repurpose <file>`, `/blog audit`, and `/blog analyze <file>`."

### On `/blog flow prompts`
1. Read `references/prompts/README.md`.
2. Display the full index: 30 prompts grouped by stage (Find, Leverage,
   Optimize, Win) with name and trigger conditions.
3. State that local-SEO prompts are excluded by design; point users to
   `claude-seo` (`/seo flow local`) if they need them.

### On `/blog flow sync`
1. Tell the user that automatic sync is **not implemented**. Do not attempt to
   run a sync script — none ships with Clade, and inventing one on the spot
   would fetch third-party content into their tree without their say-so.
2. Report what is actually on disk: the prompts under `references/prompts/`
   are vendored at the state recorded in `references/flow-prompts.lock`.
3. Verify the vendored copy has not drifted, and show the result:
   From the skills root (`~/.claude/` in an install, `configs/` in the repo): `sha256sum -c --quiet skills/blog-flow/references/flow-prompts.lock` — the manifest's paths are rooted there, not at `references/`.
4. To update, point them at the upstream repo
   (github.com/AgriciDaniel/flow) to review changes and re-vendor deliberately.
5. Show the attribution notice.

---

## Context Matching (Optimize stage)

The optimize stage has 21 prompts. Dumping all 21 is noise. Select by priority:

1. **Niche** (SaaS or B2B blog leans on-page plus technical; lifestyle leans
   freshness plus E-E-A-T; publisher leans authority plus citations).
2. **Prior skill output** (`/blog analyze` E-E-A-T gap routes to authority
   prompts; `/blog seo-check` failures route to on-page prompts; `/blog geo`
   gaps route to extraction-format prompts).
3. **URL signals** (commercial pages need conversion prompts; informational
   posts need freshness plus answer-first prompts).

Always surface exactly 2 to 3 prompts. State which prompts you chose and why.

---

## Reference Files

Load on demand. Do NOT load all at startup.

- `references/flow-framework.md`. FLOW operating model. Load on every `/blog
  flow` activation.
- `references/bibliography.md`. Evidence sources. Load when citing studies or
  statistics.
- `references/prompts/README.md`. Prompt index. Load for `/blog flow prompts`.
- `references/prompts/find/`. 5 prompts. Load for `/blog flow find`.
- `references/prompts/leverage/`. 1 prompt. Load only when surfaced through
  `/blog flow prompts`.
- `references/prompts/optimize/`. 21 prompts. Load selectively for `/blog flow
  optimize`.
- `references/prompts/win/`. 3 prompts. Load for `/blog flow win`.

If `references/` is missing, the install is incomplete — tell the user to run
`./install.sh` again. Do not point at `/blog flow sync`; it fetches nothing.

---

## Provenance and updates

The prompts under `references/prompts/` are **vendored**, not fetched. They come
from github.com/AgriciDaniel/flow and are pinned by
`references/flow-prompts.lock`, a sha256sum-compatible manifest. Check for local
drift with:

```bash
cd ~/.claude   # or configs/ in the repo checkout
sha256sum -c --quiet skills/blog-flow/references/flow-prompts.lock
```

There is no sync script, and there should not be one. Earlier revisions of this
document described `scripts/sync_flow.py` in enough detail to look shipped — it
never existed in this repository, so step 1 of `/blog flow sync` failed on a
missing file.

Building it was measured rather than argued (2026-08-17, GitHub API): upstream
has **8 commits total**, all on 2026-04-25/26, and **not one of them touched a
prompt file** after the initial release. The prompt content has been frozen since
publication. A fetch-on-demand mechanism — with its token handling, rate limits,
path-traversal guards and lockfile refresh — would exist to track a corpus that
has never changed, while adding the one thing this skill has no business
deciding: whether third-party content may be written into a user's tree
unreviewed. Re-run that check before reopening the question.

Updating is therefore a deliberate act: review the upstream diff, re-vendor,
regenerate the lockfile.

Only the blog-applicable stages (`find`, `leverage`, `optimize`, `win`) are
vendored. The `local` stage is intentionally absent — it targets brick-and-mortar
work, so it stays with `claude-seo` (`/seo flow local`).

---

## Attribution

Every `/blog flow` activation (any sub-command) outputs before analysis:

```
Framework and prompts (c) Daniel Agrici, CC BY 4.0. Source: github.com/AgriciDaniel/flow
```

Do not omit or modify the attribution. Synced files also carry an HTML comment
license header injected by the sync script.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| `references/flow-framework.md` missing | The vendored reference is gone from the install. Reinstall Clade (`./install.sh`) rather than fetching it — say so plainly instead of pointing at a sync that does not exist. |
| Prompt file missing | Same: the vendored copy is incomplete. Reinstall, then re-check `sha256sum -c --quiet skills/blog-flow/references/flow-prompts.lock` from the skills root. |
| `sha256sum -c` reports a mismatch | A vendored prompt was edited locally. Name the files it listed; do not overwrite them without asking — the edit may be intentional. |
| User asks to auto-sync from upstream | Not implemented, by omission rather than oversight — see *Provenance and updates*. Offer to show the upstream diff instead. |
