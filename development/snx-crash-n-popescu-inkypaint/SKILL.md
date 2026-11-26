---
name: snx-crash
description: "Take a ScarletNX crash report, svcBreak or hang from the log to the mechanism that causes it, using the symbolizer and disassembler on the game's code. Use when the game crashes (signal 11 or 7), calls svcBreak or fatal, hangs, or when a log shows \"*** Crash\". Also for corrupted data showing up in game structures."
---

# Crash to mechanism

The goal is the mechanism: which instruction read what, where the bad value came from, and what the runtime did
that real hardware wouldn't. A fix without that is a guess.

## 1. Read the report

```
*** Crash (signal 11) at host pc=0x7f..., access to 0x7f... (game address cf8617f8) ***
  inside the recompiled code of game function cf195f0 (+41b on the host)
  thread 131 ()
  x0 = ... x30 = ...
  pc=cf34380 lr=cf1aacc sp=... fp=...
  pc <NvDdkVicExecuteSync+320>  lr <NvRmStreamFlushSync+1c>
   #0 cf1aacc <NvRmStreamFlushSync+1c>
  code ADDR: words...
  mem xN ADDR: what the register points at
```

- **game function** is the function the crash is in. `pc` is the last call site the runtime recorded, often in the
  caller, so start from the game function.
- **game address** is the guest address that faulted. Find which register (or register plus offset) it is: that is
  the bad pointer.
- A crash in the runtime itself prints `in the runtime itself (exe offset +OFF)`. The presets build with symbols:
  `addr2line -e build/scarletnx -f -C -i 0xOFF` (the build that was deployed).
- `svcBreak` means the SDK's own assert failed. The interesting code is the caller's check, just before the
  `svc #0x26`.

## 2. Name and disassemble

```bash
tools/symbols.py work/<Game> ADDR...                         # the crash report's game addresses
tools/disasm.py work/<Game> NvRmStreamFlushSync              # a whole function
tools/disasm.py work/<Game> START END                        # a range
```

Both read the modules through the recompiler's own loader (`build/scarletnx --dump-modules`, or the binary
`SNX_SCARLETNX` names), so the build must exist. The dump is cached per game folder in `~/.cache/scarletnx/module-dumps`.

Find the faulting instruction (the load or store whose address is the game address) and walk back to where its
base register came from. Every value is either loaded from memory (from where, written by whom), passed in, or
computed. Keep going until you reach something the runtime provided: an IPC answer, an ioctl result, shared memory
the runtime writes, a buffer a device filled.

Large functions: disassemble only the part you need. Use the `crash-triage` agent to do the walk in its own context
when it takes many steps, and the `sdk-scout` agent to work out what an SDK function expects.

When it reproduces, look at it live. Start the game with `-S` (or `-s`, to stop before the runtime starts), then use
the `scarletnx` MCP server's GDB tools: `gdb_attach` with the game, `gdb_threads` (every host thread, and each guest
thread's state and guest pc), `gdb_guest` (a guest thread's registers and guest backtrace) and `gdb_command`
(`thread apply all bt` shows which lock each runtime thread waits on, for a hang). A crash stops at `crash_report`.
Add `--gdb_jit=1` when the frames are in code the JIT compiled, at the cost of a stop per compile. The stub takes one
connection per run.

## 3. Common shapes

| Shape | Where to look |
| --- | --- |
| A pointer holds floats (`3f800000...` is 1.0) or other data | Memory reused or written by something else: an out-of-bounds write by the game because the runtime gave it an out-of-range value (the 128-entry syncpoint table), a GPU write-back (render target, compute, DMA) landing on memory the game reused, or a race between game threads |
| `svcBreak` right after a service call | The service answered something real hardware never does. Read the assert's condition |
| A wait that never ends (`threads.txt`) | An event the runtime never signals, or a release the game waits for (audio buffers) |
| Works once, crashes on the second movie, scene or submit | State the runtime keeps between uses: fixed ids, unreset buffers |
| Access to `(nil)` with a game address near `ffff8...` | A guest null or garbage pointer translated: look at the register, not the host address |

## 4. Confirm before fixing

Write down the chain from the runtime's behavior to the faulting instruction, with the addresses you read. Then fix
the runtime's side so it behaves like the console. Verify with repeat runs (`snx-run`), with the crash rate before and
after in the commit message. If the chain has a link you inferred rather than read, say so in the commit.
