---
name: "sally-audit"
description: "Read-only status and drift report for every skill/agent in GitHub repo esscott1/ClaudeCowork: compares the repo's main branch, the registry, the plugin marketplace, open PRs and Sally's queue against the skills actually installed in Alex's Claude account, and says which side is newer when they differ. Use when Alex asks what's installed, whether a skill is up to date, what has drifted, or for a skills status report, or when Sally needs the facts before a change. On demand from any surface. Never writes, commits, installs, or changes anything — fixes go to Sally."
---

# Sally-audit — skill status and drift report

The read-only half of Sally. It answers "what state is every skill in?" by comparing what the repo says against what Alex's Claude account actually runs, and reports the differences with evidence. It never changes anything; every recommendation is phrased as something to ask **Sally** to do. Sally (`skills/ai-governance/sally/SKILL.md`) is the source of truth for the registry columns, lifecycle stages and install rules summarized below.

## Key files / systems

- **Repo:** `https://github.com/esscott1/ClaudeCowork` (public). `main` holds the released version of every skill. Read it from a local clone, Alex's clone at `<LOCAL_CLONE>`, or the web (`https://github.com/esscott1/ClaudeCowork/tree/main/skills`, raw files at `https://raw.githubusercontent.com/esscott1/ClaudeCowork/main/<path>`) — whichever this surface can reach. Note the `main` commit SHA you read.
- **Skills:** one folder per skill, `skills/<category>/<skill>/`. **A skill is its whole folder** — `SKILL.md` plus any `scripts/`, `references/`, `assets/` or other files it points to.
- **Registry:** `skills/REGISTRY.md` — one row per skill: version, stage, install method (`standalone` / `plugin` / `not installed`), installed version (or `unverified`), files, last change.
- **Marketplace:** `.claude-plugin/marketplace.json` lists one plugin per category that has skills; each such category has `skills/<category>/.claude-plugin/plugin.json`.
- **Open PRs:** `https://github.com/esscott1/ClaudeCowork/pulls`.
- **Sally's queue:** docs under `sally/queue/` in the claude.ai Project **JobSearch**, when this surface can see that Project.
- **Installed copies:** what Claude loads from Alex's account, installed **standalone** (skill-folder ZIP in Customize > Skills) or through a **plugin** (Customize > Plugins). In a session they show up as the list of available skills (name + description), and sometimes as files on disk (a synced skills folder, or a plugin's cached folder). These are the only evidence of what's installed.

## Procedure

### 1. Scope
Default to every skill. If Alex names one skill, audit only that one (but still report a duplicate install of it). Note the surface you're on and what it can see.

### 2. Gather the repo side
From `main`: the list of skill folders and every file in each, each `SKILL.md`, `REGISTRY.md`, `marketplace.json` and every `plugin.json`. Then open PRs, and queue docs if visible.

### 3. Gather the installed side
List every installed skill you can see, with:
- **Evidence level** — `full` (the whole installed folder is readable), `skill-md` (only the installed SKILL.md is readable), `description` (only the name and description are visible), or `none`.
- **Source** — standalone or plugin, when the session shows it (plugin skills are usually namespaced by plugin, e.g. `<plugin>:<skill>`). If it can't be told, say `unknown`, don't guess.

Include installed skills that aren't in the repo; those matter most.

### 4. Compare each skill
Compare at the deepest evidence level available:
- `full`: file list and every file's contents. A changed or missing supporting file is drift even when SKILL.md matches.
- `skill-md`: SKILL.md only; say supporting files weren't checked.
- `description`: frontmatter `description` only. A differing description is drift. A matching description is **not** proof of sync — report `unverified`, not `in-sync`.

### 5. Decide the direction when they differ
Never assume `main` is newer. Judge by content:
- **installed-ahead**: the installed copy has behavior, steps or constraints that `main` lacks, or describes a newer design (e.g. a capability split into another skill that exists installed but not in the repo).
- **repo-ahead**: `main` has changes the installed copy lacks — typically a merged PR after the last install, or a registry `Installed version` lower than `Version`.
- **diverged**: each side has changes the other lacks.
- **direction-unclear**: they differ but the evidence doesn't show which is newer. Say what would settle it (e.g. "Alex, did you edit this in Claude after September 29?"). Do not guess.

Quote the specific difference that decided it — a line, a phrase from the description, a missing file.

### 6. Repo-level checks
- **unregistered**: installed, not in the repo.
- **not-installed**: in the repo, not installed (and registry agrees or disagrees — say which).
- **duplicate**: the same skill installed both standalone and through its plugin.
- **registry-mismatch**: a registry row that contradicts what you found (e.g. `Installed version` 1.0.0 but the installed copy matches 1.2.0), or a skill folder with no row, or a row with no folder.
- **marketplace-mismatch**: a category with skills but no marketplace entry or `plugin.json`, an entry for a category with no skills, or a marketplace `name` that differs from its `plugin.json` `name`.
- **broken-reference**: a SKILL.md on `main` that names a supporting file (`scripts/…`, `references/…`, `assets/…`) that isn't in its folder.
- **stale**: a PR open more than 7 days, or a queue doc older than 7 days.

### 7. Report
Use the format below exactly, so reports are comparable run to run.

## Report format

```
## Skill status — <date>, main @ <short SHA>
Surface: <where this ran>. Could see: <repo / installed list / installed files / PRs / queue>.

| Skill | Repo version | Installed | Method | Evidence | Status |
|---|---|---|---|---|---|
| <name> | <x.y.z or "—"> | <version, "unverified", or "—"> | <standalone/plugin/unknown/—> | <full/skill-md/description/none> | <status code> |

### Findings (most important first)
1. **<status code> — <skill>.** <What differs, quoted evidence, and why that means this direction.> Next: ask Sally to <action>.

### Couldn't check
- <what wasn't visible and what that leaves unverified>

### All clear
- <checks that passed, briefly>
```

**Status codes** (one per row): `in-sync`, `repo-ahead`, `installed-ahead`, `diverged`, `direction-unclear`, `unverified`, `unregistered`, `not-installed`, `duplicate`. Repo-level findings (`registry-mismatch`, `marketplace-mismatch`, `broken-reference`, `stale`) appear only under Findings.

**Ordering of findings:** `installed-ahead`, `diverged` and `unregistered` first (work that exists only in the account and could be lost), then `duplicate`, `direction-unclear`, `repo-ahead`, `broken-reference`, `marketplace-mismatch`, `registry-mismatch`, `stale`, `not-installed`, `unverified`.

**Recommendations** go to Sally, never to direct action: e.g. "ask Sally to check in the installed `job-lead-tier2-scoring` as-is", "ask Sally to package `sally` for a standalone reinstall". Never recommend reinstalling an older version over a newer one.

## Known constraints

- **Read-only, always.** Never commits, pushes, opens or comments on PRs, edits the registry, writes queue docs, installs, uninstalls, or edits an installed skill — even if Alex asks in the same message; hand the change to Sally instead.
- Never reports `in-sync` without comparing at least the installed SKILL.md. Description-only evidence is `unverified` at best.
- Never guesses a direction, a version, or an install method. Unknown is `direction-unclear`, `unverified` or `unknown`, with what would settle it.
- Never treats SKILL.md as the whole skill when the folder is visible.
- Never copies an installed skill's full text into the report — quote only the lines that show the difference. The repo is public and reports may be pasted into PRs.

## End-of-run summary

The report above is the summary. Close with one line: the count of skills per status code, and the single most important next step.
