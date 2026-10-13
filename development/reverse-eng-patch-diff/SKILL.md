---
name: reverse-eng-patch-diff
description: >
  Turn a vendor security patch into a working N-day: diff the patched and unpatched binaries,
  read the newly added safety checks back to a bug class, then write a PoC that crashes the
  unpatched build. Load for a CVE with a patch but no public PoC, Patch Tuesday triage
  (ntoskrnl / win32k / afd.sys / clfs.sys), Linux LTS backport analysis, bindiff / ghidriff /
  Diaphora workflows, patch diff, binary diffing to find what a patch fixed.
domain: reverse-engineering
type: technique
stability: learning
modes: [pentest, bugbounty]
severity: high
cwe: [CWE-787, CWE-362, CWE-416, CWE-190, CWE-200]
tools: [bindiff, ghidriff, diaphora, radiff2, ghidra, ida, symchk]
schema_version: 1
---

# N-day patch diffing to exploit

## When it applies
A vendor shipped a fix but no details: a CVE advisory says "out-of-bounds write in component
X" with no PoC, a Patch Tuesday drop needs triage, or a Linux distro backport may be
incomplete on some branch. The goal is to recover *what the patch fixed* and prove the bug
against the unpatched build. Weaponizing an N-day is only legitimate against in-scope,
authorized targets (a program that accepts it, an engagement, your own lab) — confirm with
`tradecraft-scope-roe` and record it in `scope.txt`.

## Why it works
A security patch is a confession. The added bounds check, lock, zeroing, or refcount tells you
exactly which invariant the old code violated — and the unpatched binary still violates it.
Diff the two builds, filter to functions that changed *moderately* (identical = untouched,
completely different = new feature), and the fix pattern maps almost one-to-one onto a bug
class you can then trigger.

| The patch adds... | Likely bug class |
|---|---|
| `if (a + b < a)` / `__builtin_add_overflow` | integer overflow |
| `KeAcquireSpinLock` / `mutex_lock` | race condition (TOCTOU / double-free) |
| `if (idx >= MAX)` / `if (len > buf_size)` | OOB read / write |
| `RtlZeroMemory` / `memset(struct, 0, ...)` | uninitialized-memory info leak |
| `InterlockedDecrement` + refcount check | UAF / refcount error |
| `ProbeForRead` / `ProbeForWrite` / `access_ok` | unvalidated user-mode pointer |
| `SeAccessCheck` / capability check | missing authorization |
| removed / tightened IOCTL codes | attack-surface reduction — study the old interface |

## Method
1. **Get the before/after binaries.** Windows: download the MSU for build N (patched) and N-1
   from the Microsoft Update Catalog, unpack with `expand.exe`. Linux: `apt download` the two
   kernel/package versions and `dpkg-deb -x` / `rpm2cpio` them. Third-party software: grab the
   N-1 and N installers. Exact commands per platform in [`cheatsheet.md`](cheatsheet.md).
2. **Align symbols.** Windows: pull PDBs from the Microsoft symbol server with `symchk`.
   Linux: matching dbgsym / debuginfo, and `extract-vmlinux` to turn `vmlinuz` back into an
   ELF. No symbols for one side → migrate them from the nearest version before diffing.
3. **Diff.** Feed both binaries to BinDiff, ghidriff, or Diaphora:
   ```bash
   ghidriff ntoskrnl_old.exe ntoskrnl_new.exe -o diff_out/
   bindiff --primary=old.BinExport --secondary=new.BinExport --output_dir=./bindiff_out/
   ```
4. **Locate the change.** Filter to functions with similarity ≈ 0.5–0.95. Read what was
   *added*: new `if` guards, new loop bounds, new locks — and what was *deleted* (removed code
   is a clue too). Map the pattern through the table above to a bug class; before/after
   pseudocode pairs are ideal LLM input for a root-cause hypothesis (patterns in
   `cheatsheet.md`).
5. **Write and verify the PoC** against the *unpatched* build:
   - integer overflow → boundary values (`0xFFFFFFF0 + 0x100`) so the wrap yields a small
     allocation but a large copy;
   - race → threads hammering two syscalls on one object (close + IOCTL concurrently);
   - UAF → spray → free → reclaim → use;
   - OOB → drive length/index just past the boundary the new check now guards.
   Success criteria are symmetric: the PoC crashes the unpatched build reliably and runs clean
   on the patched one.

## Gotchas
- **Mitigation ≠ fix.** Added CFG/XFG instrumentation (`_guard_xfg_dispatch_icall_fptr`) is
  hardening, not the bug fix — keep looking.
- **Compiler noise fakes changes.** Inlining decisions, switch-table reordering, and PGO make
  unchanged source look different — diff N against N-1 (same toolchain), never across major
  versions, and read control/data flow rather than token-level diffs.
- **Alignment failure.** If overall matched ratio < ~90%, stop: wrong pairing, different
  compiler, or rebase mismatch — fix the inputs before reading results.
- **A patch may shrink the blast radius, not fix the bug** — the same root cause may still be
  reachable via another path (one bug, multiple harvests).
- **A crash on the unpatched build alone proves nothing** — environment faults look identical;
  you need the patched build clean *and* a stated root cause before claiming the CVE
  (`reporting-triage-validation`).
- **Redact in write-ups** — target hostnames, internal IPs, usernames become placeholders.

## Verify success
You can name the function, the added check, and the violated invariant; your PoC crashes the
unpatched build (BSOD/panic/KASAN naming the expected class) within a predictable window and
exits cleanly on the patched build. That pairing — plus the root cause — is the reproducible
N-day.

## References
Microsoft Update Catalog & MSRC CVRF API; BinDiff / ghidriff / Diaphora docs;
`reverse-eng-binary-triage`, `exploit-poc-development` in this library.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
