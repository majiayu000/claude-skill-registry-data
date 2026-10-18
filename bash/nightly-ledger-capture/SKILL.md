---
name: nightly-ledger-capture
agent: none
description: Discovers missing honesty, trust-decay, failure-mode, and decision-outcome entries from local evidence; stages judgment and permits direct mutation only after an executable oracle.
allowed-tools: Read, Write, Bash
user-invocable: true
status: PRODUCTION - stage first and never self-confirm
triggers:
  - nightly ledger capture
  - stage measurement candidates
  - ledger capture
---

# /nightly-ledger-capture

This is Leg F's capture protocol. It keeps human judgment human-gated while
making mechanical claims reproducible.

## Local sources

Read:

- today's valid capsules by frontmatter `created_at`;
- canonical dated Session Log blocks;
- explicitly referenced local Git commits and diffs;
- current `HONESTY_LEDGER.md`, `TRUST_DECAY.md`, and `FAILURE_MODES.md`;
- `DECISION_LOG.md` and `DECISION_OUTCOMES.md`.

These sources discover claims. An agent-authored capsule or log entry cannot
verify its own claim. The implementation has no dependency on an external
coordination service and reports its source scope as local memory plus Git.

## Candidate predicates

### Honesty

Stage when the day contains consequential multi-file work, a large change, a
verified/shipped/deployed/merged claim tied to an artifact, or an uncaptured
tradeoff/cost/stopped-short statement. Honesty classification requires
judgment, so it is always staged.

### Trust decay

Stage the one to three most consequential confident claims only when
consequential work is also present. Capture the exact claim, claimant, source
reference, and proposed executable resolution predicate. Later narration is
not a resolution oracle.

### Failure mode

Stage when a diagnosis contains a verified cause plus a real red-before and
green-after receipt and the class is not already represented.

### Decision outcome

An exact operator answer has already crossed its human gate. Direct append is
legal only when all are true:

1. exact authored text is `HELD | DRIFTED | REVERSED | STILL UNCLEAR`;
2. decision date and exact heading uniquely match one decision;
3. interval is exactly 30, 60, or 90 days and is due inside the documented
   tolerance;
4. the interval is absent from the matching outcome entry; and
5. the pre-write SHA-256 still matches.

Invoke:

```text
node daemons/nightly-decision-outcome.mjs --root <aigent-root> \
  --as-of <YYYY-MM-DD> --decision-date <YYYY-MM-DD> \
  --decision-title "<exact heading>" --interval <30|60|90> \
  --outcome "<enum>" --operator-text "<exact enum>" \
  --operator-source "<durable direct operator ref>" \
  --expected-file-sha "<pre-read sha256>"
```

The writer compare-and-swaps, appends one check, verifies it, and dedupes
replay. Ambiguity remains staged.

## Staging product

Append through the sole writer to:

`vault/memory/runtime/NIGHTLY_CAPTURE_CANDIDATES.jsonl`

```text
node daemons/nightly-ledger-stage.mjs --root <aigent-root> \
  --date <YYYY-MM-DD> --candidate-json '<serialized object>'
```

Candidate fields:

```json
{
  "candidate_id": "nc-YYYYMMDD-NN",
  "ledger": "honesty|trust_decay|failure_modes|decision_outcomes",
  "claim": "...",
  "source_refs": ["..."],
  "evidence_class": "judgment|mechanical",
  "predicate_proposal": {
    "type": "file_sha256_equals|json_field_equals|git_commit_present",
    "args": {},
    "expected": "..."
  },
  "predicate_receipt": null,
  "status": "staged",
  "created_at": "ISO"
}
```

The writer allocates max suffix plus one, hashes normalized content for
dedupe, forces `status=staged`, serializes JSON, and re-parses the complete
file. Mechanical evidence requires a current green receipt; judgment may carry
only a proposed predicate.

## Direct mutation predicate

Direct ledger mutation is legal only when:

1. `daemons/nightly-ledger-predicate.mjs` executed it;
2. type is `file_sha256_equals`, `json_field_equals`, or
   `git_commit_present`;
3. arguments are structured data rooted inside the selected root, never shell
   text;
4. receipt hash, observed result, literal exit, and expected result match;
5. the artifact is external to the claim narration and directly decides it;
6. mutation delegates to the existing canonical ledger owner and embeds the
   receipt.

Otherwise stage. Never flip a prose resolution based on self-confirmation.

After capture, run `daemons/nightly-ledger-review.mjs`. Its literal
`FRIDAY_MEASUREMENT` receipt reports the weekly counts without applying any
judgment-bearing proposal.

Return:

```text
LEDGER_CAPTURE PASS staged=<N> direct=<N> duplicates=<N> sources=local-memory,git
```
