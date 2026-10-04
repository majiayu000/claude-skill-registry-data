---
name: accessibility-audit
description: >-
  Adversarial, authorized accessibility deep-audit loop for a React frontend you
  own — fans out one accessibility-auditor subagent per WCAG 2.2 principle / a11y
  family in parallel, each probing the RUNNING stack (axe-core on the rendered
  DOM, keyboard-only traversal, and accessibility-tree / accessible-name /
  screen-reader semantic checks) AND inspecting the JSX/ARIA source (jsx-a11y
  lint, semantic-HTML + ARIA-pattern audit), verifies every candidate by
  reproducing the barrier against the running stack (no false positives), maps it
  to a WCAG 2.2 Success Criterion + conformance level + severity band, then drives
  root-cause, suppression-free fixes through react-implementer with a
  failing-then-passing regression test per fix and re-dispatches only still-open
  families until a clean pass. Use when accessibility-auditing, a11y-reviewing,
  WCAG-auditing, or keyboard / screen-reader / contrast-checking an authorized
  React frontend, or when the review stage triages the accessibility lens.
  Defensive / authorized use only — probe ONLY the profile-resolved local stack.
  Skip dynamic probing with a note when capabilities.dynamic_a11y_testing is false
  or make.start is null; the static JSX/ARIA audit always runs.
---

# Accessibility Audit Skill

## Profile keys consumed

- `make.a11y`
- `capabilities.accessibility_audit`
- `capabilities.dynamic_a11y_testing`
- `capabilities.publish_pr_comments`
- `make.start`
- `make.start_prod`
- `make.ci`
- `make.lint_eslint`
- `make.test_visual`
- `make.post_review_findings`
- `architecture.source_root`
- `architecture.modules`
- `architecture.component_prefix`
- `framework.ui`
- `framework.router`
- `framework.i18n`

Read these from `.claude/react-sdlc.yml` at runtime (no per-repo rendering; run
`/fe-sdlc-setup` if the profile is missing). Every path, module, and component
family resolves from the profile — never from source-project literals. A `null`
`make.*` value means that lane is unconfigured: substitute the bundled static lane
(`make.a11y: null`) or degrade with a note (`make.start: null`), never improvise a
raw host command. Where a key is absent, treat the dependent family as
N/A-with-reason rather than fabricating a finding.

## Gating

**Authorized / defensive use only.** This skill audits a frontend the repo owner
controls. The four boundary rules are a hard contract, restated here and in
[`../../agents/accessibility-auditor.md`](../../agents/accessibility-auditor.md)
verbatim, and enforced at the Allowed-actions / Constraints level (a forbidden
action, not advisory prose):

1. **In-scope target only (verified, not assumed)** — drive ONLY the
   profile-resolved local stack (the base URL of the `make.start`-booted stack).
   BEFORE any dynamic probe, verify the target host resolves to loopback
   (`127.0.0.0/8`, `::1`), an RFC1918 / private range (`10.0.0.0/8`,
   `172.16.0.0/12`, `192.168.0.0/16`, `fc00::/7`), or a known container / compose
   network name. If it does not, **refuse** — skip dynamic probing with a note and
   record a boundary-violation; never drive a public, remote, or third-party host
   even if one is supplied in the dispatch.
2. **No exfiltration** — never copy data, secrets, or credentials out of the
   disposable container instance.
3. **Interact via the app's own UI only** — drive the rendered page with
   keyboard / click / axe through the running stack; never mutate persistent state
   out-of-band to force a reproduction.
4. **Container-only, no destructive non-UI operations** — run through `make` /
   `docker compose exec` against the configured stack, never host binaries; touch
   only what is needed to reach and exercise the audited view on a disposable
   instance.

**Capability gates and their degrade paths** (each completes the stage
SUCCESS-WITH-REPORT — never a loop or hard-fail, NFR-3):

- `make.a11y: null` ⇒ run the bundled static lane directly through the container
  surface (the jsx-a11y / ARIA rules via the target mapped by `make.lint_eslint`,
  the axe static-rule pass, and ARIA-pattern + semantic-HTML inspection); add no
  dynamic dependency.
- `capabilities.dynamic_a11y_testing: false` OR `make.start: null` ⇒ dynamic
  probing is `SKIPPED:` with a note ("dynamic a11y probing skipped —
  `capabilities.dynamic_a11y_testing` false / `make.start` null / stack
  unreachable"); the static JSX / ARIA / semantic-HTML lanes still run, and the
  static-determinable classes (§5.3) stay promotable by deterministic in-tree
  demonstration.
- `capabilities.accessibility_audit: false` ⇒ the bundled axe / ARIA tool lane is
  `SKIPPED:` with a note, but the source-level JSX/ARIA audit still runs over
  `architecture.source_root` so every family still gets an explicit verdict — never
  a silent skip (NFR-6).
- A family whose surface is absent on this target (a tables family with no data
  table, a media-captions family with no audio / video, a route-announcement family
  with `framework.router` unset) is recorded **N/A-with-reason** up front and never
  dispatched (NFR-8 cost gate).

## Context

This skill is the plugin's **accessibility deep-audit lens** — an adversarial,
multi-subagent audit loop over an authorized React frontend. It is the frontend
twin of the backend security lens: same triage → fan-out → find → verify → fix →
regress → re-verify machinery, with the domain swapped from OWASP / CWE to WCAG 2.2
AA. It runs at two entry points with one identical body:

- **Triaged inside the Stage 4 review gate** — the review gate's applicability
  triage records an EXECUTE / NOT-APPLICABLE verdict for it like every other skill.
  It is the accessibility counterpart to the quality lens (the `code-quality-reviewer`
  agent) and the spec lens (the `fr-nfr-reviewer` agent).
- **Standalone** — invokable directly as `react-frontend-sdlc:accessibility-audit`
  against an authorized target.

The skill **owns the loop** (triage → fan-out → find → verify → fix → regress →
re-verify → loop); the `accessibility-auditor` subagents are **find / verify only**;
all code edits route through the existing `react-implementer` agent. Its culture is
**no false positives** (a jsx-a11y / axe candidate is never a finding until
reproduced, or deterministically demonstrated in-tree for the static-determinable
classes), **root-cause only** (no `eslint-disable`, no jsx-a11y disable, no axe rule
suppression, no baseline, no threshold edit), and **container-only** execution.

Technique-level remediation guidance may draw on the companion accessibility-lead
agent team and the a11y review / audit skills documented in
`docs/companion-skills.md`. A WCAG match never waives the visual-regression gate
(the target mapped by `make.test_visual`) or the performance floors that follow.

This skill body PRESCRIBES the fan-out as text. It contains **no Task-tool call** —
skills never invoke agents. The orchestrator that loaded this skill (the review
agent or a standalone invocation that holds the `Task` tool) executes the dispatch
the steps describe.

## Task

Drive the target React frontend to **zero new verified accessibility findings**:

- Every WCAG 2.2 principle / a11y family in
  [`reference/wcag-catalog.md`](reference/wcag-catalog.md) receives an explicit
  verdict — PROBE or N/A-with-reason. 100% triaged, no silent skips (NFR-6).
- Every PROBE family is driven to zero new verified findings through the bounded
  loop.
- Every reported finding carries a working reproduction, a WCAG 2.2 Success
  Criterion id, a conformance level (A / AA), and a severity band-with-rationale.
- Every fix is root-cause and accessible-by-default, routed through the
  `react-implementer` agent, and carries a failing-then-passing regression test.

## Steps

The canonical loop. Every **enumeration** (WCAG families, per-family probes,
remediations) lives in a `reference/` file — never inline here — so this SKILL.md
stays focused (NFR-9).

### 5.1 Triage

Read [`reference/wcag-catalog.md`](reference/wcag-catalog.md) and record a
**per-family verdict table** (PROBE / N/A-with-reason) covering the entire WCAG 2.2
AA corpus, grouped by POUR principle plus the cross-cutting surfaces (forms, modals,
keyboard, live-regions, contrast, alt-text / headings, links, tables). No silent
skips. Exclude N/A families **before** fan-out to control token cost (NFR-8):

- A family whose surface does not exist on this target (no data table → tables
  family N/A; no audio / video → media-captions N/A; `framework.router` unset →
  SPA route-announcement family N/A).
- A family whose only checks need a capability that is off, recorded with the gate
  reason (see **Gating**) rather than dropped silently.

The catalog file is the single source for the dispatchable family set and its WCAG
SC mappings; do not re-enumerate families here.

### 5.2 Fan-out (parallel a11y audit)

First, **boot the stack** when dynamic testing is in scope: if
`capabilities.dynamic_a11y_testing` is true and `make.start` is non-null, the
orchestrator boots the stack via the `make.start` target and captures its in-scope
base URL (loopback / private / container host per boundary rule 1). If the
capability is false or `make.start` is null, dynamic probing degrades to
skip-with-note and only the static lanes run — no base URL is passed.

**Capture and report the booted build mode** alongside the base URL. A dev-server
build can **mask or inflate** findings: a dev error overlay injects extra focusable
nodes (a false keyboard-order / focus finding), React StrictMode double-invokes and
can duplicate `id`s or live-region announcements, and dev-only attributes differ
from production output. So: pass the build mode in every dispatch; a family whose
verdict depends on rendered output toggled by the build (focus order, live-region
timing, duplicate-`id` ARIA) must cross-check against a production-parity build
before reporting CLEAN or promoting a finding, and state the build mode in its
verdict. Prefer booting the production-parity build (the target mapped by
`make.start_prod`) for the authoritative dynamic pass when one exists — it is the
same artifact the visual-regression and Lighthouse gates audit.

Then dispatch **one `accessibility-auditor` subagent per PROBE family, in
parallel** — the proven parallel-`react-implementer` idiom (no new infrastructure).
The orchestrator issues N `Task`-tool dispatches in one turn. Each dispatch passes:

- the assigned WCAG family id and its
  [`reference/audit-playbooks.md`](reference/audit-playbooks.md) entry;
- the report contract (the finding-record schema in **Format** below);
- the current iteration number from this loop's `MAX_ITERATIONS=5` guard;
- the resolved base URL of the booted in-scope stack and its build mode (omitted
  when dynamic testing is degraded — the auditor then runs static lanes only);
- on re-dispatch, the prior ledger for that family.

Resolve the family set and its profile gates from
[`reference/wcag-catalog.md`](reference/wcag-catalog.md). N/A families from 5.1 are
**never dispatched**.

### 5.3 Find → verify-by-reproduction

Each subagent runs the static lane (jsx-a11y / ARIA lint via the target mapped by
`make.lint_eslint`, the axe static-rule pass, semantic-HTML + ARIA-pattern
inspection over `architecture.source_root`) **and** adversarial dynamic probing per
its [`reference/audit-playbooks.md`](reference/audit-playbooks.md) entry (axe-core on
the rendered DOM, keyboard-only traversal, accessibility-tree / accessible-name /
role queries, and — when `framework.router` is set — route-change focus + live-region
announcement checks). A static result is a **candidate**, never a finding, until:

- **reproduced against the running stack** — an axe-core violation on the rendered
  DOM, a keyboard sequence that traps or cannot reach a control, an
  accessible-name / role query that returns the wrong value; OR
- for the **static-determinable classes** that need no rendered styles —
  deterministically demonstrated in-tree: a missing `alt` on a meaningful image
  (1.1.1), a form control with no associated label (1.3.5 / 3.3.2 / 4.1.2), a
  missing or wrong `<html lang>` (3.1.1, the `framework.i18n` sink), a positive
  `tabindex` (2.4.3), or an ARIA `role` missing its required ARIA property (4.1.2) —
  the attribute provably absent or malformed in the JSX.

A candidate that can neither be reproduced against the stack nor deterministically
demonstrated in-tree (a contrast ratio that needs computed styles, a focus-order or
live-region-timing question, a keyboard-trap behavior) is recorded
**downgraded/dropped** with the reason — never reported, never fixed.

### 5.4 Aggregate / dedupe / promote

The orchestrator collects the N subagent reports and:

- **Dedupes** findings by the tuple `(WCAG SC id, JSX/component sink file:line,
  exercised surface)` — two families hitting the same component sink collapse to one
  finding (NFR-8). A reusable `architecture.component_prefix` primitive that emits
  the same barrier across many views is one finding at the component, not one per
  view.
- **Promotes** only reproduced (or in-tree-demonstrated) candidates to findings; a
  candidate without that proof is recorded downgraded/dropped, never reported — the
  subagents already enforce this; the orchestrator is the second gate.
- **Orders** the promoted findings by severity band (Critical → Low) for the fix
  queue. Severity weighs impact (does the barrier block completion of a task) and
  reach (a shared component vs a single view).

### 5.5 Fix → regression-test

Route each verified finding to the **`react-implementer` agent** (never edited here,
never by the auditor) with the `{location, remediation, regression_test}` slice of
its finding record and the cited remediation from
[`reference/remediation-patterns.md`](reference/remediation-patterns.md). Each fix is
**root-cause and accessible-by-default** — a semantic-HTML element, the correct ARIA
pattern, or the right `framework.ui` component slot — and carries a
**failing-then-passing regression test** that reproduces the barrier and then proves
it closed (an axe assertion on the rendered component, or a Testing Library
`getByRole` / `getByLabelText` query for the now-correct accessible name / role).
No `eslint-disable`, no jsx-a11y disable directive, no axe rule suppression or
baseline, no config relaxation, no `quality.*` threshold reduction — ever. Locate
elements by user-facing semantics, never by a test-only `data-testid`.

### 5.6 Re-verify → loop

Re-dispatch only **still-open families** (the re-dispatch set shrinks each
iteration, NFR-8). The affected family's `accessibility-auditor` re-verifies that its
reproduction no longer succeeds and that the added regression test now passes. The
loop is bounded `MAX_ITERATIONS=5`:

```text
iteration ← 1
loop:
  dispatch accessibility-auditor for each still-open PROBE family (parallel)  # 5.2
  collect + dedupe + promote verified findings                               # 5.4
  if zero new verified findings: exit SUCCESS-WITH-REPORT                     # exit
  route each finding → react-implementer (root-cause fix + regression test)   # 5.5
  affected-family re-verify                                                   # 5.6
  iteration ← iteration + 1
  if iteration > 5  OR  react-implementer / Ralph breaker tripped:            # NFR-2
     emit canonical escalation block; STOP (never auto-reset the breaker)
final: run the make.ci target once; forbidden-suppression scan; emit report
```

Run the full `make.ci` target **once at loop close** (not per iteration — the
affected-family reproduction is the per-iteration correctness signal, the final
`make.ci` is the safety net). Exit on the first iteration that yields zero new
verified findings. On `iteration > 5`, or on a tripped `react-implementer` / Ralph
circuit breaker, emit the canonical escalation block and STOP — never auto-reset a
breaker (NFR-2).

### 5.7 Publish (gated)

When `capabilities.publish_pr_comments` is `true`, project this loop's promoted
finding records (§5.4) — deduped on the same `(wcag, location, surface)` tuple, each
`auto_fixed: true` with its `regression_test` when routed through §5.5 — to the
canonical ledger JSON at
`${SDLC_LEDGER_DIR:-.sdlc/review-ledgers}/accessibility.json`, then publish ONE
consolidated, idempotent PR comment via the target mapped by
`make.post_review_findings`; when that key is `null`, the plugin substitutes its
bundled review-findings poster. The poster is idempotent (a hidden
`<!-- sdlc-review:accessibility -->` marker — it updates its prior comment, never
spams), authorized (writes only to the resolved repo's own PR), and DEGRADES
(NFR-3): `capabilities.publish_pr_comments` false / absent, `gh` absent, no PR, an
empty ledger, a mismatched base repo, or a write failure all skip-with-note and exit
0 — publishing NEVER fails this loop. When the flag is false / absent, skip this step
with a note.

## Constraints

**NEVER**:

- Drive any host or URL outside the profile-resolved local stack, exfiltrate data,
  mutate state outside the app's own UI, or run a destructive non-UI operation (the
  four boundary rules in **Gating**).
- Run host binaries — execution is container-only (`make` / `docker compose exec`).
- Report a finding without a working reproduction or a deterministic in-tree
  demonstration (§5.3), or fabricate a finding for an N/A family (NFR-6).
- Edit code from this skill or from an `accessibility-auditor` subagent — fixes
  route through the `react-implementer` agent only.
- Add an `eslint-disable`, a jsx-a11y disable directive, an axe rule suppression or
  baseline, a `@ts-ignore`, a config relaxation, or a `quality.*` threshold
  reduction to make a finding disappear — thresholds are raise-only; fix the code.
- Add a `data-testid` to make a barrier or a regression test pass — locate elements
  by `getByRole` / `getByLabelText` / `getByText`, falling back to a stable `id`
  only when no semantic query fits.
- Loop or hard-fail on an absent capability — degrade with a note (NFR-3).
- Loop past `MAX_ITERATIONS=5` or auto-reset a tripped breaker (NFR-2).
- Use source-project literals — every path / module / component family resolves
  from the profile (NFR-4).
- Issue a Task-tool call from this skill body — it is text the orchestrator
  follows.

**ALWAYS**:

- Record an explicit verdict (PROBE / N/A-with-reason) for every family in
  [`reference/wcag-catalog.md`](reference/wcag-catalog.md) — 100% triaged.
- Promote only reproduced (or in-tree-demonstrated) candidates to findings; record
  the rest as downgraded/dropped.
- Map every finding to a WCAG 2.2 SC id + conformance level + severity
  band-with-rationale and cite its remediation from
  [`reference/remediation-patterns.md`](reference/remediation-patterns.md).
- Route every fix through the `react-implementer` agent with a
  failing-then-passing regression test.
- Re-dispatch only still-open families; run `make.ci` once at loop close; scan the
  diff for forbidden suppressions (the
  [`../code-review/SKILL.md`](../code-review/SKILL.md) suppression scan) before
  declaring success.
- Run the §5.7 Publish step gated on `capabilities.publish_pr_comments`; it degrades
  with a note (NFR-3) and never fails this loop.

## Format

**Finding-record schema** — the single hand-off shape, emitted by each
`accessibility-auditor` and consumed by the orchestrator → `react-implementer`:

```text
FINDING <family-id>-<n>
  wcag: <SC id + name, e.g. 1.4.3 Contrast (Minimum)>   # mapped from reference/wcag-catalog.md
  level: A | AA                                         # WCAG 2.2 conformance level
  severity: Critical|High|Medium|Low                    # band + one-line rationale (impact + reach)
  location: <architecture.source_root>/<path>:<line>    # the component/JSX sink, profile-resolved
  surface: <route/view> — <element role + accessible name>   # the exercised UI surface
  reproduction:
    1. <exact container command: axe-core run / keyboard sequence / accessible-name query>
    2. <exact command>                  # copy-pasteable against a freshly booted stack
  expected: <accessible behavior>   observed: <the barrier>
  remediation: <semantic-HTML / ARIA pattern / framework.ui slot primitive + cited WCAG technique>
  regression_test: <test path the fix must add>   # failing-before / passing-after (axe / role+name)
```

`react-implementer` receives `{location, remediation, regression_test}` and produces
the root-cause fix + the failing-then-passing test; the affected-family
`accessibility-auditor` re-verifies the barrier no longer reproduces. Severity is a
**band-with-rationale**; the WCAG technique reference (e.g. an ARIA Authoring
Practices pattern id) is an optional field, never mandated.

**Run report shape** — emitted at loop close:

```text
ACCESSIBILITY-AUDIT RUN REPORT
  per-family verdict table: <family> → PROBE | N/A (<reason>)
  build mode: <dev | production-parity> (base URL or "static-only")
  per-iteration finding counts: iter 1: <n> … iter k: <n>
  iterations used: k / MAX_ITERATIONS=5
  promoted findings: <count by severity band> (by WCAG level: A / AA)
  dropped candidates: <count> (no reproduction / not in-tree-demonstrable)
  make.ci: <PASS|FAIL>   forbidden-suppression scan: <CLEAN|VIOLATION>
  status: SUCCESS-WITH-REPORT | ESCALATED
```

**Canonical escalation block** (on `MAX_ITERATIONS=5` breach or breaker trip):

```text
=== SDLC ESCALATION ===
stage: accessibility-audit
iteration: <n>/5
exit_condition: zero new verified findings (all dispatched families CLEAN)
status: NOT MET
blocking_finding: FINDING <family-id>-<n> (<wcag SC> / <level> / <severity>)
iteration_log: <one line per iteration: open families + candidates/reproduced/re-verified counts>
recommended_action: <next step for the owner, e.g. route FINDING <id> to react-implementer>
=== END ===
```

## Verification

- [ ] Every family in [`reference/wcag-catalog.md`](reference/wcag-catalog.md)
      received a recorded verdict (PROBE / N/A-with-reason) — 100% triaged, no
      silent skip.
- [ ] N/A families (no-table tables, no-media captions, no-router route
      announcement, capability-gated lanes) were excluded before fan-out with a
      recorded reason.
- [ ] Every reported finding carries reproduction steps + a WCAG 2.2 SC id +
      conformance level + severity band-with-rationale + a cited remediation.
- [ ] Every non-reproducible, non-in-tree-demonstrable candidate was recorded
      downgraded/dropped, not reported.
- [ ] Every fix is root-cause, routed through the `react-implementer` agent, and
      carries a failing-then-passing regression test.
- [ ] Only still-open families were re-dispatched each iteration (shrinking set).
- [ ] The loop exited on a zero-new-verified-findings iteration, or escalated at
      `iteration > 5` / breaker trip with the canonical escalation block — no
      breaker auto-reset.
- [ ] The `make.ci` target exits `0` at loop close and the forbidden-suppression
      scan reports zero suppressions introduced (no `eslint-disable` / jsx-a11y
      disable / axe baseline / `data-testid` added to dodge a gate).
- [ ] No action targeted an out-of-profile host or performed a destructive non-UI
      operation (the four boundary rules held throughout).

## Related Skills

- [`../code-review/SKILL.md`](../code-review/SKILL.md) — the forbidden-suppression
  scan and per-comment evidence ledger this loop reuses.
- [`../frontend-testing-workflow/SKILL.md`](../frontend-testing-workflow/SKILL.md) —
  where each failing-then-passing regression test (axe / Testing Library) lives.
- [`../frontend-component-development/SKILL.md`](../frontend-component-development/SKILL.md) —
  the accessible-by-default component patterns the root-cause fixes follow.
- [`../ci-workflow/SKILL.md`](../ci-workflow/SKILL.md) — the `make.ci` gate run once
  at loop close.
