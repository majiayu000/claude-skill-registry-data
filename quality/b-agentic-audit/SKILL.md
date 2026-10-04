---
name: b-agentic-audit
description: >
  Four-dimension read-only b-agentic audit covering source/design
  conformance, whole-project and first-party-extension health, canonical
  skill/kernel quality, and currentness/MCP compatibility, with evidence
  thresholds and approval-gated live probing. Routing signals: b-agentic
  audit, suite audit, maintainer audit, design-conformance audit,
  decision-design drift. Delegated: runs only in the `b-reviewer`
  subagent; the main session never executes it itself.
metadata:
  phase: Validate
  execution_mode: subagent
  agent: b-reviewer
---

<!-- Generated from skills/registry.yaml and skills/b-agentic-audit/prompt.md. Edit those sources, not this file. -->

# b-agentic-audit

Run a read-only, source-based b-agentic audit across four dimensions:

1. **Existing source/design conformance** — compare the evidence-backed decision
   record with canonical sources, generated assets, workflow, safety, install,
   tooling, and verification behavior; report actual source, safety, or semantic
   drift.
2. **Whole-project and first-party-extension health** — inspect for concrete
   defects, integration gaps, harmful duplication, maintainability friction, and
   performance candidates. Performance evidence threshold: measured hotspot or explicit algorithmic, safety, or complexity evidence. Never infer a problem from file size or export count alone.
3. **Canonical skill/kernel quality** — assess skill boundaries, evidence
   thresholds, routing, safety/privacy rules, read-only handoffs, prompt
   maintainability, and generated synchronization against the canonical prompt,
   registry, and kernel sources.
4. **Currentness/MCP compatibility** — resolve local package pins and installed
   versions, then use bounded primary upstream evidence for version/API
   compatibility without transmitting repository or private data. Live MCP schema probing is approval-gated because it may start configured processes,
   use authentication, or populate caches; if it is not approved or unavailable,
   report currentness/live evidence as unverified.

This audit supplements deterministic checks; it does not mechanically prove all
prose semantics and never substitutes for changed-code `b-review`.

## Delegation boundary

`b-agentic-audit` runs only in the `b-reviewer` subagent.

- Main session: reading this file prepares the handoff; it never authorizes running the steps below yourself. Gather the parent-owned evidence and confirm the effective `b-reviewer.md` (project `.pi/agents/` over the Pi agent directory's `agents/`) is readable and its parsed frontmatter `tools` value, normalized to a list (comma-separated scalar or YAML sequence), is explicit, non-empty, and contains neither `edit` nor `write` (a missing, blank, or null `tools` grants them), then call `subagent` with agent `b-reviewer` and a bounded task naming `b-agentic-audit`. Do not do this skill's work with your own tools, even for a quick, small, or single-lookup request. If the subagent is unavailable or fails, or its result notes an unknown agent type or `general-purpose` fallback (discard that result), report the gap and ask the user; never fall back to self-execution. Evaluate the returned result before any user-facing or worktree action.
- `b-reviewer` child: execute the steps below read-only, return this skill's Output format to the main session, and do not delegate again.

## Mandatory origin freshness gate

Before any other audit step or repository read, require the main session to
supply its completed origin-freshness evidence:

1. The main session refreshes local remote-tracking metadata and resolves the
   current branch and its configured `origin/*` upstream without pull, merge,
   rebase, or working-tree modification.
2. It supplies the metadata-only comparison of `HEAD` with that upstream and
   its ahead/behind counts. Proceed only when both counts are zero.
3. If the evidence is missing, the branch is detached, the `origin` ref is
   missing, the metadata-only branch comparison fails, or the branch is ahead,
   behind, or diverged, report only: `BLOCKED: current branch is not up to date
   with origin; synchronize it and rerun the audit.` Do not read audit sources,
   run audit checks, perform MCP/currentness probes, or issue normal findings or
   a verdict.

## When to use

- The user requests a b-agentic repository audit, suite audit, maintainer audit,
  or design-conformance audit.
- The repository decision record, canonical skills/kernel, generated assets,
  workflow, safety, install, tooling, or verification behavior may have drifted.
- A maintainer needs evidence-backed whole-project health, skill/kernel quality,
  or currentness/MCP compatibility findings before a release.

## When NOT to use

- Reviewing a working-tree, staged, checkpoint, or commit-range code diff -> use
  **b-review**.
- Implementing an audit finding -> use **b-frontend** for frontend/UI production changes,
  **b-implement** for other production changes, or **b-refactor** for a named
  behavior-preserving transform after the audit.
- Planning an ambiguous audit scope -> use **b-plan**.
- General UI/design review or broad external research -> use **b-browser**,
  **b-design**, or **b-research** as appropriate.

## Tool guidance

- Read-only shell commands (for example `git status`, `git diff`, `rg`) are
  available for inspecting repository evidence; do not run mutating commands.
  Inspect the main session's supplied freshness, status, audit-script, and
  narrow-check evidence; state an explicit evidence gap when a required check
  cannot be run read-only.
- `read` - inspect `docs/decision_design.md` and the canonical source files it
  cites; prefer sources over generated assets when comparing behavior.
- `context7` or bounded primary upstream documentation/release metadata - verify
  versioned package/API currentness only when needed; do not upload local files,
  repository content, credentials, or private URLs.
- `codegraph` - select when a concrete repository-wide architecture, impact, or
  affected-test question is central to the audit and likely valuable; use an
  available index for that question and report an absent-index gap to the main
  session. Spanning files alone never justifies it.

## Steps

1. Confirm the main session's mandatory origin-freshness and status evidence
   before defining the four-dimension audit surface or reading repository files.
   If it is incomplete, report the blocking evidence gap.
2. Read the decision record and identify relevant decisions, evidence markers,
   referenced sources, generated surfaces, explicit non-goals, and local pins.
3. Assess the main session's `scripts/b-agentic-audit.sh` output for structural,
   generated-sync, behavioral, and decision-design traceability results. Treat a
   passing script as evidence for those checks only; report it as missing when it
   was not supplied.
4. Perform the source-based comparison for conformance and health: read cited
   canonical sources, inspect first-party extensions and integration seams, and
   report concrete defects, gaps, duplication, maintainability friction, and
   measured or explicitly evidenced performance candidates. Do not turn broad
   suspicion into a finding.
5. Assess canonical skill/kernel quality by checking routing boundaries,
   evidence thresholds, safety/privacy guidance, no-edit handoffs, prompt
   cohesion, generated assets, and kernel headroom against the source record.
   When recurring memory lessons plausibly generalize across
   sessions, flag them as distillation candidates for canonical skill prompts;
   promote them through b-implement against `skills/*/prompt.md` with
   `registry_sync`, rather than leaving them only in volatile memory.
6. Assess currentness/MCP compatibility from local pins and installed versions.
   Use `context7` or bounded primary upstream evidence for compatibility claims. A live MCP
   schema probe is an explicit operational step: require the main session to
   obtain approval and supply its result, and if approval, evidence, or a usable
   environment is missing, report the limitation rather than guessing or
   exposing raw errors.
7. Use native inspection first. Select CodeGraph when a distinct concrete
   architecture/impact/affected-test question is central to the audit and
   likely valuable; use an available index for that question and report an
   absent-index gap to the main session. Spanning files alone never justifies
   initialization.
8. Separate deterministic results from semantic findings. Order findings by
   severity and cite repository-relative paths, evidence, impact, and the
   smallest follow-up route. State what was not mechanically proven.
9. Keep the audit read-only. Record needed changes as follow-up; do not edit during the audit.

## Output format

Findings (ordered by severity), four-dimension source-based comparison,
automated checks, checked-and-clean areas, currentness/live-evidence status,
residual limitations, and follow-up. If the freshness gate fails, report the
blocked notification only and do not emit the normal findings or verdict.
Verdict:

- `NEEDS FIXES` when there is actual source, safety, or semantic drift.
- `READY WITH FOLLOW-UPS` when no finding exists but required external,
  currentness, or live MCP evidence is unavailable or unverified.
- `READY FOR PR` only when all required dimensions and evidence are verified.

## Rules

- Keep the audit strictly read-only: do not edit, stage, commit, push, run
  mutating commands, or apply fixes. Route frontend/UI production fixes to **b-frontend**,
  other behavioral fixes to **b-implement**, and named behavior-preserving
  transforms to **b-refactor**; do not edit during the audit.
- The main-session origin freshness evidence is mandatory before every audit
  action. A missing, failed, or non-zero comparison is a blocked audit, not a
  finding; return the blocking message to the main session and stop without auditing or issuing a verdict.
- Prefer repository evidence over assumptions and cite repository-relative paths.
- Do not claim that passing structural or traceability checks proves all prose
  semantics, production readiness, health, currentness, or the absence of drift.
- Do not treat generated assets as canonical when a source file exists.
- Do not transmit repository/private data or credentials for currentness checks.
- Do not use live MCP schema probing without approval; report it unverified when
  unavailable. Do not expose credentials, token values, private URLs, or raw
  operational errors.
- Do not use this skill as a generic code-diff review; triggered independent
  review of a frozen changed candidate belongs to **b-review**.
