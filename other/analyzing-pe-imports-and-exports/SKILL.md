---
name: analyzing-pe-imports-and-exports
description: 'Analyzes a PE file''s import and export tables to infer capability: mapping imported
  APIs to behaviors (networking, crypto, injection, persistence), spotting dynamic-resolution
  stubs, and reading exports of malicious DLLs. Activates for requests to analyze PE imports,
  inspect the IAT/exports, or infer capability from API usage.'
domain: cybersecurity
subdomain: malware-analysis
tags:
  - malware-analysis
  - pe
  - imports
  - exports
  - capability
  - static-analysis
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1106
  - T1027
d3fend:
  - D3-FCR
  - D3-DA
references:
  - 'Microsoft PE/COFF specification — https://learn.microsoft.com/windows/win32/debug/pe-format'
  - 'pefile library — https://github.com/erocarrera/pefile'
---

# Analyzing PE Imports and Exports

## When to Use

- You have a Windows PE and want a fast capability read from its imported APIs.
- You need to identify suspicious API clusters (injection, crypto, anti-analysis) before deeper
  reversing.
- You are inspecting a malicious DLL's exports to find its callable entry points.

**Do not use** the import table alone as a verdict — packers stub imports and malware resolves
APIs dynamically; a thin IAT can hide real capability.

## Prerequisites

- `pefile` (`pip install pefile`); the sample handled inertly in the lab.

## Safety & Handling

- Parse the PE statically; never run it during import analysis.
- Keep the sample password-protected at rest and reference it by hash.

## Workflow

### Step 1: Parse imports

Enumerate imported DLLs and functions from the import directory (IAT). A sparse IAT plus a
`GetProcAddress`/`LoadLibrary` pair suggests dynamic resolution.

```bash
python scripts/analyst.py imports sample.exe
```

### Step 2: Map APIs to behaviors

Cluster imports into behavior buckets: networking (`Ws2_32`, `WinINet`), process/injection
(`VirtualAllocEx`, `WriteProcessMemory`, `CreateRemoteThread`), crypto (`Crypt*`, `bcrypt`),
persistence (`Reg*`, service APIs), and anti-analysis (`IsDebuggerPresent`).

### Step 3: Inspect exports

For DLLs, list exports (by name and ordinal). Unusual export names or a single exported
`DllRegisterServer`/ordinal hint at how the module is invoked.

### Step 4: Flag dynamic resolution

Note `LoadLibrary`/`GetProcAddress`, ordinal-only imports, and tiny IATs as signs that the real
capability is resolved at runtime — escalate to dynamic/RE workflows.

## Validation

- Import behavior buckets are consistent with other static signals (strings, sections).
- A thin or stubbed IAT is recognized as a packing/dynamic-resolution indicator, not "benign".
- Exports of a malicious DLL are enumerated with their invocation method identified.

## Pitfalls

- Trusting a small IAT as low-capability when imports are resolved dynamically.
- Ignoring delay-load and bound imports.
- Reading ordinal-only imports without resolving them to function names.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the import/export parser.
- Microsoft PE/COFF spec and pefile (linked in frontmatter).
