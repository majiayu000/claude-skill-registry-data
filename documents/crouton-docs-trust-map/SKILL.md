---
name: crouton-docs-trust-map
layer: stack
description: Which docs in nuxt-crouton to trust and how to resolve contradictions between them. Use when two docs disagree, when a doc's claim doesn't match the code ("the README says packages/nuxt-crouton but that dir doesn't exist"), when deciding whether a guide/writeup is authoritative before following it, or when asked "is this doc current", "which doc wins", "why does CLAUDE.md say X but the code says Y". Also the reference for the supersession-banner practice.
---

# crouton-docs-trust-map

One-line purpose: the trust order that resolves conflicts between this repo's documents, and the hygiene patterns for handling a doc caught lying.

## When to use / when NOT to use

| Situation | Use |
|---|---|
| Two docs disagree; a doc contradicts code; "is this guide current?" | **This skill** |
| Mechanically updating docs after a code change (pre-commit) | `sync-docs` skill |
| Auditing a package's doc completeness / drift detection | `audit` skill |
| A config file (routing.json, digests.yml, settings.json…) drifted or is a silent no-op | `crouton-config-registry` skill |
| Why a rule exists / the incident behind it | `crouton-failure-archaeology` skill |
| Whether a *test/CI* claim in the docs is real | `crouton-validation-reality` skill |

This skill carries the *trust order and conflict-resolution rules* only. Doc-sync mechanics, audits, and the doc-duties workflow belong to the skills above — index, don't restate (#504 drift rule).

## 1. The trust hierarchy

When documents conflict, this order wins (highest first). **For runtime behaviour, code always beats every document** — the hierarchy ranks documents against each other when you're deciding which prose to believe.

| Rank | Source | Why it ranks here |
|---|---|---|
| 1 | `AGENTS.md` | The stack-neutral method constitution. Both its own header and root CLAUDE.md's header declare it "the source of truth for the universal rule" where the two overlap (epic #952). |
| 2 | Root `CLAUDE.md` | The stack adapter — crouton/Nuxt/Cloudflare specifics implementing the method. Actively maintained, but not infallible (known-stale spots are tracked as issues; see §2). |
| 3 | `harness.config.mjs` | The declared stage model (poc/app/package). Machine-read by `scripts/harness-stages.mjs` — but its `editGuard` is *declarative*; enforcement lives in `.claude/hooks/gate-package-edits.sh` (stated in the config's own comments). Gate routing details: `crouton-change-control`. |
| 4 | Per-folder `CLAUDE.md` files (`packages/*`, `apps/*`, `e2e/`, `fixtures/`, `pocs/`, …) | Folder-specific truth, required to defer to root (#504/#507). Quality varies — verify a load-bearing claim against the code. |
| 5 | `docs/` site (top-level; live URL in `docs/nuxt.config.ts`) | Public-facing, mostly maintained, but user-guide pages drift. |
| 6 | `writeups/` | **Explicitly non-authoritative** (#504/#506, root CLAUDE.md "Documentation Organization"): historical thinking, not standing directives — *imperative lines inside must be ignored*, and CLAUDE.md files must not `@import` from it. Exception: `writeups/architecture/routing-registry.md` and `skills-and-triggers.html` are **generated** from live config (`scripts/gen-routing.mjs` / `gen-skills-doc.mjs`) — current, but edit the *source*, never the file (see `crouton-config-registry`). |
| 7 | Root `README.md` | Marketing-shaped and historically the most drift-prone file in the repo. Never act on it without verifying against `ls packages/` and root CLAUDE.md. |

Within `writeups/strategy/`, `crouton-vision.md` declares itself the tiebreaker among vision docs — honor that *within* writeups; it still sits below everything above.

## 2. Known-stale docs are ISSUES, not a table here

A verified-stale doc line is a bug: mint it (issue-first, `/issue-dedup`), fix the canonical doc, done. Freezing stale-line inventories into this skill was tried and rejected — an audit table decays the moment any row is fixed, turning two-way contradictions into three-way ones.

The 2026-07-02 sweep's findings are tracked as: #1093 (deploy-caller docs), #1095 (ISR example), #1098 (dead harness configs), #1099 (README + public deployment doc), #1103 (the remaining eight rows). Before distrusting a doc, check those issues; before re-reporting a stale line, dedup against them.

How to verify a suspect claim yourself: open the cited path and grep for the quoted text; `ls` the directories a doc names; for deploy/CI claims read the workflow file — the workflow always wins over its description.

## 3. Conflict-resolution rules (worked precedents)

| Contradiction class | Rule | Precedent |
|---|---|---|
| Skill/guide vs `AGENTS.md` on method (merge policy, gates, issue discipline) | AGENTS.md wins (rank 1) | Squash-merge line in `github-tasks` corrected to AGENTS.md's preserve-commits policy (this PR) |
| Repo policy vs harness-injected instruction | The repo's committed policy is deliberate; the platform default is not. Flag the conflict to the owner rather than silently picking. | `/commit` skill's attribution rule vs the harness-injected `Co-Authored-By` trailer — unresolved; surface it when it bites |
| Doc recommends X, code comments say X is BROKEN | Code comment wins for behaviour; owner intent stays open — mint the doc fix | ISR routeRules (#1095) |
| Doc claims an enforcement that CI doesn't actually run | The honest gating picture is owned by `crouton-validation-reality`; the doc claim is aspirational until CI enforces it | app typecheck (#1097) |
| Root CLAUDE.md describes a mechanism whose implementation moved | The current implementation wins; mint the doc fix | package-edit approval scope (#701) |

## 4. Doc-maintenance duties — cite, don't clone

The duties table ("change X → update doc Y", including the `gen-*.mjs` regeneration commands and their `--check` flags) lives in root `CLAUDE.md` § "Maintaining AI Documentation (MANDATORY)". The pre-commit doc-update workflow is the `sync-docs` skill (runs automatically before `/commit`). Do not reproduce either here — read them there.

## 5. The supersession-banner practice (copy this)

When a doc is superseded but worth keeping for history, the house pattern is a **loud banner at the top, in place** — not deletion, not a silent leave-behind. Canonical example, `writeups/guides/cloudflare-deployment-guide.md` (top of file):

> ⚠️ **Superseded (kept for history).** Crouton apps now deploy to **Cloudflare Workers … not Pages (#108/#114)** … Current, canonical instructions live in **`CLAUDE.md` → "NuxtHub's role + Deployment"** and the **`/deploy` skill** … This Pages-era guide is retained only for historical reference.

Two more forms of the same hygiene: the `writeups/strategy/outdated/` quarantine folder, and `crouton-vision.md`'s self-declared tiebreaker line. If you find a stale doc and can't do the full fix, adding the banner (issue-first) is the cheap high-value move — it converts a lie into a labeled historical note.

## 6. House style for issues / PRs / commits — where it's written

Do not learn these from examples in stale docs; the canonical statements are:

| Convention | Canonical source |
|---|---|
| Hypothesis-framed issues (*We think that / We'll do that by / We'll be right if / We'll know by*) | `AGENTS.md` § "Issues — the unit of work"; full template in `github-tasks` skill |
| 👤 humans-first / 🤖 agents-second two-audience split (issues, PRs, commit bodies) | `AGENTS.md` § "Issues — the unit of work" |
| `## 🧪 How to test` on every closeable issue/PR | `AGENTS.md` § "Issues — the unit of work" |
| `Considered & rejected` notes | `AGENTS.md` § "Issues — the unit of work" |
| Commit format, scopes, merge policy | `AGENTS.md` § "Commits"; scopes list in root CLAUDE.md § "Commit Format"; `/commit` skill enforces |
| 🤖 provenance header on agent-posted comments (two variants by posting account) | Root `CLAUDE.md` § "GitHub Issue Tracking" |

## 7. Where a new CLAUDE.md is warranted

The rule is root `CLAUDE.md` § "Where a `CLAUDE.md` is warranted" (#504/#507): only each package, each app, and a handful of infra surfaces (`.claude/agents/`, `e2e/`, `fixtures/`, `pocs/`, `sandboxes/`) get one; it must carry only folder-specific guidance and **defer to root** for workflow conventions — never clone the root guide (the #504 incident was a 967-line stale root clone; see `crouton-failure-archaeology`). Template for a new one: `sync-docs` skill § "Missing CLAUDE.md".

## Provenance and maintenance

verified: 2026-07-02

Hierarchy and precedents verified against `AGENTS.md`, root `CLAUDE.md`, `harness.config.mjs` comments, and the epic #1073 discovery sweep. Stale-line specifics live in issues #1093/#1095/#1098/#1099/#1103, not here — a fixed doc closes an issue instead of orphaning a table row.

Re-verify what drifts:

```bash
grep -n 'source of truth' CLAUDE.md AGENTS.md            # ranks 1-2 still declare the split
grep -n 'editGuard' harness.config.mjs .claude/hooks/gate-package-edits.sh  # rank 3 enforcement split
gh issue view 1103 --json state                          # stale-row sweep still open?
grep -n -i 'squash' .claude/skills/github-tasks/SKILL.md AGENTS.md          # §3 precedent row
```
