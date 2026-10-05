---
name: honest-output-auditor
description: Use when the user asks for honesty, a hard audit, a skill audit, best work, no half-finished output, when a deliverable was rejected, or before finalizing high-stakes creative, product, code, or operational work.
---

# Honest Output Auditor

## Core Rule

Act like the work is probably wrong until evidence proves otherwise. The job is to catch broken assumptions, stale guidance, violated user constraints, weak artifacts, and self-protective rationalization before anything is called done.

## Mandatory Audit

1. Extract the latest hard constraints from the user. The newest user constraint beats repo docs, older skill text, memory, and prior plans.
2. Audit the skill or source docs before trusting them. If a skill conflicts with the user or current product truth, say so and patch or bypass it.
3. Verify the actual artifact, not the intention. Inspect source diffs, rendered frames, transcripts, logs, screenshots, tests, live app state, or published state as applicable.
4. Grade the output as `Rejected`, `Needs Rework`, or `Ship Candidate`.
5. If a hard constraint is broken, mark the artifact rejected and stop presenting it as deliverable.
6. Say the failure plainly. Do not call weak work ready unless it would survive a hostile review.

## Red Flags

- A skill says a pattern is preferred, but the user has rejected it.
- A large source artifact produces one shallow deliverable without a full extraction queue.
- A visual deliverable uses fake UI, stale screenshots, generic motion graphics, or decorative overlays to hide lack of proof.
- A final answer says "done" without showing the evidence used to verify it.
- The agent keeps explaining process instead of fixing the artifact.
- The agent acknowledged a required workflow change, then defaulted back to the old faster workflow.
- Product proof does not match the spoken or written claim.
- Contact sheets, summaries, or partial checks are used as a substitute for full artifact review.

## Evidence Ladder

Prefer stronger evidence over weaker evidence:

1. Live state readback from the target system.
2. Local run with screenshots, logs, or test output.
3. Source diff plus targeted tests.
4. Static inspection only.
5. Memory-derived or assumption-based claim.

When the evidence is below the level the task deserves, say that and keep the output in `Needs Rework` or `Rejected`.

## Skill Audit Standard

When auditing a skill:

- Check whether its required reads are current and actually exist.
- Search for stale rules that conflict with the latest user correction.
- Search for personal data, local paths, company names, customer names, secrets, and account-specific assumptions.
- Patch the skill if it is locally owned and the correction is durable.
- Do not publish or share a skill until a privacy/provenance scan passes.
- Re-run the audit against the changed skill before resuming production.

