---
name: reverse-engineering-custom-c2-protocols
description: 'Reverses proprietary command-and-control protocols: locating send/recv routines,
  recovering the message framing and encryption/encoding, and reconstructing the command set
  to build a decoder or emulator. Activates for requests to reverse a custom C2 protocol,
  decode beacon traffic, or document a malware command structure.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - command-and-control
  - protocol
  - network
  - decryption
  - beacon
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1071
  - T1095
  - T1573
d3fend:
  - D3-NTA
  - D3-DA
references:
  - 'MITRE ATT&CK T1071 Application Layer Protocol — https://attack.mitre.org/techniques/T1071/'
  - 'MITRE ATT&CK T1573 Encrypted Channel — https://attack.mitre.org/techniques/T1573/'
---

# Reverse Engineering Custom C2 Protocols

## When to Use

- A sample uses a non-standard protocol (or a custom layer over HTTP/TCP) and you must decode
  its traffic.
- You need to recover message framing, the encryption/encoding scheme, and the command set.
- You want to build a standalone decoder or emulator to parse captured beacon traffic.

**Do not use** this for documented protocols handled by existing dissectors — use the protocol
analyzer directly instead of reversing from scratch.

## Prerequisites

- A disassembler/debugger and a network capture (PCAP) of the sample's traffic where possible.
- The crypto/obfuscation skills for recovering keys and encodings.

## Workflow

### Step 1: Locate the network routines

Find `send`/`recv`/`WSASend`/`WinHTTP` calls (or the framework wrappers) and the buffers they
operate on. These bracket the serialization and crypto.

### Step 2: Recover framing

Trace how outbound buffers are built: magic bytes, length prefixes, sequence/ID fields, and
type/opcode fields. Document the header layout.

```text
[ magic(4) ][ len(4 LE) ][ opcode(1) ][ flags(1) ][ payload(len) ]
```

### Step 3: Recover crypto/encoding

Identify the transform applied before send / after recv (XOR with embedded key, RC4, AES,
base64). Recover keys from the binary or from the key-setup routine.

### Step 4: Reconstruct the command set

Map opcodes to handlers (shell, download, upload, sleep/jitter, exit) by following the
dispatch switch. Build a table of command → behavior.

### Step 5: Build a decoder and validate

Implement a parser/decryptor and run it against captured traffic; confirm it yields coherent
commands and recovers the beacon's config.

```bash
python scripts/analyst.py decode capture.bin --key 0x5a --magic 4d5a4331
```

## Validation

- The decoder parses every message in a real capture without desync.
- Decrypted payloads are coherent (printable commands / structured config).
- The opcode table matches the dispatch logic observed in the binary.

## Pitfalls

- Assuming fixed keys when the protocol negotiates a session key in the first exchange.
- Missing a length/sequence field and desynchronizing after the first message.
- Confusing transport (TLS) with the inner custom layer; decode the inner layer.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the framing decoder.
- MITRE ATT&CK T1071 and T1573 (linked in frontmatter).
