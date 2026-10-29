---
name: snx-service
description: "Implement or fix a high-level-emulated Switch service or device (IPC commands, nvdrv ioctls, shared memory). Make it answer as the console does, as the SDK code of the game expects. Use it when a log shows an unimplemented command, or a game stalls and waits on a service. Use it also when an svcBreak follows a service call, or when you add audio, input, video or system services."
---

# Services

## Where

- A `.swipc` file declares the interfaces, and no code dispatches them by hand. Each service file has a `.swipc`
  beside it, in the language of SwIPC. Examples in `src/nx/` are `hle/services/acc.c` with
  `hle/services/acc.swipc`, `hle/services/network/bsd.swipc` and `hle/filesystem/fs.swipc`. `docs/IPC.md` has the
  language, the layout that the generator applies, and the C side.

  `tools/swipc/swipc.c` generates `<file>.swipc.h` and `<file>.swipc.inc` into
  `build/<preset>/src/nx/snx_hle-swipc/`. The C file of the service includes the `.inc`, which has the exact
  prototype of each handler. Other files include the `.h`.
- The handler of a command is `static int nn_ns_IFoo_Command(SvcObj* self, inputs..., outputs...)`. Scalars come by
  value, structs as `const T*` and buffers as `IpcBuf` (address, size). Objects are `SvcObj*` in and `SvcObj**` out.
  Handles are `u32` in and `u32*` out. Outputs start zeroed. It returns 0 or `RC(module, description)`, and a failure
  answers no outputs.
- `I_new(data_size)` makes an object of interface `I`, with zeroed state in `o->data`. `I_register(ctor)` registers a
  constructor under the `is` names of the `.swipc` (in `services.c`, or in the init of the service). `@stub` answers
  success and zeros without a handler. `@unsorted` keeps the raw arguments of a command in declaration order, for the
  few commands that the SDK lays out that way.

  `@fallback(fn)` selects the function that answers undeclared commands. The default is `stub_ok`, which logs.
  `types.swipc` comes first in every `snx_swipc` list of the runtime files. It also comes first in the list of a test
  that uses its types.
- `src/nx/hle/kernel/ipc.c` has the HIPC/CMIF parser, the replies, sessions, domains and the registry.
  `services_int.h` declares what the service files share.
- In `services/` are `hid.c` (input and its shared memory), `vi.c` (display, binder), `nvdrv.c` (nvhost devices),
  `audren.c` (`audren_update`), `pl.c` (shared fonts) and `misc.c` (the small services). Also see
  `src/nx/hle/filesystem/fs.c`, and `src/nx/gpu/video/` (host1x channels, NVDEC, VIC).

## Procedure

1. **Find the command.** `-v` logs every call. Use `grep "IAudioOut cmd" run1.log | sort | uniq -c`. The name of the
   object is the name of the interface (`nn::audio::detail::IAudioOut`). But the objects of bsd and ldr have the name
   of the service (`bsd:u` and `ldr:ro`).

   The fallback of the interface logs an undeclared command the first three times:
   - `[undeclared] I cmd N -> ok` comes from `stub_ok`. It gives success with no outputs. For a command that gives an
     object or a handle, the game then calls through null.
   - `[unknown]` comes from `ipc_unknown`.
   - `[not implemented]` comes from the fallback of bsd.
   - `quiet_ok` logs nothing.

   `[undeclared] NAME cmd N -> ok` also comes from the stand-in of sm for a service that the runtime does not have.
   A `[bad request] I cmd N: pid .., A .., ... -> InvalidCmifRequest` means that the declaration does not agree with
   what the SDK sends (step 2). The game gets an error, and often aborts on it.
   `[bad request] ... -> InvalidNumInObjects` is the same error for the objects of a domain request.
   `... takes objects, on a session that isn't a domain -> NotSupported` shows a call on a plain session to a command
   that declares objects.

   The Switchbrew page for the service gives the name and layout of the command. The client struct of libnx shows the
   raw layout and the buffer attributes.
2. **Declare it** in the `.swipc` with the full signature of the console. Include the inputs and outputs that the
   runtime ignores. Give the exact buffer attributes, because they decide the A/B/X/C list.

   Never write offsets by hand. The generator sorts raw arguments by alignment, from the smallest to the largest, as
   the SDK does. Check a command with mixed alignment against the `InRawArgumentInfo<size, alignment, offset>`
   templates of the SDK. A few commands use declaration order (`@unsorted`). `pid` is one 8-byte slot (write the
   `(u64, pid)` of SwIPC as `pid`). `aruid` is the ClientAppletResourceUserId slot of a command.
3. **Read the caller.** The SDK wrapper of the game (`nn::audio::...`, `nn::hid::...`) shows what it reads from the
   reply, and what it does with it. Use `tools/symbols.py` and `tools/disasm.py` on the wrapper, or the `sdk-scout`
   agent. A field that the SDK reads and the runtime never writes is a bug, also when nothing crashes yet.
4. **Answer like the console** in the handler. Give the same result codes, the same output values, and the same
   handle and event behavior. Where the console times something (audio buffers, vsync), keep the same times. Games
   sync against them.
5. **Be careful with threads.** Service calls come from game threads, which run in parallel on the host. State that
   calls share must have a lock (`PMutex`, `pm_lock`). Events go through `kevent_signal`.

   Some objects need a lock for every command. Give such an object its own dispatcher around `I_dispatch`
   (`file_disp`, `dir_disp` and `fs_disp` in fs.c, `ro_dispatch` in ldr.c). Make it with `svcobj_new` and that
   dispatcher, not with `I_new`.
6. **Verify** with the scene that uses it (`snx-run`). Grep the `-v` log to see the new answers. A test that includes
   the C file of a service generates the dispatchers of that service itself (`snx_swipc` in `tests/CMakeLists.txt`).

## References and licenses

Switchbrew documents commands and structures. Ryujinx (MIT) is the best reference for behavior. You can port from it
with its notice. You can also port from yuzu and its forks (GPL-2.0-or-later or GPL-3.0), because ScarletNX is
GPL-3.0-or-later. Keep their copyright lines and say where the code came from. You cannot port GPL-2.0-only code:
read Atmosphère, but never port it.

## Known traps

- If the runtime reports more than one npad style for a controller, the SDK asserts in `GetVibrationDeviceHandles`.
- An `IAudioOut` that never releases buffers stalls CRI movies after a few frames. Clear the array of released buffers
  first, because the SDK reads every slot.
- `WaitSynchronization` with zero handles is legal (a plain sleep).
- nvhost syncpoint ids above 127 overflow the tables of NvRmStream. Allocate them with `syncpt_alloc()`.
