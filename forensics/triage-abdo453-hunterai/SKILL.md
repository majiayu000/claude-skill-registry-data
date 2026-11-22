---
name: "triage"
description: "Batch-validate ALL findings through the 7-Question Gate. Kills weak findings in bulk. Usage: /triage"
---

# Triage

*Sourced from h-mmer-pentest-agents*

Batch triage all findings.

ALL validator agents dispatched by this command MUST use .

## Process

1. Read findings.md and/or findings.json
2. List all findings with a numbered summary
3. For EACH finding, launch `validator` agent with the finding details
4. Collect results: PASS / KILL / DOWNGRADE / CHAIN REQUIRED
5. Output summary table:

```
TRIAGE RESULTS
═══════════════
#  Finding                              Decision    Reason
1  GraphQL schema leakage               KILL Q7     Never-submit: introspection alone
2  Config exposure SayTech               KILL Q7     SPA client config is by design
3  Internal service URLs                 KILL Q6     Not exploitable externally
4  IDOR on /api/users/{id}              PASS        Confirmed with real data
5  XSS on comments                      PASS        Cookie theft PoC works

PASSED: 2 findings → ready for /report
KILLED: 3 findings → removed from queue
```

6. Update brain with triage results
7. For KILLED findings: `uv run python3 ../../tools/brain.py record <target> exhausted "<finding>" "<kill reason>"`
8. For PASSED findings: suggest `/report` or `/validate` for full PoC + evidence

## Top-Tier Triage Standard

Batch triage should reduce the queue aggressively.

For each finding, produce:
- decision: PASS, KILL, DOWNGRADE, CHAIN REQUIRED, DUPCHECK REQUIRED, EVIDENCE REQUIRED
- deciding gate: the first question or artifact that controlled the outcome
- missing proof: exact command, account, request, browser check, or chain needed
- reportability: bounty-grade, pentest-note, internal hardening, or discard
- memory action: confirmed, exhausted, partial, duplicate-risk, or chain-pending

Do not average weak findings into a stronger story. Chain them only when one finding provides a capability the next finding consumes.

