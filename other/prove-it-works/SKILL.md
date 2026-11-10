---
name: prove-it-works
description: Assess whether observed evidence proves the requested behavior before declaring work complete. Consult for verification planning, interpreting checks, or distinguishing a real result from a proxy.
license: MIT
---

# Prove It Works

Match the completion claim to evidence from the actual artifact and requested
behavior. This is a shared verification principle, not a mandatory extra test
suite or authorization to execute arbitrary checks.

1. State the observable result required by the task and the artifact/revision
   being checked. Inspect current state rather than trusting an earlier run or
   a delegate's completion message.
2. Select the smallest relevant documented check. Ask what defect would make
   it fail. A check that reproduces the implementation or cannot detect the
   reported failure is weak evidence.
3. Observe the required surface: user interaction for a UI claim, command output
   and effects for a CLI, actual results for a library or data transformation.
   Build success, HTTP 200, timestamps, and screenshots from another revision
   establish only their narrow facts.
4. Record the command or observation, input identity, expected result, actual
   result, and relevant evidence path. Separate observation from inference.
   Prefer a rerunnable existing check; add a probe only when it improves the
   evidence enough to justify its cost.
5. If verification fails, distinguish an application defect from an incorrect
   probe or environment. Diagnose before retrying, and do not weaken the
   acceptance criterion to obtain a pass.

Respect read-only tasks and existing approval limits. Running code may write
files, start services, or contact external systems; inspect those effects first.
When execution is outside the authorized scope, state what source inspection
establishes and leave execution pending.

Report passed, failed, blocked, and unverified coverage accurately. A pending
manual check is not a pass. Keep evidence separate from durable documentation
and preserve it through owned-process cleanup. Do not commit artifacts merely
because they were used for verification.

## Source

Adapted from Lauren Tan's [pstack Prove It Works](https://github.com/cursor/plugins/blob/12d587dfb20741cafc376c42c696c5f6e2a64487/pstack/skills/principle-prove-it-works/SKILL.md).
Local changes: scope-aware checks, minimal verification, explicit revision and
coverage, and no unconditional script or commit requirement. See [LICENSE](LICENSE).
