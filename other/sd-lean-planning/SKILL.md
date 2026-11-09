---
name: sd-lean-planning
description: Generate a lean feature plan with tlc-spec-lean and an independent review, stopping at frozen, proof-backed checks with no task breakdown. Use when user says 'lean plan', 'plan this feature lean', 'plan with spec-lean', 'sd-lean-planning', or wants one reviewed plan and obligations instead of a spec, design and task list.
model: opus
effort: high
disable-model-invocation: true
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

# Steps

See [diagram](references/diagram.md) for a visual flow overview.

Add the following steps as tasks using the `TaskCreate`, `TaskUpdate`, `TaskGet`, and `TaskList` tools. Update the status as you progress through each step to keep the user informed.

This skill wraps the first two phases of `/tlc-spec-lean` and changes two things in them, because `plan.md` and `checks.md` freeze early and the review has to land first:

- The plan is reviewed **before** it is presented, since approval is the one default stop for a human.
- It stops after Checks. `references/checks.md` tells the agent to continue into Build without waiting; here Build belongs to `/sd-lean-execute`.

1. **Settle open architecture first.** Check the definitions in [docs-adr](../sd-planning/references/docs-adr.md). An open bet that meets the criteria (which of two architectures, job or request cycle) is settled in an ADR before the plan, which then records the shape that won. Offer the ADR to the user; skip this step when no such bet exists.
2. **Plan.** Execute the `/tlc-spec-lean` skill and follow its `references/plan.md` up to and including `validate_plan.py <feature>` exiting 0. Do not present the plan yet. For a change under roughly three files with no one-way door, write only `checks.md` with its `## Intent`, without running `validate_checks.py`: step 3 then reads that file, step 4 presents it, and step 5 skips straight to its gate.
3. **Verifier pass (always-on, author ≠ verifier):** dispatch a fresh sub-agent — no inherited context from steps 1-2 — to run `/sd-review-spec` in report-only mode against `plan.md` (or `checks.md` on the short path) and any cited ADRs. Give it only: the original feature request (verbatim, as the user stated it), and the feature's spec dir path. It audits every doc claim against the real code and checks the full set covers everything the original request needs — scope, constraints, edge cases and dependencies. It does not edit anything; it returns the severity-classified gap report (same table as `/sd-review-spec` step 8). If gaps exist: show them to the user and apply fixes per `/sd-review-spec` steps 4-7, then rerun `validate_plan.py`. Do not skip this step and do not ask the user whether to run it — only ask what to do with findings.
4. **Approval.** Present the plan as `references/plan.md` "Then confirm" says, and offer `/spec-to-requirements-table` as a plain-language review sheet. It is a reading aid, not a gate: run it only if the user accepts, settling the output language first, because it runs isolated and cannot ask. Then stop. Write `**Approved**: <YYYY-MM-DD> - user: "<their words>"` only from words the user gave. On the short path there is no `plan.md` and no approval line: the user's go-ahead on `checks.md` is what lets step 5 run.
5. **Checks.** Follow `/tlc-spec-lean` `references/checks.md` to write `checks.md` from the approved plan. Before `validate_checks.py` freezes them, dispatch a fresh sub-agent with `/sd-review-spec` in report-only mode, given only the spec dir, to confirm every criterion in `plan.md` has a check and each proof reaches its claim: `validate_checks.py` only checks structure, not that traceability. Apply the fixes, then run `validate_checks.py <feature>` until it exits 0. **Stop here: do not continue into Build.**
6. At the end of the session, evaluate whether there is anything worth saving as permanent memory. Save as permanent memory only what the next session will need and cannot rediscover by reading the code, Git, or CLAUDE.md—such as the _reason_ behind a decision, a non-obvious invariant, or a user preference; if it is already in the repo or only matters for this specific conversation, do not save it. Use the `ai-memory-durable-pages` skill to persist it.

Tell the user the next step is `/sd-lean-execute <feature>`.
