---
name: emulating-shellcode-with-unicorn
description: 'Emulates position-independent shellcode in a controlled CPU emulator (Unicorn) to
  trace executed instructions, memory writes, and decoded second stages without running it on a
  real host. Activates for requests to emulate shellcode, trace a decoder stub, or recover a stage
  unpacked at runtime by shellcode.'
domain: cybersecurity
subdomain: reverse-engineering
tags:
  - reverse-engineering
  - shellcode
  - emulation
  - unicorn
  - dynamic-analysis
version: 1.0.0
author: analyst-ai-pack
license: Apache-2.0
mitre_attack:
  - T1027
  - T1620
  - T1055
d3fend:
  - D3-DA
  - D3-SDA
references:
  - 'Unicorn CPU emulator framework — https://www.unicorn-engine.org/'
  - 'MITRE ATT&CK T1620 Reflective Code Loading — https://attack.mitre.org/techniques/T1620/'
---

# Emulating Shellcode With Unicorn

## When to Use

- You have a raw shellcode blob (decoder stub, egg hunter, staged loader) and want to observe its
  behavior via emulation rather than native execution.
- You want to recover a second stage that the shellcode decrypts/decompresses in memory.

**Do not use** native execution for this — emulation contains the code. Unsupported API calls must
be stubbed; emulation is not a full Windows environment.

## Prerequisites

- The shellcode blob and the `unicorn` Python package (degrades gracefully if absent — the script
  reports that emulation is unavailable and still does static prep).

## Safety & Handling

- Even under emulation, treat the blob as malicious; run on an isolated VM and store stages
  password-protected.

## Workflow

### Step 1: Prepare and validate the blob

```bash
python scripts/analyst.py prep shellcode.bin --arch x64
```

Reports size, detected architecture hints, and whether Unicorn is available.

### Step 2: Emulate with an instruction/memory trace

```bash
python scripts/analyst.py emulate shellcode.bin --arch x64 --max-insns 200000
```

Maps the code into emulator memory, sets up a minimal stack, hooks instruction and memory-write
events, and stops on a self-modified region or instruction budget.

### Step 3: Dump decoded stages

If the shellcode writes a new executable region, dump that buffer for follow-on analysis.

### Step 4: Document

Record the entry behavior, decoded stage offset, and any observed (stubbed) API references.

## Validation

- Emulation halts on the instruction budget or a clear decode-complete signal — never hangs.
- A decoded stage, if produced, has a recognizable header (MZ/known opcode prologue).
- Unsupported instructions/APIs are reported, not silently ignored.

## Pitfalls

- Missing API/syscall environment causing early faults — stub the calls the stub needs.
- Wrong architecture/bitness producing immediate invalid-instruction faults.
- Emulating an anti-emulation stub that detects timing/missing APIs.

## References

- See [`references/api-reference.md`](references/api-reference.md) for the emulator harness.
- Unicorn engine and ATT&CK T1620 (linked in frontmatter).
