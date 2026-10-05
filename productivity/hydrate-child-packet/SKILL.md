---
name: hydrate-child-packet
description: Create an initiative child task packet in the selected child row's `Packet Root` at `.plans/<task-slug>/` with imported context, placeholder plan ownership, and packet-phase bootstrap metadata before planning begins.
---

# hydrate-child-packet

Use only after split review is `ready` and the chosen child row is `ready` in `TASK_GRAPH.md`.

## Read first
- `../references/initiative-packet-contract.md`
- `../references/initiative-workflow-contract.md`
- `../references/task-packet-contract.md`
- `../references/final-state-authoring-policy.md`
- parent initiative `INDEX.md`, `BRIEF.md`, `UBIQUITOUS_LANGUAGE.md`, `DECISIONS.md`, `INVARIANTS.md`, `REPO_MAP.md`, `CONTRACTS.md`, `TASK_GRAPH.md`, `OPEN_QUESTIONS.md`
- `../../references/communication-mode.md`

## Create in the selected child row's `Packet Root` at `.plans/<task-slug>/`
- `INDEX.md`
- `BRIEF.md`
- `PLAN.md`
- `AMENDMENTS.md`
- `ARTIFACT_CANDIDATES.md`

Optional later file:
- `CONTRACT_DECISION.md`

## Required bootstrap semantics
- `PLAN.md` must say `Status: not_authored`
- `INDEX.md` must say `Packet phase: hydrated_for_planning`
- `BRIEF.md` must contain `Parent Initiative`, `Packet Root`, `Imported Context`, `Goal`, `Repo Scope`, `Scope`, `Out of Scope`, `Contract Surface`, `Dependencies`, and `Validation Expectations`
- imported context is a frozen subset, not a giant copy of the parent packet
- when hydrating into another repo, write child-packet references from the child repo's perspective:
  - `Parent Initiative` points back to the orchestrating repo initiative packet
    - use a relative path when the parent initiative repo is available locally from the child repo
    - otherwise use a repo-qualified reference
  - `Packet Root` is the child packet's repo-local owner path in the current repo/root, usually `.` at repo root
  - do not paste the parent row's raw cross-repo `Packet Root` locator into the child packet metadata

## Parent updates
- set the hydrated child row in `TASK_GRAPH.md` to `active`
- do not mutate parent initiative status here
- keep the parent initiative packet in the orchestrating repo; hydration only creates the execution packet in the child row's `Packet Root`

## Writing rule
Write the child packet as a clean execution shell.
Do not leave notes about older packet shapes or migration residue inside canonical child files.

## Do not
- author the real child plan here
- invent parallel packet files
- copy the whole initiative packet into the child brief
- duplicate a child packet in both the orchestrating repo and the owner repo

## Communication
Honor active caveman mode for user-facing replies per `../../references/communication-mode.md`. Keep durable artifacts normal unless the human asks otherwise. Drop caveman for safety/clarity when needed, then resume.
