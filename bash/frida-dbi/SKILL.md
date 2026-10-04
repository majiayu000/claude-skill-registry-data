---
name: frida-dbi
description: "Frida dynamic binary instrumentation for RE and security research: spawn/attach, Interceptor hooks, NativeFunction, Memory scanning, Stalker tracing, gadget modes, anti-anti-debug bypass patterns, il2cpp/mono bridges for games, OPSEC of frida-server, and reliability discipline for long sessions. Local stack: frida 17.17.0 + frida-tools 14.10.4 via pip."
version: 1.0.0
license: GPL-3.0-or-later
metadata:
  package: unleash-skills
  author: NetVar1337/unleash
  category: re
  triggers:
    - "frida"
    - "interceptor"
    - "stalker"
    - "dynamic instrumentation"
    - "hook"
---

# Frida dynamic instrumentation

Local setup (verified in `tool-index.md`): frida 17.17.0 / frida-tools
14.10.4 installed via pip. The `frida` CLI scripts live in
`C:\Users\Admin\AppData\Local\Python\bin\` — not on PATH; call
`python -m frida_tools.repl` (or `...repl -U` for USB/Android) or add that
bin dir to PATH.

## Session basics

```bash
python -m frida_tools.repl -f C:/target/game.exe -l hook.js --runtime=v8   # spawn
python -m frida_tools.repl -n game.exe -l hook.js                          # attach
python -m frida_tools.repl -U -f com.vendor.app -l hook.js                 # android
```

Spawn > attach for early code (loaders, anti-debug init). `-f` suspends at
entry; call `resume()` from the script or `--pause` flows when you must hook
before the first instruction.

## Interceptor (the 90% tool)

```js
const f = Module.getExportByName(null, "ws2_32!send");   // null = search all modules
Interceptor.attach(f, {
  onEnter(args) { this.buf = args[1]; this.len = args[2].toInt32(); },
  onLeave(rv) {
    if (this.len > 0) send({tag:"send", data: hexdump(this.buf, {length: Math.min(this.len, 256)}).toString()});
  }
});
```

- `Module.getExportByName(null, name)` resolves across loaded modules; for
  unexported targets compute the address first (`pattern-scanner` in-process:
  `Memory.scan` on module ranges) and `Interceptor.attach(ptr, {...})`.
- Calling natives: `new NativeFunction(addr, retType, argTypes)`; keep
  `ABI` defaults (Windows x64 = MSVC ABI).
- Replace vs attach: `Interceptor.replace` swaps implementation (use for
  neutering, e.g. anti-debug); `attach` preserves behavior — prefer attach
  when the target must keep working.
- Always wrap per-hook logic in try/catch and keep hooks idempotent: a hook
  that throws poisons every subsequent call through that site.

## Memory & module APIs

- `Memory.scan(base, size, "48 8B ?? 05")` — live pattern validation before
  committing a signature to the DB (`offset-dumper` pipeline step).
- `Process.enumerateModules()`, `Module.load()`, `Process.findRangeByAddress`
  for VAD-ish views usermode-side.
- `Memory.readPointer/readByteArray/writeU…` + `Memory.protect` for patching;
  scope writes behind flags — a stray patch survives you.

## Stalker (tracing, expensive)

```js
Stalker.follow(threadId, {
  events: { call: true, ret: false, exec: false },
  onReceive(events) { /* parse binary array; batch-send, never per-event send() */ }
});
```

- Follow one thread at a time; `exec: true` floods (millions/s).
- Use for: recovering dispatch tables (follow the packet-handler thread and
  record call targets), locating checks (follow until a "bad" result, bisect
  the trace), coverage-guided triage.
- `Stalker.unfollow` + `Stalker.flush()` on teardown; leak a follow and the
  process dies with it.
- Cheaper alternative first: `frida-trace` with `-i`/`-a` module!function
  filters, or Interceptor-only call maps.

## Anti-anti-debug / analysis-resistance patterns

| Check | Bypass shape |
|---|---|
| `IsDebuggerPresent` / PEB.BeingDebugged | `Interceptor.replace` → return 0, or write PEB byte once (`teeb` walk from `gs:[0x60]`) |
| `NtQueryInformationProcess` (ProcessDebugPort/Flags/ObjectHandle) | hook and rewrite the info buffer onLeave |
| `CheckRemoteDebuggerPresent` | same via API hook |
| Timing (`rdtsc`-via-cpuid gates, `GetTickCount` deltas) | hook `GetSystemTimeAsFileTime`/`QueryPerformanceCounter` families and normalize; cpuid-based gates need Stalker or a patched branch |
| `NtSetInformationThread(ThreadHideFromDebugger)` | hook and swallow |
| Hardware bp checks (`GetThreadContext` Dr registers) | rewrite CONTEXT onLeave |
| EnumerateLoadedModules / module scans for frida itself | see OPSEC below |

Apply bypasses narrowly (one check at a time, verified) — wholesale
"anti-anti" scripts break games/apps and destroy evidence of *which* check
fired. For deep debugger-based work switch to `x64dbg-anti-debugger`.

## Games (mono / il2cpp)

- Unity mono: enumerate `mono.dll` exports (`mono_get_root_domain`,
  `mono_thread_attach` first!), walk assemblies via `mono_assembly_foreach`
  NativeFunctions; or use community `frida-il2cpp-bridge` for il2cpp games
  (npm-installable; pairs with `offset-dumper`'s il2cpp pipeline for static
  ground truth).
- Dump vtables/methods at runtime when static metadata is encrypted —
  often the only stable source on protected builds.

## Gadget & server modes

- **frida-server (remote/Android)**: run on device, connect `-U`/`-H`.
  OPSEC: default name/port is a first-order IOC — rename binary, non-default
  port, bind localhost + adb forward (`adb forward tcp:PORT tcp:PORT`).
- **gadget** (embedded in the app you own/build): config modes
  `listen/connect/script/directory`; use `script` for fully offline
  instrumentation with zero server artifacts.

## Reliability discipline (long sessions)

1. One concern per script version; reload (`-l` again / `%reload`) after
   edits rather than stacking variants.
2. Batch `send()` — coalesce per 50 ms or per N events; per-event RPC kills
   throughput and can desync the REPL.
3. Save state: dump captured structures to files via `rpc.exports` +
   host-side writer; don't keep everything in JS heap.
4. Teardown: unfollow Stalkers, detach Interceptors (`Interceptor.detachAll`
   or per-listener handles) when the mission ends — leave a target running
   with hooks and your next attach inherits the mess.
5. Record: target build + module hashes in every capture log header
   (`windows-internals` provenance rules apply).

## Pair with

`offset-dumper` (live validation + encrypted-pointer recovery),
`network-protocol-re` (plaintext hooks at send/EncryptMessage),
`js-reverse`/`mobile-reverse` (ecosystem-specific flows),
`x64dbg-anti-debugger` (debugger-side counterpart),
`malware-analysis` (sample triage), `edr-bypass-re` (defender-side hooks
being studied).
