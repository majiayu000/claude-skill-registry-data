---
name: audit
description: Step 2 of the five-step flow. Runs at most 3 Swarm rounds (10 Interns each) to falsify claims and eradicate defects.
---

# audit: try to prove it wrong

A system's own tests, CI, and issue states are claims written by the system. A test cannot catch its author's premise.
Audit runs **at most 3 Swarm rounds** via `subagent_batch`. Each round dispatches 1 Swarm of 10 Interns (`M=10`).

## Phase 0: Touch Reality (run before any scout)

1. **Label the delivery state.** Run `ws-delivery-status` (the `z` skill holds the canonical state table). Never report `Done` or `Complete` before merge and a passing Business Reality Probe (`VERIFIED_COMPLETE`).

2. **Touch two independent oracles** that this repository did not write: the vendor or upstream source,
   and the real runtime (database query, byte check with sha256, scheduler failure log, staging against production).
   Operate the real surface (the real TUI or the browser) when the claim is about user behavior.
3. **Scan the three failure shapes.** Each passes lint, tests, and CI.
   - WRONG FORMULA: one formula breaks an edge case.
   - GREEN-WHILE-EMPTY: a filter removes all rows and the job reports success.
   - STALE-REPORTED-AS-FRESH: stale data carries a fresh label.
4. **Implausible output is evidence.** Explain it before you propose anything else.
5. **A score must come from executed checks.** Run the command, record the exit code, and cite it. A score without a command is not reported.
6. **Disclose.** Name the inputs you did not verify, the sample size, the data age, and the oracles you did not use.
   Ask "Sufficient?" (could an unverified input overturn the conclusion?) and "MECE?" (overlap or orphan?). A troubling answer is a finding.
7. **Facts block.** At the start of an audit, run a read-only command that prints:
   - Per repository touched by the audit: `HEAD` commit SHA, `origin/main` commit SHA, and dirty status flag.
   - Skill copy integrity: `tree_hash` digest of each installed or `.ws-agy-managed` skill copy next to its `dev_env` source.
   - Settings: Effective value and configuration source of each setting the audit depends on.
   The audit report must include this block before any scout findings.

## Four gates

1. **The auditor must read code.** Use a read-only native agent, or pass target files via `context_files` (with diffs and contracts) to `subagent_batch` workers so the worker injects code from disk without prompt duplication. Never ask an auditor to judge code that the auditor cannot see.
2. **See each new test fail first.** Run only the target test case on unfixed code and confirm RED (`pytest <file>::<test> -x`).
3. **Re-review every fix independently.** The reviewer gets only the new code, not the defect story.
   For a security fix, ask for "the second chain from the same entry".
4. **Screening output carries anchors.** Each fact cites `file#Lxx-Lyy` or a note id.
   The Director reads 1 to 2 anchors before a decision. Lossy small-model summaries hide facts.

## The 10-Intern Scout Matrix (used in Round 1 Discovery Swarm)

The 10 parallel Interns in Round 1 are allocated across non-overlapping audit dimensions:
- M1 breaking changes (Intern 1): Renamed fields, new required parameters, breaking protobuf/schema contracts.
- M2 design promises (Intern 2): Does code do what the README and architecture specify, or stub it with `pass` and TODO?
- M3 blast radius (Intern 3): Shared state, events, or middleware that break downstream consumers or callers.
- M4 semantic drift (Intern 4): Config names, default values, environment variable names, error codes.
- G1 SRE defense (Intern 5, doc-blind): Leaks, missing locks, child processes not killed as a group, timeouts, shutdown signals.
- G2 hygiene (Intern 6, doc-blind): Swallowed errors (`except: pass`, ignored error objects), dead code, empty stubs, hidden hardcodes.
- G3 fake tests (Intern 7, doc-blind): GREEN-WHILE-EMPTY, `assert True`, `assert len(x) >= 0`, over-mocking, shadowed test functions.
- T1 completeness (Intern 8): Did the change finish the stated goal, or only the happy path?
- T2 side effects (Intern 9): Latency, rate limits, lock contention, broken global invariants.
- S1 SSOT and drift (Intern 10): Mismatches between implementation, MANIFEST.yaml keys, and rule boundaries.

## 3-Round Swarm Pipeline

This skill is the one source for the audit round count and the Intern count. Rounds run in sequence:

### Control claims

Each round includes at least one claim known true (`holds`) and one claim known false (`breaks`). The Director records expected verdicts before dispatch. The batch header prints the control result (`calibrated` when all controls match expected verdicts, `uncalibrated` otherwise). A round with an `uncalibrated` result carries no evidentiary weight.

### Rounds

1. **Round 1 (Discovery Swarm: M=10)**: Dispatch 10 Interns across the Scout Matrix (M1-M4, G1-G3, T1-T2, S1). Output dense defect hypotheses with exact `file#Lxx-Lyy` anchors and line-1 JSON verdict contract.
2. **Round 2 (Adversarial Confrontation Swarm: M=10)**: Pair Interns as opponents (Red Team vs Blue Team) answering the same question about the same claim using the single `holds` / `breaks` / `unknown` verdict contract. A disagreement inside a pair is the signal. Surviving broken claims advance to Round 3.
3. **Round 3 (Independent Blind Check: M=10 + Director Touch Reality)**: 10 fresh Interns blind-verify surviving broken claims. The Director executes read-only Touch Reality probes to confirm or reject findings.

### Findings and Probe column

The findings table must report:

| claim | worker verdicts | probe (command, exit code) | status |
|---|---|---|---|

Every finding must cite an executed physical probe (`command`, `exit code`). Findings without an executed probe show `unprobed` and are not counted as confirmed in the summary line.

## Exit rule

- **Stop after a round that leaves no open finding:** Round 1 finds no hypothesis, or Round 2 disproves all of them. Round 3 is the last round. A HIGH finding still contested after Round 3 goes to the Senior (SHZP).
- **Terminal Round**: The final round is audit-only. It edits no code.
