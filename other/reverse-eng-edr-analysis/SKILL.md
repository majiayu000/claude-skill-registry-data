---
name: reverse-eng-edr-analysis
description: >
  Reverse engineer the EDR/AV on an authorized target host, then evade it — fingerprint the
  product, dump its userland hook table, and assemble a matching bypass stack: ntdll unhooking,
  direct/indirect syscalls (Hell's/Halo's/Tartarus Gate), ETW and AMSI patching, hardware-breakpoint
  Blindside, call-stack spoofing, PPID spoof, sleep masks. Load for "bypass EDR", implant OPSEC
  against CrowdStrike/Defender/SentinelOne, or when telemetry keeps killing your payload. Signals:
  unhook, direct syscall, ETW patch, AMSI patch, ETW-TI, Sysmon evasion, MITRE T1562. Pentest only.
domain: reverse-engineering
type: methodology
stability: learning
modes: [pentest]
severity: high
mitre: [T1562, T1562.001, T1562.006, T1027, T1055]
tools: [windbg, ida, pe-sieve, syswhispers3, api-monitor, sysmon]
schema_version: 1
---

# EDR analysis & evasion (red team)

## When it applies
An authorized red-team / adversary-emulation engagement requires an implant to survive on a host
running a modern EDR, or you're evaluating an EDR's detection coverage against your own
environment. Confirm the engagement covers defense evasion in writing first (`tradecraft-scope-roe`
+ `scope.txt`) — this is pentest-only, never bug bounty. You need the EDR's internals understood
(`reverse-eng-binary-triage` on its DLLs) before you can evade them deliberately.

## Why it works
An EDR is not a black box: it watches four surfaces — userland `ntdll` inline hooks, kernel
callbacks (Ps/Cm/Ob routines), ETW telemetry (notably the Threat-Intelligence provider), and AMSI
scans — and every one of them can be reverse engineered with IDA/windbg and then neutralized with a
matching technique. No single bypass is enough (unhooking doesn't stop ETW; an AMSI patch doesn't
stop syscall hooks), and the order matters: blind the telemetry before you touch memory the
telemetry watches.

## Method
> **Hook survey, unhook/syscall techniques, ETW/AMSI patch bytes, and the OPSEC order:** see
> [`cheatsheet.md`](cheatsheet.md) next to this file.

1. **Fingerprint the EDR on the host** — services, drivers, minifilters:
   `Get-Service | Where-Object {$_.Name -match 'CSAgent|SentinelAgent|elastic-endpoint|ekrn|MsMpEng|sysmon'}`,
   `fltmc filters`. Match against the fingerprint table in the cheatsheet to learn which surfaces
   this product actually uses.
2. **Dump its hook table.** Attach windbg to any injected process, dump the in-memory `ntdll.dll`
   `.text`, and diff it against the clean on-disk `C:\Windows\System32\ntdll.dll` — every divergence
   is a hook. Faster: `pe-sieve64.exe /pid <pid> /shellc 3 /modules 3 /dir hooks_dump`. Follow the
   `jmp` targets to identify the EDR module behind each trampoline.
3. **Pick the bypass combo per surface:**
   - ntdll inline hooks → indirect syscalls with dynamic SSN resolution (Halo's Gate; SysWhispers3
     `--mode jumper`), or HWBP Blindside (no memory writes at all)
   - ETW-TI → patch `EtwEventWrite` head (`xor eax,eax; ret`) — after securing an unhooked
     `NtProtectVirtualMemory` path
   - AMSI (PowerShell/.NET) → patch `AmsiScanBuffer` (`mov eax,0x80070057; ret`) or HWBP variant
   - kernel callbacks → you can't unhook from userland: call-stack spoof and use legitimate trigger
     chains
   - Sysmon ProcessCreate → PPID spoof to `explorer.exe`, avoid remote threads (Event ID 8) and
     hollowing (Event ID 25)
4. **Implement in the implant.** Generate syscall stubs with SysWhispers3
   (`python3 syswhispers.py --preset all --action edit --mode jumper -o syscalls`), add an
   ETW/AMSI patch step, and wrap execution in a call-stack spoofer. For long residency, add a sleep
   mask (Ekko/Foliage) that encrypts the implant's `.text` and zeroes the stack while sleeping.
5. **Validate in a local sandbox copy** of the target stack (trial EDR; Defender + Sysmon with the
   olaf config is a good baseline: `sysmon64.exe -i sysmonconfig.xml`). Run the implant and watch
   Defender AMSI, ETW-TI, Sysmon Event IDs 1/7/8/10/25, and the EDR console — silence on all four
   is the bar.
6. **Deliver quietly** — drop into legitimate software directories, PPID-spoof the launcher, then
   continue the kill chain (lateral movement, persistence) per the engagement plan.

## Gotchas
- **Order is everything** — AMSI → ETW → (indirect-syscall `NtProtectVirtualMemory`) → unhook →
  stack spoof → payload. Unhook first and ETW-TI reports the memory modification before you're
  blind.
- **Direct syscalls are visible from kernel** — a `syscall` instruction executing from your
  implant's `.text` instead of ntdll is itself a signal; use *indirect* syscalls (`jmp` into a
  legitimate ntdll `syscall;ret`).
- **Hell's Gate breaks on hooked ntdll** — the SSN isn't in the first bytes anymore; Halo's Gate
  infers it from unhooked neighbours (SSNs increment sequentially).
- **Spoof during sleep too** — EDRs sample stacks periodically, not just at syscall time.
- **Per-thread hardware breakpoints** — Blindside DRx settings don't propagate; set them on every
  thread, and note `NtSetContextThread` may itself be hooked.
- **Never treat "no alert in one run" as proof** — validate across reboots, sleep cycles, and the
  EDR's cloud lookups.

## Verify success
The implant executes its full action (injection, credential access, C2 callback) on the sandboxed
target stack with zero detections across AMSI, ETW-TI, Sysmon, and the EDR console — reproducibly,
including after a sleep cycle. Report against ATT&CK T1562.001/.006, T1027, T1055.

## References
pe-sieve; SysWhispers3; Hell's/Halo's/Tartarus Gate PoCs; CallStackSpoofer & SilentMoonwalk; Ekko/
Foliage sleep masks; MITRE ATT&CK T1562. Find the EDR's DLLs worth reversing with
`reverse-eng-binary-triage`; the defender's view is `defense-detection-sigma`.

---
_Portions adapted from [reverse-skill](https://github.com/zhaoxuya520/reverse-skill) by zhaoxuya520, MIT License._
