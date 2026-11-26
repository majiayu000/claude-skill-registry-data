---
name: snx-service
description: "Implement or fix a high-level-emulated Switch service or device (IPC commands, nvdrv ioctls, shared memory) so it answers the way the console does, as the game's SDK code expects. Use when a log shows an unimplemented command, a game stalls waiting on a service, an svcBreak follows a service call, or when adding audio, input, video or system services."
---

# Services

## Where

- Interfaces are declared, not hand-dispatched: each service file has a `.swipc` beside it (in `src/nx/`:
  `hle/services/acc.c` and `hle/services/acc.swipc`, `hle/services/network/bsd.swipc`, `hle/filesystem/fs.swipc`), in
  SwIPC's language. `docs/IPC.md` has the language, the layout the generator applies and the C side.
  `tools/swipc/swipc.c` generates `<file>.swipc.h` and `<file>.swipc.inc` into `build/<preset>/src/nx/snx_hle-swipc/`.
  The service's C file includes the `.inc`, which has each handler's exact prototype; other files include the `.h`.
- A command's handler is `static int nn_ns_IFoo_Command(SvcObj* self, inputs..., outputs...)`: scalars by value,
  structs as `const T*`, buffers as `IpcBuf` (address, size), objects `SvcObj*` in and `SvcObj**` out, handles `u32`
  in and `u32*` out. Outputs start zeroed. It returns 0 or `RC(module, description)`, and a failure answers no
  outputs.
- `I_new(data_size)` makes an object of interface `I` with zeroed state in `o->data`; `I_register(ctor)` registers
  a constructor under the `.swipc`'s `is` names (`services.c`, or the service's own init). `@stub` answers success
  and zeros without a handler; `@unsorted` keeps a command's raw arguments in declaration order, for the few the SDK
  lays out that way; `@fallback(fn)` picks what answers undeclared commands (`stub_ok`, which logs, by default).
  `types.swipc` comes first in every `snx_swipc` list of the runtime's files, and in a test's that uses its types.
- `src/nx/hle/kernel/ipc.c`: HIPC/CMIF parsing, replies, sessions, domains, the registry. `services_int.h`
  declares what the service files share.
- In `services/`: `hid.c` (input and its shared memory), `vi.c` (display, binder), `nvdrv.c` (nvhost devices),
  `audren.c` (`audren_update`), `pl.c` (shared fonts), `misc.c` (the small services). `src/nx/hle/filesystem/fs.c`,
  and `src/nx/gpu/video/` (host1x channels, NVDEC, VIC).

## Procedure

1. **Find the command.** `-v` logs every call: `grep "IAudioOut cmd" run1.log | sort | uniq -c` (the object's
   name is the interface's, `nn::audio::detail::IAudioOut`, but bsd's and ldr's carry the service's, `bsd:u` and
   `ldr:ro`). An undeclared command is logged by the interface's fallback, the first three times: `[undeclared] I cmd N
   -> ok` from `stub_ok` (success with no outputs: for a command that gives an object or a handle the game ends up
   calling through null), `[unknown]` from `ipc_unknown`, `[not implemented]` from bsd's, nothing from `quiet_ok`.
   `[undeclared] NAME cmd N -> ok` also comes from sm's stand-in for a service the runtime doesn't have. A
   `[bad request] I cmd N: pid .., A .., ... -> InvalidCmifRequest` means the declaration doesn't match what the SDK
   sends (step 2): the game gets an error, and often aborts on it. `[bad request] ... -> InvalidNumInObjects` is the
   same for a domain request's objects, and `... takes objects, on a session that isn't a domain -> NotSupported` a
   command declared with objects called on a plain session.
   Switchbrew's page for the service gives the command's name and layout; libnx's client struct shows the raw
   layout and buffer attributes.
2. **Declare it** in the `.swipc` with the console's full signature, inputs and outputs the runtime ignores
   included, and the exact buffer attributes (they decide the A/B/X/C list). Never write offsets by hand: the
   generator sorts raw arguments by alignment, ascending, as the SDK does (check a mixed-alignment command against
   the SDK's `InRawArgumentInfo<size, alignment, offset>` templates: a few use declaration order, `@unsorted`).
   `pid` is one 8-byte slot (write SwIPC's `(u64, pid)` as `pid`), `aruid` a command's ClientAppletResourceUserId
   slot.
3. **Read the caller.** The game's SDK wrapper (`nn::audio::...`, `nn::hid::...`) shows what it reads from the
   reply and what it does with it. `tools/symbols.py` and `tools/disasm.py` on the wrapper, or the `sdk-scout` agent.
   A field the SDK reads and the runtime never writes is a bug even when nothing crashes yet.
4. **Answer like the console** in the handler. Same result codes, same output values, same handle and event
   behavior. Where the console times something (audio buffers, vsync), keep the timing: games sync against it.
5. **Mind the threads.** Service calls come from game threads, which run in parallel on the host. State shared
   between calls takes a lock (`PMutex`, `pm_lock`), events go through `kevent_signal`. An object whose every
   command needs a lock gets a dispatcher of its own around `I_dispatch` (fs.c's `file_disp`, `dir_disp` and
   `fs_disp`, ldr.c's `ro_dispatch`), and is made with `svcobj_new` and that dispatcher, not `I_new`.
6. **Verify** with the scene that uses it (`snx-run`), and grep the `-v` log to see the new answers. A test that
   includes a service's C file generates that service's dispatchers itself (`snx_swipc` in `tests/CMakeLists.txt`).

## References and licensing

Switchbrew documents commands and structures. Ryujinx (MIT) is the best behavioral reference and can be ported
from with its notice. yuzu and its forks (GPL-2.0-or-later or GPL-3.0) can be ported too, ScarletNX being
GPL-3.0-or-later: keep their copyright lines and say where the code came from. GPL-2.0-only code can't be
(Atmosphère is read, never ported).

## Known traps

- Reporting more than one npad style for a controller makes the SDK assert in `GetVibrationDeviceHandles`.
- An `IAudioOut` that never releases buffers stalls CRI movies after a few frames. The released-buffer array must
  be cleared first, because the SDK reads every slot.
- `WaitSynchronization` with zero handles is legal (a plain sleep).
- nvhost syncpoint ids above 127 overflow NvRmStream's tables: allocate with `syncpt_alloc()`.
