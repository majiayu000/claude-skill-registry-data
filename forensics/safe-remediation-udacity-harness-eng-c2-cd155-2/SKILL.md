---
name: safe_remediation
description: Use when a request asks for a restart, rollback, production mutation, or the safest remediation process.
---

# Safe remediation

Treat a production mutation as a proposed action until execution evidence says
otherwise. Before recommending a restart or rollback, require a fresh health
check, relevant logs, and deployment history. A rollback target must be present
in that history and identified as last-known-good.

Describe the process without claiming execution: verify evidence, obtain the
required authorization, perform one controlled action, and re-check health
before another mutation. Do not repeatedly restart or roll back in response to
the same unchanged signal.

Never mark an incident resolved merely because remediation was proposed or
started. Resolution requires observed recovery. Deterministic hooks enforce
safety invariants; the authorization layer independently verifies that the
authenticated subject may perform the requested action on this incident.
