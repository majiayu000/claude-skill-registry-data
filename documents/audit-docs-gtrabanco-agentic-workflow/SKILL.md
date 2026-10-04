---
name: audit-docs
user-invocable: true
version: 2.2.0
argument-hint: "[--fix]"
author: "Gabriel Trabanco <1969593+gtrabanco@users.noreply.github.com>"
license: MIT
description: >
  Audit cross-document coherence: docs ↔ roadmap ↔ code ↔ fix index ↔ issues.
  Finds drift — features in docs/ not in the roadmap (or vice versa), fix-index
  entries already merged/closed, broken documentation-map links, dependency
  cycles, artifacts in the wrong language, naming-convention violations — and
  reports them ranked by severity, fixing only low-risk items on request.
  Model-agnostic: the skill inherits whatever model and effort your agent
  session is already using.
  Triggers: "check doc consistency", "are the docs in sync", "audit the docs",
  "doc coherence review", "did the docs drift", "validate the roadmap".
---

# Audit Docs

A read-first audit answering "do the docs still match reality?" Produces a
findings report; it does not silently rewrite docs.

## Turn contract — verify before ending the turn

```
✓ The AUDIT DOCS fixed-format report was printed, ending in `Decision: PASS | FAIL`
✓ No doc was rewritten without explicit --fix / user go-ahead
✓ The closing `→ Next:` block is printed as the ABSOLUTE last output
```

About to end the turn with any box unchecked? The turn is NOT done — complete
the missing box first (weak models drop end-of-document duties; this list is
first on purpose).

## When to use

- Before a release or milestone, after merging several features/fixes, or
  whenever the doc set might have drifted from the code and issues.

## Step 0 — Discover the project (always first)

Per the agent guide's **Workflow conventions** + **documentation map**, then read
what THIS skill needs: the roadmap, the fix index + template, and the feature
folder layout — the map tells you which links and invariants to check.

## Checks

Run these and collect findings (cite paths/lines/issue numbers each):

1. **Roadmap ↔ feature folders.** Every `docs/features/<NN>-<slug>/` is in the
   roadmap, and every roadmap entry has a folder (or is explicitly "scheduled").
2. **Feature dependencies.** SPEC `Depends on` / `Branch` fields are valid; no
   dependency cycles; ordering is consistent with the roadmap.
3. **Fix index hygiene.** Every entry maps to an **open** issue and an unmerged
   branch; flag entries whose issue is closed or whose PR merged (should have
   been removed). Flag open fix branches missing from the index.
4. **Documentation-map links resolve.** Every file the map references exists;
   flag "scheduled, not yet authored" items so they aren't mistaken for drift.
5. **Broken intra-doc links.** Relative links/anchors point at real
   files/sections.
6. **Issue references.** Acceptance/known-issues lines referencing `#N` aren't
   pointing at long-closed issues without note.
7. **Language & naming conventions.** Artifacts in the project's docs language
   (this repo: **English**); file/dir naming matches conventions (e.g.
   kebab-case TS files, PascalCase components).
8. **Invariant tags.** If the project uses invariant/decision IDs (e.g.
   INV-/D-/KI-), spot-check that referenced IDs exist where claimed.
9. **PR-link integrity on `done` rows.** Every roadmap row (and fix-index
   entry) with status `done` carries a linked PR reference —
   `done · [#<pr>](<pr-url>)`. For each bare `done`, find its PR in the forge
   (`gh pr list --state all --head feat/<NN>-<slug>` or by title) and propose
   the row update; a `done` with no PR found at all is HIGH severity (the unit
   may never have been closed out).

**Workflow discipline (checks 10–14)** — the executor skills enforce these at
write time; this audit verifies they actually held. Each check is mechanical:
run the command shown, don't infer.

10. **Phase naming.** `grep -rnE '\bS[0-9]+\b|\bStep [0-9]' docs/features/*/{PLAN,TASKS,progress}.md`
    must return nothing — plans use `P1, P2, …` ("phases") only. Any hit: LOW
    (rename), plus check the executor argument still resolves.
11. **Per-phase doc discipline.** For every M/L feature `in-progress`/`done`:
    completed phases are ticked in `TASKS.md`, `progress.md` has one entry per
    completed phase, and (features planned under the current template) the
    final phase ends with the literal close-out tasks (open PR + print URL,
    link roadmap row, push the link commit). A `done` feature with unticked
    tasks or a phase missing from `progress.md`: HIGH.
12. **Branch & PR discipline vs the forge.** For every `done` unit: its PR
    exists, targets the default branch, has a non-empty body, and carries
    `Closes #<n>` when the unit is issue-born (SPEC references an issue).
    Also scan recent default-branch history (`git log --first-parent`) for
    feature/fix-scoped changes committed directly without a PR: HIGH.
13. **Generated-docs provenance (only when the documentation map declares a
    `Docs site` block; otherwise state n/a).** Scan the declared content dir
    for orphan pages
    each: (a) its `source-unit` exists in the roadmap or fix index — no match
    is an **orphan** (low: propose deletion or re-attribution); (b) the
    unit's PR merged **after** the page's `updated` date with commits touching
    the page's subject paths — that page is **stale** (LOW: propose
). Cite page path + unit per finding.
14. **Commit format & dependency discipline.** Sample the unit branches'
    commits: `<type>(<scope>): <summary>` conventional format (violations:
    LOW). Every `in-progress`/`done` row's `Depends on:` closure was merged —
    a unit built on unmerged deps is HIGH unless `decisions.md` records a
    user-forced override (`--force`), which downgrades it to LOW (documented
    risk).

Adapt the list to what the project has; skip checks for absent structures and
say so.

## Process

1. Discover, then run the checks with `grep`, file reads, and the forge CLI
   (per Workflow conventions; examples use `gh`).
2. Produce the findings report — **return exactly** (fixed output contract):

   ```
   AUDIT DOCS — scope: <docs tree / roadmap / fix index / issues checked>

   | # | Check (1-14) | Finding | Sev | Evidence | Proposed fix |
   |---|-------------|---------|-----|----------|--------------|
   | 1 | <which>     | <what>  | high|low | <path:line / #issue> | <smallest action> |

   Checks run: <n>/14 (skipped: <which + why — absent structures only>)
   Summary: <1-2 sentences>
   Decision: PASS | FAIL   (FAIL if any high-severity finding is open)
   ```

   Sev: **high** = misleading or broken; **low** = cosmetic.
   Only `high` and `low` are defined in this legend
3. **Fix only on request.** With explicit `--fix` (or user go-ahead), apply the
   low-risk corrections (remove a merged fix-index row, fix a dead link, register
   a missing roadmap entry, add a verified PR link to a bare `done` row). Leave judgment calls to the user.

## Guardrails

- Read-first; never bulk-rewrite docs unprompted.
- Distinguish genuine drift from intentionally "scheduled/deferred" items —
  don't report deliberate tradeoffs as errors.
- Keep changes surgical and within docs; no code or behavior changes.

## Portability (agents other than Claude Code)

The workflow is the contract; Claude Code features are conveniences. On an
agent that lacks one, apply the fallback — never skip the step the feature
enables:

- **No slash-command menu** — where this skill says `/<skill>`, open that
  skill's `SKILL.md` (wherever your agent installed the skills) and follow it
  literally, in a fresh conversation: hand-offs assume a clean context.
- **No per-skill `model:`/`effort:`** — no skill pins a tier; pick tiers yourself:
  these are mostly mechanical cross-document checks — a mid-tier model is
  enough; escalate to your strongest only for a deep audit.

## Relationship to other skills

- Complements `unit-lane` (which *creates* the docs this audits) and
  `triage-issue` (which keeps the fix index honest).
- Run standalone anytime; no required predecessor.

## Done when

- A severity-ranked findings report exists, and any approved low-risk fixes are
  applied — with genuine deferrals left untouched and labeled as such.
- **The closing `→ Next:` block is printed:**

  ```
  → Next: apply the approved low-risk fixes, then re-run /audit-docs to confirm clean
    · real drift (not cosmetic) → /triage-issue   · a concrete defect → /unit-lane --fix <n>
    · already clean → nothing to do
  ```
