---
name: adopt
description: Run-once onboarding for a fork of a project that ships this governance pack. A maintainer's clone carries accumulated operational working-state (audit-trail registers, session handoff, a queue of next actions, per-document review anchors) that is meaningless to a fresh adopter; this skill either resets present machinery-core working-state to clean adopter baselines or, when the configured working-state location is absent, treats it as already clean and creates only the adopter-local state a public versioned consumer requires, settles how the adopter will handle the project's optional external dependencies (their own, or self-contained with in-repo stubs `/adopt` creates or functional in-repo substitutes), strips maintainer-only operational residue, and records the adopter's choices in the project's committed adoption marker so the resume mechanism proceeds in adopter mode without re-asking. It runs ONLY on a confirmed adopter fork (a fork origin), never on the upstream maintainer repository or an upstream maintainer's fresh-machine clone, and only once (an existing adoption marker short-circuits it).
derives_from: ../../governance/session-lifecycle.md
---

# Adopt (run-once fork onboarding)

## Project wiring (the parent library's instantiation; adopters substitute their own)

Portable procedure, concrete names. In the parent GRC library this skill runs with:

- Operator classifier: `tools/detect-env.py` (its `probe_identity` block prints an
  `operator_identity` of `maintainer` / `maintainer-fresh-machine` / `adopter`,
  by the git `origin` remote against `jposluns/grc_library` plus sibling presence).
- Adopt-config: `.claude/adopt-config.json` (committed by the adopter; its presence
  marks the fork adopted and is what the resume step reads to skip re-onboarding).
- Sibling placeholders: the OPTIONAL in-repo `.ref` / `.scratch` / `.private` stubs that
  `/adopt` can create to stand in for `grc_library_ref` / `grc_library_scratch` /
  `grc_library_private` when a sibling is absent (not shipped by default; a present stub's
  shape is guarded by the sibling-repo stub-guard gate, guard-if-present-as-stub).
- Machinery-core working-state (the reset target): the gate-read `.working/` files
  that a maintainer's clone fills with operational history, enumerated in step 3.
- Resume wiring: the `/orch` resume command proposes `/adopt` when the classifier
  says `adopter` and no adopt-config exists; once the config is present, resume
  proceeds in adopter-mode.
- Reference-acquisition manifest + bootstrap planner (sibling model, enrichment): the public
  bibliography `/adopt` can bootstrap an EXTERNAL `.ref` from (`docs/reference-acquisition-manifest.md`),
  and the planner `tools/adopt-bootstrap-ref.py` that categorizes it into auto-fetchable /
  free-manual / licensed-manual (PR #1007). Adopters substitute their own equivalents.

An adopting project maps each bullet to its own classifier, config, placeholders,
working-state, and resume flow; the procedure below refers to them generically.

## Overview

A project that distributes this pack may be designed to be cloned and run by a fork (its
governed content, the pack, its audit tooling, and its gates all run without the maintainer's
optional external dependencies, the adopter-clone portability invariant). But a maintainer's
clone also carries operational WORKING-STATE that is the maintainer's, not the adopter's:
audit-trail registers, the session handoff and its queue of next actions, work ledgers,
pending-decision and override queues, and per-document review state. The parent GRC library's
concrete inventory of those surfaces is enumerated, with that provenance labelled, in step 3;
an adopting project maps it to the state surfaces its own workflow keeps. Carried into an
adopter fork unchanged, that state is at best noise (a queue of next actions for work the
adopter is not doing) and at worst misleading (a session handoff asserting surfaces clean that
the adopter has since changed).

`/adopt` is the run-once onboarding that resolves this. It confirms the clone is genuinely
an adopter fork (not the maintainer's own repository, and not a maintainer's fresh-machine
clone that merely has not fetched its optional external dependencies yet), settles how the
adopter will handle those dependencies (in the parent GRC library, the sibling
repositories named in the project wiring above; its former worker-exchange sibling is retired, so only
the reference-base and private-operational siblings apply to the maintainer, while an adopter may still keep
its own worker-exchange repository), resets the machinery-core working-state to
clean baselines the adopter starts fresh from, strips maintainer-only operational content, and
records the adopter's choices in the project's committed adoption marker. After it runs once,
the project's resume mechanism reads that marker and proceeds in adopter mode without
re-asking.

It is deliberately conservative: it runs only on a confirmed adopter clone, only once, and
it resets working-state to EMPTY baselines rather than fabricating adopter history. It
seeds nothing else in the first cut (no starter backlog, no example sweeps); the adopter
builds their own history from a clean slate. It never deletes the governed project content,
the pack, the tooling, or the gates, which are the product the adopter came for.

## When to Use

- On the FIRST resume of a freshly-cloned adopter fork, when the operator classifier
  reports `adopter` and no adopt-config exists (the resume step proposes it).
- Ad-hoc, when an adopter wants to re-baseline their working-state (with the maintainer's
  or their own governance authority's awareness, since it clears working history).

Do NOT use it on the maintainer's own repo, on a maintainer's fresh-machine clone (the
fix there is to clone the siblings, not to reset working-state), or a second time on an
already-adopted fork (the existing adopt-config short-circuits it).

Execute the onboarding per the seven-step process:

### 1. Confirm this is an adopter clone, and that adoption has not already run

Run the operator classifier named in the project wiring and read its configured identity result.
Proceed ONLY if it is `adopter`. If it is `maintainer`, STOP (this is the maintainer's
repo). If it is `maintainer-fresh-machine`, STOP and advise cloning the required sibling
repositories instead (in the parent GRC library, `grc_library_ref` and `grc_library_private`; the retired
`grc_library_scratch` is never cloned) (a fresh maintainer clone is not an adopter; resetting its
working-state would destroy the maintainer's audit trail). If an adopt-config already
exists, STOP (the fork is already adopted; re-baselining is the ad-hoc case above and
needs explicit confirmation). A misclassification in the dangerous direction (a maintainer
treated as adopter) is foreclosed by the classifier's host-pinned origin match, but confirm
the classification with the operator before any reset.

### 2. Choose the sibling model

Ask the adopter how they will handle each optional external dependency named in the project
wiring, and record the choice:

- **External dependencies**: the adopter supplies its own configured external resources and
  records their locations for the project's resolver.
- **Self-contained**: the adopter uses project-supported in-repository substitutes,
  placeholders, or clean no-op degradation for the optional resources it does not supply.

The parent GRC library's three-sibling choices are labelled in the project wiring above.
The dependency model is an authorial decision for the adopter; surface the supported
options with their consequences and do not pick silently.

### 3. Reset the machinery-core working-state to clean adopter baselines

First determine whether the configured working-state location is PRESENT. A fresh public
clone may find it ABSENT (in the parent GRC library the public working-state tree was removed
once it moved to the maintainer's private sibling). If it is ABSENT, treat working-state as
ALREADY CLEAN. There is no maintainer history to read, clear, preserve, or reconstruct, and you
do NOT recreate an absent working-state tree to reproduce its former inventory. Create only the
adopter-local working-state your chosen dependency model (step 2) actually needs, deriving each
file's SHAPE from the public versioned consumer (a gate, a tool, or a slash command) that reads
it, never from a deleted file; if no public schema or template backs a former historical
surface, create nothing and invent no history. Then continue to step 4. The rest of this step
applies only when working-state is PRESENT.

For each machinery-core working-state surface, clear the maintainer's accumulated content
to an empty or stub baseline the adopter starts fresh from, preserving each file's required
SHAPE (headers, metadata blocks, table headers, and the lifecycle fields the gates
validate) while emptying its DATA rows. Seed nothing else in the first cut. Enumerate the
surfaces from the project's own configuration before clearing any of them; the parent GRC
library's inventory, recorded here as its provenance and mapped by an adopting project to the
equivalent surfaces its own workflow keeps, is: the session-concurrency lease and the session
handoff (reset to a clean stub with a released lease and an empty queue); the audit-trail
registers (validation-sweep history, per-PR validate-pr history, the retrospective log, the
credit-offload metrics, the reference-audit history and per-document state) reset to their
header plus an empty table; the closed-work ledger and the next-actions projection emptied;
the pending-decisions and verifier-override queues emptied to their `Status: empty` form; the
overnight-work file reset to its stub; the deep-assessment register emptied; and the detailed
change-log mirror reset to an empty current period. Do NOT reset the governed project content,
the pack, the tooling, the gates, the primary change record, or the version surfaces (the
adopter inherits the version lineage). Clearing the pending-decisions and verifier-override
queues and the deep-assessment register is a SANCTIONED exception to the pack's
never-silently-drop-a-pending-item invariants, scoped to a confirmed adopter clone (the queued
items are the maintainer's, meaningless to the adopter) and confirmed with the operator in
step 1; it is not a breach of those invariants.

Read each surface before clearing it and preserve the shape its consumer requires, but note
the verification asymmetry: for the GATED surfaces (in the parent GRC library the session
lease and the per-PR validate-pr history) the step-7 sweep confirms the shape, while the
surfaces no gate reads are convention-verified only, so the adopter's first resume is the real
check. Preserve each gate-exempt surface's parseable shape deliberately rather than relying on
the sweep to catch a malformed one, and never treat a gate as validation of a surface outside
that gate's scope.

### 4. Handle the sibling placeholders per the chosen model

Apply the step-2 choice. For **external dependencies**, record the adopter's configured
locations so the project's resolver and its resume mechanism find them, and (for a reference
base) optionally bootstrap the adopter's EXTERNAL dependency from the acquisition manifest and
bootstrap planner named in the project wiring (portable procedure; adopters run their own
equivalent). A planner reads the committed public manifest and emits a categorized acquisition
plan (machine-readable, for the assistant to drive): **auto-fetchable** (freely redistributable
and an upstream URL is recorded), **free-manual** (freely available but no URL recorded yet),
and **licensed-manual** (licensed). Drive the bootstrap from that plan: fetch each
**auto-fetchable** source INTO the adopter's EXTERNAL dependency location, and list the
**free-manual** and **licensed-manual** entries for the adopter to acquire by hand (freely, or
lawfully under the issuer's licence). The planner itself NEVER fetches, downloads, or writes:
it reads only the manifest's bibliographic metadata, so the network and write side stays in the
assistant layer where the human is in the loop, and the copyright boundary is explicit (only
freely redistributable sources are auto-fetched; licensed items are never redistributed). For
**self-contained**, the in-repo placeholders are NOT shipped, so `/adopt` CREATES the ones the
adopter wants: a README-only stub per slot whose first line is the placeholder marker the
stub-guard validator parses, which is what keeps the stub payload-free. That marker is a
machine-read literal, so write exactly the form the validator parses: in the parent GRC library
it is `<!-- SIBLING-PLACEHOLDER: <name> -->` as the stub README's first line, with `<name>` the
slot token (`ref`, `scratch`, or `private`), and the stub-guard gate then holds a declared stub
to a README-only, line-capped shape. The acquisition manifest (and the same planner) then serves
as a bibliography the adopter can use to build an external dependency later (converting to the
external-dependency model). Fetched content goes into an EXTERNAL location, NEVER into a
declared in-repo STUB: a payload-bearing declared stub hard-fails the stub-guard validator and
breaks step 7's green sweep. An adopter who instead wants a FUNCTIONAL in-repo substitute (a
real checkout at the slot rather than an external one) materializes a functional directory
there, which is out of the stub-guard validator's scope (an unmarked, non-stub directory, so
different guards or none apply).

### 5. Strip maintainer-only machinery

Remove or neutralize any residual maintainer-only operational content that should not carry
into an adopter fork: pointers to maintainer-only stores, personal contact or watermark
tokens, and maintainer-specific runbook references that configured product surfaces do not
depend on. Do not touch the governance pack, its gates, or governed project content; this
step is scoped to operational residue, not product.

### 6. Record the adopt-config

Write and commit the adoption marker named in the project wiring, recording the adopter's
choices, so the project's resume mechanism proceeds in adopter mode without re-asking. The
minimal schema records the mode, the adoption date in UTC, the step-2 dependency choice, and an
integer marker-schema version. Those fields are machine-read, so use the exact names the
project's own classifier and resume mechanism parse; in the parent GRC library the marker is
`.claude/adopt-config.json` and the fields are `mode` (`"adopter"`), `adopted_at` (the UTC
date), `sibling_choice` (`"own-siblings"` | `"self-contained"`), and `adopt_config_version` (an
integer, `1`), which is the schema its operator classifier (`tools/detect-env.py`) reads back.
The committed marker is the durable signal that this fork is adopted; its presence is what
step 1 and the resume mechanism read to skip re-onboarding.

### 7. Verify and report

Confirm that the reset clone passes the adopting project's configured audit sweep, that its
resume mechanism reports adopter mode without re-proposing onboarding, and report what was
reset, which dependency model was recorded, and where the adoption marker lives. If a gate
fails, restore the affected surface's required shape and re-run it. Because a green sweep
confirms only surfaces the configured gates cover, separately parse-check or exercise every
reset state surface outside gate coverage before declaring onboarding complete.

The onboarding terminates when the working-state is reset to clean baselines, the sibling
model is settled and recorded, the adopt-config is committed, and the sweep is green; it is
a single run-once pass, not a cadence and not a fix-to-fixed-point loop.

## Prohibited anti-patterns

- **Running on a non-adopter clone.** Resetting a maintainer's (or a maintainer
  fresh-machine's) working-state destroys the audit trail; step 1's classification gate
  exists to prevent it, and a classification is confirmed with the operator, never assumed.
- **Fabricating adopter history.** The reset produces EMPTY baselines, not invented sweeps,
  retros, or backlog; a clean slate is honest, a fabricated history is not.
- **Clearing a working-state surface past its required shape.** A gate validates each
  surface's shape (headers, metadata, lifecycle fields); emptying the DATA is correct,
  destroying the SHAPE breaks the gate. Read before clearing.
- **Deleting product.** Governed project content, the pack, tooling, gates, and version
  lineage are product surfaces; `/adopt` never touches them.
- **Silently picking the sibling model.** It is the adopter's authorial choice; surface
  both options with consequences.
- **Re-running on an already-adopted fork without confirmation.** The committed adopt-config
  short-circuits `/adopt`; a re-baseline clears working history and needs explicit
  governance-authority confirmation.

## Framework alignment

| Requirement | NIST SSDF | CSA CCM | ISO 27001 |
| --- | --- | --- | --- |
| Clean-baseline onboarding of a forked control set | N/A | GRC-01, CCC-01 | A.5.1, A.5.4 |
| Authorial choices recorded before action | N/A | GRC-04 | A.5.4 |
| Audit-trail integrity (no fabricated history) | N/A | LOG-02, GRC-05 | A.8.15, A.5.36 |
| Scope-bounded reset (product preserved) | N/A | CCC-02, CCC-03 | A.5.4, A.8.32 |

The skill expresses the same audit-trail-integrity principle as the rest of the pack, at the
fork-onboarding boundary: an adopter starts from an honest clean baseline with its choices
recorded, never from the maintainer's working-state carried in unchanged or from a fabricated
history.
