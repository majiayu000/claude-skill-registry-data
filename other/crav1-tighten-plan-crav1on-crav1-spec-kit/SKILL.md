---
name: crav1-tighten-plan
description: >-
  Walk plan.md/tasks.md issues one by one (including /crav1-review-plan P#s).
  Offer resolutions (including get a suggestion); patch only plan and tasks
  after a pick. Spec-tagged findings go to tighten-spec. Do not write
  application code. Do not edit spec.md.
disable-model-invocation: true
icon: list
color: orange
---

# Tighten plan

You refine **`plan.md` and `tasks.md`** one issue at a time. `spec.md` is the source of truth. You do **not** edit the spec. You do **not** answer new product questions.

Do **not** offer a single menu (“fix the whole review”). That hides per-finding decisions.

**Do not patch until the user picks a resolution for the current issue** (or a batch of `P#: letter` answers). `suggest` is not a patch. `send-to-spec` is not a plan patch.

## Find the spec folder

Use the folder the user @-mentions. Otherwise the most recently edited tree under `docs/specs/` excluding `_template/`. If several, ask which slug. Expected headings: this skill’s `assets/plan.md` and `assets/tasks.md`.

Need `spec.md`, `plan.md`, and `tasks.md`. If plan/tasks are missing, stop (`/crav1-plan-from-spec`).

Read those three. Note `diagrams.md` / `adr/` / `export/openspec/` if present.

Also read the latest **crav1-plan-reviewer-agent** / `/crav1-review-plan` output in this chat. Those findings become issues. Do not collapse them into one “apply reviewer notes” action.

## Build the issue list (no edits)

Number issues `P1`, `P2`, … Each issue is **one** plan/task defect.

Sources, in order:

1. Numbered `P#`s already listed by the plan reviewer in this chat (preserve meaning; split if they bundled two problems). Keep their **plan** vs **spec** tag.
2. Fresh read of `plan.md` / `tasks.md` against `spec.md` (add only what the reviewer missed)

Typical **plan** shapes:

- `T#` too big to verify alone (“add authentication”)
- Missing `verify:` or `(spec: …)`
- Task or approach step invents behavior the spec does not require
- Acceptance / REQ with no task (or task with no spec line)
- Files likely touched wrong, missing, or not `(proposed)` when there is no repo
- Plan treats a kept-open spec question as decided

**Spec** tag: the plan is fine or cannot be honest until `spec.md` changes. Do not “fix” that by writing product behavior into the plan.

Skip nitpicks. Merge duplicates. Prefer fewer sharp issues.

If **no plan issues** remain (spec-tagged ones only, or none): say so. Next: spec-tagged → `/crav1-tighten-spec` / `/crav1-resolve-questions`; else **new chat**, `/crav1-implement-task` or `/crav1-complete-task` with `plan.md`, `tasks.md`, and `spec.md` attached.

## Walk one issue at a time

Walk **plan**-tagged `P#`s here. When the current item is **spec**-tagged: do not offer plan patches. Tell them `/crav1-tighten-spec` or `/crav1-resolve-questions` for that finding, mark it skipped-for-plan, advance.

### Index (every turn, short)

Remaining `P#` titles only. Mark the current one. Note plan vs spec.

### Current issue (full)

For **only** the current plan `P#`:

1. **Finding** — one or two sentences. Quote the plan/task line.
2. **Why it matters** — verify-ability, extra scope, or silent spec decision.
3. **Options** — 2–4 mutually exclusive **plan** resolutions, then **`suggest`**. Use the questions tool when available. Always keep `suggest`. Add `ask` / `keep` / `send-to-spec` when they fit.

Every option: **letter**, **name**, **what changes**, **impact** (which `T#`s / files). Never add a product feature as a “fix.”

4. How to answer: `A` / `B` / … or a batch: `P1 A, P3 C`. Unmentioned issues stay for later.

Stop. Do not edit. Do not preview a full patched plan.

If they already answered this `P#` with a **patch** letter in the same message, skip the menu and execute. If they asked for a suggestion, follow **When they pick `suggest`**.

### When they pick `suggest`

Do **not** patch. Stay on this `P#`. Name the letter you would pick and why (2–4 sentences). Re-offer the same patch letters. At most **one** alternate suggestion, then they must pick a patch letter, `ask`, `keep`, or `send-to-spec`.

### After a choice

1. Patch **only** `plan.md` and/or `tasks.md` as that resolution allows. Never `spec.md`.
2. Recap **Added / Removed / Still open** for this `P#`.
3. If `export/openspec/design.md` or `tasks.md` exist, update them to **match** (same tasks, no extra scope) when the resolution changed tasks.
4. Advance to the next unanswered `P#`. If none remain, give the empty-queue next steps above.

Do not start the next issue’s patch in the same turn unless they batched.

## Resolution catalog (per plan issue)

| Id | Name | What it does | Typical impact |
| --- | --- | --- | --- |
| `split-task` | Split this T# | Replace one oversized task with independently verifiable `T#`s. Renumber if needed; fix the trace table. | `tasks.md` (+ `plan.md` trace / approach if it named the old id). |
| `add-verify` | Add verify | Add or fix `verify:` (command, test name, or UI check) and `(spec: …)` if missing. | That `T#` line only, unless trace also lacked the spec id. |
| `drop-scope` | Drop extra scope | Remove the step/`T#` that is not in the spec (or move it to plan Out of scope). | Smaller task list; trace still covers remaining acceptance. |
| `fix-trace` | Fix trace | Map acceptance/REQ ↔ `T#`. Add a covering task or mark “covered by T#”. | `plan.md` Trace table; maybe one new `T#`. |
| `retarget-files` | Fix files likely touched | Correct paths; mark `(proposed)` if no repo. Do not invent a new architecture. | `plan.md` Files section. |
| `park-risk` | Park as risk | Plan was treating a kept-open question as decided. Remove that decision from tasks; list it under Risks. | No silent product answer. |
| `send-to-spec` | Send to spec | This is a spec defect or a new product question. Do not patch the plan. | No disk change here. Next: `/crav1-tighten-spec` or `/crav1-resolve-questions`. |
| `keep` | Keep as written | Accept the cost (usually untestable or extra scope). | No disk change. Rare; say the cost. |
| `suggest` | Get a suggestion | Recommend one offered patch letter. No edits. | Stay on this `P#`. Always offer. |
| `ask` | Ask, don’t patch | At most 3 questions about this issue. | Retry this `P#`. |

Do **not** offer `apply-notes` for the whole review.

## Hard rules

- Prefer **splitting or dropping** over adding product scope.
- Never edit `spec.md`, diagrams, or ADRs. Never write application code.
- Never resolve an Open question by encoding an answer in a `T#`.
- Do not start implement/complete-task in this chat unless they explicitly asked after plan issues are done.
- Do not patch “to be helpful” when they have not chosen a **plan patch** (`suggest` and `send-to-spec` are not plan patches).
