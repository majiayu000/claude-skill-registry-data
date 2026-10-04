---
name: reverse-engineering-binaries-with-ghidra
description: 'Uses Ghidra to disassemble and decompile a binary, navigate to key routines via
  imports and strings, annotate decompiled code, and run headless scripts to automate
  extraction of C2, crypto, and config. Activates for requests to reverse engineer with
  Ghidra, decompile a binary, or script Ghidra headless analysis.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - ghidra
  - decompilation
  - disassembly
  - headless
  - static-analysis
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1140
  - T1480
d3fend:
  - D3-FA
  - D3-FCR
references:
  - 'Ghidra documentation — https://ghidra-sre.org/'
  - 'Ghidra API (FlatProgramAPI / headless) — https://ghidra.re/ghidra_docs/api/'
---

# Reverse Engineering Binaries with Ghidra

## When to Use

- Static/dynamic triage has identified functionality that needs code-level understanding.
- You need to reverse a C2 protocol, decryption routine, or custom obfuscation.
- You want to extract hardcoded config (C2, keys, campaign IDs) from compiled code, or
  automate extraction across many samples via headless scripts.

**Do not use** Ghidra as a first step for unknown samples — triage statically and behaviorally
first, and unpack before decompiling a packed binary.

## Prerequisites

- Ghidra 11.x with JDK 17+.
- An isolated analysis host.
- Familiarity with x86/x64 (or the target arch) and OS API conventions.
- The sample unpacked (decompiling packed code wastes effort).

## Safety & Handling

- Ghidra performs static analysis and does not run the sample, but still work in the lab.
- Treat any dumped/derived payloads as live samples.

## Workflow

### Step 1: Import and auto-analyze

Create a project, import the binary (Ghidra detects PE/ELF/Mach-O and arch), and run
auto-analysis with default analyzers.

### Step 2: Navigate to interesting code

Start from imports (Symbol Tree) and strings (Defined Strings). Cross-reference (`X`) from a
suspicious API or string to its callers to reach the relevant function quickly.

```text
VirtualAlloc/WriteProcessMemory -> injection logic
InternetOpen/WinHttp*           -> C2
CryptEncrypt / custom XOR loops -> crypto/config decode
```

### Step 3: Annotate the decompiler output

Retype variables, rename functions, and add comments as you understand the code. Good naming
turns the decompiler into readable pseudo-C and compounds across a session.

### Step 4: Automate with headless scripts

For repeatable extraction, run Ghidra headless with a post-script. The bundled Python uses
`analyzeHeadless` to export functions/strings to JSON:

```bash
python scripts/analyst.py headless --ghidra /opt/ghidra --bin sample.bin --out out.json
```

### Step 5: Extract the target artifact

Recover the C2 string, key, or config and validate it against dynamic observations.

## Validation

- Renamed/retyped routines produce coherent pseudo-C consistent with observed behavior.
- Extracted config (C2/keys) matches what the sample uses at runtime.
- Headless export reproduces the interactive findings.

## Pitfalls

- Decompiling packed/obfuscated code — unpack first or the output is meaningless.
- Trusting decompiler types blindly; verify against the disassembly for crypto/pointer logic.
- Ignoring TLS callbacks/constructors that run before the entry point.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the headless wrapper.
- Ghidra documentation and API (linked in frontmatter).
