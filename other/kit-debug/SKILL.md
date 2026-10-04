---
name: kit-debug
description: Force the guardrails debugging discipline — reproduce first, CAUSE line, failed-attempts ledger, escalation ladder. Use when debugging is flailing, the same fix keeps failing, or asked to debug systematically.
---

Read docs/guardrails/DEBUG.md and restart the discipline at D1:
- Reproduce first and paste the failing output; no fix before the `CAUSE:` line (D3).
- Log every failed fix as an `ATTEMPT n [L<level>]` ledger entry (D6) and obey the ESCALATION LADDER.
- Check the red-flag table against your own last message — the left column is the tripwire.
