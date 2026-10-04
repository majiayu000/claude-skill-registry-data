---
name: unit-lane
user-invocable: true
version: 1.2.0
argument-hint: <NN-slug | "<idea>"> [--retriage] | --fix <issue-number> | --from-issue <issue-number>
description: >
  One-shot lane conductor for a delivery unit: triage, implement, evidence, and
  close in a single document. Triggers: "unit-lane", "run the lane",
  "work on this feature/fix", "build this unit".
---

# Unit Lane — Adaptive Conductor

One document, adaptive steps. The lane reads a closed catalog, triages which
steps a unit needs, executes them in order, and commits at each gate. Replaces:
design-feature, plan-feature, review-spec, review-plan.

## Turn contract

Tick every box before ending the turn; an unchecked box means the turn is not
done:

```
✓ Triage ran (bun scripts/unit-route.mjs --triage <slug>) and its block pasted
  verbatim into the unit doc's Evidence section as the authoritative step list
✓ Unit doc exists at docs/features/<NN>-<slug>/SPEC.md (created from template
  if new, with all mandatory sections filled or n/a)
✓ Guard ran (bun scripts/diff-guard.mjs --base <ref>) after each implement step;
  on BREACH: re-triage or record exception, never shrink the diff
✓ Unit doc's Evidence rows updated (command → exit/digest → output → verified-by)
  and Progress log updated (dated entry) before every commit
✓ → Next: block printed as the absolute last output
```

## When to use

- A known unit slug: `unit-lane <NN-slug>`
- A raw idea (no slug yet): `unit-lane "<idea description>"`
- A tracked fix issue (no fix folder yet): `unit-lane --fix <issue-number>`
- A tracked roadmap feature issue (no feature folder yet): `unit-lane --from-issue <issue-number>`
- Force re-triage: `unit-lane <NN-slug> --retriage`

Both `--fix <n>` and `--from-issue <n>` are the exact forms
`scripts/unit-route.mjs` prints for a tracked issue with no unit folder
(`route: plan-from-issue`) — never invent a different spelling.

## Step 0 — Discover the project

Per the agent guide's **Workflow conventions** + **documentation map**, then read
`docs/features/_TEMPLATE/SPEC.md` (the unit doc template). If the unit folder
exists, read its current `SPEC.md` to avoid overwriting.

## Process

### 1. Resolve or create the unit doc

If the unit folder already exists, read its `SPEC.md` and continue. Otherwise
create it from the tree the unit belongs to:

| Invocation | Folder | Template | Index to register |
|---|---|---|---|
| `<NN-slug>` / `"<idea>"` | `docs/features/<NN>-<slug>/` | `docs/features/_TEMPLATE/SPEC.md` | `docs/features/ROADMAP.md` |
| `--fix <issue-number>` | `docs/fix/<issue-number>-<topic>/` | `docs/fix/_TEMPLATE/SPEC.md` | `docs/fix/README.md` |
| `--from-issue <issue-number>` | `docs/features/<NN>-<slug>/` | `docs/features/_TEMPLATE/SPEC.md` | `docs/features/ROADMAP.md` (row links `#<issue-number>`) |

For `--fix`/`--from-issue`, read the tracked issue in the forge first and keep
its number; the folder name carries it (`fix/<issue-number>-<topic>`). Fill
objective, why, user outcome, and non-goals from the invocation (or the issue).
Acceptance criteria are induced from user scenarios — **ask-don't-infer**; if the
request is too vague, STOP and ask the user with concrete options. See
[the unit doc template](references/STEPS.md) for section order.

### 2. Triage — read the catalog, never re-derive

Run `bun scripts/unit-route.mjs --triage <slug>` (or `<NN>` for numeric). PASTE
its stdout block **verbatim** into the unit doc's Evidence section header under
a `## Triaged steps` heading. This block is authoritative. The model never
re-derives, reorders, or invents steps — it executes only what the catalog says.

### 3. Execute triaged steps in order

For each step the triage returned, follow its reference file. Execute **one step
per turn-commit**:

1. Read the step's reference — for example:
   [research](references/RESEARCH.md), [design](references/DESIGN.md),
   [plan](references/PLAN.md), [implement](references/IMPLEMENT.md),
   [tests](references/TESTS.md), [evidence](references/EVIDENCE.md),
   [review](references/REVIEW.md), [docs](references/DOCS.md),
   [release](references/RELEASE.md) — only the ones the triage demands).
2. Perform the step's checklist items.
3. Write/update evidence in the unit doc.
4. Update the Progress log with a dated entry.
5. Commit with a conventional commit message.
6. For implement steps, run the diff guard (step 4 below).

### 4. Diff-size guard (after each implement step)

Run `bun scripts/diff-guard.mjs --base <last-reviewed-ref> --unit <NN>`. Paste
the output verbatim. On **BREACH**: stop, re-triage the unit, or record an
exception. **Anti-gaming: NEVER shrink a diff by deleting comments, blank lines,
docs or tests.** If the unit cannot fit the budget, record the exception and stop.

### 5. Update evidence and progress

Before every commit:

- **Evidence rows**: One row per AC satisfied — `| AC | command | exit/digest |
  output (≤2 lines) | verified-by |`
- **Progress log**: `YYYY-MM-DD HH:MM — <what was done> → <commit sha> — next:
  <what is next>`

### 6. Close the unit

When all triaged steps are done, run the review pack axis summary, update the
unit doc's status, and print the closing block.

## Guardrails

**Allowed:**
- Only the triaged steps listed by the catalog
- Changes scoped to the acceptance criteria
- Documentation updates in docs/ and template/
- Conventional commit messages per the project's Workflow conventions

**Forbidden:**
- Never expand scope beyond what Non-goals define — findings discovered during
  implementation never widen the unit
- Never invent an acceptance criterion — ask the user with concrete options
- Never skip a triaged step silently — every step the catalog demands must run
- Findings never authorize scope growth — record them, route to their owner
- Never commit red (test failure) — fix or replan, never silence tests
- Never alter a triaged step's order

## Relationship to other skills

`unit-lane` absorbed the retired fixed-pipeline skills (design-feature,
plan-feature, review-spec, review-plan) into catalog steps. The review pack axes
(`review-implementation`, `review-code`, `review-security`, `review-perf`,
`review-a11y`, `review-debt`) compose the review step; `triage-issue` feeds
issues into the lane; `workflow-status` computes the next lane invocation.
`init-workspace` seeds the unit doc template and catalog conventions into target
projects.

## Portability (agents other than Claude Code)

- **No slash menu** — open this `SKILL.md` and follow it literally in a fresh
  conversation. Where it says `run`, execute the shell command directly.
- **No model tiers** — triage and review use the strongest model; execution
  steps may use cheaper. Never review with a weaker model than the author.
- **No `/loop`/subagents** — re-invoke manually and follow the closing `→ Next:`
  block at each step boundary.

## Done when

- Every triaged step is executed and committed.
- The unit doc's Evidence rows, Progress log, and References section are current.
- The diff guard passed for all implement steps.
- The review step is complete (or skipped per catalog).
- **The closing `→ Next:` block is printed.**

## Closing recommendation

```
→ Next: /unit-lane <NN-slug> — continue to the next triaged step
  · all steps done → /review-change (review the accumulated diff)
  · re-triage needed → /unit-lane <NN-slug> --retriage
  · finished and merge-ready → /audit-pr (merge gate)
```