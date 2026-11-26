---
name: spec-drift-detection
description: Use after implementation completes and before review begins, to verify the actual change matches the approved spec — files touched, public contracts added, security impact, and declared scope.
type: skill
license: MIT
compatibility:
  - claude-code
  - codex
user-invocable: false
effort: high
---

# Spec-Drift Detection

> **Tool discipline:** read-only — `Read`/`Grep`/`Glob` and read-only `Bash` (`git diff`, the drift scripts). Never `Edit`/`Write` code or the spec; report drift, never fix it.

## Overview

Verify that the implementation delivered what the spec promised — nothing more, nothing less.
Drift between spec and implementation means the Phase 2.5 approval gate did not cover the final
code, a compliance risk in regulated environments; detect divergence before review.

## When To Use

- After implementation batches complete, before handing to `compliance-reviewer` in Phase 4
- A spec manifest exists at `docs/specs/<date>-<slug>.json` and the reviewer wants to confirm the declared scope was honored

### When NOT To Use

- Quick fixes, typo fixes, or config updates that ran without a spec, or sessions where no spec manifest was ever produced

## Workflow

1. **Locate the spec manifest.**
   - Default: the latest `docs/specs/*.json` on the current branch.
   - Override: accept an explicit path if the engineer supplies one.
   - If no manifest exists, **stop** and report `BLOCKED — no spec manifest
     found; drift cannot be checked. Either generate one via
     `spec-driven-development` or confirm this change is quick-fix scope.`

2. **Load the manifest schema fields:**
   - `scope` — classification string
   - `change_manifest` — array of `{ path, action, purpose }`
   - `public_contracts` — array of `{ kind, signature, change }`
   - `success_criteria` — array of `{ id, description, verification }`
   - `out_of_scope` — array of strings
   - `security_impact` — enum string

3. **Collect actual change data:**
   - **Preferred (deterministic):** run
     `bash scripts/validate-handoff.sh docs/specs/<date>-<slug>.json`
     to compute file-level and security-impact drift against the
     manifest. Treat its output as authoritative for those axes.
   - If the handoff has an `implement.actual_files` array, diff it
     against `change_manifest[].path` directly — no git invocation needed.
   - Otherwise, fall back to `git diff --name-status <base>...HEAD`.
   - For contract-level drift (not covered by the script): grep the diff
     for added/modified public contracts (controller routes, handler
     classes, exported functions, etc., per active tech stack).

3a. **EARS / ANT structural lint of the spec itself (extended-mode specs only).** When the spec header says `Spec mode: extended`, run
   `bash scripts/lint-ears.sh <spec.md>` (the markdown spec next to the JSON
   sidecar). EARS / ANT violations on the spec count as drift of the spec
   from its own contract — emit one finding per violation with
   `source: "drift"`, `severity: "warning"`, `confidence: 100`,
   `rule: "EARS / ANT"`. They do not block on their own (warning, not
   critical), but they signal a spec that should be tightened before the
   next iteration. Standard-mode specs have no EARS section; skip this step. If
   `scripts/lint-ears.sh` is absent, skip with a one-line note in the output.

4. **Compare and emit findings** per
   `.claude/references/review-finding-schema.md`, with `source: "drift"`:

   | Axis | Finding criteria | Confidence band |
   |------|------------------|-----------------|
   | File-list match | File touched that is not in change_manifest | 95–100 (deterministic) |
   | File-list match | Derived artifact touched that is not in change_manifest | **not a finding** — see below |
   | File-list match | File declared in change_manifest that was not touched | 95–100 |
   | Public contract | Signature added that is not in public_contracts | 85–95 |
   | Public contract | Contract declared but not implemented | 90–100 |
   | Security impact | `security_impact: none` but auth/payments/audit files touched | 95+ |
   | Out-of-scope | Declared out_of_scope item that appears to be implemented | 80–90 |
   | Success criteria | Criterion has no mapped test in the diff | 80 |
   | Ownership | Touched a slice/module not listed in the spec's declared ownership (cross-slice creep) | 80–90 |
   | Dependency shift | New package, SDK, or external service in the diff that was not declared in the spec's dependency intake | 90–100 |
   | Usage | Public contract removed/renamed but call-sites in other slices weren't updated | 85–95 |

   **Derived artifacts are collateral, not drift.** `validate-handoff.sh` sorts
   undeclared files into machine-written and hand-written before reporting:
   lockfiles, snapshots, generated sources (`*.Designer.cs`, `*.g.cs`,
   `*_pb2.py`, `*.generated.*`), minified bundles, and any file whose own first
   lines say it is generated land in a `NOTE:` section rather than the CRITICAL
   one. Do **not** ask the planner to enumerate machine output in the
   change_manifest — that trains the manifest to list files no human writes, and
   the one that gets forgotten then reports as drift for a file nobody typed
   (a 2026-09 field run lost a drift slot to a regenerated `INDEX.md`). What is
   worth checking is the *regenerator*: confirm the tool that produced them
   belongs to this change. An undeclared lockfile stays critical via the
   dependency axis, which reads its contents rather than its path.

   **Ownership.** Parse the spec's declared slice/module ownership (from the
   architecture-and-design section or `change_manifest[].path` prefixes) and
   compare against the slice prefixes of every touched file. Cross-slice
   touches without justification are drift.

   **Dependency shift.** Diff the lockfile / project file (`packages.lock.json`,
   `*.csproj <PackageReference>`, `requirements.txt`, `pyproject.toml`,
   `package.json` + `package-lock.json`, `pnpm-lock.yaml`, `Cargo.toml`) and
   list any added/upgraded dependencies. Cross-check against the spec's
   declared dependency intake (Claude-Ready checklist +C #6). Undeclared
   dependencies are drift — they should have triggered the security/license
   review gate during spec writing.

   **Usage.** For removed/renamed public contracts in `public_contracts`,
   grep the repo for remaining call-sites. Any unupdated call-site is a
   usage-drift critical finding.

   **Coverage.** For every `coverage_claims[]` entry in the sidecar, re-grep the
   write sites now that the code exists. A claim that one point covers several
   callers is drift the moment a caller bypasses it — and this is the drift class
   that leaves a feature passing every test while doing nothing for one of its
   paths. An entry with `verified: false`, an empty `write_sites`, or a newly
   added write site that does not route through the claimed point is a
   **critical** finding. An unenumerated coverage claim in the spec body is the
   same finding: the claim was never checkable.

   **Pre-authorised descopes.** Read `conditional_descopes[]`. An entry with
   `fired: true` is a legitimate scope *reduction* (item 4 below) — but only with
   `evidence` naming what made the condition true. `fired: true` without
   evidence is silent drift wearing the spec's authority, and is a critical
   finding. Conversely, work that quietly stopped matching the manifest while a
   matching descope sat unfired is an unrecorded reduction: flip it, evidence it,
   and re-score rigor.

   **Collateral churn.** Run `bash hooks/collateral-guard.sh --range <base>...HEAD
   --manifest docs/specs/<date>-<slug>.json`. Whitespace/EOL-only rewrites,
   undeclared generated files, and wholesale asset regeneration are not spec
   drift in the contract sense, but they land in the same commit and they hide
   the real diff from every reviewer downstream. Report the verdict; a finding
   here is a warning unless the collateral is a lockfile carrying an undeclared
   dependency, which the dependency axis already makes critical.

5. **Emit the schema-conformant output** (markdown table + fenced JSON).
   Drift findings mix with any AI review findings downstream. `severity`
   mapping:
   - Missing/extra file → `critical` (spec approval didn't cover this code),
     except a derived artifact, which is reported as a note and scores nothing
   - Contract divergence → `critical`
   - Security-impact understated → `critical`
   - Success criterion unmapped → `warning`
   - Out-of-scope hit → `warning`
   - Ownership / cross-slice creep → `warning` (escalates to `critical` if
     the crossed slice is regulated — auth, payments, audit)
   - Dependency shift (undeclared) → `critical`
   - Usage drift (stale call-site after rename) → `critical`

6. **Verdict:**
   - Any `critical` drift → `NEEDS_CHANGES`. The engineer either fixes the
     implementation to match the spec, or re-opens the spec, amends it, and
     re-runs through the Phase 2.5 approval gate.
   - No critical drift → `PASS`. Continue to Phase 4 review. A clean PASS is
     the precondition for archiving the spec delta into its baseline
     (implement Phase 7.5, `scripts/spec-archive.sh`) — do **not** archive
     while any critical drift is open, or the baseline would record a state
     the code does not match. See `.claude/references/delta-spec-model.md`.

## Monorepo Ripple Check

After comparing the manifest, also run a cross-package ripple check on the change manifest. This catches "one-package change with many-package impact" surprises.

```bash
bash scripts/monorepo-ripple.sh $(git diff --name-only <base>...HEAD)
```

`<base>` is the same base as step 3 (the branch point of this change). A bare `HEAD` would only see uncommitted edits and miss every batch already committed.

- Exits 0 on non-monorepo (no output) — no false positives.
- On a monorepo, emits lines `RIPPLE <pkg>: affects <downstream>`.
- Treat ≥1 ripple line as a **warning-level** drift finding (not blocking), unless the spec's `change_manifest` already lists the downstream packages — then it's expected and silent.

## Rules

- No drift check without a spec manifest. If the manifest is missing,
  escalate; do not fabricate one from the git diff.
- Drift findings are high-confidence by construction: they come from
  comparing two structured lists, not from judgment.
- The spec is the source of truth — do not rewrite it silently to match
  implementation. If the implementation is correct and the spec is wrong,
  stop and ask the engineer to amend the spec and re-approve.
- A clean `PASS` does not mean the code is good — only that it matches what
  was approved. Code quality still goes through `compliance-reviewer`.

## Architecture Principle Drift (S1.15)

In addition to manifest drift, also compare the implementation against tagged
principles in `.claude/references/architecture-principles.md`. Severity is
determined by the principle's confidence tag:

| Tag | Contradicting change → |
|---|---|
| `[EXTRACTED]` | **block** (critical drift) — the principle was directly observed in code; violating it is a regression. |
| `[INFERRED:>=0.7]` | **flag** (medium drift) — likely-correct pattern; surface for engineer decision. |
| `[INFERRED:<0.7]` | **note** (low drift) — weak inference; mention but do not block. |
| `[AMBIGUOUS]` | **note** — sources disagree; surface both options. Do not block. |

If `architecture-principles.md` is missing or has no tags (legacy format),
skip principle drift and continue with manifest drift only — emit a one-line
note that principle drift was unavailable.

## Gate

If the workflow artifact is active, drift findings flip the `phase_exit_gate` for the review phase. Critical drift → `phase_exit_gate fail` (triggers remediation). Spec amendment with engineer approval → re-evaluate `plan_trust_gate` from `pending`. See `.claude/references/orchestration-gates.md`.

## Verification

- [ ] Spec manifest was loaded from disk, not reconstructed from memory
- [ ] Touched files, public contracts added in the diff, and `security_impact` were each compared against the manifest
- [ ] Ownership, dependency, and usage axes ran: cross-slice creep flagged; undeclared lockfile/project-file additions flagged critical; renamed/removed public contracts grepped for remaining call-sites
- [ ] Coverage and descope axes ran: every `coverage_claims[]` entry re-grepped against the implemented code (unenumerated or bypassed claims critical); every fired `conditional_descopes[]` entry carries evidence and no unrecorded reduction was left unflipped
- [ ] Collateral axis: `hooks/collateral-guard.sh` was run and its verdict reported
- [ ] Findings follow `.claude/references/review-finding-schema.md` with `source: "drift"`; verdict matches the severity of the drift (critical → NEEDS_CHANGES)
- [ ] No silent spec edits were made to suppress drift findings
- [ ] Extended-mode spec: `bash scripts/lint-ears.sh` was run against the spec markdown (or skipped with a note when the script is unavailable)
