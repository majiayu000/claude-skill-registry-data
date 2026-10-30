---
name: pwn-chain
description: |
  Full-chain engineering methodology from reverse engineering to working exploit.
  Applicable scenarios: got binary + vulnerability point + target environment, need to write a stably working exploit (not just a script that only reproduces locally and crashes remotely).
  Covers three directions: stack overflow / heap exploitation / kernel pwn. Emphasizes the engineering gap between "CTF local pass to real remote stable exploit": libc version mismatch, heap spray timing, SMEP/SMAP/KASLR, stack alignment, remote buffering.
  Core toolchain: pwntools + GEF/pwndbg + ROPgadget/Ropper + one_gadget + libc-database + qemu-system kernel debugging.
  Trigger keywords: pwn, stack overflow, heap overflow, ROP, ret2libc, ret2csu, one_gadget, libc-database, heap exploitation, tcache, fastbin, unsorted bin, kernel pwn, kROP, SMEP, SMAP, KASLR, modprobe_path, pwntools, GEF, pwndbg.
---

## ACTION REQUIRED (execute immediately after reading)

2. `NOW`: Confirm the current task matches this skill's scope
4. `NEXT`: When tools are missing, call bootstrap - do not guess paths
5. `ACT`: Enter the first step of the "Workflow" and execute - do not stop at confirmation state

# From Vulnerability Point to Working Exploit (Pwn Chain)

## Scope

Use this skill when the task falls into these scenarios:

1. **Got binary + known vulnerability point** - static/audit/fuzz already found overflow/UAF/double free, need to go from trigger to getting shell
2. **CTF challenge passes locally, does not work remotely** - remote environment differences cause script failure, need stabilization
3. **Real target binary exploitation** - SRC / red team scenario, already identified memory corruption vulnerability, need to construct RCE
4. **Linux kernel driver ioctl bug** - user-mode trigger, goal is privilege escalation to root

**Prerequisite**: you already know "where it crashes". This skill does not discover vulnerabilities (that is fuzzing/auditing), it handles "writing exploit from vulnerability point".

### Division of labor with other skills

| Scenario | Use which |
|----------|-----------|
| Identify custom VM / anti-debug / complex obfuscation | `reverse-engineering/` |
| Open binary from scratch for static analysis | `ida-reverse/` or `radare2/` |
| **Have vulnerability point, write exploit to work remotely** | **This skill** |
| Integrate shell obtained via pwn into complete attack chain | `attack-chain/` (downstream) |

`reverse-engineering/` focuses on "understanding what the program does" (pattern recognition, protocol restoration, solving CTF challenge mechanisms); this skill focuses on "turning an already-understood vulnerability into an executable attack". The two are often used together, but have clear division of labor.

## Core workflow

```text
Step 1: Confirm vulnerability type + protection mechanism
   - checksec ./vuln (NX / Canary / PIE / RELRO / Fortify)
   - file ./vuln  + readelf -d ./vuln
   - Vulnerability classification: stack overflow / format string / heap (UAF/DF/OF) / integer / race / kernel
   - decide which references/ to follow

Step 2: Choose exploitation strategy
   - NX off + no ASLR -> direct shellcode
   - NX on + libc given -> ret2libc / one_gadget
   - NX on + no libc -> leak then libc-database reverse lookup
   - Heap -> technique by glibc version (tcache/fastbin/unsorted/large)
   - Kernel -> commit_creds / modprobe_path / core_pattern

Step 3: Prepare libc + gadgets
   - libc-database: ./find puts 0x6f0
   - ROPgadget --binary ./libc.so.6 --only "pop|ret"
   - one_gadget ./libc.so.6
   - Calculate base: leak_addr - libc.sym['puts']

Step 4: Write pwntools template (local process)
   - context.binary = ELF('./vuln')
   - p = process('./vuln')  /  p = gdb.debug('./vuln','b *main+xx')
   - payload = cyclic(N) + p64(ret) + ...
   - p.interactive()

Step 5: Pass locally
   - Repeatedly attach + check registers + adjust offset
   - Use pwndbg/GEF vmmap / heap / bins / telescope
   - After passing, switch to remote()

Step 6: Remote stabilization
   - libc offset: use leak + libc-database reverse lookup, do not guess
   - Stack alignment: 16-byte misaligned -> movaps crash -> add a ret gadget
   - Remote network latency -> recvuntil precise anchor strings, disable fuzzy sleep
   - Remote buffering: sendlineafter more stable than sendline
   - Heap spray success rate: increase spray count + leave padding chunks to prevent merge
   - Multiple runs: write while True to verify success rate >= 95%
```

## Typical scenarios

### Scenario 1: Remote 64-bit binary (NX+PIE+canary, libc given)

```text
Have: ./vuln (64-bit ELF, NX, PIE, canary) + ./libc.so.6 + nc host port
Vulnerability: read(buf, 0x200) but buf only 0x40 bytes -> stack overflow
Protection: canary blocks, PIE randomizes .text

Strategy:
1. First leak canary (stack/format string/partial read)
2. Then leak a libc function address (puts@got)
3. Use libc.address = leaked - libc.sym['puts'] to calculate libc base
4. one_gadget ./libc.so.6 select a magic gadget whose constraints can be satisfied
5. payload = padding + canary + saved_rbp + (pop_rdi + bin_sh + system) or directly one_gadget
6. Add a ret gadget to fix stack alignment (critical!)
```

Complete template see `references/stack-pwn.md`.

### Scenario 2: Linux kernel driver ioctl OOB write -> get root

```text
Have: vmlinux + bzImage + initramfs.cpio.gz + custom vuln.ko
Vulnerability: ioctl(0x1337, ptr) copy_from_user length controllable -> kernel heap overflow (kmalloc-64 slab)
Protection: SMEP, SMAP, KASLR, KPTI

Strategy:
1. Modify init script to get root shell (CTF) or first leak KASLR base then continue (real)
2. Leak kernel base via /proc/kallsyms (may be restricted) or uninitialized heap spray
3. Spray tty_struct / msg_msg / pipe_buffer in kmalloc-64 slab
4. Overwrite vtable pointer to user-mode -> does not work (SMEP), switch to stack pivot + kernel ROP
5. ROP chain: prepare_kernel_cred(0) -> commit_creds -> swapgs+iretq -> user-mode execve("/bin/sh")
6. Or easier: overwrite modprobe_path to "/tmp/x", write a /tmp/x, then trigger modprobe
```

Complete template see `references/kernel-pwn.md`.

## On-Demand Bootstrap

Bootstrap/install commands below are reference-only; package, gem, git-clone and apt installs are mutations requiring explicit authorization and an isolated environment. Do not run them during review.

### Tool dependencies

| Tool | Purpose | Install method |
|------|---------|---------------|
| pwntools | Exploit writing framework | `pip install pwntools` |
| GEF | gdb enhancement (recommended for kernel + user mode) | `git clone https://github.com/bata24/gef` (actively maintained fork) |
| pwndbg | gdb enhancement (best heap debugging experience) | `git clone https://github.com/pwndbg/pwndbg && ./setup.sh` |
| ROPgadget | Gadget search | `pip install ropgadget` |
| Ropper | Gadget search (alternative, supports more architectures) | `pip install ropper` |
| one_gadget | libc magic gadget finder | `gem install one_gadget` (requires ruby) |
| libc-database | libc fingerprint reverse lookup | `git clone https://github.com/niklasb/libc-database && ./get` |
| qemu-system-x86_64 | Kernel challenge debugging | `apt install qemu-system-x86` |
| binwalk / cpio | initramfs unpacking | `apt install binwalk cpio` |
| patchelf | Switch libc version | `apt install patchelf` |

### Bootstrap check script

```bash
# One-click check + install core tools
for t in pwntools ropgadget ropper; do
  pip show $t >/dev/null 2>&1 || pip install $t
done

command -v one_gadget >/dev/null || gem install one_gadget

[ -d ~/tools/libc-database ] || git clone https://github.com/niklasb/libc-database ~/tools/libc-database
[ -d ~/tools/libc-database/db ] || (cd ~/tools/libc-database && ./get ubuntu debian)

[ -d ~/tools/pwndbg ] || (git clone https://github.com/pwndbg/pwndbg ~/tools/pwndbg && cd ~/tools/pwndbg && ./setup.sh)
```

##
