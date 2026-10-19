---
name: ctf-pwn
description: >
  CTF pwn challenge playbook — fast pwntools workflow against "nc host port" services: reproduce
  the remote environment locally with the provided libc/ld (patchelf, Docker), exploit format-string
  bugs (the CTF staple) for leaks and writes, and iterate a script from crash to flag. Load when the
  handout is a binary plus connection info. Signals: "pwn" category, nc host port, checksec output,
  provided libc.so.6/ld-linux, Dockerfile, "%p" reflections, menu-driven heap note apps.
domain: ctf
type: technique
stability: learning
modes: [pentest]
severity: critical
cwe: [CWE-121, CWE-134, CWE-416]
tools: [pwntools, checksec, patchelf, gef, pwndbg, ropgadget, one_gadget, libc-database, docker]
schema_version: 1
---

# CTF pwn challenges

## When it applies
The handout is a binary, usually with `nc host port`, often with a bundled `libc.so.6` +
`ld-linux-x86-64.so.2` and sometimes a Dockerfile. This skill covers the CTF-specific *workflow* —
environment reproduction, remote iteration, and format-string handling. For the exploit chains
themselves (ret2libc/one_gadget, tcache/fastbin/unsorted techniques, kernel pwn, stabilization),
work `exploit-pwn-chain`; for finding the bug, `reverse-eng-binary-triage` and
`exploit-memory-corruption`.

## Why it works
CTF pwn is deterministic: the organizer ships you the exact remote environment (libc, ld, sometimes
the whole image), so "local works, remote crashes" is a *choice*, not a hazard — if you run the
provided libc locally, offsets are identical and the only remote variables left are ASLR (leak it)
and network timing (anchor your reads). Format strings recur constantly because they're a compact
way to give both a leak and an arbitrary write.

## Method
1. **Triage the handout (3 minutes).** `checksec --file=chall`, `file chall`, note provided files.
   Run it, feed it garbage and long input, try `%p %p %p` on any echo. Read the Dockerfile if given:
   it pins the OS/libc, the flag path, and any seccomp wrapper.
2. **Reproduce the remote environment locally — always.** With a provided libc/ld:
   ```
   patchelf --set-interpreter ./ld-linux-x86-64.so.2 --set-rpath '$ORIGIN' ./chall
   ```
   or run via `./ld-linux-x86-64.so.2 --library-path . ./chall`. With only a Dockerfile,
   `docker build -t chal . && docker run -it --cap-add=SYS_PTRACE chal` and exploit inside it.
   Never exploit against your host libc and hope.
3. **Set up the pwntools loop.** One script, toggleable target:
   ```python
   from pwn import *
   context.binary = elf = ELF('./chall')
   context.log_level = 'debug'
   io = gdb.debug('./chall', 'b main\nc') if args.GDB else \
        (process('./chall') if args.LOCAL else remote('host', port))
   ```
   Use `sendlineafter(b'> ', payload)` anchored on the actual prompt; `cyclic()`/`cyclic_find()`
   for offsets; finish with `io.interactive()`.
4. **Format strings — the CTF staple.** When input is reflected:
   - **Leak**: `%7$p`-style direct-parameter reads dump the stack — hunt libc pointers (return
     addresses into `__libc_start_main`), PIE base (code addresses on the stack), and the canary
     (the value ending in `00` at a consistent slot). `FmtStr(execute_fmt=send_payload)` in pwntools
     finds the offset for you.
   - **Write**: `%n`/`%hn`/`%hhn` — write `pwntools`' `fmtstr_payload(offset, {addr: value})`
     instead of hand-crafting. Classic targets: GOT entry → `system` (partial RELRO), a saved
     return address, `__free_hook` (glibc < 2.34), or a global `auth`/`is_admin` variable.
   - GOT overwrite often needs the function to be *called again* — loop the menu or re-trigger.
5. **Match the rest to checksec** (defer to `exploit-pwn-chain` for depth): no PIE + no canary +
   `system`/`/bin/sh` in binary → plain ret2win; NX + libc leak → ret2libc/one_gadget against the
   *provided* libc; menu-driven add/edit/delete/show note app → heap, technique picked by the
   provided libc's version (tcache poisoning ≥2.27, safe-linking ≥2.32, no hooks ≥2.34).
6. **Handle the CTF-only obstacles.** Seccomp (`seccomp-tools dump ./chall`) restricting syscalls
   → open/read/write ROP instead of `system`, or an ORW shellcode (`open("/flag"); read; write`).
   Read-only flag perms → the SUID flag-reader on the box is the second stage.
   Forking server → canary is constant across children; brute it byte-by-byte if you have a crash
   oracle.
7. **Iterate remotely like a scientist.** Run the same script ≥ 20 times against remote; a
   1-in-N success rate usually means an unhandled alignment (`movaps` — add one `ret`) or a leak
   parse that occasionally grabs the wrong slot (anchor `recvuntil` tighter).

## Gotchas
- **Wrong libc is the #1 remote-only failure** — if the handout ships a libc, use *it*, not
  libc-database guesses. Verify locally: `./libc.so.6` prints its version banner.
- **`%n` writes need writable target memory** — Full RELRO kills GOT overwrites; pivot to a saved
  return address or a function pointer the app uses (menu structs often have one).
- **Format-string payload too long for the read size** — keep it under the `fgets` limit by writing
  two bytes at a time (`%hn`) and packing addresses at the end.
- **Stack misalignment on remote only** (`movaps`) — insert a single `ret` gadget before the call
  that crashes; see `exploit-pwn-chain`.
- **`system("/bin/sh")` broken by seccomp or missing shell** — fall back to `execve` ROP or ORW;
  check allowed syscalls *before* choosing the final stage.
- **Interactive menus desync silently** — one `sendline` where a `sendlineafter` was needed
  shifts every later read; debug with `context.log_level='debug'` and match on exact prompts.

## Verify success
`cat /flag` (or the shell) from the *remote* service, reproducibly — the script lands the flag
in consecutive remote runs, not once by luck. Record the leaked libc symbol and offset used.

## References
Chains and glibc-version heap table: `exploit-pwn-chain` (+ its `cheatsheet.md`); bug hunting:
`reverse-eng-binary-triage`, `exploit-memory-corruption`; pwntools docs (`FmtStr`,
`fmtstr_payload`); seccomp-tools. Triage via `ctf-methodology`.
