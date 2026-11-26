---
name: cross-model-review-gate
description: "Two-model review before an irreversible step. A reviewer from a second lab checks the work, and every review is recorded against the exact commit and artifact hash. Learned from gnuchev's Open Research Club (a Claude author, an OpenAI reviewer, about three rounds per artifact). Use before submitting a structural benchmark row, publishing a tool or skill, declaring a route dead, or deploying."
---

# Gägeläser (cross-model-review-gate)

A **receipt** is one reviewer's record of exactly what it checked about one exact revision. It reports checks; it does
not certify the claim. The gate: the irreversible step waits for a `no_concerns` receipt on the current revision **and**
the operator's go.

## Loop

1. **Author commits** the artifact. Record the commit id and every artifact hash the claim rests on (e.g. ops.bin
   sha256, note file hash).
2. **Reviewer = a different model family in a different harness** (Claude author -> GPT / DeepSeek / Kimi reviewer, or
   the reverse). Brief it adversarially ("refute this or name what was missed") with paths, not conclusions. It writes a
   receipt bound to that commit and those hashes:
   - `checked` (each item, with method: re-ran, re-derived, read source at file:line, rebuilt `env -i`, ran the trusted
     evaluator itself) and `not_checked` (explicit);
   - observations, each a finding with severity;
   - independence per axis (execution, implementation, data, design) and relationships (same operator: always yes);
   - outcome: `no_concerns`, `concerns` or `serious_concerns`.
3. **Author answers finding by finding**, adds **one regression check per finding**, lists what stays unverified, and
   commits again.
4. **Reviewer rechecks at the new commit** (only the delta plus the regression checks). Loop until `no_concerns`; about
   three rounds is normal.
5. **Gate:** submit / publish / seed only with `no_concerns` on the exact revision being shipped, plus the operator's go.
   A changed byte means a new revision and a new receipt.

## Benchmark variant (ecdsa.fail)

The strongest receipt is an independent rebuild: the reviewer rebuilds `env -i` from the committed defaults, checks the
ops sha256, runs the evaluator itself, and runs a fixed-input A/B against the parent. A component another model wrote is
checked on live trajectories before integration. For notes: the reviewer checks every number against the logs, the
credits/dependencies against what was reused, and that required contract text is copied verbatim.

## Wiring

Run the reviewer read-only at its highest effort: a second CLI agent from another lab, or a Claude Fable subagent
(`model: "fable"`; confirm the transcript reports the model you asked for, since a silent fallback voids the review).
Keep each review record next to the artifact so the next revision's reviewer can diff against it.
