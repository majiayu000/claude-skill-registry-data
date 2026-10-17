---
name: kanban-flow
description: Drive a kanban feature or bug through brainstorm, planning approval, start-or-backlog decision, implementation, testing, review and archive using the kf CLI. Use when the user requests the kanban workflow or resumes a work item managed in .works. Delegates each phase to its dedicated skill.
---

# Kanban Flow — Orchestrator

**The user describes the idea; the agent decides the rest.** One command runs the whole lifecycle; each phase runs a dedicated skill.

**ARGUMENTS:** `<context> <feature_name>` — e.g. `kanban auth user-login` or `kanban billing payment-timeout --type bug`

State is enforced by the `kf` CLI: artifact gates, approval fingerprints, execution ids, report statuses and traceability. The agent authors and verifies the content; file presence alone cannot prove that code was tested.

**Human boundary:** user participates in **Phase 1 (brainstorm/bug triage)**, **Phase 2 (approval)** and the explicit **start-now vs backlog** decision. After the user chooses start, run everything autonomously within the approved scope. Stop and ask only for a decision on backlog start, REQUIREMENT_BUG or a scope change; do not ask "continue?" between normal phases.

**Preflight:** if the project has no `.works/`, run `kf init --defaults` first (full bootstrap without prompts; use `kf init -i` when the user should answer the setup questions). Detect project stack/tooling by READING the repository — never assume.

---

## Phase model & artifact contract

```
brainstorm → planning → implementation → testing → review → dones
                 ↘ backlog ↗
```

Folder name: `{feature_name}_{timestamp}` (created by `kf new`). Artifacts follow `phase-{x}-{name}.md`.

| Phase | Skill | Gate artifacts (filled to LEAVE) | Notes |
|-------|-------|----------------------------------|-------|
| 1. Brainstorm / Bug triage | `kanban-brainstorm` or `kanban-bug` | `phase-1-spec-requirement.md` (`status: confirmed`) | Human + agent refine requirement or reproduce bug |
| 2. Planning | `kanban-plan` | Feature: four phase-2 files + `use-cases/UC-###(-<slug>).md`; bug: confirmed bug report | **Human approval, then start/backlog decision** |
| Backlog | — | Approved planning contract remains intact | Waiting for explicit user decision to start |
| 3. Implement | `kanban-implement` | — (tasks.md tracks) | Autonomous |
| 4. Testing | `kanban-test` | `phase-4-testing-result.md` (`status: PASS`) | FAIL/REJECT → loop to implementation |
| 5. Review | `kanban-review` | `phase-5-review-report.md` (`status: PASS`) | FAIL/REJECT → loop; REQUIREMENT_BUG → STOP |
| 6. Closure | `kanban-archive` | Feature: `phase-6-feature-report.md`; bug: current test/review evidence | Feature canonical docs or affected bug docs, then archive |

**Two gate layers on every move:**
1. **Artifact gate** — files exist and contain no template placeholders.
2. **Directional gate** — report `status` semantics: FAIL/REJECT blocks forward motion and forces a loop back to implementation; REQUIREMENT_BUG blocks **all** motion (STOP FEATURE — never silently rewrite the requirement).

For features, `kf validate` checks each `## TC-###` for FR references and matching individual UC files. Approval fingerprints the requirement, four planning artifacts and individual UC files. For bugs, approval fingerprints only the bug report; feature planning artifacts and feature report are not required. A changed contract must return to planning for human approval. Each entry to testing creates a new execution id; testing and review reports must carry that id in `execution:`. Read templates with `kf instruct <artifact> --change <feature>` to obtain the current id and exact output path.

Feature canonical docs are synced by the CLI on archive:
- Requirement: `docs/requirement/{context}/{feature_name}.md`
- Use cases: `docs/use-cases/{context}/{feature_name}/README.md`, one `UC-###(-<slug>).md` per use case and `diagram.md`
- Test plan/result: `docs/testplan/{context}/{feature_name}.md` and `{feature_name}-result.md`

Work item type is stored in `.kfw.json` as `kind: feature|bug`. Create a bug with `kf new <name> --type bug`; route it to `kanban-bug` for reproduction and triage before planning.

Bug closure updates the existing related feature docs only if needed. Do not auto-create feature docs for a bug or overwrite a feature requirement with bug-report content.

---

## How to delegate phases

The pipeline is ONE run but each phase has a specialist skill. Drive it like this:

```bash
kf status --all                # which phase is each feature in?
kf status --change {feature}   # current phase + artifact checklist + Next: + Approval
```

Then **load the skill for the feature's CURRENT phase** and follow it to its endpoint (each skill ends pointing at the next one). Do not re-read old phase instructions you've already executed; go straight at the target.

If planning is already approved and its fingerprint is unchanged, ask whether to start now or keep the item in backlog. If an item is in backlog, do not start implementation without an explicit user decision. If review has a current PASS report, the item is awaiting delivery — hand off to kanban-archive once the change has landed (a recorded `pr` merged, or the human confirms); `kf archive` refuses while a recorded PR is unmerged. If already in dones, validate and finish only missing closure work; never implement again. Resume existing artifacts and tasks instead of recreating the item or approved plan. `kf status --all` includes backlog and dones.

## Multi-agent harness

If `.kf/config.json` has `harness.stages`, some stages are assigned to **roles** (writer, coder, tester…), each backed by a runner CLI. Before doing a stage's work yourself, read `kf status --change {feature} --json`: when `assignedRoles` is non-empty, you are the orchestrator for that stage — do not do the work, hand it off:

```bash
kf run {feature}            # blocking; runs the stage's whole role chain in order
kf run {feature} --detach   # long stages (implementation): returns a chain id
kf runs {feature}           # poll until the runs are done, then read their STATUS
kf run {feature} --role writer   # re-run one role of the chain
```

A stage can list several roles (`brainstorm: ["researcher", "writer"]`); they run one after another and each gets told where the previous one wrote. If a role does not finish `DONE`/`DONE_WITH_CONCERNS`, the chain stops there and the later roles never run — read the log of the role that stopped, do not simply re-run the chain.

When polling a detached chain, check the chain column in `kf runs` (`1/2`, `2/2`): a run marked `chain stopped 1/2` means the later roles never ran, so the stage is **not** done even though nothing is running. Treat it like a stopped chain: read that role's log before deciding.

Then act on the worker's `STATUS:`: `DONE` → `kf validate --change {feature}` and decide the transition as usual (gates, not the worker's word, decide); `DONE_WITH_CONCERNS` → read the concerns in the run log, then decide; `BLOCKED` / `NEEDS_CONTEXT` → stop and ask the user. A run without a `STATUS:` line or with a non-zero exit is not done. Never do an assigned stage yourself unless the user says so. Human gates stay with you.

If you are resuming mid-pipeline (the feature already exists), skip straight to the phase skill for its current phase. **Never trust a folder location alone — a stage folder is not "done"; artifact + report completeness is.**

---

## Interaction policy

- User gives ONE command. Agent does everything else automatically.
- Brainstorm asks about **material ambiguity** only (missing scope, unclear behavior, conflicting acceptance criteria). Minor details → reasonable assumption + record it in the spec.
- Confirm the requirement in Phase 1, then obtain execution-contract approval in Phase 2. Present a tight summary + implementation plan and ask for approval. On approval run `kf approve`. Without approval, do not start autonomous execution.
- If scope must change after approval, stop implementation and explain the change. On the user's direction run `kf stage <feature> planning`, revise the contract and obtain fresh approval. REQUIREMENT_BUG blocks this route too; report it and await a human decision.
- Auto-fix benign blockers once. Stop + ask only when genuinely stuck.
- Never bypass a failed gate with `--force` unless the user explicitly approves.

---

## CLI reference

```text
kf init                        # scaffold .works/ + hooks + docs
kf doctor [--fix] [--json]     # diagnose the project; --fix applies the repairs needing no human decision
kf issues [view <n>|create|link|sync <feature>]  # GitHub issues on the configured repository, via gh
kf contexts [--json]           # declared contexts + counts, or a survey brief when none
kf new {feature} --context {ctx} [--type feature|bug]   # Phase 1: create feature/bug + seed spec
kf status --change {feature}   # artefact checklist + Next: + approval state
kf instruct {artifact} --change {feature}   # current execution id + exact output path
kf approve {feature}           # Phase 2 HITL gate
kf validate --change {feature}  # gate + traceability issues
kf stage {feature} {phase}     # move (gates + hooks run; planning → backlog/implementation)
kf run {feature} [--detach]    # run the roles assigned to the current stage (harness.stages), in order
kf runs {feature}              # worker run history (role, runner) + STATUS lines
kf archive {feature}           # the delivery gate: merged-PR check → review → dones + docs + issue close + board + delivered stamp
```

Contexts: a project may declare the ones it uses in `.kf/config.json`, and the first entry is the default. `kf new` refuses a context outside that list and names the nearest declared one; a case-only variant is refused too. Run `kf contexts --json` before `kf new` and use a declared name exactly. When `restricted` is false nothing is declared and any valid name works. Never add a context to the config to get past a refusal — naming a business domain is the human's call.

Phase hooks: `<project>/.kf/hooks/{phase}.sh` run automatically before entering a phase (project → user `~/.kf/hooks` → package precedence). Exit non-zero blocks the transition (`--skip-hooks` bypasses). The agent does NOT run hooks manually — `kf stage` does. Hooks also receive `KFW_REPOSITORY` when `.kf/config.json` sets `repository` (`owner/name`) — a hook that syncs work items to GitHub reads it rather than hardcoding the repo, and `kf issues` works off the same field. When `.kf/config.json` also has a `project` block (GitHub Projects board), hooks get `KFW_PROJECT_OWNER`/`KFW_PROJECT_NUMBER`/`KFW_PROJECT_AC_GATE`/`KFW_PROJECT_STATUS_<STAGE>`; `kf init` can seed the generic sync pack (issue on new, spec sync, AC gate at archive) into `.kf/hooks/`.

---

## Hard rules

- Do NOT ask "continue to next step?" — autonomous after the user chooses start at the Phase 2 decision gate.
- Obtain requirement confirmation and planning approval; after approval continue within the approved scope.
- After planning approval, explicitly ask whether to start implementation now or move to backlog. Never infer this choice.
- Never `mv` feature folders manually — always `kf stage` / `kf archive`.
- Never bypass a failed gate with `--force` unless the user explicitly approves. Every real bypass (`--force` on a failing gate, `--skip-hooks` on an existing hook) is recorded in `.kfw.json` and reported by `kf status`/`kf validate`.
- Always write `phase-4-testing-result.md` and `phase-5-review-report.md` — gates enforce it.
- FAIL/REJECT loops back to implementation and re-testing before review. REQUIREMENT_BUG → STOP, never rewrite the requirement. When the item should be dropped for good (requirement wrong at the root, work superseded, user says stop), **propose** `kf cancel {feature} --reason "<why>"` and let the user decide; never cancel on your own. Reopening later is `kf stage {feature} <the stage it was cancelled from>`.
- No scope creep beyond the approved plan.
- Follow the project's AGENTS.md and the user's permissions. Autonomous execution does not authorize unrelated changes, database operations, deployment or messages to others.
- Never silently swallow errors. If a step can't complete and can't be auto-fixed, STOP and report.
- The user's single command IS authorization for the full pipeline — up to the Phase 2 approval gate.
