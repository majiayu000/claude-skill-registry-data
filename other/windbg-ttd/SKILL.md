---
name: windbg-ttd
description: "WinDbg workflows for RE and driver research: KDNET kernel debugging setup, symbol discipline, crash-dump triage (!analyze, bugcheck semantics incl. PatchGuard 0x109), driver debugging (breakpoints on load, IRP/device trees), live kernel inspection, TTD (Time Travel Debugging) when WinDbgX is available, and cdb automation. Local: classic suite at Windows Kits\\10\\Debuggers\\x64 (windbg/cdb/kd/ntsd)."
version: 1.0.0
license: GPL-3.0-or-later
metadata:
  package: unleash-skills
  author: NetVar1337/unleash
  category: re
  triggers:
    - "windbg"
    - "kdnet"
    - "kernel debugging"
    - "time travel"
    - "ttd"
    - "crash dump"
    - "bugcheck"
---

# WinDbg & TTD

Local reality (verified): classic debuggers at
`C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\` — `windbg.exe`,
`cdb.exe`, `kd.exe`, `ntsd.exe`. WinDbgX (Store) is **not** installed —
TTD and JS scripting need it: `winget install Microsoft.WinDbg`.
Put the directory on PATH for the session or call by full path.

## Symbols (do this first, every box)

```
set _NT_SYMBOL_PATH=srv*C:\symbols*https://msdl.microsoft.com/download/symbols
```

`.symfix; .reload` in-session. Unresolved `nt!` symbols = everything after
this is guessing. For third-party drivers: private PDBs when you have them,
else `!dh`/raw disassembly (see `ida-reverse` for the deep static pass).

## KDNET kernel debugging (VM or 2nd box)

Target (admin):
```
bcdedit /debug on
bcdedit /dbgsettings net hostip:<debugger-ip> port:50000 key:<1.2.3.bugkey>
```
Debugger: `windbg -k net:port=50000,key=<same key>,target=<target-ip>`.
Break at boot with `bcdedit /bootdebug on` (bootmgr) when driver init is the
target. VMs: Hyper-V/KVM both carry KDNET fine; attach KDNET *before*
loading test drivers (see the bring-up loops in `kernel-dev`,
`stealth-hypervisor`).

## Command economy

| Question | Command |
|---|---|
| What crashed | `!analyze -v` |
| Context of current thread | `.thread` / `!thread`, `k`, `kv` (frame pointers), `ub` (before-fault disasm) |
| Process context switch | `!process 0 0` → `.process /i <eproc>` (invasive) / `/p` (non-invasive) |
| Driver loaded where | `lm t n`, `!drvobj <drv> 7`, `!devobj`, `!devstack` |
| IRP story | `!irpfind`, `!irp <addr>` |
| Pool forensics | `!pool <addr>`, `!poolused 2`, `!poolfind <tag>` |
| Memory/PTE | `!address <addr>`, `!pte <addr>`, `!vad` |
| Object manager | `!object \Device`, `!handle <addr> f` |
| Break on driver load | `sxe ld:mydriver.sys` then `bu mydriver!DriverEntry` |
| Data access break | `ba r4 <addr>` (hardware bp — survives where `bp` code patches would be seen) |
| Search physical/virtual | `s -a 0 L?7fffffff "pattern"` / `!search` on dumps |

`bp` on module!symbol before load → use `bu` (deferred). Set
`.reload /f mydriver.sys` after load if symbols lag.

## Crash dump triage (driver dev loop)

1. Configure: `Sysdm.cpl → Startup and Recovery → Kernel/Complete dump` +
   keyboard-initiated crash (Ctrl-ScrollLock registry) for *deliberate* trips.
2. Open: `windbg -z C:\Windows\MEMORY.DMP` → `.symfix; .reload; !analyze -v`.
3. Read the bugcheck like an engineer:

| Code | Meaning for your work |
|---|---|
| `0x109` CRITICAL_STRUCTURE_CORRUPTION | PatchGuard caught a modification — identifies *what* (`Parameter 1/4` type) → your SSDT/IDT/MSR/static-hook just failed; PG does **not** catch callback-array DKOM (see `kernel-callbacks`) |
| `0x50` / `0xA` | bad memory ref at IRQL — usually a dangling pointer/IRQL violation in your driver |
| `0x7E` | unhandled exception in driver |
| `0x133` DPC_WATCHDOG_VIOLATION | DPC >100 µs: your DPC loops; also seen when spinlock-held too long |
| `0x1A` MEMORY_MANAGEMENT | pool corruption — enable Driver Verifier special pool and reproduce |
| `0x124` WHEA | hardware/hypervisor instability — suspect your VMX code before the hardware |

4. Driver Verifier on the target driver (`verifier /standard /driver
   mydrv.sys`): special pool catches overflows at the *allocation*, not the
   crash — most kernel 0-day candidates surface here (`windows-driver-0day`
   flow).
5. Second-chance discipline: on a live KDNET box you rarely need dumps —
   break in (`Ctrl+Break`), inspect live state, continue.

## TTD (Time Travel Debugging) — usermode

TTD records an execution trace you can run **backwards** (`g-`, `p-`, `t-`) —
the killer feature for: anti-debug logic (set bp on the *result* of the check
and walk back to the branch), races (replay the exact interleaving),
corrupted-then-crashed buffers (watch the write that corrupted it:
`ba w4 <addr>` then `g-`).

- Requires WinDbgX: `winget install Microsoft.WinDbg` (TTD engine ships with
  it). cdb classic does not record TTD.
- Record: launch under WinDbgX → `tt record`-style via the UI/`bptrace`;
  heavy — cap the scenario (small repro, narrow window).
- Replay: `windbgx -z trace.run` → `!tt 0`, `g-`, watch `time-travel` menu
  travel (positions `2:3` style), `dx -g $tt` for timeline queries.
- TTD + `ba w4` → backward data-watchpoint is the single highest-value RE
  primitive in this skill. If you catch yourself bisecting a corruption
  manually, you skipped this.

Kernel TTD: not available — the closest analog is a scripted KDNET session
(`cdb -c "...; q"` chains) plus ETW correlation.

## Automation

```
cdb -z dump.dmp -c ".symfix; .reload; !analyze -v; q"
cdb -g -G target.exe -c "bu *server!dispatch; g; k; qd"     // scripted usermode
kd -k net:port=50000,key:... -c "lm t n; q"                  // headless kernel recon
```
Log with `-logo session.log`; scripts via `-cf file.txt`. Batch triage of a
dump corpus becomes a one-liner per file.

## Pitfalls

- Wrong-bit debugger (x86 cdb on x64 target) — pick `Debuggers\x64`.
- Symbols stale after a Windows update: `.reload /f nt` — caches lie across
  build bumps; verify with `lm t n` module timestamps vs target build.
- KDNET behind DHCP changes: hostip changes break the target's settings —
  re-run `bcdedit /dbgsettings`.
- Dump-only sessions can't `ba` (no execution) — data watchpoints need live
  KDNET or TTD.
- VM snapshots + KDNET: resume-from-snapshot sometimes drops the pipe —
  restart the debuggee, not the debugger.

## Pair with

`kernel-dev` / `driver-comm` (what you're debugging), `kernel-callbacks`
(bugcheck-0x109 triage), `windows-driver-0day` (verifier-driven hunting),
`pwndbg-dynamic-analysis` (Linux-side counterpart), `debugger` (general
debugger theory), `frida-dbi` (usermode dynamic counterpart).
