---
name: architecture-normalizer
description: "Decomposes large modules, god files, classes, or packages in reviewable steps while preserving public APIs. Not for routine refactors."
---

# Architecture Normalizer

## Purpose

Use this skill as an architecture normalization engine, not as a general refactoring assistant. Its job is to move a repository toward deterministic, high-cohesion, low-coupling module hierarchy while preserving behavior and public APIs.

The central rule: every architectural decision must be produced as an explicit reviewable artifact before any source file is changed.

## Required References

- Read `references/policy-format.md` before creating, editing, or applying architecture policies.
- Read `references/artifact-contract.md` before generating, reviewing, or executing `.architecture/` artifacts.
- Read `references/analysis-signals.md` when scoring cohesion, coupling, entropy, god files/classes/packages, split candidates, or dependency risk.
- Use `scripts/repo_fingerprint.py <repo> --json` for manifest repository hashes and execution preflight checks.

## Non-Negotiable Contract

- Do not modify source files during Analysis. Analysis may only create or update `.architecture/` artifacts.
- Do not execute normalization without completed Analysis artifacts and explicit approval for the specific actions being executed.
- During Execution, never invent moves, splits, renames, import updates, exports, compatibility layers, or deletes. Execute approved artifact actions only.
- Preserve public imports and exports whenever possible. Generate compatibility exports for moved public API paths.
- Load policies before analysis. Do not hardcode language thresholds, layout rules, public API rules, or allowed dependency rules into the plan.
- Keep output deterministic: sorted paths, stable action IDs, stable artifact filenames, and stable YAML/JSON ordering where feasible.
- Stop when the repository fingerprint differs from the manifest, artifacts conflict, a policy is missing or ambiguous, or validation cannot be run.
- Do not print or store secrets. Prefer structural evidence: imports, exported symbols, file names, non-secret config keys, tests, and public APIs.

## Phase 0: Policy Loading

1. Inspect repository structure and dependency/config files enough to identify languages and tooling.
2. Load existing policies from `.architecture/policy.yaml` or `.architecture/policies/*.yaml` when present.
3. If no approved policy exists, resolve a conservative baseline policy from `references/policy-format.md`, write it under `.architecture/policies/<language>.yaml` with `status: proposed`, and mark all execution actions unapproved.
4. Record the resolved policy files and versions in `.architecture/manifest.yaml`.

Execution is forbidden when the relevant policy is only proposed, rejected, missing, or internally inconsistent.

## Phase 1: Architecture Analysis

Analysis is read-only for repository source files. It must generate deterministic artifacts inside `.architecture/`.

Required analysis behavior:

- Compute the repository fingerprint with `scripts/repo_fingerprint.py`.
- Detect single-responsibility violations, multiple public types, god files, god classes, god packages, cyclic imports, dead code candidates, duplicate models/DTOs/enums/errors, forbidden generic names, large files/classes/functions, hidden public APIs, layer violations, dependency violations, feature envy, and architecture entropy.
- Generate explicit remediation artifacts for every proposed change.
- Use stable IDs such as `MOVE-0001`, `SPLIT-0001`, `RENAME-0001`, `IMPORT-0001`, `EXPORT-0001`, and `COMPAT-0001`.
- Sort actions by normalized source path, action kind, then destination path.
- Include evidence and rationale for every action. Evidence should cite files, symbols, imports, exported APIs, tests, or dependency edges.
- Use `generated_at: null` unless a deterministic repository-derived timestamp is available, such as the HEAD commit timestamp.

Required artifact set:

- `.architecture/manifest.yaml`
- `.architecture/analysis.md`
- `.architecture/entropy.json`
- `.architecture/dependency-graph.graphml`
- `.architecture/package-layout.graphml`
- `.architecture/move-plan.yaml`
- `.architecture/split-plan.yaml`
- `.architecture/rename-plan.yaml`
- `.architecture/imports-plan.yaml`
- `.architecture/exports-plan.yaml`
- `.architecture/compatibility-plan.yaml`
- `.architecture/risk-report.yaml`
- `.architecture/validation-plan.yaml`

If a graph format cannot be produced with available tooling, create the file with a deterministic placeholder graph containing the nodes/edges that were derived and record the tooling gap in `risk-report.yaml`.

## Phase 2: Human Review

Artifacts are the review boundary.

- Treat user edits to artifacts as authoritative unless they violate the non-negotiable contract.
- Execute only actions with `status: approved` or with an explicit current user instruction approving the exact action set.
- Treat missing, proposed, rejected, stale, or conflicting actions as not executable.
- If review changes introduce new decisions, return to Analysis and regenerate affected artifacts before execution.

## Phase 3: Architecture Execution

Execution reads approved artifacts only. It must not perform fresh architectural analysis.

Before editing source files:

1. Recompute the repository fingerprint.
2. Compare it with `.architecture/manifest.yaml`.
3. Inspect `git status --short` and avoid overwriting unrelated user changes.
4. Stop if the repository changed, unless the user explicitly asks to regenerate Analysis.

During execution:

- Prefer `git mv` for file moves.
- Apply approved moves, splits, renames, import updates, public exports, and compatibility layers in dependency-safe order.
- Preserve public APIs through explicit exports: Python `__init__.py`, TypeScript/JavaScript `index.ts` or `index.js`, Rust `pub use`, Go exported symbols, C/C++ public headers.
- Do not use wildcard exports.
- Delete obsolete files only when an approved delete action exists.
- If a needed action is missing, stop and write `.architecture/execution-blockers.yaml`.

Execution must be idempotent. Running it twice against the same approved artifacts should produce no further source changes.

## Phase 4: Validation

Validation is mandatory after execution.

Run the validation commands declared by policy and confirmed from repository configuration when available:

- formatter
- linter
- compiler or type checker
- unit and integration tests
- import/public API validation
- architecture layout validation

Record validation commands and results in `.architecture/validation-results.yaml`. Report failure exactly; do not claim success unless commands were run and passed.

## Output Discipline

When reporting results:

- Separate Analysis, Review, Execution, and Validation status.
- List generated or changed artifacts.
- List source files changed only after Execution.
- Include exact validation commands and outcomes.
- State when execution was refused because approval, policy, fingerprint, or validation gates were not satisfied.
