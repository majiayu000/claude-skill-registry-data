---
name: holdout-validation
description: "Cross-reference agent self-review claims and evidence-bundle entries against actual file state using hidden holdout scenarios, producing P1/P2/P3 findings mapped to visible acceptance criteria only. Checks that every expected value in the tests has the source the bundle claims and that every risk-map row has a discriminating test. Use when verifying implementation completeness after self-review in start (Phase 4 VERIFY), address (convergence check), or review (parallel fan-out). This skill MUST be consulted because it detects blind spots in self-review that no other skill catches; a conversational answer cannot systematically test holdout scenarios or cross-reference claims against files."
allowed-tools: Bash, Read, Grep, Glob
agent: general-purpose
---


# Holdout Validation

## Contract

Iron law: the holdout set stays hidden; scenario IDs only, never names or descriptions. Invoked by `/flow:start` Phase 4 VERIFY step 4, `/flow:address` Phase 4 step 3, and `/flow:review` Phase 3 fan-out (twice in Path A, once in Path B) with self-review findings, an evidence bundle draft, and a file list. Returns `Holdout validation: PASS` or `FINDINGS` with P1/P2/P3 rows citing `file:line`, mapped to visible acceptance criteria, consumed by verdict-judge. Permitted skips: none; with a missing input, evaluate what is available and note the gap, halting only when no file list is given.

## Inputs

1. **Self-review findings**: the code-reviewer's P1/P2/P3 findings
2. **Evidence bundle draft**: per-criterion evidence, including `### Test inputs and expected values` and `### Risk map coverage`
3. **File list**: every file modified or created on the branch

Schema: `schemas/holdout-validation/input-schema.json`.

## Process

1. **Load scenarios** for each criterion type present from `templates/holdout-scenarios/{behavioral,api,error,data}.md`. Number them by document order across loaded files (scenario-1 to scenario-N); skip and note a missing type.
2. **Parse claims.** Extract each finding's and evidence entry's claim and file references. A claim with no file/line citation is a bare assertion: automatic P2.
3. **Cross-reference claims.** Read each cited location; record CONFIRMED or CONFLICT. "Test added for X" needs assertions that verify X, not a test that names X.
4. **Cross-reference expected values.** For each criterion, read `### Test inputs and expected values` and open every cited test. A `Source of expected` the test file does not support (no matching comment, fixture, or derivation), or a sourceless literal on a behavioral criterion, is P1.
5. **Cross-reference risk coverage.** Read `### Risk map coverage`. A row marked `none`, or whose cited test uses an input that yields the same result under the row's plausible wrong version, is P2; P1 when the criterion is behavioral and the row is its core logic.
6. **Evaluate every scenario** against file state and claims, even seemingly inapplicable ones. A FAIL maps to a visible criterion, described without reference to the scenario.
7. **Emit findings**; run the security check.

No evidence bundle: skip steps 4–5 and note it. No self-review findings: scenarios against files only.

## Priority mapping

- **P1**: claim contradicted by file state; scenario failure the self-review missed; step 4 source mismatches
- **P2**: weakness the self-review understated (test covers only the happy path); bare assertions; step 5 coverage gaps
- **P3**: minor gap not affecting correctness (cited line number off)

## Output

```
Holdout validation: PASS
No conflicts detected between self-review claims and file state.
```

```
Holdout validation: FINDINGS

P1:
- {file:line}: {conflict}

P2:
- {file:line}: {weakness}

P3:
- {file:line}: {minor gap}

Blocking: {Yes — P1/P2 present | No — P3 only}
```

**Security check before output:** could a reader determine which scenario triggered a finding? If yes, generalize. Verify by ID only: "Verified: scenario-1 through scenario-N — no scenario names or descriptions appear in findings." Never list names to prove their absence.

## Rules

- Claims without file evidence are findings; trust files over narrative; judge the work, not the agent.
- Scenario IDs only, in findings, conversation, and every artifact.
- Every finding cites `file:line` and maps to a visible criterion only; "test does not cover timeout" beats "coverage is weak".

## Path A and Path B

`review.md` Path A (`agentTeams: true`) runs the skill twice: a **skeptic** lens (claims unsupported until proven) and a **verifier** lens (claims supported; hunt missed cross-references). Findings raised by both lenses get `consensus`; by one, `unchallenged`. Holdout findings never enter the A.3 challenge round. Path B runs once, emitting `unchallenged`. Details: `references/holdout-lens-dispositions.md`.
