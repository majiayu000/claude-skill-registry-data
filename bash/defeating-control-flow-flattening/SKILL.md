---
name: defeating-control-flow-flattening
description: 'Defeats control-flow-flattening obfuscation by identifying the dispatcher/state-
  variable structure and reconstructing the original control flow so the logic becomes readable.
  Activates for requests to defeat control-flow flattening, deobfuscate an OLLVM-flattened function,
  or recover original control flow from a dispatcher loop.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - obfuscation
  - control-flow-flattening
  - ollvm
  - deobfuscation
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1027.013
  - T1140
d3fend:
  - D3-DA
  - D3-SDA
references:
  - 'OLLVM control-flow flattening (Obfuscator-LLVM) — https://github.com/obfuscator-llvm/obfuscator'
  - 'MITRE ATT&CK T1027 Obfuscated Files or Information — https://attack.mitre.org/techniques/T1027/'
---

# Defeating Control-Flow Flattening

## When to Use

- A function is flattened (a dispatcher loop switching on a state variable, with original blocks as
  switch cases) and you need to recover the original control flow.
- You are reversing OLLVM-style or similar flattening.

**Do not use** this on non-flattened code — confirm the dispatcher/state-variable pattern first.
This skill analyzes disassembly/CFG data statically and executes nothing.

## Prerequisites

- A disassembled function's basic-block/edge data (e.g., exported from Ghidra/IDA/Binary Ninja as
  JSON).

## Workflow

### Step 1: Detect the flattening structure

```bash
python scripts/analyst.py detect cfg.json
```

Identifies a dispatcher block (high in-degree, switch/compare on a state variable) and the relay/
case blocks that all branch back to it.

### Step 2: Recover state transitions

Track the constant assigned to the state variable in each case to determine the successor block,
rebuilding the true edges.

### Step 3: Reconstruct the original CFG

Emit the deflattened successor mapping (case → next case) for re-annotation in the disassembler.

### Step 4: Verify

Confirm the recovered flow has a single entry, sane successors, and no orphan blocks.

## Validation

- The dispatcher is identified by in-degree and state-variable comparison.
- Each case's next-state constant maps to a real successor block.
- The reconstructed CFG covers all original (non-relay) blocks.

## Pitfalls

- State variable computed (not a constant) — requires emulation/symbolic execution.
- Multiple dispatchers or nested flattening.
- Opaque predicates and bogus blocks inflating the case set.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the deflattener.
- OLLVM and ATT&CK T1027 references (linked in frontmatter).
