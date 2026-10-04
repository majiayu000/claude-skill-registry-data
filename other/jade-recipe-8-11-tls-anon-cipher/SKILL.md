---
name: jade-recipe-8-11-tls-anon-cipher
description: >-
  Resolves hard-coded anonymous TLS cipher suites (DH_anon / ECDH_anon), which
  JDK 11 disables by default through jdk.tls.disabledAlgorithms. Agent-mode
  recipe: the shard contract names the files; this document defines the
  transform, its limit, and when the fix stops being the agent's call.
mode: agent
arguments: [--shard-json]
---
# jade-recipe-8-11-tls-anon-cipher — anonymous suites no longer negotiate

The JDK 11 `java.security` default for `jdk.tls.disabledAlgorithms` contains
`anon, NULL`. The JSSE reference guide states these algorithms will not be
negotiated for TLS/DTLS connections **even if they are enabled explicitly by an
application**. `SSLServerSocket.setEnabledCipherSuites(...)` with an anonymous
suite therefore no longer produces an unauthenticated handshake on JDK 11; it
produces a handshake failure at connect time. This is a runtime behavior change,
not a compile error — the code still compiles, which is why it needs a rule.

## Scope of one task

You receive a shard contract. This rule is `blast_class: body-local`
(`parallel_safe: true`). Edit only that shard's `editable_files`;
`read_only_context` is read-only.

## The two sites

| file | line | construct |
|---|---|---|
| `src/jade/src/jade/imtp/leap/SSLHelper.java` | 29 | `TLS_ECDH_anon_WITH_AES_128_CBC_SHA` in the `supportedKeys` list |
| `src/jade/src/jade/imtp/leap/JICP/JICPSPeer.java` | 224 | `SSL_DH_anon_WITH_RC4_128_MD5` passed to `setEnabledCipherSuites` |

Both are `String` literals inside a `String[]` initializer. The declared types
(`List`, `String[]`) and every surrounding signature stay identical — that is
what makes this body-local.

## What the agent may decide, and what it may not

The agent **may** replace an anonymous suite with another suite only when the
replacement needs no new key material and no new configuration: same
`String[]` shape, same call, nothing else in the file changes.

The agent **must not** silently move JADE from unauthenticated to authenticated
TLS. Every non-anonymous suite requires a server certificate, which means a
keystore, which means new configuration, a new failure mode for every existing
deployment, and a decision about what JADE ships by default. That is an
architectural change for the user to make, not a mechanical fix. Never invent a
keystore path, never generate a self-signed certificate, never add a property.

If the only correct replacement requires authentication, report `NEEDS_REVIEW`
with the two options stated plainly:

1. Adopt authenticated suites, and specify where key material comes from.
2. Keep anonymity as an explicit, documented deployment choice by removing
   `anon` from `jdk.tls.disabledAlgorithms` in the deployment's
   `java.security`, accepting that this is a downgrade a reviewer must sign off
   on and that it is a JVM-level setting, not a JADE source change.

Do not choose between those on the user's behalf.

## Invariants

- No public signature changes — this rule is `body-local`.
- No new imports, no new fields, no new configuration keys.
- No change under `consumer-playground/`. The consumers carry their own
  occurrences (`JICPSConnection.java`, `SSLEngineHelper.java`,
  `HTTPSClientConnection.java`); they are outside the workspace and outside
  this shard. If a JADE-side change would force a consumer edit, that is
  `NEEDS_REVIEW`, because consumers must keep passing untouched.

## Verification

- `verify_shard.py` applies normally here: the files survive and must compile.
- A JICP-S handshake between two JADE containers on JDK 11 must complete
  without `SSLHandshakeException`.
- All four consumers must still PASS, with no edit on their side.

## Status to report

| status | when |
|---|---|
| `FIXED` | the anonymous suite is gone and the replacement needs no new key material or configuration |
| `NEEDS_REVIEW` | the only correct fix requires authentication, key material, or a JVM security-property change |
| `SKIPPED` | the flagged literal is not actually reachable configuration (prove it, do not assume it) |
| `FAILED` | the file does not compile after the edit, or a consumer stops passing |
