---
name: gap-and-contradiction-register
description: "Maintain `00-control/assumptions-questions-and-contradictions.md` — the assumptions and open-questions register (`AQ-####`) and the contradiction register (`CT-####`) — classifying each entry as blocking, material but non-blocking, or minor, and routing blocking gaps to owner resolution before drafting proceeds. Use when a source is silent on a required topic, when two sources disagree, or when a verification pass reports conflicting evidence for the same claim. This skill MUST be consulted because a documented unknown is a deliverable and a silently-filled gap is a defect — a package that papers over a contradiction transfers risk to the reader without telling them it exists."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
context: fork
agent: general-purpose
---

# Gap and Contradiction Register

Owns what the package does **not** know, and where its sources disagree. The evidence ledger asserts; this register refuses to.

## Iron Law

**NEVER RESOLVE A CONTRADICTION BY CHOOSING. Record both sides, name the decision impact, escalate to the owner.**

Picking the more convenient version is the single most damaging thing a documentation run can do, because the result is indistinguishable from a verified fact and carries the same authority.

## Two registers

| Register | ID | Records |
|---|---|---|
| Assumptions and open questions | `AQ-####` | Something required is not established: a silent source, an inaccessible system, an unstated owner, an assumption the package rests on |
| Contradictions | `CT-####` | Two or more sources disagree about the same claim |

Both live in one file because they answer the same reader question — "what is not settled here?" — and splitting them buries half the answer.

Column schemas and ID grammar: `references/register-schemas.md`.

## Gap classification

Classify on decision impact, not on effort to resolve.

| Class | Definition | Effect on the run |
|---|---|---|
| **Blocking** | Documentation would materially mislead a reader without resolution | Drafting of the affected document stops. Everything else continues |
| **Material, non-blocking** | The package can proceed with a visible qualification in the affected document | Draft with the qualification inline; the row stays open |
| **Minor** | Useful refinement, not decision-changing | Record it, draft normally |

Do not stall the entire package for a non-blocking unknown. A package delivered with twelve honest open questions is more useful than a package delayed indefinitely for one of them.

## Before escalating a blocking gap

In this order. Escalation is the last step, not the first.

1. **Search again by a different route.** A different search term, a different directory, git history, a schema, a test fixture, a configuration default. Most gaps are findable, and the first search was one route.
2. **Run a safe check** the action ceiling permits. An executed command answers what a document may only assert.
3. **Ask a concise, evidence-seeking question** — only if a person genuinely must resolve it, and only when `allowedActions.contactHumans` is true. Ask for the specific artifact, not for an explanation: "Is there an approved data-retention record for the analytics store?" beats "Can you explain how retention works?"
4. **Otherwise mark the affected claims and documents unresolved** and continue.

## Recording a contradiction

Every `CT-####` row carries:

- Both claims **verbatim**, each with its evidence ID, authority level, and observation date
- The likely cause — most contradictions are staleness, environment difference, or scope difference, not error
- The **decision impact**: which reader, making which decision, would be misled by picking the wrong side
- Current resolution or `unresolved`, with an owner and the next verification action

The likely-cause analysis matters because it usually dissolves the conflict. "The IaC says three replicas, the dashboard shows two" is often not a disagreement at all — it is a claim about the file and a claim about the running system, which are different claims and want different rows.

When authority levels differ, the higher level is *preferred*, not *correct*. Record both, prefer one, and say which and why. Higher authority is not the same as more current.

## Resolution

A contradiction is resolved when new evidence settles it — not when someone decides. Record the settling evidence ID and the reasoning. Both original rows stay in the ledger; the superseded one gains a `Notes` entry pointing at its successor.

An owner **accepting** one side without new evidence is not resolution; it is an accepted risk, recorded as such, with the accepting authority named. That distinction is what a diligence reader is actually looking for.

## Owner-decision items

Some rows cannot be closed by any amount of inspection: a business decision, a legal interpretation, a disclosure approval, a risk acceptance. Mark these `needs-owner`. They are not failures of the run, and they must not be quietly dropped at the end.

`needs-owner` rows block the release gate. That is deliberate — an unmade decision is a real reason a package is not ready.

## Output Format

Two tables in `00-control/assumptions-questions-and-contradictions.md`, plus the derived views below.

```markdown
## Assumptions and Open Questions

| ID | Question or assumption | Why it matters | Working position | Evidence needed | Owner | Class | Affected documents | Status |
|---|---|---|---|---|---|---|---|---|
| AQ-0001 | {question} | {decision it changes} | {what the package currently assumes} | {the smallest artifact that would settle it} | {role or `unassigned`} | blocking / material / minor | {paths} | open / resolved / needs-owner |

## Contradictions

| ID | Claim A (evidence, authority, date) | Claim B (evidence, authority, date) | Likely cause | Decision impact | Resolution | Owner | Next action |
|---|---|---|---|---|---|---|---|
| CT-0001 | {verbatim} [EV-0042, L2, 2026-07-20] | {verbatim} [EV-0043, L3, 2026-07-24] | {staleness / environment / scope / error} | {who is misled, deciding what} | unresolved | {role} | {specific check} |
```

Also emit, ordered by decision impact rather than by ID:

```markdown
### Blocking decisions
### Recommended evidence requests
| Request | Settles | Decision impact | Owner |
```

The evidence-request list is the highest-value output of this skill. It converts "we do not know" into "here is the one artifact that would tell us", which is the difference between a complaint and a deliverable.

## Rationalization Prevention

| Excuse | Response |
|--------|----------|
| "The code is authoritative, the doc is just stale" | Then say so in a `CT-` row with that as the likely cause. Do not delete one side. |
| "This contradiction is too minor to record" | Then it is a minor-class row and costs one line. Judging it minor without recording it is how it stops being minor unnoticed. |
| "I will ask the user about all twelve unknowns" | Ask about the blocking ones. The rest go in the register — that is what it is for. |
| "Nobody owns this component, so I will list the last committer" | The last committer is not an owner. `unassigned` is true; a name is a fabrication with consequences during an incident. |
| "The team will know which is right" | Then record both and ask them. Guessing on their behalf removes their chance to answer. |
| "It resolved itself once I read more code" | Then new evidence settled it — record the settling evidence ID. Silent disappearance is not resolution. |
| "This gap is unresolvable so there is no point recording it" | An unresolvable gap is exactly what a diligence reader most needs to see. |

## Integration

Invoked in Phase 3 of `/dossier:baseline`, throughout `/dossier:refresh`, and by `/dossier:reconcile` when a finding cannot be repaired by the agent. `finding-reconciliation` routes cross-pass disagreements here as `CT-` rows. `bin/dossier-gate.sh` reads the `needs-owner` and `blocking` counts as gate inputs.

References: `references/register-schemas.md`, `references/source-authority-and-claim-states.md`, `references/finding-schema.md`.
