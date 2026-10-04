---
name: plan
description: Use this skill at the START of every coding task — new builds, bug fixes, and change requests. Classifies the work item, validates it against project scope, produces a high-level estimate, proposes a technology stack, and checks stack compatibility. Writes a plan artifact to .claude/sdlc/plans/ that every downstream phase and hook depends on. Must run before any Edit, Write, or code-generation tool call. Trigger this skill whenever the user says "implement", "fix", "add", "change", "build", "refactor", or references a ticket/requirement ID — even if the request seems small.
config_requirements:
  - key: tracker.type
    required: false
    on_skip: degrade_to_req_id_only
  - key: tracker.project
    required: false
    on_skip: skip_project_validation
next_suggestions:
  - when: all_signoffs_present
    suggest: "run /analyze to produce requirements with REQ IDs"
  - when: pending_signoff_for_current_user
    suggest: "write your sign-off at sign-offs/<REQ-ID>-<role>.md, then /analyze when all roles are covered"
  - when: plan_gate_signed
    suggest: "run /analyze to produce requirements with REQ IDs"
---

# Plan (Phase 1)

Produce a plan artifact before any code is touched. The plan-gate hook blocks `Edit`/`Write` until this file exists.

## Step 1 — Classify the work item

Ask (or infer from context) which of these the request is:

- **New build** — a new feature or capability not previously delivered
- **Fix** — a correction to existing behavior
- **Change request (CR)** — a modification to previously agreed scope

The classification drives different validation downstream (Phase 4 Build).

## Step 2 — Resolve scope

**If `.claude/sdlc/scope.md` exists and is signed:** read it and proceed. Run a quick re-validation check — if the plan task looks materially different from what scope.md describes, invoke `scope-ingest` in re-validate mode and surface the drift report before continuing.

**If `.claude/sdlc/scope.md` does not exist:** ask the human to point at source material (file path or paste text). Then invoke the `scope-ingest` agent, which produces a draft at `.claude/sdlc/scope-drafts/<timestamp>.md`. Show the draft to the human and wait for review. The human copies/renames it to `.claude/sdlc/scope.md` and signs it before the plan proceeds.

**Fallback — no source material:** if the human has no source to point at, ask for a one-paragraph scope statement and write `.claude/sdlc/scope.md` directly (existing behavior, preserved for minimal-friction cases).

Then validate the resolved scope against the work item:

- **New build:** confirm the request is within documented scope. If not, surface a **scope-delta** and ask the human whether to (a) treat as a CR, (b) expand scope, or (c) defer.
- **Fix:** confirm the fix addresses in-scope behavior. An out-of-scope fix is a CR in disguise.
- **CR:** require a change-request ID. If missing, create one under `.claude/sdlc/change-requests/CR-<n>.md` using `templates/change-request.md` and ask the human for sign-off before continuing.

See `agents/scope-ingest.md` for accepted source formats and draft output spec.

## Step 2.5 — Domain expert check

After scope validation and before writing the plan, invoke the `domain-expert` skill. It runs the two-source domain lookup (project `domains/` then plugin `domains/`), matches the task against the domain index, and — when a match is found — prepares a `## Domain context` block to be appended to the plan artifact in Step 3.

If no domain matches, the skill exits silently. Do not wait for the human or prompt them unless the skill itself surfaces a medium/low-confidence match that requires confirmation.

See `skills/domain-expert/SKILL.md` for the full matching and output specification.

## Step 3 — Write the plan

**Version check (before writing).** If `.claude/sdlc/plans/<task-slug>.md` already exists and a signed plan gate (`gates/plan-<task-slug>.md`) exists for it, compare the intended new content against the current plan's material fields:

- `Classification` (new-build / fix / change-request)
- `In-scope files` list
- `In-scope functions` list
- `Out-of-scope` list
- `Risks & rollback` section

If any material field changed, do **not** write yet. Prompt the human with a narrative message that names the specific change and its consequence:

> Changing Classification from `fix` to `new-build` will archive the current plan as v\<N\> (superseded). Your existing sign-off will not carry over to v\<N+1\>. Continue? [Y/n]

On **yes**: read the current plan's `Version:` field (treat absent as 1 for legacy plans). Rename `<task-slug>.md` to `<task-slug>.v<N>.md` and set `Status: superseded` in the renamed file. Then write the new plan at `<task-slug>.md` with `Version: <N+1>` and `Status: draft`. Print: `Saved as v<N+1>. v<N> archived at plans/<task-slug>.v<N>.md (superseded).`

On **no**: discard the changes to material fields and resume with the current plan unchanged.

Non-material edits (prose, typos, formatting) pass silently — do not trigger this check.

**Write** to `.claude/sdlc/plans/<task-slug>.md` using `templates/plan.md`. Required fields:

- **Task ID & classification** (new-build / fix / CR + reference ID)
- **Problem** (1–2 sentences)
- **In-scope files** (explicit list — hooks enforce this)
- **In-scope functions** (explicit list — hooks enforce this)
- **Out-of-scope** (explicit "do not touch" list)
- **Approach** (3–5 bullets)
- **Tests to add/update** (function-level — only modified code gets new tests)
- **Risks & rollback**
- **Estimate** (t-shirt size or story points; see `config/tools.json` for convention)
- **Version** (start at 1; increment on each material edit of a signed plan)
- **Status** (`draft` until plan gate is signed; `signed` after; `superseded` when replaced by a newer version)

Keep it short. The plan is a contract, not a design doc — Phase 3 handles design.

## Step 4 — Technology stack

For new builds, propose the stack (language, framework, major libraries, platform, data store). For fixes and CRs on existing code, record the *existing* stack the change lives in.

Validate compatibility:

- Language/runtime versions against existing platform
- Library licenses against project policy (if recorded)
- Data schema compatibility if the change touches data
- Auth/identity compatibility
- Deployment target compatibility

Produce a compatibility matrix as a markdown table in the plan file. Any `FAIL` row halts planning and requires human decision.

## Step 4.5 — Scope gate (first task per project only)

If `.claude/sdlc/gates/scope-<project-slug>.md` does not exist, draft and sign the scope gate before proceeding to the plan gate. If the file already exists, skip this step entirely.

**Derive the project slug** from the `project_name` field in `scope.md` (slugify: lowercase, hyphens, no spaces). If `scope.md` has no project name, use the repository directory name.

**Draft the scope gate** at `.claude/sdlc/gates/scope-<project-slug>.md` using `templates/scope-gate.md`:

- Fill `## Scope summary` — one paragraph summarising what the scope covers and what source material was used.
- Fill `## Source material` — source path (or "pasted text"), extraction confidence per field, provenance pointer to the scope draft.
- Pre-tick `## Scope fields confirmed` for every field that was present and reviewed in the scope draft. Leave unchecked fields that were absent or low-confidence.
- Fill `## Open items carried forward` with any low-confidence or absent fields from the draft that the plan must still resolve.
- Compute `gate_hash`: sha256 of the file content **above** the `## Required sign-offs` heading at this point in the draft. Write it into the `gate_hash:` line before presenting the gate to the human.

**Ask the human to sign** the scope gate (same chat sign-off prompt as a phase gate). Acceptable inputs: a URL, or `no ticket REQ-SCOPE-<project-slug>` for degraded mode. Write the signed gate file.

After sign-off, `plan-gate.sh` will stop warning about the missing scope gate on all future `/plan` invocations for this project.

## Step 5 — Second opinion review (hard rule — cannot be skipped)

Before presenting the plan to the human, run a self-contained second-opinion review. Re-read the complete plan artifact as if encountering it for the first time and check:

1. **Classification** — is it unambiguously one of: new-build / fix / change-request? Any ambiguity must be resolved before proceeding.
2. **In-scope files** — explicit, non-empty list. "TBD" is not acceptable at gate time.
3. **In-scope functions** — explicit or documented as deferred (allowed before Build only).
4. **Out-of-scope** — not the template placeholder; must name specific things excluded.
5. **Tests to add/update** — non-empty; function-level.
6. **Risks & rollback** — non-empty; names specific failure modes and the rollback path.
7. **Compatibility matrix** — no unresolved `FAIL` rows; `UNKNOWN` is treated as an open item, not a pass.

If any item fails the checklist, surface the gap explicitly and ask the human to resolve it **before** requesting sign-off. Do not present the gate summary until all checklist items pass.

Present the second-opinion findings to the human in this format:

```
Second opinion — plan review
✓ / ✗ Classification: [result]
✓ / ✗ In-scope files: [result]
✓ / ✗ In-scope functions: [result]
✓ / ✗ Out-of-scope: [result]
✓ / ✗ Tests: [result]
✓ / ✗ Risks & rollback: [result]
✓ / ✗ Compatibility matrix: [result]

[If any ✗: list gaps and ask human to resolve before sign-off.]
[If all ✓: "Plan passes second-opinion review. Proceeding to sign-off."]
```

## Step 6 — Human gate

Produce a one-screen summary of the plan and ask the human to confirm before Analyze/Design/Build proceeds. Write the confirmation to `.claude/sdlc/gates/plan-<task-slug>.md` using `templates/gate.md` — later commands check for this file.

The gate summary must show what the human **is** approving (scope, classification, risks) and what they are **not** approving (architecture, implementation approach — those belong in later phases).

## What this skill must NOT do

- Do not write code.
- Do not modify files outside `.claude/sdlc/`.
- Do not skip the scope check, even if the task feels obvious.
- Do not approve the plan on the user's behalf — the gate file requires the human to confirm.
- **Do not present the gate summary (Step 6) before completing the second-opinion review (Step 5).** This is a hard rule. A plan that skips Step 5 is not ready for sign-off.

## References

- `templates/plan.md` — plan artifact template
- `templates/change-request.md` — CR template
- `templates/gate.md` — phase-gate template
- `templates/scope-gate.md` — scope gate template (Step 4.5)
- `agents/scope-ingest.md` — scope draft producer (Step 2)
- `skills/domain-expert/SKILL.md` — domain context injector (Step 2.5)
- `docs/SDLC.md` — full phase reference

## Next step hint

After writing the gate file, pipe the `next_suggestions` conditions to `skills/_shared/next-hint.sh` and print any output:

```bash
printf '%s\n' \
  'all_signoffs_present|run /analyze to produce requirements with REQ IDs' \
  'pending_signoff_for_current_user|write your sign-off at sign-offs/<REQ-ID>-<role>.md, then /analyze when all roles are covered' \
  'plan_gate_signed|run /analyze to produce requirements with REQ IDs' \
  | bash skills/_shared/next-hint.sh
```

Print any output verbatim. If the script outputs nothing (suppressed, faded, or no match), add nothing.
