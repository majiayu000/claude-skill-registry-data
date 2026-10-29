---
name: binary-patching
description: "Use when patching binaries in a lab on authorized targets: your own software, CTF binaries, or client approved test builds. Covers byte patching, assembly level fixes, and verifying patches. Also use when demonstrating a fix for a found vulnerability."
version: 1.0.0
domain: binary
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [ghidra-basics, pwn-fundamentals, secure-coding]
tools:
  - name: Python
    version: "3.12"
  - name: Ghidra
    version: "11.3"
---
Binary patching modifies compiled code directly: flip a check, NOP a
call, or fix a vulnerability when source is unavailable. This skill
covers the lab method on binaries you own or may test: finding the
bytes, making minimal patches, and verifying behavior. Never patch
someone else's software or production systems.

## Quick Workflow

1. Work on a copy; keep the original hash for comparison.
2. Locate the target in a disassembler: the check, the call, or the
   vulnerable code.
3. Design the minimal patch: same size or smaller is easiest.
4. Apply the bytes with a patcher or Python.
5. Verify: the behavior changed as intended and nothing else broke.
6. Test the surrounding functionality, not just the patched path.
7. Document the offset, original bytes, and new bytes.
8. Prefer fixing the source; patching is for when you cannot.

## 1. Byte patching

```bash
# Example: flip a JE (74) to JNE (75) to invert a check (lab binary)
# 1. find the offset in Ghidra/objdump, 2. patch the copy
cp target target.patched
printf '\x75' | dd of=target.patched bs=1 seek=$((0x1234)) conv=notrunc 2>/dev/null
# Verify the disassembly changed as intended
objdump -d target.patched | grep -A2 -B2 "1234:" | head -10
```

```python
#!/usr/bin/env python3
"""Minimal patcher with backup and verification."""
import shutil, hashlib

path = "/tmp/lab/target"
shutil.copy(path, path + ".bak")
data = bytearray(open(path, "rb").read())

patches = [
    # (offset, original, new) - invert JE to JNE at the auth check
    (0x1234, b"\x74", b"\x75"),
]
for off, orig, new in patches:
    assert data[off:off+len(orig)] == orig, f"unexpected bytes at {hex(off)}"
    data[off:off+len(new)] = new

open(path + ".patched", "wb").write(data)
print("sha256 original:", hashlib.sha256(open(path,'rb').read()).hexdigest()[:16])
print("sha256 patched: ", hashlib.sha256(open(path+'.patched','rb').read()).hexdigest()[:16])
```

## 2. Common patch patterns (lab)

```bash
# NOP out a call: replace E8 xx xx xx xx (5 bytes) with 5x 0x90
# Force a check to pass: replace TEST+JZ with XOR EAX,EAX (success code)
# Disable a nag screen: patch the conditional jump around it
# Fix a strcpy: harder; needs code cave or same size replacement
echo "rule: same size patches are safe; growing needs a code cave"
```

## Edge cases

- The binary is signed or has integrity checks. Patching breaks
  the signature; that is expected, note it.
- Patch space is too small. Use a code cave: jump to empty space,
  do the work, jump back.
- Position independent code: patch relative offsets carefully, not
  absolute addresses.

## Escalation

- Need to add substantial logic: write the new code as a shared
  library and LD_PRELOAD it instead of patching.
- Patching production: do not. Fix the source and redeploy.

## Detection and defender view

Defenders detect patching with code signing, integrity monitoring,
and hash allowlists. Patching is also how attackers crack software,
which is why the authorization boundary matters: this skill is for
your binaries and lab targets. The durable defense for vendors is
signed updates and tamper detection, not obscurity.

## Key references

- Ghidra patching workflows.
- "Practical Binary Analysis": patching chapters.
