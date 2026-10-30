---
name: integrity-failures
description: Detects unsafe deserialization, unverified software updates, and tampered CI
  artifacts. Use when writing deserialization code, processing pickled or
  marshalled data, implementing software update mechanisms, consuming CI/CD
  artifact downloads, or handling data from untrusted sources that gets
  reconstructed into objects.
---

# Software and Data Integrity Failures Security Check (A08:2025)

## What this checks

Protects against arbitrary code execution and tampered artifacts. Deserializing
untrusted data with code-executing formats gives attackers remote code execution;
unsigned software updates allow supply-chain compromise.

## Vulnerable patterns

- Code-executing deserializer (Python `pickle`/`marshal`/`shelve`, Java `ObjectInputStream`, Ruby `Marshal.load`, PHP `unserialize`, .NET `BinaryFormatter`, unsafe YAML loader) called on attacker-reachable bytes
- Deserialized object whose fields are read by business logic with no schema validation of names, types, or allowed values
- Software update, plugin, or CI artifact downloaded and executed without signature or digest verification
- Trusting reduce/wakeup-style reconstruction hooks invoked on user-controlled serialized blobs
- Verification key or pinned hash hardcoded as a string literal in source rather than loaded from a trusted external source

## Fix immediately

Flag the vulnerable code and explain the risk. Translate the principles below to the
audited file's language and serialization library — use that stack's documented
safe-loader, schema-validation, and signature-verification APIs.

For each finding, establish these properties:

1. **No code-executing deserializer touches untrusted input.** Replace it with a
   data-only format — JSON, safe-mode YAML, protobuf, CBOR without tags — so
   parsing alone cannot trigger constructor or callback execution.
2. **Every deserialized object from untrusted input is validated against an
   explicit schema** — field names, types, allowed values — before any field is
   read by business logic. Applies to JSON, YAML, XML, form bodies, message-queue
   payloads, and binary formats alike; format doesn't matter.
3. **Artifacts are signature- or digest-verified before trust.** Software updates,
   plugin loads, CI-artifact downloads: check a cryptographic signature against a
   trusted public key, or a digest against a pinned hash, before executing or
   loading.
4. **Keys and pinned hashes come from outside the source tree** — environment
   variable, secrets manager, OS keystore, or a build-time constant baked into
   the binary. A value received as a function parameter with no visible origin
   does not demonstrate this.

## Verification

Confirm these properties hold for every relevant pattern present:

- [ ] No code-executing deserializer (pickle, marshal, shelve, `ObjectInputStream.readObject`, `Marshal.load`, `unserialize`, `BinaryFormatter`, unsafe `yaml.load`) receives attacker-reachable bytes. Safe formats (JSON, safe-mode YAML, protobuf) may accept untrusted input if the next criterion is met.
- [ ] Every deserialized object produced from untrusted input is validated against an explicit schema — field names, types, allowed values — before any field reaches business logic
- [ ] For every software-update, plugin-load, or CI-artifact download, the artifact's signature or digest is verified before it is executed, loaded, or written to a trusted path
- [ ] Verification keys and pinned hashes are read from an environment variable, secrets manager, OS keystore, or build-time constant — not hardcoded literals in source, and not opaque function parameters

## References

- CWE-502 ([Deserialization of Untrusted Data](https://cwe.mitre.org/data/definitions/502.html))
- CWE-345 ([Insufficient Verification of Data Authenticity](https://cwe.mitre.org/data/definitions/345.html))
- [OWASP A08:2025 – Software and Data Integrity Failures](https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/)
