---
description: >
  Run (or re-run) Stage 4 only — the Claim Verifier: extract every claim from
  the draft, verify each against its declared evidence source (numerical ±5%,
  citation entailment, method-code alignment), refine failures, finalize the
  paper, and run the Chain-of-Evidence audit. Requires paper/draft.md.
argument-hint: "[--run <run-id>]"
disable-model-invocation: true
---

# /verify-claims — Stage 4: Extract → Verify → Refine → Finalize

Arguments: `$ARGUMENTS`

Current state: !`python3 .claude/scripts/ledger.py status`

Preconditions: resolve the run (`--run` or ACTIVE_RUN); `paper/draft.md` must
exist — otherwise stop and point to `/write-paper`.

1. **Extract**: `python3 .claude/scripts/extract_claims.py <run>` →
   `paper/claims.jsonl`.
2. **Verify**: launch the `claim-verifier` subagent (run dir). It runs
   `verify_claims.py`, judges the PENDING_LLM claims (citation entailment vs
   `literature/` notes; method-code alignment vs `best/solution.py`) with a
   verbatim supporting quote per PASS/PARTIAL, and writes
   `paper/verification-report.md`. A stop-gate hook prevents it from
   finishing with unresolved or quote-ungrounded claims.

   **Best-of-N votes** (if `run-config.json#verifier_votes` is N ≥ 2): the
   LLM judgments are sampled N times and disagreements resolved
   conservatively. SEQUENTIALLY, for k = 1..N-1: launch a `claim-verifier`,
   then `python3 .claude/scripts/verdict_votes.py snapshot <run> <k>` (this
   archives vote k under `paper/votes/` and resets the LLM-judged claims so
   the next verifier judges blind — votes must NOT run in parallel, they
   share `paper/claims.jsonl`). Launch the final claim-verifier, then
   `python3 .claude/scripts/verdict_votes.py merge <run>` — on any
   disagreement the weakest verdict wins (FAIL < PARTIAL < PASS). Append the
   merge summary to `paper/verification-report.md` under a
   `## Vote reconciliation` header, and re-run
   `python3 .claude/scripts/verify_claims.py <run>` for the post-merge tally.
3. **Refine loop** (max 2 rounds): if any claim is FAIL, launch `refiner`
   (run dir + the failure list), then re-run
   `python3 .claude/scripts/verify_claims.py <run>`. Remaining FAILs after
   round 2 are reported honestly, not hidden.
4. **Finalize**: copy `paper/draft.md` → `final/paper.md`.
5. **Chain-of-Evidence audit**:
   `python3 .claude/scripts/chain_of_evidence.py <run>` — Score Verification,
   Reference Verification, Specification Violation, Method-Code Alignment.
6. Ledger: `python3 .claude/scripts/ledger.py append '{"event":"stage_verify","detail":"<tally>"}'`

Report: claim tally (pass/partial/fail), the chain-of-evidence table, and the
final paper path. Offer `/paper-to-latex`.
