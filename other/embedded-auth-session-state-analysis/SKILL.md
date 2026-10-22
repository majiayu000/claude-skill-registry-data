---
name: embedded-auth-session-state-analysis
description: Trace native login handlers, authentication state, encrypted sessions, bindings, replacement, and expiry in embedded firmware. Use when web-auth captures must be correlated with native control flow.
---

# Embedded Auth Session State Analysis

Use this skill to identify the server-side state that turns a valid login
into an authenticated management session and to explain stale-session
responses conservatively.

## Workflow

1. Record firmware identity, architecture, load base, symbols/strings, and disassembly provenance.
2. Trace login parsing through credential/token comparison. Mark success and every failure return separately.
3. Follow writes installing AES keys/IVs, auth flags, session pointers, peer address/User-Agent, counters, and timestamps.
4. Enumerate all readers and writers of each state object; include indirect/table callers.
5. Trace privileged dispatch from HTTP entry through decrypt, authorization, operation lookup, handler, and response.
6. Trace timeout, logout, reboot, and subsequent-login replacement paths. Distinguish auth-state clearing from key zeroization.
7. Correlate native branches with captures using two independent indicators; never treat HTTP status alone as proof.

## State model

Represent states explicitly, for example:

```text
UNAUTHENTICATED -> TOKEN_VALIDATED -> AUTHENTICATED + AES
                 -> replacement / expiry / logout
```

For each transition record address, condition, destination, source value,
and failure behavior. Treat global AES state, per-client slots, tokens,
cookies, and auth flags as distinct objects until code proves otherwise.

## Safety and evidence

Use read-only tests first, with bounded timing and no session flooding. Mark
results `PROVEN FROM CODE`, `VERIFIED IN FIRMWARE`, `OBSERVED ON DEVICE`,
`HIGH-CONFIDENCE INFERRED`, or `UNKNOWN`. Do not test bypass hypotheses when
static analysis finds a potentially privileged missing gate.
