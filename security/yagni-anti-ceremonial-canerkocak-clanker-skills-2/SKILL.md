---
name: yagni-anti-ceremonial
description: >
  Always-on YAGNI and anti-ceremonial gate for proposed guards, fallbacks,
  recovery rails, symmetry changes, policy findings, and legacy handling.
  Determine applicability and the current contract before producer and inventory
  checks; include code, manual, migration, replay, recovery, and external
  producers. Use when reviewing decision-changing feedback or touching money,
  auth, remediation, dead paths, or legacy state. Also use when drafting issues
  or plans that turn findings into proposed work or acceptance criteria.
---

# YAGNI and anti-ceremonial gate

Default to the smallest change that closes a current contract. A logically
possible guard is not automatically useful code. Equally, an empty database
snapshot does not prove a state can never be produced again.

Use native repository search plus semantic-blast-radius for producers and
consumers. Use an authorized database skill for inventory. Use
migration-apply-time when a migration's mutability matters. Do not depend on a
named navigation tool that is unavailable in the current environment.

## Issue and plan scope gate

For a writing-only task, use existing evidence first. Do not launch a code audit
or inventory sweep merely to polish an issue. Apply the technical decision order
below when a material claim needs further verification; otherwise state the
specific evidence limit.

Before turning a finding into requested work:

1. Identify the requested outcome and destination audience. Separate the user's
   requested breadth from findings that merely appeared in the same research.
2. Check what is already completed in the relevant deployment. Keep completed
   work as brief context only when it changes the remaining task; do not reopen
   it as an acceptance criterion without new evidence.
3. Distinguish observed behavior, demonstrated contract violations, and policy
   proposals. A different fee, limit, or behavior in a sibling path does not by
   itself prove a defect or require symmetry. Preserve unresolved policy as a
   concrete decision, not an implementation instruction.
4. Keep requirements that are necessary for the requested outcome. Put unrelated
   findings outside the candidate's requirements. If the user explicitly asks
   for related status or a combined issue, include it with clear scope; do not
   turn independent work into a completion dependency by accident.
5. Test each reference, status row, and acceptance criterion for a reader-facing
   purpose: does it change understanding, verification, ownership, or action?
   Remove research chronology and decorative provenance. Preserve evidence and
   uncertainty that materially affect the decision. Use prompt-leakage for
   whether retained references depend on access to the source conversation.

A configured value proves configuration, not adequacy against operating costs.
A recommendation proves a proposal, not that it was adopted for every path.
Do not inflate a narrow issue with a new fee framework, telemetry project,
governance process, or generic test checklist without a demonstrated need.

Before delivery, compare the title, body, and completion criteria: all must
express the same remaining scope. Report only the useful conclusion and evidence
limits; the full classification worksheet is not required in an issue draft.

## Mandatory decision order

Run this order before adding or accepting a check, fallback, guard, recovery
path, or symmetric branch.

### 0. Reachability envelope

Bind the claim to the exact target before searching for hypothetical states:

- branch, deployment, and rollout epoch;
- supported product entry points and input shapes;
- unsupported inputs that still matter because an untrusted caller can reach a
  security boundary;
- historical versions or formats that actually shipped to that target;
- residual state that can survive into the cutover;
- explicit non-goals and authorized scope.

Use evidence already available and stop when it disproves a load-bearing
premise. Do not run an inventory query for a format that never shipped to the
target. A staging-only producer does not establish production inventory. A
technically constructible custom client request is not a product-support
obligation, although it may still be a security input at an untrusted server
boundary.

### 1. Applicability

State the current product or metric contract. Ask whether the proposed bad state
can change that contract. A reachable state may still be not applicable to the
claim—for example, a record outside the cohort or valuation basis.

If it cannot change the contract, classify N/A with the semantic reason. Do not
continue merely to justify code.

### 2. Intent and policy

Search the current specification, durable code comments, tests, commit and PR
history, rollout records, and incident history for the intended behavior,
acknowledged residual risk, and explicit non-goals. Resolve contradictions by
authority and recency; do not count repeated reviewer wording as policy evidence.

If the reachable behavior and its residual exposure match the current documented
contract, and no higher-authority contract or observed breach contradicts it,
classify POLICY rather than a defect. A comment or commit proves engineering
intent, not necessarily organizational authority. When authority is material but
cannot be established, classify PARTIAL and name the missing evidence. Never
invent an approval role, written-acceptance requirement, or governance process.

### 3. Authorized scope

If the state is applicable and reachable but belongs to a different product
contract or would materially expand the user's requested work, classify
FOLLOW-UP. Report it; do not silently implement it in this candidate.

### 4. Producer set

Enumerate every producer class that can create the state today:

- current application, worker, API, queue, or database code;
- admin endpoints, scripts, and manual operator actions;
- migrations, backfills, imports, replays, retries, and recovery jobs;
- external integrations, webhooks, chain events, and legacy clients;
- historical producers that may have left residual inventory.

No code producer is not no producer. Record inaccessible producer classes as an
evidence gap.

### 5. Inventory and identity

Query the authorized environment at the exact row or event identity and grain.
Record database, role, time, cohort, and predicate. Inventory greater than zero
can make a dead producer operationally relevant. Inventory zero is only a
timestamped snapshot; it supports CEREMONIAL only when the producer search is
also complete enough to show the state cannot recur.

### 6. Reachability and harm

Show the transition by which a user, operator, external system, or recovery
process reaches the state and the concrete contract violation it causes. A
similar sibling branch is not reachability evidence.

### 7. Authority

Ask whether the proposed change alters who may move money, credit, settle,
withdraw, retry, or mark state terminal. Treat authority gaps as high risk, but
still prove the actual boundary. A check on an unreachable branch is theater.

### 8. Evidence strength

Distinguish source proof, runtime proof, synthetic tests, and inference. A
copied expression can verify arithmetic logic; it cannot prove the production
query, data cohort, role, or deployed boundary. Mark the result PARTIAL when a
material producer or runtime boundary is inaccessible.

## Classification

| Label | Meaning | Action |
|---|---|---|
| **LIVE** | Applicable producer and harmful reachable transition exist. | Implement the smallest current-contract fix. |
| **RESIDUAL** | Producer is gone, but applicable inventory remains. | Heal or support the inventory; prefer bounded remediation over permanent branches. |
| **POLICY** | Reachable behavior and acknowledged exposure match the current documented contract. | Do not report a defect or recommend a fix. Record policy reconsideration separately only when it is requested or materially relevant. |
| **N/A** | State cannot affect the named contract, cohort, unit, or metric. | Decline for this claim. |
| **FOLLOW-UP** | Real issue, but outside the authorized candidate. | Report separately; do not smuggle it into the patch. |
| **CEREMONIAL** | No current producer, no residual inventory, and producer coverage is sufficient to rule out recurrence. | Decline code. |
| **THEATER** | The code looks protective but does not change a reachable authority or failure boundary. | Decline code and state the real boundary. |
| **PARTIAL** | Evidence is useful but producer, inventory, identity, or access coverage is incomplete. | Do not greenlight or dismiss; name the missing proof. |

## Review-feedback gate

For every suggested change:

1. Restate it as: In target T, producer P can create state S, which is
   applicable, reachable at rollout R, and harmful to contract C.
2. Record the strongest intent/policy evidence and the strongest counterevidence.
3. Run the decision order above.
4. Implement only LIVE or justified RESIDUAL work inside the authorized scope.
5. Keep POLICY, N/A, FOLLOW-UP, CEREMONIAL, THEATER, and PARTIAL distinct.

Forbidden justifications without evidence include cheap so why not, better safe
than sorry, defense in depth, and the sibling function has it. Never perform
agreement before verification.

The consolidating agent owns the final classification. A delegated reviewer,
automated tool, priority badge, repeated conclusion, or verified call-chain edge
does not adjudicate the defect. Rechecking the same path with the same product
assumption corroborates mechanics; it is not orthogonal evidence of a contract
violation.

## Decision bridge and remedy safety

Before a technical finding changes a payment, merge, deployment, production, or
acceptance recommendation, cite the user instruction or governing contract that
connects the verified finding to that decision. Without that bridge, keep the
finding informational. A technically real exposure does not create an unstated
payment or governance condition.

Before recommending a state-machine or accounting change, name the canonical
state or cost owner and enumerate producers, writers, readers, retries,
terminal transitions, triggers, and compensating calculations. Show why the
remedy is exactly-once and cannot double-count, reopen terminal state, or move
the inconsistency to another reader. If this non-interference proof is missing,
classify PARTIAL and request proof rather than code.

## Default build stance

- Prefer one atomic current path over guards on a dead split path.
- Prefer bounded repair of residual rows over permanent compatibility code.
- Prefer deleting false legacy documentation over encoding its story forever.
- Do not create an abstraction solely to make unrelated surfaces symmetrical.
- Preserve an explicit boundary when owners, units, lifecycle, authority, or
  change cadence differ.

## Compact output

~~~text
classification: LIVE | RESIDUAL | POLICY | N/A | FOLLOW-UP | CEREMONIAL | THEATER | PARTIAL
contract/applicability: <why S can or cannot affect C>
intent/policy: <current contract evidence and authority>
producer set: <classes searched and evidence>
inventory: <environment, role, timestamp, predicate, count or NOT CHECKED>
reachability/harm: <transition and violated contract>
authority: <changed boundary or unchanged>
counterevidence: <strongest evidence against the claim>
evidence limit: <none or exact gap>
decision bridge: <contract linking this result to the requested decision or NONE>
remedy safety: <canonical owner and non-interference proof or NOT ESTABLISHED>
action: <smallest fix, remediation, decline, follow-up, or proof needed>
~~~
