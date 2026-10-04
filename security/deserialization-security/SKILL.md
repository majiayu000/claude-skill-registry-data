---
id: deserialization-security
version: "2.0.0"
title: "Deserialization Security"
description: "Block unsafe deserialization and unsafe XML parsing in Java, Python, .NET, PHP, and Ruby: gadget chains, unrestricted type resolution, external entity expansion, and safer formats. Use when parsing or deserializing data from an untrusted source, wiring cookies, sessions, queues, or RPC payloads, or reviewing pickle, unserialize, Marshal, ObjectInputStream, BinaryFormatter, or XML parser configuration."
category: prevention
severity: critical
applies_to:
  - "when generating code that deserializes data from any untrusted source"
  - "when configuring an XML, YAML, or object-graph parser"
  - "when wiring cookies, sessions, message queues, or RPC payloads"
  - "when reviewing pickle / unserialize / Marshal / ObjectInputStream / BinaryFormatter usage"
languages: ["java", "python", "csharp", "php", "ruby"]
token_budget:
  minimal: 800
  compact: 1300
  full: 1700
rules_path: "rules/"
related_skills: ["crypto-misuse", "ml-security", "ssrf-prevention", "api-security"]
last_updated: "2026-08-12"
sources:
  - "OWASP Deserialization Cheat Sheet"
  - "OWASP XML External Entity Prevention Cheat Sheet"
  - "CWE-502: Deserialization of Untrusted Data"
  - "CWE-611: Improper Restriction of XML External Entity Reference"
---

# Deserialization Security

## Rules (for AI agents)

### ALWAYS
- Prefer data-only serialization formats — JSON, Protobuf, MessagePack with an
  explicit type map — over formats that reconstruct arbitrary runtime objects. What
  makes a format safe here is not schema validation; it is whether the parser can
  instantiate a class the payload names.
- Constrain polymorphic type resolution to an explicit set of expected application
  types. Never let payload data choose the runtime class — that is the mechanism
  behind every gadget chain, whichever serializer is involved.
- Treat an object-reconstructing deserializer crossing a trust boundary as high risk:
  `pickle`, `ObjectInputStream`, `BinaryFormatter`, `unserialize`, `Marshal.load` and
  their framework equivalents. Adding one to a request-handling path needs explicit
  review — check the platform reference for the exact API and the version behaviour
  before accepting or remediating a use.
- Disable external entity resolution and DTD processing on every XML parser that
  receives untrusted input. A parser that resolves entities is a file-read and
  server-side request primitive before it is a parser; `ssrf-prevention` owns where
  the outbound request lands.
- Where serialized state carries a signature or MAC, verify it **before** invoking the
  deserializer — and treat that as defense in depth, not a licence to keep an unsafe
  format. `crypto-misuse` owns the signing key, its algorithm and its rotation.
- Apply parser and object-graph limits — type filters, graph depth, array length,
  stream size — as defense in depth. Where legacy native deserialization is
  unavoidable and execution isolation is genuinely required, isolate at the OS,
  process or container boundary: a deserializer filter constrains what may be
  constructed, never what the constructed code may then do.

### NEVER
- Deserialize attacker-controlled or unauthenticated bytes with a native,
  object-reconstructing format.
- Assume a MAC, a signature, TLS, or a trusted network makes an unsafe serializer
  safe. Some serializers cannot be made safe at any level of authentication, and
  their own vendors say so.
- Allow unrestricted class-name or type resolution from serialized input.
- Treat a type or object-graph filter as a process sandbox.
- Re-enable a serializer the platform vendor classifies as unsafe for compatibility
  alone. That needs a recorded legacy risk acceptance, strict filtering, a
  least-privilege execution boundary, and a migration plan — not a false-positive
  waiver.
- Copy a framework-specific deserialization example without checking it against the
  installed library version. Defaults in this area have moved repeatedly, and an
  example that was correct three releases ago may name an API that no longer exists.

### KNOWN FALSE POSITIVES
- Build-time or configuration-time deserialization of files that ship in the
  repository — test fixtures, vendored config — provided they are never loaded from a
  download.
- A parser that is hardened by its library's current defaults is not a finding merely
  because an older release of the same library was unsafe. Check the installed
  version, not the library name.
- A cryptographically authenticated session format where the MAC genuinely gates the
  deserializer and the framework's own current default serializer is in use.

## Context (for humans)

Object-reconstructing deserialization is the most reliable RCE primitive in modern
enterprise stacks. The economics are simple: when a serializer instantiates whatever
class the payload names, the application has already loaded thousands of classes, many
with side effects in `readObject`, `__reduce__`, `__wakeup` or `Read*` callbacks. A
gadget chain strings those side effects into execution. Mature tooling — ysoserial,
ysoserial.net, marshalsec, the pickle gadget catalogs — means "is this exploitable" is
almost always "yes, with what is already on the classpath."

The fix is a format that cannot instantiate arbitrary classes, not a better filter.
XML belongs in the same skill for the same reason: an entity-resolving parser does
more than parse, and the exploit needs no gadget at all.

Two things date fast here and are deliberately kept out of these rules: exact API
names and version-dependent defaults. Both have moved repeatedly — safe-by-default
constructors, flipped loader defaults, vendor-obsoleted serializers — and a rule that
hard-codes them ages into a false positive or, worse, into an API that never existed.
The platform references carry them, with the version each statement applies to.

## References

- `references/verifying-findings.md` — confirm or refute a finding, then lock it
- `references/java.md` — ObjectInputStream, Jackson polymorphic typing, SnakeYAML,
  XStream: current APIs, version gates, safe configuration
- `references/python.md` — pickle family, PyYAML loaders, numpy, ML checkpoints
- `references/dotnet.md` — BinaryFormatter and its relatives, vendor status
- `references/php-ruby.md` — `unserialize` magic-method chains, Marshal, Psych
- `references/xml.md` — per-platform flags to disable DTD and external entities
- `rules/unsafe_deserializers.json` — build-time catalogue, not shipped to the agent
- [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html).
- [OWASP XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html).
- [CWE-502](https://cwe.mitre.org/data/definitions/502.html) · [CWE-611](https://cwe.mitre.org/data/definitions/611.html).
