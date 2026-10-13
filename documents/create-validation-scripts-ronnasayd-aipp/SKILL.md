---
name: create-validation-scripts
description: Create a deterministic, stdlib-only Python validation script that checks a generated markdown artifact (spec, requirements table, tasks list, report) against explicit rules, turning a skill's prose verification checklist into a checkable pass/fail gate. Use when user says "create a validation script for this skill", "turn this checklist into a script", "add a validator", "make this a deterministic gate", "enforce this verification section with code", or a skill's output has a verification or anti-patterns section but no script enforcing it.
---

# Create Validation Scripts

Turn a skill's verification checklist into a deterministic pass/fail script,
so structural rules are enforced by code, not memory.

## Procedure

| #   | Step                                 | Action                                                                                                                                                                                                                                                                                                   | Gate                                                             |
| --- | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| 1   | Find existing pattern                | Read every sibling validation script in the same skill family before writing one. Not just one — extract the shared convention (CLI shape, exit codes, check style).                                                                                                                                     | convention identified, not invented                              |
| 2   | Extract rules from the source doc    | Read the doc that defines the target artifact (SKILL.md, spec, template). Pull rules from: an explicit "verification"/"anti-patterns" section (maps 1:1 to a check); required structure (sections, columns) → presence check; an example output already in the doc → test fixture, never invented format | every check traces to a stated rule, not a guess                 |
| 3   | Classify each rule ERROR vs WARN     | ERROR = breaks a formal invariant, always wrong (missing section, empty required field, malformed id). WARN = heuristic, can false-positive (suspicious pattern, defensible in an edge case)                                                                                                             | an ambiguous rule is WARN, never ERROR                           |
| 4   | Write stdlib-only                    | Zero dependencies. Heuristic line-by-line regex parsing, not a full parser — say so in the docstring ("heuristic markdown inspection, not a full parser")                                                                                                                                                | no imports beyond stdlib                                         |
| 5   | Match sibling CLI interface          | `python3 <script>.py [target] [--root DIR] [--strict]` — target optional with autodetect, `--strict` promotes warnings to errors, exit 0 pass / 1 failures / 2 usage error                                                                                                                               | interface identical to siblings                                  |
| 6   | One docstring, no scattered comments | Single top-of-file block: what it checks (ERROR/WARN list), usage, exit codes. Function/variable names carry meaning in the body — no inline comments, except a terse WHY-comment guarding a non-obvious invariant (e.g. why a match is scoped one way and not another)                                  | docstring complete, body uncommented except justified WHY notes  |
| 7   | Build minimal local test fixtures    | In the scratchpad (never in the repo): one artifact that should pass, one failing case per new ERROR rule. Run the script against both, fix regex until it matches                                                                                                                                       | pass case exits 0, each fail case exits 1 with the right message |
| 8   | Isolate regex on unexpected miss     | A check that doesn't fire as expected: test the regex alone against the exact fixture text in a throwaway snippet — don't guess, confirm the actual mismatch (e.g. `**Label:**` vs `**Label**:`)                                                                                                         | root cause confirmed before editing the script again             |
| 9   | Confirm both exit codes              | Run against the passing fixture AND the failing fixture. A script that only detects failure but false-positives on a clean case is useless                                                                                                                                                               | exit 0 on pass, exit 1 on fail, correct message                  |
| 10  | Wire into the producing skill        | Edit the skill/procedure whose output this validates: add the script call as an explicit gate in the verification step, before manual checks — deterministic check first, human judgment after                                                                                                           | skill's own verification step invokes the script                 |

## Anti-patterns

| Anti-pattern                                      | Why it fails                                                                 |
| ------------------------------------------------- | ---------------------------------------------------------------------------- |
| Inventing checks not traceable to the source doc  | Script enforces opinion, not the actual spec                                 |
| Marking an ambiguous heuristic as ERROR           | False positives block valid output; use WARN                                 |
| Adding a dependency for parsing                   | Breaks the stdlib-only, zero-install convention                              |
| Skipping sibling scripts before writing a new one | Produces an inconsistent CLI/exit-code contract                              |
| Testing only the failing fixture                  | Misses false positives on clean input                                        |
| Leaving the script unwired                        | Prose "run this script" is exactly the memory-reliance this pattern replaces |
