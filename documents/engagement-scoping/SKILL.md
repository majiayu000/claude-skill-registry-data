---
name: engagement-scoping
description: "Resolve the documentation engagement scope from the settings cascade — project identity, source roots, output root, delivery mode, action ceiling, confidentiality default, and the exact file set this run may touch — and freeze it to `<outputRoot>/00-control/.scope.json`. Use when any /dossier:* command starts, when the delivery mode changes, or when a run must prove it stayed inside its permitted boundary. This skill MUST be consulted because a run that widens its own scope mid-flight produces a package nobody can audit — the action ceiling and the touched-file set are decided before the first file is read and are immutable for the remainder of the run."
allowed-tools: Bash, Read, Glob, Grep
context: fork
agent: Explore
---

# Engagement Scoping

Phase 0 of every dossier run. Establishes what this run is, what it may touch, and what it may do — before it reads a single source file.

## Iron Law

**RESOLVE SCOPE BEFORE READING ANYTHING. The action ceiling and the file set are fixed in Phase 0 and never widen mid-run.**

A run that discovers a reason to read one more directory, execute one more command, or write one more file has stopped being auditable. Record the need as an `AQ-####` row and finish inside the ceiling you started with.

## Resolution order

Every value comes from `bin/dossier-resolve-config.sh`, never from reading a settings file directly — reading one directly skips four layers of the cascade. See `references/config-resolution.md`.

```bash
OUTPUT_ROOT=$(bin/dossier-resolve-config.sh --default "docs/dossier" dossier.project.outputRoot)
MODE=$(bin/dossier-resolve-config.sh --default "full" dossier.engagement.deliveryMode)
bin/dossier-validate-config.sh || printf '%s\n' "config findings above must be resolved before drafting"
```

Validate before scoping. A config that fails `dossier-validate-config.sh` produces a package whose containment guarantees do not hold, and finding that out in Phase 5 wastes the whole run.

## The twelve inputs

| Input | Config key | When absent |
|---|---|---|
| Project name | `project.name` | Blocking in `full`/`targeted`. Ask — never infer, because an inferred product name propagates into public documents |
| Mission | `project.mission` | Record `U`. Derive what evidence supports; never invent intent |
| Sources | `project.sources` | Blocking in `full`/`targeted` |
| Output root | `project.outputRoot` | Blocking in every mode |
| Version or commit | `project.versionOrCommit` | `auto` resolves the current SHA and **pins it for the whole run** |
| Due-diligence context | `engagement.dueDiligenceContext` | Produce a general technical and product readiness assessment. Never invent transaction-specific acceptance criteria |
| Stakeholders | `engagement.stakeholders` | Ownership is `unassigned`, which is a true statement; a plausible name is a false one |
| Constraints | `engagement.constraints` | Each constraint that blocks a check becomes a `not executed` reason, not an unexplained gap |
| Disclosure policy | `disclosure.policy` | Defaults to `internal-only` — draft the public documents fully, release none |
| Regulatory context | `engagement.regulatory` | Identify candidates; applicability is itself a claim needing evidence |
| Allowed actions | `engagement.allowedActions` | Restrictive defaults. The safe failure is an honestly-labelled unverified claim, not an unauthorized action |
| Delivery mode | `engagement.deliveryMode` | `full` |

## Delivery modes

| Mode | Inspection | Writes | Completion condition |
|---|---|---|---|
| `full` | The whole scope | Creates or rebuilds all 23 files | Every canonical file exists with a status and a `last-verified` date |
| `targeted` | Changed evidence first, then everything downstream of it | Only affected documents and their dependents | Affected set updated **and** the whole package re-checked for contradictions — a targeted refresh that skips the package-wide contradiction sweep is a `full` run with holes |
| `verification-only` | The existing package plus the sources needed to check it | `07-verification/` only, unless `allowedActions` permits repair | The verification report is written and the gate verdict issued |

`targeted` resolves its blast radius through `bin/dossier-blast-radius.sh` and `references/change-triggers-and-blast-radius.md`. The changed-evidence set is the input; the affected-document set plus every document that consumes a changed claim is the output.

## The action ceiling

`engagement.allowedActions` is not advice. `hooks/scripts/enforce-output-root.sh` and `enforce-allowed-actions.sh` block violations at `PreToolUse`, so a scope decision recorded here is a scope decision enforced.

| Action | Off means |
|---|---|
| `runBuild` / `runTests` | Every setup, build, and test claim is `not executed` with a reason — never assumed to pass |
| `networkAccess` | Vendor lifecycle, CVE, and license claims are labelled rather than answered from model memory |
| `runSecurityScan` | osv-scanner is never invoked (by the isolated scan job or, as a backstop, directly). Vulnerability evidence is limited to scan artifacts the project already produced, or reported as not run |
| `runCodeQualityScan` | pyscn is never invoked. Independent of `runSecurityScan` — enabling one never enables the other |
| `readSecrets` | Record a secret's type, location category, and rotation need. Never its value |
| `writeOutsideOutputRoot` | The package is the only artifact. Unrelated user work is preserved untouched |
| `contactHumans` | Non-blocking unknowns go to the open-questions register instead of stalling the run — the default in CI |

## Classifying the project

Classify from evidence before scoping the inspection, because the classification changes which sources matter. Record the classification with its supporting evidence IDs — a wrong classification produces a subtly wrong package. See `references/project-type-adaptation.md`.

Structure never adapts. All 8 directories and all 23 files exist for every project type; only emphasis and justified `N/A` change.

## Large scopes

When the scope exceeds one context, build an inspection map and process it in bounded batches. Record the batch boundaries in the scope file.

Never silently skip a directory, a service, or an evidence class. A skipped area is an inspection-coverage gap with an `AQ-####` row, and it appears in the evidence ledger's source-inventory section. Silence here is indistinguishable from "we looked and found nothing".

## Output Format

Write `<outputRoot>/00-control/.scope.json` and emit the summary below. The file is the run's contract; later phases read it rather than re-resolving config.

```json
{
  "schema_version": 1,
  "resolved_at": "<ISO-8601>",
  "project": { "name": "", "type": "", "version_or_commit": "", "sources": [] },
  "output_root": "",
  "delivery_mode": "full | targeted | verification-only",
  "allowed_actions": {},
  "disclosure": { "policy": "", "confidentiality_default": "", "approval": "" },
  "touchable_paths": [],
  "inspection_batches": [],
  "blocking_gaps": [],
  "access_limitations": []
}
```

```markdown
### Scope

| Field | Value | Source layer |
|-------|-------|--------------|
| {input} | {value} | env / local / project / user / plugin / default |

### Work plan
{ordered phases for this delivery mode}

### Source access limitations
| Evidence class | Available? | Effect on the package |
|---|---|---|

### Blocking gaps
{questions that must be answered before drafting, or `none`}
```

Non-blocking unknowns never appear in "blocking gaps". They go to the register and the run continues.

## Rationalization Prevention

| Excuse | Response |
|--------|----------|
| "I need to read one file outside `sources` to understand this" | Then `sources` was wrong. Record an `AQ-####` and finish inside the ceiling. |
| "Running the test suite would verify so much at once" | Not with `runTests: false`. Mark the claims `not executed` and say why. |
| "The project name is obvious from `package.json`" | Obvious to you. It goes in every header and every public document. Ask. |
| "Disclosure policy is unset but this is clearly public" | Unset means `internal-only`. Draft everything, release nothing. |
| "I will note the scope after I see what's there" | Then the scope is whatever you found, which is not a scope. |
| "This is a small project, the mode does not matter" | The mode decides whether a contradiction sweep runs. It matters most when the package looks easy. |

## Integration

Invoked first by `/dossier:init`, `/dossier:baseline`, `/dossier:refresh`, `/dossier:audit`, and `/dossier:gate`. `dossier-evidence-collector` loads it to know its inspection boundary. Every other skill reads `.scope.json` rather than re-resolving configuration.

References: `references/config-resolution.md`, `references/project-type-adaptation.md`, `references/change-triggers-and-blast-radius.md`.
