---
name: snx-crash
description: "Take a ScarletNX crash report, svcBreak or hang from the log to the mechanism that causes it. Use the symbolizer and disassembler on the code of the game. Use it when the game crashes (signal 11 or 7), calls svcBreak or fatal, or hangs. Use it also when a log shows \"*** Crash\", or when game structures contain corrupted data."
---

# Crash to mechanism

The goal is the mechanism. Find which instruction read what, and where the bad value came from. Find also what the
runtime did that real hardware would not do. A fix without that is a guess.

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

- **game function** is the function that the crash is in. `pc` is the last call site that the runtime recorded, often
  in the caller. Thus start from the game function.
- **game address** is the guest address that faulted. Find the register (or register plus offset) that gives this
  address. That register holds the bad pointer.
- A crash in the runtime itself prints `in the runtime itself (exe offset +OFF)`. The presets build with symbols. Use
  `addr2line -e build/scarletnx -f -C -i 0xOFF` on the deployed build.
- `svcBreak` means that an assert of the SDK failed. The important code is the check in the caller, immediately
  before the `svc #0x26`.

## 2. Name and disassemble

```bash
tools/symbols.py work/<Game> ADDR...                         # the crash report's game addresses
tools/disasm.py work/<Game> NvRmStreamFlushSync              # a whole function
tools/disasm.py work/<Game> START END                        # a range
```

The two tools read the modules through the loader of the recompiler (`build/scarletnx --dump-modules`, or the binary
that `SNX_SCARLETNX` names). Thus the build must exist. The tools keep the dump in a cache for each game folder, in
`~/.cache/scarletnx/module-dumps`.

Find the instruction that caused the fault: the load or store whose address is the game address. Then go back to the
source of its base register. Every value comes from one of three sources: a load from memory (from where, and which
code wrote it), an argument, or a calculation. Continue until you get to something that the runtime gave. Examples
are an IPC answer, an ioctl result, shared memory that the runtime writes, or a buffer that a device filled.

For large functions, disassemble only the part that you need. When the walk back takes many steps, let the
`crash-triage` agent do it in its own context. Use the `sdk-scout` agent to find what an SDK function expects.

When the crash occurs again, look at it live. Start the game with `-S` (or `-s`, to stop before the runtime starts).
Then use the GDB tools of the `scarletnx` MCP server:
- `gdb_attach` with the game.
- `gdb_threads`: every host thread, and the state and guest pc of each guest thread.
- `gdb_guest`: the registers and guest backtrace of a guest thread.
- `gdb_command`: for a hang, `thread apply all bt` shows which lock each runtime thread waits on.

A crash stops at `crash_report`. Add `--gdb_jit=1` when the frames are in code that the JIT compiled. This causes a
stop for each compile. The stub takes one connection per run.

## 3. Common shapes

| Shape | Where to look |
| --- | --- |
| A pointer holds floats (`3f800000...` is 1.0) or other data | Something else used the memory again, or wrote to it. It can be an out-of-bounds write by the game, because the runtime gave it an out-of-range value (the 128-entry syncpoint table). It can be a GPU write-back (render target, compute, DMA) that lands on memory that the game used again. It can also be a race between game threads. |
| `svcBreak` immediately after a service call | The service gave an answer that real hardware never gives. Read the condition of the assert. |
| A wait that never ends (`threads.txt`) | An event that the runtime never signals, or a release that the game waits for (audio buffers) |
| It works one time, then crashes on the second movie, scene or submit | State that the runtime keeps between uses: fixed ids, buffers that the runtime does not reset |
| Access to `(nil)` with a game address near `ffff8...` | The runtime translated a guest null or garbage pointer. Look at the register, not at the host address. |

## 4. Confirm before you fix

Write down the chain from the behavior of the runtime to the instruction that caused the fault. Include the addresses
that you read. Then fix the side of the runtime so that it behaves like the console. Verify with repeat runs
(`snx-run`). Put the crash rate before and after the fix in the commit message. If the chain has a link that you
inferred and did not read, say so in the commit.
