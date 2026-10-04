---
name: coverage-gap-audit
description: Audit Jest test coverage to separate real testing gaps (business logic, security paths) from false negatives (wiring, config, generated code) that shouldn't count against coverage metrics. Use when the user says "audit test coverage", "which files actually need tests", "reduce coverage noise", "why is coverage low", "exclude files from coverage", or asks to review/clean up `collectCoverageFrom`.
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: 1.1.0
---

# Coverage Gap Audit

Classify low/zero-coverage files as real gaps or false negatives, then optionally suppress the false negatives in `jest.config.js`. Coverage % is a symptom, not a verdict — the only signal that matters: does this file contain a decision a test could get wrong?

## Steps

| #   | Step                   | Action                                                                                              | Gate                                                                                                                                |
| --- | ---------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Read config            | Find `jest.config.js`, note existing `!`-prefixed `collectCoverageFrom` excludes                    | don't re-litigate prior exclusions, build on top                                                                                    |
| 2   | Run coverage           | `npx jest --coverage --coverageReporters=text`                                                      | text table only — gives per-file %+uncovered lines in one pass; avoid `json-summary` alone                                          |
| 3   | Triage                 | Sort mentally: 0% files first, then low%, grouped by directory (table is already folder-grouped)    | —                                                                                                                                   |
| 4   | Classify each file     | Read actual source — does it decide/calculate/validate/transition state/gate security?              | yes → real gap; no (pure bootstrap/wiring/DI/OpenAPI reg/thin singleton wrapper/base class covered via subclasses) → false negative |
| 5   | Sibling heuristic      | If sibling files in same layer have good `.spec.ts` coverage and this one doesn't → real gap signal | read one sibling spec, note its mocking/fixture pattern for reuse                                                                   |
| 6   | Produce two lists      | Real gaps (risk-ordered, security/auth first) + false negatives — never blended                     | see list fields below                                                                                                               |
| 7   | Suppress (if approved) | Edit `collectCoverageFrom`, one `!`-exclude per false-negative _category_ not per file              | narrowest glob that still hides the category — don't blanket a folder with only one false negative in it                            |
| 8   | Re-verify              | `npx jest --coverage --coverageReporters=text \| grep "^All files"`                                 | test count unchanged + overall % increased                                                                                          |
| 9   | Stop                   | Hand back real-gaps list as next unit of work                                                       | do not start writing tests automatically                                                                                            |

### Classification traps

- Small files with real logic (`EventBus.ts`, `isExpired()`) → real gap (low priority), not false negative. Zero decision logic is the only bar for false-negative status.
- Base/abstract classes (`Entity`, `AggregateRoot`) covered transitively via tested subclasses → not a gap, unless the base itself has non-trivial logic.

### List fields (Step 6)

- **Real gaps**: file, line count, current %, one-line reason it matters, sibling spec to pattern-match.
- **False negatives**: file, one-line reason it's structurally untestable-as-unit or valueless (needs integration/e2e, or is static config/codegen).

## Examples

- "audit our coverage, lots of noise" → Steps 1-6 → present lists → if approved, Steps 7-9.
- "which of these low-coverage files actually matter?" → Steps 1-6 only, no config edit.

## Troubleshooting

| Symptom                           | Cause                            | Fix                                             |
| --------------------------------- | -------------------------------- | ----------------------------------------------- |
| Coverage output too noisy to scan | wrong reporter                   | re-run with `--coverageReporters=text`          |
| Unsure if file is false negative  | unread branch inside wiring code | read full file, don't guess from name/directory |
