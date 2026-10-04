---
name: patpat-verifier
description: Create or maintain a project-specific verification skill that launches, exercises, observes, and cleans up the real system. Use when a repository lacks repeatable proof of its user-facing behavior.
disable-model-invocation: true
---

# Patpat Verifier

When invoked directly, read the [operating protocol](../patpat-loop/references/operating-protocol.md) in full. Do not load the router.

Read [proof over proxy](../patpat-loop/principles/proof-over-proxy.md), [preserve safety](../patpat-loop/principles/preserve-safety.md), and apply the [project verifier playbook](../patpat-loop/playbooks/project-verifier.md).

Inspect the actual application surface and reuse an existing harness when it can prove the claim. Otherwise create the smallest project-local verifier at `.agents/skills/verify-<app>/SKILL.md` with exact `Launch`, `Doctor`, `Exercise`, `Evidence`, and `Cleanup` procedures. Seed `features/README.md` plus one file per identified high-value user surface so later runs can select proof from maintained coverage instead of the easiest available path. Do not invent features to reach a quota.

Make every command executable as written. Own and stop only processes started by the verifier; never terminate by broad process name. Keep secrets out of prompts, logs, artifacts, and external calls. Preserve evidence long enough for independent inspection.

Isolate instances so two can run side by side (ports, data dirs, profiles), or refuse to double-drive a shared instance.

Prove the verifier end to end by launching the system, checking readiness, exercising one mapped workflow, inspecting the authoritative result, cleaning up, and confirming the evidence survived cleanup. When maintaining a verifier, restrict edits to its directory unless the user separately authorizes a product fix. Reconcile every feature-map entry to a concrete source entry point and live result. Report product defects instead of hiding them in verification instructions.

## Proof closure

Close repository mutations through:

- [`patpat-verify`](../patpat-verify/SKILL.md)
- [`patpat-review`](../patpat-review/SKILL.md)
