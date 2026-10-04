---
name: reviewer-calibration
description: "Run matched A/B reviewer calibration for /f through the binary-owned review controller, using digest-bound prompts, envelopes, and receipts."
---

# Reviewer Calibration

Use this skill when `/f`, `/factory`, or a PR/work-item review needs to compare
independent reviewer backends against one frozen target.

## Rule

Calibration is default-on for real `/f` runs. Treat
`--reviewer-calibration=true` as present unless the user explicitly passes
`--reviewer-calibration=false` and gives a reason.

Do not claim one reviewer underperformed another unless controller receipts
prove both reviewed the same frozen base/head pair, task digest, prompt digest,
and envelope digest.

## Frozen Envelope

Create a task file containing only the untrusted PR/work-item text. Determine:

- `target_repo`
- `target_pr` or `work_item`
- `head_sha`
- `base_sha`
- `diff_path` or embedded diff hash
- PR body / task text snapshot
- evidence artifact paths and hashes
- test log paths and hashes
- factory `run_id`
- output directory for each backend lane

Do not create reviewer instructions. The controller constructs and binds the
diff, changed files, task snapshot, evidence metadata, static prompt, and exact
response contract.

## Controller command

Run the Codex reviewer through this exact binary-owned interface:

```bash
dark-factory review \
  --workdir <repo> \
  --base-sha <full-40-hex-sha> \
  --head-sha <full-40-hex-sha> \
  --task-file <path> \
  --output-dir <dir> \
  --backend codex
```

The controller v1 adapter accepts only `codex` through its tool-free JSONL
transport. A valid PASS requires non-empty `evidence_checked` and
`commands_executed: []`. Its `ReviewTransportReceipt` and controller terminal
receipt bind the prompt, envelope, response, reviewed revision/tree, and
evidence manifest. Do not add model names, inline prompts, or vendor CLI
flags. Factory/in-graph results may be compared only when their controller
receipt proves the same bindings.

## Artifacts

The binary, not this skill, writes each lane directory:

```text
evidence/<run-id>/reviewer-calibration/
  <backend>/
    controller-receipt.json
    envelope.json
    prompt.txt
    reviewer.output.md
    findings.json
  comparison.json
  adjudication.md
```

`prompt.txt` is a binary-emitted audit capture only. It is not prompt
authority. Never author it in a skill/workflow, copy it from the target repo,
or pass it to a vendor CLI. The source-root-pinned controller template and the
receipt digest are authoritative.

Before using a lane, require `controller-receipt.json` to bind:

- controller prompt ID and prompt SHA-256;
- envelope SHA-256 and task/diff snapshot digests;
- exact base SHA and head SHA;
- backend identity, exit status, and response SHA-256.

Recompute the emitted `prompt.txt` and `envelope.json` SHA-256 digests and
compare them to the receipt. Record the controller receipt file's own SHA-256
in `comparison.json`. A missing receipt/digest, mismatch, nonzero controller
exit, or stale SHA makes that lane `inconclusive`. If a backend is unavailable,
record `unavailable` in `comparison.json`; do not fabricate a replacement
result.

## Finding Schema

Each reviewer should return JSON plus free-form text:

```json
{
  "reviewer": "<controller backend>",
  "target_head_sha": "...",
  "verdict": "blockers|no_blockers|inconclusive",
  "findings": [
    {
      "severity": "blocker|major|minor",
      "claim": "...",
      "file": "...",
      "line": 123,
      "evidence": "...",
      "repro_or_reason": "..."
    }
  ],
  "confidence": "high|medium|low"
}
```

## Adjudication

A finding is confirmed only if one of these is true:

- the user confirms it;
- the PR/work item changes to fix it;
- CI/test/review evidence later proves it;
- another independent reviewer confirms it with exact evidence.

Classify reviewer deltas:

- `confirmed_miss`: reviewer A missed a later-confirmed blocker found by reviewer B.
- `unconfirmed_delta`: reviewers disagree, but no ground truth exists yet.
- `false_positive`: reviewer claimed a blocker later disproven by evidence.

## Final /f Output

Include:

```text
Reviewer calibration: enabled <artifact-path>
Raw Codex verdict: <...>
Delegated reviewer verdict: <...>
Factory reviewer verdict: <...|unavailable>
Agreement: <yes|no|partial>
Confirmed gap: <pending|yes|no>
```

If disabled:

```text
Reviewer calibration: disabled <explicit reason>
```
