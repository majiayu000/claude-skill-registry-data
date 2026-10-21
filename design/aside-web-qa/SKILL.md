---
name: aside-web-qa
description: "Client-facing web QA orchestration through the installed Aside CLI. Runs aside-functional-qa and aside-visual-qa as one combined engagement with a shared preflight, one browser session plan, cross-phase defect routing and deduplication, and a single merged client report. Use when asked for combined or end-to-end web QA, a full client QA report, both behavior verification and UI/UX review, 통합 QA, 종합 QA, 웹 QA 오케스트레이션, or 클라이언트 QA 총점검. Use aside-functional-qa alone for behavior-only asks and aside-visual-qa alone for design- or UX-only asks."
---

# Aside Web QA (Orchestration)

Orchestrate the two Aside QA skills into one client-facing engagement. This
skill owns routing, sequencing, the shared preflight, cross-phase defect
routing and deduplication, and the merged report. It never replaces the
sub-skills' own contracts.

## Use and Boundaries

Use when one engagement must cover both browser-observable behavior
(functional) and design intent, accessibility, responsiveness, and coherence
(visual). Route single-dimension asks to the matching sub-skill and stop:

- behavior, requirements, state transitions, persistence → `aside-functional-qa`;
- design intent, UX, accessibility, responsive behavior → `aside-visual-qa`.

Skip pure API, backend, CLI, or library work with no browser surface.

## Sub-skill Contract

Before execution, load both sub-skills, resolved relative to this skill's
directory:

- `../aside-functional-qa/SKILL.md`
- `../aside-visual-qa/SKILL.md`

Both remain authoritative for their phase: their Immutable Safety Rules,
rubrics, coverage rules, result classification, self-audit, and report
templates apply in full. This skill may sequence and merge them; it may never
relax, reinterpret, or shorten their rules. Where this skill adds obligations
(shared preflight, cleanup deferral, deduplication, verdict merge), the
stricter rule wins.

## Inputs

Required:

- `TARGET`: URL or explicit access path to the running product.
- `SCOPE`: named capability, user journey, or screens under engagement.
- `REQUIREMENTS`: requirements or acceptance criteria for the functional
  phase.
- `INTENT`: design intent, references, or expected outcome for the visual
  phase.

Optional: the union of both sub-skills' optional inputs — IDs and priority,
role/account class and safe authentication path, allowed mutations and cleanup
contract, test data and boundary values, expected viewports, locale, color and
reduced-motion mode, reference images, exclusions, known defects, and report
output path.

If `REQUIREMENTS` or `INTENT` is missing and cannot be reconstructed from
repository evidence, ask one narrow question when the gap materially changes
the verdict. Otherwise run the satisfied dimension through its sub-skill,
record the other dimension `Not Run` with the reason, and never present the
partial run as full coverage.

## Immutable Safety Rules

Every sub-skill safety rule applies during its phase. In addition:

1. Load both sub-skill contracts before any browser action. Never improvise a
   phase workflow from this file alone.
2. Run the Aside browser-contract preflight once per engagement. Both phases
   consume the shared preflight record; do not repeat it per phase.
3. Keep one engagement-level tab-ownership plan. Test-owned tabs stay owned by
   this engagement until the final cleanup; never close, navigate, or
   repurpose attached user tabs between phases.
4. Defer destructive cleanup that would remove states the visual phase must
   review. Record every deferral and execute the cleanup before completion.
5. Reuse evidence across phases only when build, state, viewport, and locale
   match, and record its freshness. Never present phase-1 evidence as a
   phase-2 observation without that check.
6. Deduplicate shared-cause defects before reporting. Never split one root
   cause into two findings to pad a section.
7. Merge verdicts by severity ordering, never by averaging or test count.

## Workflow

### 1. Route the ask

Confirm the engagement needs both dimensions. If not, hand off to the matching
sub-skill and stop. State the phase order and the merged deliverable up front.

### 2. Shared preflight

Run the browser-contract preflight once and record, without identities:

- installed Aside version and signed-in state;
- target build and actual URL;
- viewport, locale, and role class actually available;
- test-data prefix and engagement cleanup plan;
- union of REPL methods required by both phases.

If the target, daemon, authentication, or safe data is unavailable, mark both
phases `Blocked`; do not downgrade and do not proceed with one phase as if the
engagement were healthy.

### 3. Functional phase

Execute the `aside-functional-qa` workflow end to end under its own contract,
using the shared preflight record. Additionally produce the
**reachable-state map** for the visual phase: every route, state, role, and
data dependency actually reached, with entry action, stability, and evidence
reference. Obey the cleanup-deferral rule for states the visual phase must
review.

### 4. Visual phase

Execute the `aside-visual-qa` workflow end to end under its own contract,
using the shared preflight record. Enumerate coverage from the declared
`SCOPE` plus the reachable-state map. States unreachable because of a
functional failure are `Blocked by FQA-...`; preserve causality instead of
silently dropping coverage.

### 5. Cross-phase consolidation

Apply the routing and deduplication rules in
[the orchestration reference](references/orchestration.md):

- assign every defect to its primary owner (`BUG-...` functional,
  `VQA-...` visual) and cross-link the other phase's symptom;
- merge shared root causes into one finding;
- build one evidence index with a single environment block and per-phase
  artifact IDs;
- compute the merged verdict from the two phase verdicts by severity
  ordering.

### 6. Produce the merged client report

Follow [the merged report sample](examples/sample-report.md). Lead with one
plain-language executive summary and exactly one release recommendation, then
provide the functional section (functional template), the visual section
(visual template), the consolidated defect list ordered by user impact, the
coverage view, and the shared limitations and cleanup.

### 7. Self-audit

Complete both sub-skills' self-audit lists, then verify the orchestration
additions:

- the preflight ran once and both phases consumed it;
- deferred cleanup was executed and recorded;
- every cross-phase defect has one primary owner and cross-links;
- blocked visual coverage cites the blocking functional result;
- the merged verdict equals the least ready phase verdict;
- no partial run is presented as full coverage.

## Verdict Merge

Order: `Not ready` < `Conditionally ready` < `Ready with minor fixes` <
`Ready`. The merged verdict is the least ready of the two phase verdicts, with
rationale drawn from both. If one phase is entirely `Blocked` or `Not Run`,
base the recommendation on the executed phase alone and state the coverage gap
explicitly. Never convert a non-Pass status or an unreviewed state into
readiness.

Before merging, verify sub-reports directly instead of trusting their summary:
at minimum re-run or re-observe every `Fail`, `Inconclusive`, and borderline
item yourself, and confirm each `Pass` item cites a captured artifact. A
sub-verdict whose items lack evidence links merges as `Not Run` for that scope,
never as ready.

## Completion and Stop Conditions

Complete only when both phases completed under their own contracts (or were
explicitly routed out), consolidation and merged report are recorded, deferred
cleanup is executed, and both self-audits pass. Stop with `Blocked` when safe
execution requires unavailable credentials, environment, data, or
authorization. Stop before destructive behavior and ask for explicit approval.

Do not claim “fully tested,” “all requirements pass,” “pixel perfect,” or
“production ready” outside the declared combined coverage.
