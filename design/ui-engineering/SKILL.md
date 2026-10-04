---
name: ui-engineering
description: "Implement approved product-surface contracts in durable frontend code and produce render-grounded contract evidence. Use for authorized UI builds and read-only accessibility, motion, implementation-baseline, or contract/code drift audits. Do not use to invent missing UX or interface decisions, review PRs, or replace completed-feature verification."
argument-hint: "[audit | authorized UI implementation request]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
disable-model-invocation: false
---

# UI Engineering

Translate an approved experience and interface contract into the existing frontend architecture. Own durable UI code, the Implementation Bridge section, and render-grounded design-fit evidence. Never silently invent product or interface intent.

Task: $ARGUMENTS (if empty, infer the authorized implementation scope)

## Routing Precedence

1. PR, diff, or review feedback → `code-review`; stop this skill.
2. Confirmation that a completed feature meets its goal → `verify`; stop this skill. UI-engineering evidence may be an input.
3. Read-only accessibility, motion, implementation-baseline, or contract/code drift inspection → run `audit` here.
4. New or materially changed product surface → `product-craft` owns the experience and interface gates before this skill.
5. Whenever `design` independently triggers, including every expected three-or-more-file change, its technical plan must be persisted and active before durable writes.
6. Routine frontend work with no UX/UI decision and no contract need → ordinary implementation path.

Parallel sub-agents may take disjoint implementation units only after ownership, authorization, and write sets are explicit. They never own design decisions.

## Modes

- `audit` — read-only evidence collection and findings. It never authorizes source or contract edits.
- Default — durable implementation, allowed only after the authorization checklist passes.

## Authorization Checklist

Before any durable product write, require all applicable items:

- An explicit user build request.
- `Experience gate: READY FOR INTERFACE` for new/material experience scope.
- `Interface gate: READY FOR BUILD` for new/material presentation scope.
- Approved changed sections for Focused Delta.
- A persisted active general `design` plan whenever its independent trigger applies.
- The applicable `design-contract.md`, or an explicitly approved in-session Seed contract with the missing durable artifact disclosed.
- The approved `Surface Obligations` rows and `## Artifact Ledger` entries from the contained
  durable contract.
- Required approvals and Recorded approvals, with every required token recorded from
  explicit user evidence. Always consume Required approvals and Recorded approvals before durable writes; approval prose is not a substitute.

If any material item is missing, stop. Authorization is scoped; it does not permit unrelated cleanup or a broader design change.

## Proof Carrier Resolution

Resolve exactly one carrier before reading or writing product source:

1. If `design` independently triggered, resolve the originating session with exact
   injected metadata:

   ```bash
   root="$(git rev-parse --show-toplevel)" || exit 1
   PM_SESSION_TOOL="<injected session tool>" PM_SESSION_ID="<exact injected session id>" \
     node "$HOME/.config/ai/lib/worktree.mjs" resolve-session \
     --root "$root" --tool "<injected session tool>"
   ```

   Require `status: ok`, `plan_status: active`, matching execution root/branch/base, and
   `## Product Surface Proof Obligations` containing the packet, exact EXP/INT rows,
   approval fields, and one Durable contract path.
2. If the independent design trigger did not apply, require an explicit no-plan handoff
   with `plan_requirement: not required`, no invented plan, an explicit build request, a
   git execution root, and the same packet already persisted under the named contract's
   Decision Log.
3. Resolve the repo-relative Durable contract path inside the execution root. Reject a
   missing or escaping path, unexpected plan, unbound required route, absent packet, or
   malformed proof obligations without writing.

Both routes require typed approvals and build authorization. The no-plan route relaxes
only the plan requirement.

## Owned Contract Section

UI engineering is the sole writer for `Implementation Bridge` after build authorization. It records existing libraries, primitives, token/code mappings, styling conventions, asset rules, technical constraints, and verification commands. It cannot override experience- or interface-owned sections.

## Required Context

1. Applicable approved contract and gate records.
2. Affected routes/screens/components and their realistic data/states.
3. Existing component primitives, design tokens, theme/style entry points, layout conventions, accessibility helpers, and tests.
4. `../product-craft/references/quality-floor.md`, `../product-craft/references/output-formats.md`, `references/implementation-baseline.md`, and `references/verification.md`.
5. The selected artifact named in the contract's `## Artifact Ledger`, read as source. Within
   the states and adaptation extremes it was reviewed at, the artifact is the authority for what the
   screen looks like — read its own substrate rather than reconstructing the look from prose.
   Recompute its revision before trusting it; a mismatch is `ARTIFACT DRIFT`, not a detail to
   reconcile by eye.

Read only the contract sections and implementation evidence needed for the selected scope.

## Implementation Workflow

### 1. Reconcile Contract and Code

Map each affected contract rule to an existing primitive, token, component, style convention, or explicit new implementation need. Prefer the project's current platform feature, dependency, and shared component before custom code.

Emit `Surface Obligations` rows with `Stage: implementation`, each deriving from the
experience or interface obligations it satisfies. Coverage follows the ancestor chain, so an
implementation row reaching an interface row also covers what that row derives from. Any
applicable upstream obligation with no implementation row above it is uncovered.

Where the contract and the selected artifact both speak, the artifact governs inside its
reviewed scope. Port from it; do not re-derive its spacing, rhythm, or type setting from
description.

Reject duplicate, unknown, or sourceless rows and unjustified N/A.

If code evidence conflicts with or cannot express approved intent:

- Emit `EXPERIENCE DELTA REQUIRED` for jobs, IA, flow, visible-state meaning, interaction semantics, recovery, or microcopy.
- Emit `INTERFACE DELTA REQUIRED` for composition, art direction, visual tokens, component appearance, adaptation presentation, or interface formatting.
- Emit `CONTRACT GAP` when intent is missing/contradictory or ownership is unclear.

Stop the affected path. Do not resolve a gap with an arbitrary implementation choice.

### 2. Implement the Smallest Contract-Faithful Change

- Preserve technical architecture and existing product invariants.
- Reuse existing primitives and tokens before creating variants or dependencies.
- Implement all applicable states and recovery paths, not only the happy render.
- Apply the invariant floor through the declared medium's mechanisms — see `../interface-design/references/medium-profiles.md`. Where a medium supplies no mechanism for an intent, that is a GAP to report, not a pass. For a medium that produces no durable source at all, this skill still owns render-grounded evidence and the Implementation Bridge records how the artifact was produced and inspected.
- Keep motion frequency-appropriate and performance-safe.
- Use realistic content constraints and explicit overflow behavior.
- Update Implementation Bridge only with verified mappings and commands.

### 3. Verify by Rendering

Follow `references/verification.md`. It runs two passes: the render compared against what was
approved, and a separate open critique using `../product-craft/references/craft-review.md` that
asks what is wrong regardless of whether the contract mentioned it. Source inspection alone
cannot prove craft readiness, and contract-row closure alone cannot either — a material craft
finding blocks readiness on its own.

While implementation remains authorized, correct an applicable measured failure and re-render, up to two source-change/render cycles. Then report exact coverage and remaining failures with the shared Design-Fit Result.

Each applicable implementation obligation must align the same requirement across concrete
code, an affirmative assertion, and an inspected render or measurement. A passing test that
positively requires behavior contrary to the contract is `contract drift` + `FAIL`; never
treat it as proof. Missing required evidence is `unverified` + `NOT VERIFIED`.

Record `Craft Findings` alongside, from the open critique pass. They are not optional
commentary — a material finding blocks readiness.

### 4. Persist Bounded Evidence

The implementation evidence under `## Implementation Bridge` is the only product-contract
mutation this stage owns:

1. Read the contained durable contract and record its SHA-256. Require exactly one
   `## Implementation Bridge`.
2. Validate the whole proposed record in memory: unique and known ids, coverage along the
   ancestor chain, recorded approvals, consistent classification and status, complete
   evidence, and justified N/A.
3. Re-read immediately and require the same hash. Write only within Implementation Bridge,
   as one exact-context patch.
4. Read back and require byte-identical sections elsewhere and a diff limited to
   Implementation Bridge. A stale hash, duplicate section, malformed record, context
   mismatch, or wider diff stops with Design-Fit NOT VERIFIED.

Never mutate canonical plan content. Return the exact contract path, the persisted Decision
Log records, and the Bridge evidence in the handoff.

### 5. Hand Off to Goal Verification

Design-fit evidence does not replace `verify`. When implementation is complete, provide the evidence and route completed-feature confirmation to `verify` against the active plan's success criteria.

## Audit

Audit is read-only.

1. Establish the applicable contract, quality floor, existing implementation baseline, and requested audit scope.
2. Inspect source and render/runtime evidence where feasible.
3. Report findings by severity with concrete observation, file/render evidence, user-job or technical impact, and one correction.
4. Separate contract drift from implementation defects and from unverified coverage.
5. Route desired contract changes to the owning stage; do not edit on the audit request alone.
