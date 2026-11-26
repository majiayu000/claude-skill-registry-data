---
name: certification-checker
description: This skill should be used when the user asks to "check certification compliance for X", "verify feature X against the conformance criteria", "run a certification check on Q6", "are we ready to certify T9", "what do we need for Q2 certification", "check if we pass the conformance criteria for A-8", or any similar request to evaluate a specific QTI feature ID against the 1EdTech certification acceptance criteria.
---

# Certification Checker

Evaluate whether the pie-qti codebase meets the 1EdTech DELIVERY acceptance criteria for a
specific QTI conformance feature ID (e.g. `Q2`, `T9`, `A-8`, `I19a`).

Public certification work in this repository must use clean-room fixtures and
`bun run test:certification:public`. The official conformance suite lives in the
private `pie-qti-conformance` project and must not be read or copied into this repo
when building public tests.

## Step 1 — Resolve the feature location

Load `references/feature-index.md` to look up the exact directory path for the given feature
ID and version. If the version is not specified, check both QTI 2.2 and QTI 3.0.

If the feature ID is ambiguous (e.g. `Q2` appears in both Basic and Advanced), check all
relevant directories.

## Step 2 — Read the acceptance criteria

Read the `README.md` in the feature's conformance directory. Extract only the **DELIVERY**
acceptance criteria (lines under the `#### DELIVERY` or `### DELIVERY` heading). Ignore
EXPORT, IMPORT, and AUTHORING criteria.

If the README references sub-directories (e.g. `single-cardinality/`, `multiple-cardinality/`),
read those READMEs as well and include all delivery criteria.

For Elevated Accessibility features (A-2a, A-9, A-13b, etc.), read the top-level
`qti3.0/Elevated Accessibility/README.md` which contains all EA acceptance criteria.

## Step 3 — Map to implementation files

Use `references/feature-index.md` (codebase mapping table) to identify the relevant
implementation files for this feature. Read those files to understand the current implementation.

For interaction features: read both the extractor and the component.
For test/assessment features: read the relevant assessment-player module.
For response processing: read the operators or templates module.
For accessibility/catalog features: read the catalog or PNP module.

If the feature maps to an unknown path, search the codebase:
- `grep -r "<featureKeyword>" packages/ --include="*.ts" -l`
- `find packages/ -name "<componentName>*"`

## Step 4 — Evaluate each criterion

For each DELIVERY acceptance criterion, determine:

- **PASS** — the codebase demonstrably satisfies the criterion. Cite the specific file and
  line range that implements it.
- **FAIL** — the codebase demonstrably does not satisfy the criterion. Explain what is
  missing and what would need to be implemented.
- **NEEDS INVESTIGATION** — cannot determine pass/fail from static analysis alone; a live
  test run is required. Explain what to look for when running the test package.

## Step 5 — Report

Produce a structured report:

```
## Certification Check: <Feature ID> — <Version> <Level>

### Acceptance criteria source
<path to README in conformance repo>

### Criteria evaluation

| Criterion ID | Summary | Status | Evidence |
|---|---|---|---|
| <e.g. Q2-D1> | <one-line summary of criterion> | PASS / FAIL / NEEDS INVESTIGATION | <file:line or explanation> |

### Overall verdict
<READY TO SUBMIT | GAPS FOUND | INVESTIGATION REQUIRED>

### Next steps
<bullet list of actions: files to fix, test commands to run, acceptance criteria to manually verify>
```

## Verification commands

When evaluating test-execution criteria (e.g. "import and display correctly"), suggest the
relevant test command:

```bash
# Run unit tests for a specific interaction
bun test packages/item-player/src/extraction/extractors/<name>Extractor.test.ts

# Run default-components evals
bun run eval --filter default-components

# Run assessment-player evals
bun run eval --filter assessment-player

# Run full test suite
bun test
```

For public regression coverage, suggest:
- `bun run test:certification:public`
- Targeted clean-room test files from `docs/certification/public-coverage-matrix.json`

Only suggest official package execution as a private-project follow-up, never as a public CI gate.

## Important constraints

- Only evaluate DELIVERY criteria. EXPORT, IMPORT, and AUTHORING criteria are out of scope
  for pie-qti.
- Do not add official 1EdTech ZIP/XML assets or tests that require `../qti-conformance` to this public repo.
- Be precise about which version (QTI 2.2 vs 3.0) the criteria come from — they differ.
- When a criterion cannot be verified without a live test run, say so clearly rather than
  guessing. The goal is an honest readiness assessment, not a rubber stamp.
- If a gap is found, reference the corresponding entry in `docs/SPEC-GAPS-PLAN.md` if one
  exists (G-01 through G-15 and beyond).
- After completing the check, offer to update the private conformance project's
  `docs/CERTIFICATION_PROGRESS.md` with the findings when the result affects
  official certification readiness.

## Additional resources

- **`references/feature-index.md`** — maps every feature ID to its conformance repo directory
  and its implementation files in the codebase
- **`docs/certification/public-coverage-matrix.json`** — public clean-room coverage source of truth
- **private `pie-qti-conformance/docs/CERTIFICATION_PROGRESS.md`** — official certification progress source of truth
- **`docs/SPEC-GAPS-PLAN.md`** — existing implementation gap plan
