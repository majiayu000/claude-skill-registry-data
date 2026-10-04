---
name: sec-audit
description: Print Peephole's security audit report for this project — current mode, binary integrity, the CWE-mapped decision tally, sec-debt items needing approval, and tamper-evident log-chain status. Use when the user says /sec-audit or asks what Peephole has blocked or flagged.
---

# Peephole security audit

Run:

```sh
sh "$CLAUDE_PLUGIN_ROOT/hooks/peephole.sh" audit
```

Present the output to the user. It reports:

- **mode** and **binary integrity** (a drift alarm means the binary or its embedded KB was tampered with — advise reinstalling).
- **decision tally** — how many writes were denied / asked / allowed / retro-flagged / rewritten, broken down by CWE and by OWASP 2025 category.
- **born-secure (N2)** — of the security-relevant hunks (heuristic-tagged), how many were clean at first write vs prevented at the gate vs landed insecure, with the born-secure rate. Instrumentation, not proof.
- **interruption rate** — asks+denies per 20 write-gate decisions (the §7.4 FP budget: ≤ 1 unsolicited ask per 20 writes).
- **sec-debt** — logged waiver requests and any **UNAPPROVED** markers in the tree (evasion risk), plus negative-test mandates that exhausted without compliance.
- **log chain** — `intact` or `BROKEN at line N`, which surfaces casual truncation or tampering of the decision log. The log is the last 30 days.

If the log chain is broken, treat it as a signal that the audit log was altered and tell the user plainly.
