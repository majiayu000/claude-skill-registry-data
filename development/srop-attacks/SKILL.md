---
name: srop-attacks
description: Use when learning Sigreturn Oriented Programming in a
  lab on CTF style binaries you own. Covers sigreturn mechanics,
  frame forging, and chaining syscalls without gadgets. Also use when
  a binary has almost no ROP gadgets and needs another path.
version: 1.0.0
domain: binary
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [rop-chains, pwn-fundamentals, shellcode-basics]
tools:
  - name: Python
    version: "3.12"
---

SROP uses the sigreturn syscall to load a whole register context
from a forged signal frame: one gadget (the syscall) becomes
arbitrary syscall execution. This skill covers the lab technique on
binaries you own: how the frame works, forging it, and the classic
execve chain. Learning and CTF use; it is a niche but powerful tool.

## Quick Workflow

1. Confirm the prerequisites: a sigreturn gadget (syscall 15) and a
   stack pivot or controlled buffer.
2. Learn the frame layout for the architecture (x86_64 sigcontext).
3. Forge the frame: set all registers, especially rax=59 (execve),
   rdi=binsh, rsi, rdx.
4. Trigger sigreturn with the forged frame on the stack.
5. Verify the syscall executes; debug the register state on
   failure.
6. Chain: use mprotect via SROP first if you need a writable and
   executable area.
7. Keep the payload compact; the frame is large but structured.
8. Document the gadget addresses and frame layout.

## 1. Frame forging (x86_64 Linux)

```python
#!/usr/bin/env python3
"""SROP frame builder sketch (pwntools style logic, stdlib shown)."""
import struct

# x86_64 sigreturn frame: registers laid out as struct sigcontext
# Key offsets (from kernel uapi): r8..r15, rdi, rsi, rbp, rbx, rdx,
# rax, rcx, rsp, rip, eflags, ... then fpstate
# Simplified: build with pwntools SigreturnFrame in practice

def p64(v):
    return struct.pack("<Q", v & 0xFFFFFFFFFFFFFFFF)

# Minimal concept: the frame sets rax=59, rdi->"/bin/sh", rip->syscall
print("frame size: ~248 bytes for x86_64")
print("set: rax=59 (execve), rdi=binsh_addr, rsi=0, rdx=0, rip=syscall_gadget")
print("trigger: ret to the sigreturn gadget with rsp pointing at the frame")
```

```bash
# Finding the gadget (lab binary):
# ROPgadget --binary target | grep -i "syscall.*ret"
# or: objdump -d target | grep -B2 "syscall" | grep ret
# You need: the ability to call rt_sigreturn (rax=15) with your frame ready
echo "classic setup: read() your frame onto the stack, then sigreturn"
```

## 2. Debugging the chain

```bash
# In gdb on your lab binary:
# - break at the sigreturn, inspect the stack as a sigcontext
# - check: does rip point at a syscall gadget, is rax 15 at entry
# - after sigreturn: verify registers match your forged values
# Common failure: wrong frame offset (uc_flags / alignment), fix by
# comparing against a real signal frame captured in the debugger
echo "capture a real frame once; diff yours against it"
```

## Edge cases

- No sigreturn gadget. SROP does not apply; use classic ROP or
  ret2libc.
- The binary is statically linked vs dynamic. Frame layout is
  kernel defined, so it works either way; gadget availability
  differs.
- seccomp blocks execve. Then SROP to mprotect plus shellcode, or
  pivot to an allowed exfiltration syscall.

## Escalation

- Frame forging by hand is error prone: use pwntools
  SigreturnFrame for real work; the sketch above is for
  understanding.
- Need more than one syscall: chain SROP frames or follow with a
  small ROP chain after mprotect.

## Detection and defender view

SROP is a niche exploitation technique seen in CTFs more than in
the wild. Defenders rely on the standard mitigations: NX, ASLR,
and seccomp, which constrain what SROP can achieve. The technique
matters for exploit developers to know and for defenders to
understand as part of the ROP family.

## Key references

- "Framing Signals" (SROP original paper, Bosman et al.).
- pwntools SigreturnFrame documentation.
- Related skills: rop-chains, pwn-fundamentals.
