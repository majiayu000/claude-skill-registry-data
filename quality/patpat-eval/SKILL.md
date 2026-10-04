---
name: patpat-eval
description: Evaluate whether an agent skill triggers and performs correctly using isolated, evidence-based trials. Use after non-trivial skill changes or when routing quality is uncertain.
disable-model-invocation: true
---

# Patpat Eval

When invoked directly, read the [operating protocol](../patpat-loop/references/operating-protocol.md) in full. Do not load the router.

Read [proof over proxy](../patpat-loop/principles/proof-over-proxy.md) and apply the [behavioral evaluation playbook](../patpat-loop/playbooks/behavioral-eval.md).

Define the target behavior and rubric before running a trial. Include at least one prompt that should trigger the skill and one neighboring prompt that should not. Run trials in isolated temporary workspaces with equivalent context, organic names, and no hidden access to the expected conclusion.

Judge produced artifacts, commands, observations, scope control, and cleanup. Do not treat an agent's explanation or confidence as evidence. Record environmental limits and keep comparisons sequential unless isolation and integration proof have earned parallel execution.

At least one frozen rubric criterion must use the behavioral oracle defined in [proof over proxy](../patpat-loop/principles/proof-over-proxy.md): an observable result or material effect through the interface the user or host uses. Reject a trial whose passing evidence only shows that a helper was called, a value is present, a constant or prompt is unchanged, or no exception was raised.

Freeze the rubric before the first trial. Record `PASS` only when inspectable evidence satisfies every predeclared criterion; record `FAIL` when observed behavior violates any criterion and `INCONCLUSIVE` when required evidence is missing or uninspectable. Never weaken or reinterpret the rubric after observing output. Do not rewrite a failed trial as a pass; record a corrected candidate as a new trial.

Promote the skill only when structural validation passes and the behavioral evidence receives `PASS` under the frozen rubric.

For a revision-bound Codex contract canary, run [`../../scripts/probe_codex_behavior.py`](../../scripts/probe_codex_behavior.py) manually against a clean committed revision and an explicit requested model. Keep the generated JSONL and private `receipt.json` outside every Git worktree. The probe also writes a strict allowlisted `attestation.json` bound to the receipt and raw-evidence digests; inspect it before explicitly posting or uploading it. Generation alone does not make the attestation external evidence. Promote is the gate: `scripts/publish_codex_attestation.py` re-hashes raw receipt.json and event streams; generation is still not external. External inspectability is the Actions artifact, not a Git blob. The probe checks bounded task behavior, observed mutation-capable commands, and response-shape conformance; it does not prove independent review, runtime enforcement, host-attested skill activation, every route, the resolved provider snapshot, or every possible transient side effect. Its producer timestamps are wall-clock observations, not trusted timestamps. Apply its result only to the recorded Codex version, requested model selection, Patpat revision, and Git tree. Do not transfer it to Cursor, Grok, Antigravity, or a later commit.
