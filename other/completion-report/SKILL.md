---
name: completion-report
description: Produce the smallest user-facing report that preserves every material fact about a task outcome, by classifying the terminal state, comparing it against the contract, filtering activity out, and checking that no material fact was lost to compression. Use this skill at a task boundary — when work is complete, partial, blocked, or failed — whenever the user asks what the outcome was or for a summary of what was accomplished, and whenever an execution run ends and its result must be communicated. Reports consequences and evidence, never the execution trajectory.
metadata:
  author: "Giuliano Lemes <giuice@gmail.com>"
---

# Completion Report

Produce the report that preserves the most material state in the least text.

Two rules generate everything else:

> **No material fact may be lost merely because the answer must be concise.**
>
> **No execution detail survives merely because it happened.**

## Boundary

This skill only communicates. It does not plan, replan, execute, verify, or repair. If work can still continue, control belongs to `execute-plan` or `plan-from-spec` — not here.

It also does not invent evidence. If something was not verified, the report says so.

## Inputs

From `spec-interview/<slug>/`:

- **the contract** — `SPEC.md` when it exists; otherwise the `Goal` in `PLAN.md` plus the union of the `Done when` conditions in the current plan **and** those the ledger records as satisfied — completed tasks leave the plan on replan, so part of the contract survives only in their ledger entries;
- **`LEDGER.md`** — the record of what became true, with each entry's `Covers`, evidence, and verification label;
- **`PLAN.md`** — for the goal statement and any task that never produced a ledger entry.

Without a ledger, reconstruct the material facts from the run before reporting — but say nothing you cannot ground in an observation that actually happened.

Never reconstruct the goal from the execution trace. Read the contract.

---

## Step 1 — Classify the terminal state

Do this before writing a word.

| Status | Meaning |
|---|---|
| `COMPLETED` | Every required acceptance criterion is satisfied, with evidence |
| `PARTIAL` | A meaningful subset is done; one or more requirements remain unsatisfied |
| `BLOCKED` | Cannot continue without external access, information, permission, or a user decision |
| `FAILED` | The required state was not reached and no valid continuation is available |
| `NO_OP` | The requested state was already true; no change was needed |

`NO_OP` applies when every ledger entry is `no_op`, or when `PLAN.md` carries `Status: no-op` and no tasks — in which case its `Already true because` and `Evidence` lines are your whole input. Report it plainly; do not dress an already-satisfied goal up as work.

Never upgrade `PARTIAL`, `BLOCKED`, `FAILED`, or unverified work to `COMPLETED` to produce a cleaner answer.

## Step 2 — Compare the final state to the contract

Ask what the contract requires — not whether the executor said it finished.

Join ledger entries to criteria through each entry's `Covers`. Build this internally; it is scaffolding, not output:

```
AC-001  satisfied     verified    integration test passed
AC-002  satisfied     verified    build passed
AC-003  satisfied     attested    the user confirmed the six accepted invitations
AC-004  unsatisfied   —           test database unavailable
AC-005  unverifiable  unverified  requires production access
```

`COMPLETED` requires every criterion in the `satisfied` column. Anything else downgrades the status.

**When several entries cover one criterion** — a task that ended `partial` and the later task that finished its remainder — judge the criterion on the combined record, not the last entry alone. A later `verified` entry supersedes an earlier `unverified` one for the same criterion. An `Unresolved` item that no later entry closed keeps the criterion unsatisfied, however many entries came after it. On a run with no SPEC, join on the `Done when` text the ledger copied instead of on `Covers`; an entry whose `Restates:` text matches an earlier entry's `Done when` continues that same criterion.

`attested` — a person confirmed it — is satisfied. It is weaker than a machine check, so the report names it as confirmed rather than measured, but it does not block completion. Otherwise no work outside an automatable domain could ever complete.

The report is the projection of **contract × final state × evidence** — not of the executor's summary. This is what stops the implementer from being the sole judge of its own success.

## Step 3 — Select material facts

> Report consequences, not activity.

A fact is **material** when omitting it could change the user's understanding of: what outcome was achieved, how behavior changed, whether the contract was met, whether the result was verified, what risk remains, what is still incomplete, what the user must do next, or whether compatibility changed.

```
NON-MATERIAL                      MATERIAL
opened five files          →      (nothing — omit)
ran a search               →      (nothing — omit)
retried a command          →      (nothing, unless it changed the outcome)
fixed formatting           →      (nothing — omit)
modified IUserRepository   →      the repository interface gained an email lookup,
                                  so other implementations must add it
```

The filename can follow the consequence for traceability. It never replaces it.

## Step 4 — Check coverage before compressing

Every material fact gets exactly one disposition: `REPORT`, `MERGE` (fully carried by another sentence), or `OMIT` (implied by a reported fact, or has no user-visible consequence).

These may never be silently omitted when present:

```
- an unsatisfied acceptance criterion
- a failed verification
- an unverified completion claim
- changed external behavior
- a changed public contract or interface
- changed user data
- a destructive or irreversible action
- an unresolved blocker
- remaining risk
- required user action
- a material deviation from the contract
- an assumption that materially affected the result
```

The ledger carries these as `State delta`, `Unresolved`, `Risk`, `User action`, and `Deviation`. Read all five; the outcome is not in `State delta` alone.

This list is the semantic checksum. The question is never *"is this concise?"* — it is *"does this concise version still carry every material fact?"*

## Step 5 — Distinguish implemented from verified

`implemented`, `verified`, `attested`, and `not verified` are four different states. Never collapse them.

A success claim must trace to an acceptance criterion satisfied, a check that passed, an observed state, a tool confirmation, an inspected artifact, or an explicit human confirmation.

```
WRONG   Everything is working correctly.
RIGHT   The parser change is implemented. Unit tests pass; integration tests were not run.
```

When verification is unavailable, say so in one clause. Do not hide it and do not apologize for it.

## Step 6 — Order and render

Render in this order, and render **only** the sections that carry material information:

```
1. OUTCOME
2. MATERIAL CHANGE
3. VERIFICATION
4. RESIDUAL STATE
5. USER ACTION
```

Do not emit empty headings. A simple successful task is two sentences with no headings at all. Length follows the amount of material information — nothing else.

Compression order: **coverage first, compression second, style third.** No word limit; hard limits cause omission.

### Language rules

- One concept, one term, throughout.
- Concrete nouns and verbs. Active voice when the actor matters.
- Keep cause and consequence in the same sentence.
- One proposition per sentence when combining them creates ambiguity.
- Report state, not self: *"The build passes"* — not *"I successfully ran the build."*
- No decorative transitions, no synonyms for variety, no generic success language.

```
AVOID                                  PREFER
Everything looks good.                 The requested endpoint is implemented.
The task was completed successfully.   The build passes.
Several improvements were made.        The integration test remains blocked by the
The code was updated accordingly.      unavailable database.
```

### Forbidden

```
- execution narration with no consequence
- unsupported success claims
- invented next steps
- restating the user's request before the outcome
- the same fact stated twice
- a hidden failure or a hidden unverified state
```

---

## Examples

Each shows a distinct terminal state or evidence class. Match the shape, not the domain.

**COMPLETED**

```
Implemented authenticated user lookup by email without changing the endpoint contract.
The build and 38 relevant tests pass.
```

**COMPLETED with a compatibility consequence**

```
Implemented authenticated user lookup by email. The repository interface now requires
an email lookup operation, so other implementations of that interface must add it.
The build and 38 relevant tests pass.
```

**COMPLETED on attested evidence — a non-code run**

```
All six candidate interviews are scheduled for the week of 3 March, each in a slot the
candidate accepted in writing. Two candidates required an evening slot, so the panel
runs until 19:00 on Tuesday and Thursday.
```

**PARTIAL**

```
The service implementation is complete and builds successfully. The integration test
could not run because the test database is unavailable, so the database-dependent
behavior remains unverified.
```

**BLOCKED, user action required**

```
Production deployment is blocked because production credentials are unavailable.
Version 2.4.0 passed the staging checks; production was not changed.
Provide production deployment access to continue.
```

**NO_OP**

```
No change was needed. Nullable reference types are already enabled globally for the project.
```

---

## Persisting the report

Render the report in the conversation. Also write it to `spec-interview/<slug>/REPORT.md` with the status and date in a header, so the folder holds the complete record of the work.

Skip the file when there is no working directory — for a one-off report, the conversation is the delivery.

---

Design rationale — **non-normative**, and older than this skill: [docs/completion-reporter-design.md](../../docs/completion-reporter-design.md). It explains why the protocol is shaped this way, at much greater length, and it predates the `attested` verification label. Where the two disagree, this file wins.
