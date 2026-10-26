---
name: rite-converge
description: Converge intent and live code. Use when resuming a half-built feature, after `/rite-adopt` drift, or live code may have diverged from the plan. Not for initial planning.
argument-hint: "[feature-slug]"
user-invocable: true
---

<!-- loads: {"always":["devrites-lib/reference/standards/core.md","devrites-lib/reference/standards/code-navigation.md","devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/spec-grammar.md","devrites-lib/reference/standards/agents.md","devrites-lib/reference/standards/tooling.md","devrites-lib/reference/standards/testing.md","rite-converge/reference/convergence-assessment.md","rite-converge/reference/anti-patterns.md","rite-build/reference/spec-drift-guard.md"],"triggers":{"applicability":["devrites-lib/reference/standards/repository-topology.md","devrites-lib/reference/standards/data-integrity.md","devrites-lib/reference/standards/integration-reliability.md"],"principles":["devrites-lib/reference/standards/principles.md"],"workflow-artifacts":["devrites-lib/reference/workspace-artifact-schema.md"]},"workspace":["brief.md","spec.md","state.md","decisions.md","assumptions.md","questions.md","decision-coverage.md","architecture.md","plan.md","tasks.md","traceability.md","eng-review.md","test-plan.md","gates.md","evidence.md"],"workspaceByRole":{"evidence-scout":["spec.md","plan.md","tasks.md","state.md","evidence.md"]},"rootOnly":["devrites-lib/reference/standards/code-index.md","devrites-lib/reference/standards/tooling.md"]} -->
> Read-set manifest: `devrites-engine context <slug> --phase converge` bundles every file named below into one deduplicated read. Trigger names map to the conditional rules in the sections that follow.


# /rite-converge: compare live code with intent

Read `spec.md`, `plan.md`, and `tasks.md` as the **sole source of intent** (with
`.devrites/principles.md` as governing constraints), assess what the **live codebase**
implements, and **append every unmet piece as a new traceable `SLICE-###`** at the
bottom of `tasks.md` so `/rite-build` can finish it. Use this for a resumed half-built
feature, an adopted codebase that drifted from its derived spec, or a build that stalled
mid-slice. **Read the active
workspace first**; if there's no `spec.md`/`plan.md`/`tasks.md`, tell the user which
prerequisite skill to run.

> **This is not a diff tool.** `/rite-converge` compares current code with intent. It
> does not use git history or compare branches. For a change-scoped
> review use `/rite-review`; to prove a finished feature use `/rite-prove`.

## Rules consulted (read on demand from `.claude/skills/devrites-lib/reference/standards/`)

Pull on demand:

- [`principles.md`](../devrites-lib/reference/standards/principles.md): the project invariants (`.devrites/principles.md`); code that violates a
  MUST principle is the highest-severity gap and produces a remediation slice.
- [`spec-grammar.md`](../devrites-lib/reference/standards/spec-grammar.md): buildable acceptance criteria vs `## Success metrics` (outcome KPIs the
  code can't make true and this pass never enqueues); structured `### Requirement:` /
  `#### Scenario:` blocks, each scenario one behavior to check as built / partial / absent.
- [`code-navigation.md`](../devrites-lib/reference/standards/code-navigation.md): find each unit's code with codebase-memory `search_graph`
  and `get_code_snippet`, check cited paths with `check_index_coverage`, then fall back to LSP/file search. Read live code, not artifact claims.
- [`testing.md`](../devrites-lib/reference/standards/testing.md): a criterion with code but no covering test is *partial*, not done.
- [`repository-topology.md`](../devrites-lib/reference/standards/repository-topology.md), [`data-integrity.md`](../devrites-lib/reference/standards/data-integrity.md), [`integration-reliability.md`](../devrites-lib/reference/standards/integration-reliability.md): only for
  triggered applicability rows; missing failure/recovery behavior is partial or absent.

## Operating rules

- **APPEND-ONLY, never rewrite.** The only write to `tasks.md` is **appending** new
  `SLICE-###` entries. Never rewrite, renumber, reorder, or delete an existing slice
  (including slices a prior convergence appended). Never edit `spec.md` or `plan.md`. Never
  touch application code: completing the appended slices is `/rite-build`'s job, not this
  skill's.
- **Clean means byte-for-byte unchanged.** When the code already satisfies everything, leave
  `tasks.md` untouched (no empty convergence header) and report a clean result. Recommend
  `/rite-prove`.
- **Use artifacts as intent.** The spec, plan, tasks, and principles are the
  contract. If assessing reveals the *spec* is wrong (the code is right and the requirement is
  stale), that's **Spec Drift**: stop and route it through the Spec Drift Guard
  ([`spec-drift-guard.md`](../rite-build/reference/spec-drift-guard.md)) + a recorded decision; never paper over a spec
  bug by appending a task that changes correct code to match a wrong requirement.
- **Partial is not done.** Code that exists but is untested, half-wired, or covers only the
  happy path is an unmet gap: enqueue the remainder, don't round it up.
- **Principles are non-negotiable.** A live violation of a declared invariant with no recorded
  exception is the top-severity gap, walked first. Absent/empty principles file → none declared
  → skip the check gracefully, never block for its absence.
- **Unadmitted bytes from a lost wright.** When a stalled slice's wright never returned an
  admitted result, act only after its terminal state is proven
  ([`parallel-dispatch.md`](../devrites-lib/reference/parallel-dispatch.md) § Cancellation);
  unproven stays a gap. Then inspect task-path bytes changed since the recorded pre-dispatch
  `git diff --name-only` baseline (none recorded → every changed task path counts). They are
  never cited `built`, never discarded (user work): classify the slice `partial (unadmitted
  bytes)` and name those paths in the appended slice. A change outside task paths stops for the human.
- **Scout observes; root classifies and writes.** Use
  [`agents.md`](../devrites-lib/reference/standards/agents.md). The evidence scout returns
  live-code citations only; the controlling chat owns built/partial/absent calls and append-only
  workspace changes.

## Workflow

0. **Read `.claude/skills/devrites-lib/reference/standards/core.md`** first (the always-on
   operating rules), then resolve the active slug, require its `state.md`, and
   read the cursor directly.
1. **Confirm the gate.** Require `spec.md` + `plan.md` + `tasks.md` in the active workspace. If
   any is missing, **STOP** and name the prerequisite (`/rite-spec` for a missing spec,
   `/rite-define` for a missing plan/tasks, `/rite-adopt` to onboard existing code). Do not
   produce partial output.
   Require `decision-coverage.md` with `Decision coverage: CLEAR`; otherwise STOP →
   `/rite-clarify`.
2. **Load intent:** [`reference/convergence-assessment.md`](reference/convergence-assessment.md).
   From `spec.md`: buildable `AC-###` / `### Requirement:` scenarios (skip `## Success metrics`);
   from `plan.md`: architecture decisions + named touch-points (files/components the plan says
   get built); from `tasks.md`: existing slices + their `Satisfies:`; from
   `.devrites/principles.md`: the invariants.
   **Completion:** every buildable criterion, touch-point, slice output, and principle is in the assessment inventory.
3. **Reconcile the map, then read the code.** Compare `spec.md`, `tasks.md`,
   `test-plan.md`, and `traceability.md` directly: every buildable AC/REQ maps to an
   existing slice, every slice maps back to real acceptance, every slice's recorded
   proof still agrees with its `test-plan.md` row, and the mapped prose preserves the
   requirement's meaning. Record orphaned, invented, duplicate, or contradictory
   mappings as gaps. Then read the live code
   (codebase-memory per [`code-navigation.md`](../devrites-lib/reference/standards/code-navigation.md)); artifact mappings never prove implementation.
4. **Assess each unit as built / partial / absent** against the live code (the rubric is in
   [`reference/convergence-assessment.md`](reference/convergence-assessment.md)): every
   acceptance criterion / scenario, every plan touch-point, and every existing slice's stated
   Produces. A principle violated in the current code is its own top-severity gap.
   Dispatch up to three independent inventory partitions to `devrites-evidence-scout` on the
   same live-code snapshot — build each scout's read-set once with
   `devrites-engine context <slug> --phase converge --role evidence-scout --out
   ctx/converge-evidence-scout.p<n>.bundle.md` and hand it the bundle path; run the wave
   through `devrites-engine dispatch <slug> open|start|seal|return` with one lane label
   per partition (`--role evidence-scout.p1 --role evidence-scout.p2 ...`, per
   [`parallel-dispatch.md`](../devrites-lib/reference/parallel-dispatch.md)), which
   auto-records dispatch/return metrics. Await their
   dossiers, then reconcile the cited facts in the root
   context. **Completion:** every inventory unit is classified once with live-code evidence.
5. **Enqueue the remainder as new slices.** For each *partial* or *absent* unit, append a
   `## SLICE-###` (continue the numbering after the highest existing id), each with a `Satisfies:` line tracing to the AC/REQ it closes and a
   `Convergence: <iso>` marker line. Dependency-order them after the existing slices; a
   principle-remediation slice sorts first. **If every unit is built → append nothing.**
   **Completion:** every partial/absent unit has one traceable appended slice, or the file is byte-for-byte unchanged.
6. **Write append-only + bookkeeping.** Append the slice batch to `tasks.md` (nothing else in
   that file changes); update `traceability.md` directly with rows for only the appended slices,
   preserving every existing row. Appending a slice changes the plan input, so invalidate the prior vet:
   update `state.md` to `Phase: plan`, `Next step: /rite-vet`, and set an existing
   `eng-review.md` field to `Implementation readiness: NEEDS REPLAN`. When nothing was unmet,
   leave the plan/vet verdict untouched and set `Next step: /rite-prove`. Append
   `decisions.md` for any material call. When slices were appended, run
   `devrites-engine check task-graph <slug>` before invoking Vet; failure stays in
   Converge for correction and never spends a Vet reviewer context.
7. **STOP.** Report units assessed, built / partial / absent / unrequested counts, slices appended, and any
   principle violation found. A direct invocation that appended slices becomes
   the caller for the mandated next step: save a return cursor
   (`return_phase`/`return_next_action`) naming this Converge pass as the
   caller, invoke `/rite-vet` inline, and consume its results — an agent-owned
   `NEEDS REPLAN` routes to `/rite-plan` repair internally under the
   fingerprint caps; its return lands here, never on the user. Stop only at
   Vet's boundary (READY readback; next step `/rite-build` for the appended
   slices). Nothing appended → recommend `/rite-prove`.

## Completion evidence (fail-closed)

Before reporting "clean" or recommending `/rite-prove`, confirm:

- [ ] Every buildable AC/REQ in the assessment inventory has a built/partial/absent
      classification with live-code citation
- [ ] Every plan touch-point and existing-slice Produces is classified with live-code citation
- [ ] Every declared principle is checked; violations are recorded as top-severity gaps
- [ ] `tasks.md` is byte-for-byte unchanged when clean, or append-only when gaps exist
- [ ] `traceability.md` updated only for appended slices
- [ ] No narrative "done" without the checklist above

**Failing case:** all units marked built but one AC lacks a test or runtime citation →
report partial, append slice, route `/rite-vet`.

## Appended slice format

Use the complete
[`canonical slice grammar`](../devrites-lib/reference/workspace-artifact-schema.md#canonical-slice-grammar)
with one added `Convergence:` field after `Satisfies:`:

```markdown
<!-- Convergence 2026-07-07: slices below appended by /rite-converge — live code assessed against intent. -->
## SLICE-014 <name of the unmet capability>
Satisfies: AC-007            # the criterion / scenario this closes
Convergence: 2026-07-07      # marks this as a convergence-appended slice, not an original
<all remaining canonical slice fields>
```

> **Mid-flight discipline.** Do not rewrite an existing slice, edit source, mark a
> happy-path-only implementation as built, or add work for a spec you suspect is wrong.
> See [`reference/anti-patterns.md`](reference/anti-patterns.md).
