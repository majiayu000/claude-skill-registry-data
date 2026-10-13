---
name: reporting-cvss-scoring
description: >
  Assign a defensible severity to a finding — build the CVSS 3.1 vector from demonstrated impact and
  reconcile it with the program's own scale. Load on "what severity", "CVSS", "rate this bug", or
  before submitting a report. Signals: a confirmed finding needing a score, a program VRT/severity
  policy, a severity dispute.
domain: reporting
type: reference
stability: locked
modes: [bugbounty, pentest]
severity: info
schema_version: 1
---

# Severity & CVSS scoring

## When it applies
A finding is reproduced and you must put a number on it — for a report, a dispute, or triage. A
defensible score gets paid/prioritised fairly; an inflated one gets you closed as N/A and hurts your
credibility.

## Why it works
CVSS decomposes severity into metrics you justify one at a time from what you *proved*, not what's
theoretically possible. Grounding each metric in demonstrated impact makes the score arguable and
consistent, and mapping it to the program's scale turns it into the right payout/priority.

## Method
1. **Score from demonstrated impact**, metric by metric (CVSS 3.1 Base):
   - **AV** (Attack Vector): Network for a remote web bug, down to Physical.
   - **AC/PR/UI**: was it reliable (low complexity)? did it need auth (privileges)? did it need a
     victim action (user interaction)? Set from what your PoC actually required.
   - **S** (Scope): Changed if the bug crosses a trust/authority boundary (e.g. SSRF into internal
     services, sandbox escape) — a big multiplier, so justify it.
   - **C/I/A**: rate confidentiality/integrity/availability from what you demonstrated, not the worst
     imaginable.
2. **Produce the vector + score** with the FIRST calculator (e.g. `AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N`).
3. **Reconcile with the program**: map to Bugcrowd's VRT or the program's severity matrix — the
   program's policy is the ruling, CVSS is the starting point (`tradecraft-bugbounty-platforms`).
4. **Write the one-line justification** for any contested metric (usually Scope and PR).

## Gotchas
- Don't claim Critical for a self-XSS, a bug needing implausible preconditions, or theoretical impact
  you didn't show — inflation gets you downgraded and distrusted.
- Scope:Changed is the most abused metric — only when a real authority boundary is crossed.
- A **chain** can score higher than any single bug; score the demonstrated chain (`exploit-chaining`).
- CVSS ignores business context; the program's own scale (or a pentest's risk rating) may override.

## Verify success
You have a CVSS vector whose every metric you can defend from your PoC, plus the program-scale
severity it maps to — and it survives a sceptical triager.

## References
FIRST CVSS 3.1 specification & calculator; Bugcrowd VRT; program severity policies.
