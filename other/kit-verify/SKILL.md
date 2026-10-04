---
name: kit-verify
description: Force the guardrails VERIFY echo protocol — prove every done/fixed/works claim with quoted command output. Use when asked to verify claims, check completion evidence, prove it works, or when "done" was claimed without proof.
---

Read docs/guardrails/VERIFY.md and execute the echo protocol against the current task's claims:
1. Walk V1–V14, one line each: `V<n>: PASS — <command> -> <output line>` | `FAIL — ...` | `N/A — <reason>`.
2. Every quoted output line must exist verbatim in a tool result in THIS turn — run any missing command now.
3. Report only in the canonical status vocabulary; while any line reads FAIL, do not claim done.
