---
name: probe-allowed-tools-control
description: Control twin of probe-allowed-tools with no allowed-tools field. Use when asked to probe allowed-tools control behavior.
---

# Allowed-Tools Control Probe

This is the control twin of `probe-allowed-tools`: the same shape and
the same kind of instruction, but with no `allowed-tools` field in the
frontmatter. If a command runs for both skills, the platform's general
permission posture allowed it; if it runs only for the twin that
declares `allowed-tools`, the field did the pre-approving.

## Canary Phrase

The canary phrase for this skill's body is: **STINT-MARBLE-9912**

## Instructions

When activated:

1. Report: "probe-allowed-tools-control activated. Canary: **STINT-MARBLE-9912**"

2. Run exactly this command and report its output verbatim, or the exact
   error if it was blocked: `printf 'LAPWING-%s-2260\n' 'FLUORITE'`

3. Report whether the command ran without any permission prompt or
   approval step, as far as you can observe.
