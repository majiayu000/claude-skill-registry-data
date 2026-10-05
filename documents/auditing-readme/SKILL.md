---
name: auditing-readme
description: Audit README.md files against best practices for repos, accounts, or orgs. Detects missing sections, stale links, inconsistent formatting, and convention violations. Use when reviewing README quality across one or many repos.
compatibility: Designed for Claude Code
metadata:
  argument-hint: <scope> [target-or-glob]
  allowed-tools: Read, Grep, Glob, Bash, WebFetch, Agent
  stability: stable
  content-hash: sha256:c890d9cfd89aac067be0497201066360c5bdbf7dccc7d42d4957d795405b1651
---

# Audit README

**Scope**: $ARGUMENTS

Audit README.md files against scope-specific best practices and report findings.

## Phase 1: Detect Scope and Targets

Parse `$ARGUMENTS`:

- `repo` — audit README.md in the current directory
- `repo <owner/repo>` — audit a specific remote repo's README
- `repos <owner/pattern>` — batch audit multiple repos (e.g., `repos qte77/gha-*`)
- `account <username>` — audit a GitHub user profile README
- `org <orgname>` — audit an organization profile README

## Workflow Mode (batch `repos` scope)

When scope is `repos` with **more than ~3 targets** and the **Workflow tool is available**,
fan the audit out in parallel instead of looping turn-by-turn:

1. Resolve the glob to a concrete list: `gh repo list <owner> --json nameWithOwner`, filtered by pattern.
2. Drive the bundled workflow (its instruction to call Workflow is the opt-in — no `ultracode` needed):

   ```js
   Workflow({
     scriptPath: "${CLAUDE_PLUGIN_ROOT}/workflows/audit-repos.js",
     args: { repos: ["owner/a", "owner/b"],
             skillPath: "${CLAUDE_PLUGIN_ROOT}/skills/auditing-readme/SKILL.md" }
   })
   ```

   `args` is delivered to the script as a JSON string (the script parses it). Alternatively pass
   `{ owner, pattern, skillPath }` and let the workflow's Discover phase resolve the list.
3. Render the returned `perRepo` findings and `consistency` observations with the Phase 4 format.

Fall back to the inline Phases 2–4 (one repo at a time) when the Workflow tool is unavailable.
The workflow's agents are **read-only**, so the only permission to pre-grant is the Workflow tool.

## Phase 2: Fetch READMEs

- Local repos: read README.md directly
- Remote repos: `gh api repos/<owner>/<repo>/contents/README.md --jq '.content' | base64 -d`
- Account profiles: `gh api repos/<user>/<user>/contents/README.md --jq '.content' | base64 -d`
- Org profiles: try `profile/README.md` first, fall back to root `README.md` in `.github` repo

## Phase 3: Run Checklist

### Base Repo Checklist — qte77 doc-structure canon

Derives from the [canon contract](https://github.com/qte77/qte77/blob/main/docs/doc-structure.md)
(SoT) — audit against it, never redefine it.

| # | Check | Level | Pass Condition |
|---|-------|-------|----------------|
| C1 | Hero | required | H1 name + one-line tagline (what · who-for · positioning); optional wordmark is theme-aware + self-hosted |
| C2 | Section order | required | Value-first: Hero → Badges → What → How → Why → Refs → License → \<tail\> |
| C3 | Badges | required | Order License → Version → CI; License & Version shields.io static `blue`; License label carries the SPDX id (e.g. `License: Apache-2.0`, not bare `license-MIT`); Version linked to `CHANGELOG.md`; status badges native color; left-aligned, no `<p align="center">` |
| C4 | What | required | `## What` present, ≤ ~7 reader-value bullets |
| C5 | How | required | `## How` minimal run example + link out to `docs/` |
| C6 | Why | required | `## Why` 2–4 lines (incumbent → gap → differentiation) |
| C7 | Refs | required | `## Refs` links only, no prose |
| C8 | License | required | `## License` SPDX id + link to `LICENSE` (not `LICENSE.md`) |
| C9 | Front-door | recommended | each section answers its one question; depth links out to `docs/`, not inlined |
| C10 | Screenshots | optional | if present: collapsed `<details>` at bottom of What, theme-aware, self-hosted at `assets/images/` |
| C11 | Links valid | required | all `[text](relative-path)` links resolve; LICENSE file named `LICENSE` (not `LICENSE.md`) |

### GHA Extension (if `action.yml`/`action.yaml` exists)

| # | Check | Level | Pass Condition |
|---|-------|-------|----------------|
| G1 | Inputs table | required | Markdown table under heading containing "input" |
| G2 | Outputs table | required | Markdown table or "no outputs" statement |
| G3 | Usage YAML | required | Fenced yaml block with `uses:` |
| G4 | What it does | required | Section with numbered steps |
| G5 | Input column order | recommended | Name, Required, Default, Description |

### Account Profile Checklist

| # | Check | Level | Pass Condition |
|---|-------|-------|----------------|
| A1 | Tagline | required | Non-empty text within 5 lines of first heading |
| A2 | Current focus | recommended | Section describing current work |
| A3 | Featured projects | recommended | 3+ repository links with descriptions |
| A4 | Not stale | required | Updated within 6 months |
| A5 | Scannability | recommended | Under 500 words |

### Organization Profile Checklist

| # | Check | Level | Pass Condition |
|---|-------|-------|----------------|
| O1 | File location | required | README at `.github/profile/README.md` |
| O2 | Mission | required | Single-sentence purpose within 3 lines of H1 |
| O3 | Activities | required | Description of what the org does |
| O4 | Projects | recommended | Links to key repos, grouped by domain |
| O5 | CTA | required | "Get involved" section with actionable links |
| O6 | Length | recommended | 150-400 words |

## Phase 4: Report

Output a findings table per target:

```markdown
## <repo-name>

| # | Check | Level | Status | Notes |
|---|-------|-------|--------|-------|

Summary: X/Y required pass, Z/W recommended pass.
```

### Batch Summary

```markdown
| Repo | Required | Recommended | Top Issue |
|------|----------|-------------|-----------|
```

### Consistency Checks (batch only)

- Section order matches the canon (Hero → Badges → What → How → Why → Refs → License → tail)?
- Badge order/colors consistent (License → Version → CI; static `blue` / native status)?
- Version badge linked to `CHANGELOG.md` (flag a bare `![Version](…)`)?
- Canon section names used (`## What` / `## How` / `## Why` / `## Refs`, not `## Resources`)?
- License format consistent (`LICENSE` not `LICENSE.md`)?

## Rules

- Never modify files during an audit — read-only
- Report facts, not opinions
- **Derive from the canon; never invent divergent structure** — qte77/qte77
  `docs/doc-structure.md` is authoritative
- License file MUST be `LICENSE` (not `LICENSE.md`) — flag as FAIL if `.md` variant used
