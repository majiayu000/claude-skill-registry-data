---
name: complex-project-discipline
description: Universal operational discipline for solo or small-team execution on complex multi-layer projects (research line + production service + funding readiness + AI-agent harness). Apply when starting a new project, establishing operational rules, scaling solo execution under AI-agent collaboration, preparing funding applications, designing UX standards for public surfaces, introducing Claude Code harness, or recovering session continuity. Trigger on phrases like "set up project discipline", "task pack", "bounded execution", "funding readiness", "UX standards canonical", "Claude Code harness", "session continuity", "memory structure", "verification gate", "append-only logs", "owner-operated disclosure", "reference prep", "preserved failure", "MERGE_MAIN_NOW".
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Complex Project Discipline

A universal operational discipline distilled from production-grade solo-engineer execution on a project that simultaneously ran (a) a research line with measured gates and preserved failures, (b) a production web service with tunneled deployment and corpus-driven verification, (c) a funding-readiness application cycle across the alignment-funder ecosystem, and (d) a layered AI-agent harness via Claude Code.

This skill is **project-agnostic**. Every rule has been formulated as a universal pattern. Adapt names to your project; keep the patterns.

---

## When this skill applies

Load full skill body when ANY of:

- Starting a new project and establishing operational rules from day 1.
- Inheriting a project that lacks discipline (no canonical state file, no append-only logs, ad-hoc commits).
- Solo or small-team execution where you need external structure to substitute for a larger team's review redundancy.
- Funding application cycle (alignment funders, public posting, fellowship, paid pilot).
- Public-surface UX work needing standards baseline (a11y, security, perf, i18n, brand).
- Introducing AI-agent harness (Claude Code settings, hooks, skills, agents) to an existing repo.
- Session continuity recovery after long break.
- Verification gate before production deploy or external claim.

DO NOT auto-load on every casual conversation. Triggers should be specific (see frontmatter `description`).

---

## Skill structure (progressive disclosure)

```
SKILL.md                                          (this file — entry + index)
docs/
  01_TRUTH_HIERARCHY_AND_STATE_FILES.md           Canonical state file pattern. 9-level hierarchy.
  02_BOUNDED_EXECUTION.md                         Task pack format + 10-step execution flow.
  03_VERIFICATION_DISCIPLINE.md                   "No artifact, no claim." Three verification states.
  04_BRANCH_AND_PUSH_DISCIPLINE.md                Main protection + explicit-override push pattern.
  05_APPEND_ONLY_LOGS.md                          Execution-log + weekly-status row format.
  06_CHANGE_CLASS_CLASSIFICATION.md               R0/R1/R2 classes + when-in-doubt rule.
  07_UX_STANDARDS_CANONICAL.md                    10-standard distilled stack + per-surface checklists.
  08_PRODUCTION_INFRA_DISCIPLINE.md               Deploy patterns + DB volume preservation + tunnel rules.
  09_CORPUS_DRIVEN_DEVELOPMENT.md                 7-step corpus pattern + thresholds.
  10_FUNDING_READINESS_DISCIPLINE.md              Owner-operated disclosure + reference qualification.
  11_COMMUNICATION_PATTERNS.md                    Apology + opt-in paths + customer-debt acknowledgment.
  12_CLAUDE_CODE_HARNESS_PATTERN.md               8-step layered harness rollout.
  13_MEMORY_STRUCTURE.md                          Repository + state + top-of-stack continuity.
  14_SESSION_CLOSE_DISCIPLINE.md                  Close gate + 6-condition final answer gate.
  15_ANTI_PATTERNS.md                             What NOT to do (catalogued anti-patterns with counter-patterns).
  16_POLISH_DISCIPLINE.md                         Critical re-read for adversarial review.
templates/
  task_pack.md                                    Reusable 9-section task pack template.
  bounded_packet.json                             Bounded execution packet JSON schema.
  agents_log_row.md                               Single-row format for append-only execution log.
  weekly_status_section.md                        Per-task ## section format.
  reference_prep_brief.md                         Integrity-aligned ground-truth context for referees.
  apology_email_pattern.md                        Customer-relationship debt closure pattern.
  paste_ready_field_map.md                        Form-submission paste-ready field map template.
  claude_settings.json                            Project-level Claude Code settings template.
checklists/
  pre_commit_check.md                             Before any git commit.
  pre_push_check.md                               Before any git push.
  session_close_check.md                          End-of-session full closure.
  final_answer_gate.md                            6-condition gate before declaring "done".
  ux_per_surface_check.md                         Per-public-surface UX checklist.
  deploy_verification_check.md                    Production deploy verification.
```

---

## The seven core principles (read first)

### 1. Truth hierarchy is non-negotiable

Every project needs a single canonical live-state file. Lower levels of documentation can give context but cannot override higher levels. When no artifact backs a claim, mark it `UNVERIFIED`. See `docs/01_TRUTH_HIERARCHY_AND_STATE_FILES.md`.

### 2. Bounded execution beats heroic execution

One task = one reason. One commit = one logical change. Acceptance criteria mandatory. Rollback plan mandatory for state changes. Audit before edit, even on "obvious" tasks. See `docs/02_BOUNDED_EXECUTION.md`.

### 3. No artifact, no claim

`PARTIAL` is allowed. `UNVERIFIED` is required when proof is missing. `SUCCESS` requires (a) measured artifact, (b) live-state updated, (c) memory updated, (d) verifier returns the new state, (e) shell-valid verification commands. See `docs/03_VERIFICATION_DISCIPLINE.md`.

### 4. Append-only logs are the spine

Old entries are never edited. New entries always appended at end. Format is rigid (pipe-separated row + section header). The discipline of writing append-only forces honesty in retrospect. See `docs/05_APPEND_ONLY_LOGS.md`.

### 5. Disclosure-first integrity beats hidden conflicts

Hidden conflicts of interest are catastrophic when discovered. Disclosed conflicts are signals of integrity. This rule applies equally to research claims, funding references, owner-operated testbeds, and any relationship that could appear as a conflict of interest. See `docs/10_FUNDING_READINESS_DISCIPLINE.md`.

### 6. Preserved failures are a competitive advantage

When an experiment fails, document it as canonical FAIL — do not silently rewrite. The discipline of preserving failure is the cleanest empirical demonstration of where your method's boundary actually is. See `docs/09_CORPUS_DRIVEN_DEVELOPMENT.md` + `docs/03_VERIFICATION_DISCIPLINE.md`.

### 7. Main branch is sacred until explicit unlock

Working branch (e.g. `test`, `dev`, feature branches) is for active work. Main branch (or production) is protected and only updated via explicit user-issued unlock command (e.g. `MERGE_MAIN_NOW`). Mechanical enforcement via `permissions.deny` in tooling settings. No `git push --force`, no `reset --hard`, no `rebase -i`. See `docs/04_BRANCH_AND_PUSH_DISCIPLINE.md`.

---

## Quick-start for a new project

If you are starting from scratch and want this discipline applied:

1. **Create canonical state file** — name it consistently (`CANON.md`, `LIVE_STATE.md`, `project_truth.md`). Single source of truth at the top of hierarchy. See `docs/01`.
2. **Create append-only logs** — execution journal (pipe-separated rows) and weekly status (per-task `##` sections). See `docs/05` + `templates/agents_log_row.md`.
3. **Create memory structure** — `memory.md` with Repository / Active Scope / Current State / Top-of-Stack sections. See `docs/13`.
4. **Define operational rules** — equivalent of `.claude/CLAUDE.md` / `OPERATING_RULES.md` / `AGENTS.md`. Sections: Language, Identification, Mandatory Startup, Source-of-Truth Hierarchy, Execution Rules, Forbidden Actions, Logging & Continuity, Class Classification, Task Completion Checklist, Session Close Checklist. See `docs/14`.
5. **Set up AI-agent harness** (if using Claude Code) — `.claude/settings.json` with allow/deny lists, SessionStart hook for canon load, layered rollout via 3 push checkpoints. See `docs/12`.
6. **Adopt UX standards canonical** (if public-surface project) — distill 10 international standards into hard rules + soft rules + measurable thresholds. See `docs/07`.
7. **Establish bounded execution flow** — task pack format for any non-trivial work, 10-step flow (audit → findings → implement → tests → verifier → commit → restart → live verify → brief → push). See `docs/02`.

---

## Quick-start for a funding application cycle

If you are preparing funding applications for an existing project:

1. **Audit funding pack** — list all draft applications, deadlines, requirements. See `docs/10`.
2. **Verify disclosures** — owner-operated systems explicitly marked, family/partner relationships flagged, no hidden conflicts. See `docs/10`.
3. **Reference qualification** — for each candidate referee: independent? engaged with methodology? willing? See `templates/reference_prep_brief.md`.
4. **Strategic skip when integrity at risk** — refusing to apply with conflicted refs is itself an alignment-discipline signal. Document the skip openly in remaining apps. See `docs/10`.
5. **Paste-ready field map** before submit — survey the form, map content to fields, polish for adversarial review, char budget audit, submit only after explicit user OK on each consent. See `templates/paste_ready_field_map.md` + `docs/16`.
6. **Append to submission log** — date, fund, ask, status, decisions made. See `docs/05`.

---

## Quick-start for production deploy

1. **Pre-deploy check** — clean git tree, tests pass, corpus pass, verifier known state. See `checklists/pre_commit_check.md`.
2. **Deploy via documented pattern** — never `docker compose down` (preserves DB volumes); always `up -d --build --force-recreate` on the app container only. See `docs/08`.
3. **Health check after every restart** — `curl /v1/health` or equivalent.
4. **Live verify on a real URL** — not just unit tests; real HTTP request to public surface. See `docs/03`.
5. **Update infra state doc** if state changed. See `docs/08`.
6. **Append to execution log** — record deploy with commit hash and verification commands.

---

## Operational language rule (universal pattern)

For multilingual projects: pick one user-facing language and one machine-actionable language; never mix in artifacts that get parsed. ZIP file contents, CSV headers, JSON keys → always one canonical language (typically English). Email body, UI copy, brief reports to user → user-facing language. See `docs/07_UX_STANDARDS_CANONICAL.md` and `docs/11_COMMUNICATION_PATTERNS.md`.

---

## What this skill does NOT replace

- A real human team (this is solo / small-team discipline, not a substitute for review/redundancy).
- Domain expertise (you still need to know your research / product / market field).
- Legal / accounting / tax advice (the funding-readiness module assumes you'll get those separately).
- A real product/market fit (discipline doesn't make a bad idea good).

---

## Update rule

This skill is a snapshot of working discipline patterns. As your project diverges, fork this skill into a project-specific copy — do not modify the canonical version. Date your fork and document divergences explicitly.

This canonical version is intentionally project-agnostic and contains no internal data, partner names, or specific identifiers from any single project.
