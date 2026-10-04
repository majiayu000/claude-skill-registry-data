---
name: retro
description: Session retrospective — update memories and project docs.
---

## 1. Lessons
0–5 bullets, ≤200 chars, non-obvious only (skip git/code-derivable). **No floor — zero is a normal outcome**: a quota manufactures lessons, and each manufactured lesson then recruits a durable-doc write in Step 3b. Showing ≠ filing — a lesson is shown here and routed to a durable doc only where Step 3b's admission test admits it, which most don't clear.

## 2. Corrections
Route each correction/confirmed approach via `~/.claude/references/recording-principles.md` (§"When asked to record information"); don't invent paths.
Graduate a steer INTO its skill/rule/CLAUDE.md the moment that target is reachable this turn — it's only reliable once in the body.
What can't graduate now stages as a `type: feedback` file (the frontmatter is the key), graduated by a later retro when its target is reachable.
Stranger test: a skill steer (impag/qimpag/…) is GLOBAL. Silent if none.

## 3. Append memories
If a project memory was already written this turn (e.g. impag stage-done), append only load-bearing facts Steps 1–2 missed.
A `project_state` pointer write does NOT discharge capture — 3b still runs.
Auto-memory pruning stays automatic and write-time: each writer trims its own memory file (`project_state.md`, `roadmap.md`, `MEMORY.md`) in the same write, dropping closed/superseded lines (`memory-system.md §Rolling state`). That is the ONLY trimming retro does — scope, and the two things that are NOT condensing and still run automatically → `memory-system.md §Write targets`.

## 3b. File the facts (the payload)
Re-discoverable/load-bearing technical facts → their durable doc, not just chat. **File only what clears `~/.claude/rules/instruction-file-discipline.md` §Write-time checks** — the normal outcome is nothing filed.
**Two bars run BEFORE that test on every candidate, and both are usually fatal:** (1) **one edit site → the seam** — a fact with one obvious edit site goes to that site (code comment, test, path-gated rule), never to a numbered ledger or taxonomy; (2) **second occurrence** — a one-off files nowhere; recurrence across arcs is the only evidence a future session re-discovers it. **What gets filed is the heading plus the MOVE and nothing else** — the incident, its date, the file it happened in and the numbers go to the commit message; a dated narrative paragraph in a durable doc is the defect, not the record. For the architecture doc's **gotchas ledger** specifically, filing is also one in, one out in the same burst, never a later sweep (`~/.claude/references/memory-system.md` §Gotchas ledger) — a seam or a rule is a fact's natural home and has no graduate-one-out move.
- A **domain reference / edit-site** (a `references/*.md`, path-gated rule, or code comment at the seam) — a fact tied to a file/seam/constant a future session would re-derive.
  Graduate to the fact's natural home; do NOT sink it into the volatile memory `roadmap.md`/`project_state` menu — a `Durable facts`/guardrail SECTION already grown there is a parking-lot defect, graduate it out **or delete it** this pass (durable knowledge never lives in a volatile file — `memory-system.md §Rolling state`).
  **Graduation is re-admission, never relocation.** A line moving out of a volatile file clears the DESTINATION's admission test at the moment it moves, one line at a time; one that doesn't clear it is deleted, not carried across. Relieving pressure on a volatile file by absorbing its contents wholesale into a git-tracked doc converts temporary lines into permanent ones and is the defect this bullet exists to stop — the shrinking memory dir is not evidence the pass worked.
- Project architecture doc (`architecture-overview.md`/`ARCHITECTURE.md`) if one exists — a pipeline/seam/data-flow correction; commit it if untracked and shipped code cites it.
  Its ledger is staging — **file only if system-specific AND durable**: (1) true with a different codebase? → generic lesson → global `rules/*`/`references/*`; (2) changes as it runs/tunes? → changing detail → plan/roadmap or git. Keepers: one-edit-site → seam.
- The design/plan doc a finding invalidates — correct or mark stale in the same burst;
  **a plan whose code all shipped this session (even if only a manual/eye/live confirm remains) is archive-ready** — apply the project's plan-archive convention (grep inbound refs → `git mv` to the archive dir → move the pending check to `project_state`).
  Wrap-up owns no archive step, so it fires here.
After a drain that appends ≥3 sections to a single doc, record `/condense <that doc>` as armed — do not run it in the same session (the context that wrote the sections is the worst judge of their redundancy).
Scope: never git-held narration. Silent; Step 6 names the docs.

## 4. CLAUDE.md / rules gaps
Scan for repeated corrections/misunderstandings/missing context.
**A repeated correction whose target already states the directive is that bullet, Edited** (`~/.claude/rules/instruction-file-discipline.md` §Top three anti-patterns #2); author a new rule only when it clears that file's §Write-time checks.
If any: Target from the RAW incident (date/path/project attached): no second project it fires in → project-tier `<project>/.claude/rules/`, created if absent.
Present Issue → Proposal → Target → Exact text, then apply — state what TO do (not "don't X"); a structural finding too big for a rule → `<project>/docs/audits/`.
Routing → `~/.claude/rules/instruction-file-discipline.md`; new rule/bullet → grep `~/.claude/references/memory-system.md §Write targets` (body schema).
Don't rewrite conformant rules. Silent otherwise.

## 5. Close
ONE terse line — e.g. `Facts→hooks-deep-dives+arch; qimpag rule updated.` Name the docs 3b filed into (or `none`). Lessons (Step 1) may still show. No table.

Silent memory ops (CLAUDE.md Iron Rule) cover Steps 2–4: tool calls / dispatch only, zero prose. Step 5 is the sole assistant text.
