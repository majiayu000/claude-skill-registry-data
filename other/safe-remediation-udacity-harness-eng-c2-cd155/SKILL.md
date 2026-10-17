---
name: safe_remediation
description: Propose incident mutations while treating permission, safety, and tool outcomes as authoritative.
---

# Safe remediation

A mutation tool call is a proposal. The Hermes harness decides whether the
trusted user is authorized and whether deterministic safety checks pass. For a
rollback, retrieve fresh health and deployment history, then propose the exact
target requested by the operator. If the proposal is denied or blocked, do not
retry through another tool and do not claim it executed. If it succeeds,
recommend a fresh health check to verify recovery.

