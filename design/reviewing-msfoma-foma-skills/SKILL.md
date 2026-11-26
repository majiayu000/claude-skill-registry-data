---
name: reviewing
description: >-
  Reviews a diff against the project's standards and spec in priority order, ending in a ship or fix-first verdict. Use when the user asks to review code, a PR or a branch, "is this ready to merge?", or for UI code feedback. Not for debugging.
license: Apache-2.0
metadata:
  level: "method"
  uses: ""
  agents: ""
  tokens: "716"
---

Review a change like the developer who will be paged when it breaks: against this project's standards and spec, in a fixed priority order, with evidence.

Path: small diff (a few files, no risky area) → steps 1–3, correctness and tests only, then the verdict; large or risky diff (auth, data, money, migrations, public API, concurrency) → all steps. Say which path in one line.

## Steps
1. Fix the range: what the user named (PR, branch, commit, files), else the uncommitted changes, else the last commit. Branch: `git diff $(git merge-base <base> HEAD)...HEAD`. Check the ref resolves and the diff is not empty.
2. Read the contract: `## Commands` and conventions in the project's CLAUDE.md, and the spec or plan if one exists (`docs/specs`, `docs/plans`, paths under `## Where things live`, issue named in the commits). Judge by those, not by generic taste. No spec: say so and skip the spec step.
3. Run the project's check (tests, typecheck, lint) fresh yourself; a report from the author or an earlier run is not evidence. No command found: say so.
4. Read the diff, then what it touches: callers of every changed signature or return value, the code it calls, its tests.
5. Review in this order, stop padding when a level is empty: correctness and security → spec fit (missing, partial, unrequested behaviour) → tests (risky logic with no test that fails when it breaks) → simplicity and scope (dead code, speculation, reuse of an existing helper) → style last, and only what the project's standards state and tooling does not enforce.
6. Write each finding as `file:line — problem — why it matters — suggested fix`. When it depends on an assumption (expected load, input range, who calls it), state the assumption.
7. Give the verdict.

## Rules
- A finding needs evidence from the code: a concrete input or situation that goes wrong. Read the callers and re-read the lines before reporting a bug; no case, no finding.
- No style nit before correctness is reviewed; never present taste as a defect.
- Do not edit the code during review unless asked; findings and fixes are suggestions.
- Severity is honest: must-fix only for bugs, security, data loss, a broken spec or a failing check. Do not pad; "nothing found" with what you checked is a valid result.
- A deliberate, commented shortcut that names its limit is a decision, not a finding, unless the real load already crosses it.

If the diff is large or risky, or you need the smell list and severity detail, read `references/priorities.md`.
If the change touches UI (components, CSS, copy, screens), read `references/ui.md`.
If you are acting on review feedback someone else gave (a PR comment, a reviewer's list), read `references/feedback.md`.

## Report
- Verdict: ship / fix first.
- Findings, must-fix first, then nice-to-have; each as in step 6.
- Check: command and result.
- Not checked: <…>
