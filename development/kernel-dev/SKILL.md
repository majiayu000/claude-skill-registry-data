---
name: kernel-dev
description: "Use when designing, writing, reviewing, debugging, or hardening Windows WDM/KMDF drivers, IRP and IOCTL paths, PnP/power lifecycles, queues, cancellation, kernel memory, callbacks, or version-pinned ring-0 research. Covers WDK, HVCI, Driver Verifier, KD triage, manual mapping, APC/VAD/DKOM research, and safe teardown; route BYOVD to byovd and user-mode exploitation to exploit-dev."
---

# Kernel development workflow

## Activation

Use when the task involves kernel-mode driver development, kernel shellcode,
manual mapping, injection, rootkit techniques, or any ring-0 code.

## Project scaffolding

Default stack: C or C++ with the WDK. Prefer KMDF for new PnP device and queue work; use WDM when a required contract is genuinely below the framework. Keep private-layout research isolated from the supported driver path.

```
<project>/
├── src/
│   ├── driver.c          # DriverEntry / EvtDriverDeviceAdd
│   ├── device.c          # device creation, ACL, interfaces
│   ├── queue.c           # dispatch, cancellation, completion
│   ├── ioctl.c           # versioned boundary validation
│   ├── pnp-power.c       # start/stop/remove and D-state ownership
│   ├── trace.c           # WPP/IFR diagnostics
│   └── util.c            # checked arithmetic and owned helpers
├── include/              # public request ABI + internal contracts
├── tests/                # malformed IOCTL and lifecycle harnesses
├── research/             # optional, build-pinned private-layout work
├── package/              # INF, catalog, signing inputs
├── <project>.vcxproj
└── README.md              # support matrix and teardown contract
```

## Coding conventions

- Link documented WDK imports normally. Use `MmGetSystemRoutineAddress` only for optional exported APIs with an explicit OS-version fallback; pattern-scanned or unexported routines are unsupported, version-pinned research dependencies.
- Give every allocation a unique, searchable `POOL_TAG`; never reuse another driver's tag to disguise ownership.
- Compile out `DbgPrint` in release builds, but retain WPP/IFR diagnostics suitable for crash correlation.
- Prefer `ExAllocatePool2` with NX `POOL_FLAG_NON_PAGED` or `POOL_FLAG_PAGED`; executable pool requires a documented design reason and a compatible HVCI policy.
- Annotate IRQL and ownership with SAL (`_IRQL_requires_max_`, `_Must_inspect_result_`, `_Post_writable_byte_size_`) and build with `/W4 /WX` plus Code Analysis for Drivers.
- Teardown every queue, callback registration, work item, timer, allocation, interface, symbolic link, and handle through the same ownership path that created it.

## Correctness before stealth

A supported driver must survive malformed requests, concurrent removal, low-resource injection, Driver Verifier, and HVCI before any version-pinned research technique is considered. Prefer KMDF for new device/queue code; choose WDM only when the required contract is not represented by the framework.

### IOCTL boundary contract

Define access deliberately; `FILE_ANY_ACCESS` is not a harmless default:

```c
#define IOCTL_LAB_QUERY CTL_CODE(FILE_DEVICE_UNKNOWN, 0x800, \
    METHOD_BUFFERED, FILE_READ_DATA | FILE_WRITE_DATA)
```

Secure the device with an INF security descriptor, `IoCreateDeviceSecure`, or `WdfDeviceInitAssignSDDLString`. Validate the caller's granted handle access as well as request contents.

| Transfer method | Buffer source | Required handling |
|---|---|---|
| `METHOD_BUFFERED` | `Irp->AssociatedIrp.SystemBuffer` | Check both stack lengths, initialize every output byte, set `IoStatus.Information` to bytes actually written. |
| `METHOD_IN_DIRECT` / `METHOD_OUT_DIRECT` | Small input in `SystemBuffer`, second buffer described by `Irp->MdlAddress` | Validate direction and length; map with `MmGetSystemAddressForMdlSafe(..., NormalPagePriority \| MdlMappingNoExecute)` and handle NULL. |
| `METHOD_NEITHER` | `Type3InputBuffer` / `Irp->UserBuffer` | Only probe inside `__try/__except` in the original requestor context at allowed IRQL, copy into owned kernel memory immediately, and never queue raw user pointers. |

In KMDF use `WdfRequestRetrieveInputBuffer`, `WdfRequestRetrieveOutputBuffer`, and `WdfRequestCompleteWithInformation`; the framework still does not validate semantic fields, integer arithmetic, nested offsets, or versioned request headers. Gate lengths before pointer addition and use checked arithmetic such as `RtlULongLongAdd`.

### IRQL and resource ownership

| Context | Allowed work | Forbidden shortcuts |
|---|---|---|
| `PASSIVE_LEVEL` | pageable code, registry/file Zw calls, waits, device setup/teardown | holding spin locks across calls or attaching indefinitely |
| `APC_LEVEL` or below | documented memory-manager operations that state this limit | touching pageable user buffers after context changes |
| `DISPATCH_LEVEL` | DPC-safe nonpaged state, spin locks, completion enqueue | blocking, pageable code/data, registry/file I/O, user probing |
| ISR/DIRQL | acknowledge hardware, capture minimal state, queue DPC | allocation, complex parsing, waits, or request completion policy |

Pair every reference with a release in the same state machine: `ObReferenceObject`/`ObDereferenceObject`, MDL lock/unlock/free, remove-lock acquire/release, WDF object parentage, rundown acquire/release, and IRP ownership. Use `EX_RUNDOWN_REF` for callbacks that race teardown and `IO_REMOVE_LOCK` in WDM PnP paths. Use work items for PASSIVE-only work; a DPC is not a generic worker thread.

## Driver lifecycle

### WDM path

1. `DriverEntry` initializes immutable state, dispatch entries (`IRP_MJ_CREATE`, `IRP_MJ_CLOSE`, `IRP_MJ_CLEANUP`, `IRP_MJ_DEVICE_CONTROL`, `IRP_MJ_PNP`, and `IRP_MJ_POWER`), `DriverUnload` where legal, and `AddDevice` for PnP drivers.
2. `AddDevice` creates the FDO, attaches with `IoAttachDeviceToDeviceStackSafe`, initializes `IO_REMOVE_LOCK`, clears `DO_DEVICE_INITIALIZING`, and unwinds every partial failure in reverse order.
3. `IRP_MN_START_DEVICE` acquires translated resources only after the lower stack completes. Do not accept I/O until start succeeds.
4. Every dispatch validates `IO_STACK_LOCATION`, acquires the remove lock, sets a cancel-safe ownership state, forwards or completes the IRP exactly once, and releases the lock on the matching completion path.
5. Use `IoCsqInitialize` or a framework queue for cancellable IRPs. The cancel routine, worker, timeout, and cleanup path must have one atomic winner; fixed sleeps are not synchronization.
6. Handle query-stop/remove, stop, surprise-removal, and remove distinctly. On remove, reject new I/O, drain with `IoReleaseRemoveLockAndWait`, detach, delete links/interfaces, then delete the device.
7. Forward power/PnP IRPs according to the WDK contract; never complete an IRP both locally and in a completion routine.

### KMDF path

`DriverEntry -> WdfDriverCreate -> EvtDriverDeviceAdd -> WdfDeviceCreate -> WdfIoQueueCreate`. Put hardware transitions in `EvtDevicePrepareHardware`/`EvtDeviceReleaseHardware`, power transitions in D0 callbacks, request work in typed `EvtIo*` callbacks, cancellation in `EvtRequestCancel`, and per-object teardown in `EvtCleanupCallback`/`EvtDestroyCallback`. Once a request is forwarded or completed, the driver no longer owns it unless the documented API returns ownership.

### Build, signing, and test matrix

```powershell
msbuild .\driver.sln /m /p:Configuration=Release /p:Platform=x64
InfVerif.exe /w .\package\driver.inf
signtool.exe verify /kp /v .\package\driver.sys
pnputil.exe /add-driver .\package\driver.inf /install
verifier.exe /standard /driver driver.sys
verifier.exe /querysettings
```

Run only in a disposable KD-enabled VM. Include checked/debug versus release, x64 versus ARM64 when supported, HVCI off/on, normal versus low-resource/special-pool verifier, start/stop/remove/surprise-remove, malformed IOCTL corpus, cancellation at each ownership edge, and repeated load/unload. Test-signing is a lab boot-policy choice; it is not production signing.

On a crash preserve the dump, exact SYS/PDB identity, verifier settings, and these KD views before changing code:

```text
!analyze -v
!verifier 3 driver.sys
!irp <address>
!locks
!pool <address>
!wdfkd.wdfdevicequeues <WDFDEVICE>
```

## Version-pinned research techniques

### Research classification

These topics preserve the skill's ring-0 research coverage, but they are not supported driver architecture. Pin the exact Windows build, module hashes, PDB identity, offsets, VBS/HVCI state, and rollback snapshot. Treat every unexported routine, pattern-derived address, or internal layout as invalid after an update until re-proven.

### APC delivery and thread context

- `MmAllocateContiguousMemory` returns kernel virtual memory backed by contiguous physical pages; it does **not** allocate target-process user memory.
- A documented `ZwAllocateVirtualMemory` path requires a process handle with the right access and strict requestor/context handling. Prefer a cooperative user-mode component for legitimate instrumentation; never retain an attach across waits or calls into unknown code.
- `PsSuspendThread`, `PsGetContextThread`, and `PsResumeThread` are not a supported WDK thread-hijack contract. A lab that studies them must resolve and validate each build independently, account for WOW64/CET state, restore context on every exit, and cannot ship this path as production code.
- Internal `KAPC` layout and queue behavior are version-sensitive. Prove target-thread lifetime, APC environment, delivery conditions, cancellation, and allocation ownership before claiming a result.

### VAD, callbacks, DKOM, and SSDT

- `MMVAD`, `EPROCESS`, `ETHREAD`, token fast references, callback storage, and service tables are private layouts. Direct edits can violate reference counts, locks, PatchGuard, HVCI, and concurrent enumerators even when one debugger observation looks correct.
- A driver unregisters only registrations it owns, using the matching cookie/handle and documented API: `PsSetCreateProcessNotifyRoutineEx(..., TRUE)`, `ObUnRegisterCallbacks`, `CmUnRegisterCallback`, `FltUnregisterFilter`, and corresponding thread/image APIs. Do not clear callback arrays or unlink filter globals.
- DKOM unlinking and token replacement are forensic experiments, not lifecycle mechanisms. Record every invariant broken and restore the original list links/fast-reference semantics from a snapshot rather than trusting unload.
- SSDT pointer edits, `CR0.WP` manipulation, and NXE changes are unsupported on x64 and conflict with PatchGuard/HVCI. Use documented filter/callback interfaces for drivers; route a genuine VMM/EPT experiment to `hypervisor-dev` or `hyper-v-offensive`.

### Dynamic resolution

```c
UNICODE_STRING name = RTL_CONSTANT_STRING(L"ExAllocatePool2");
PVOID optional = MmGetSystemRoutineAddress(&name);
```

Use this only for an exported API with a documented older-build fallback. Pattern scanning an unexported function requires static uniqueness, runtime boundary checks, fail-closed behavior, and a build-specific test matrix.

## Routing

- Batch A: `bof-coff-development`, `windows-rpc-com-attack`, `windows-telemetry-etw`, and `hyper-v-offensive`.
- Batch B: `linux-kernel-exploitation`, `c2-implant-engineering`, `ebpf-offensive`, and `linux-host-post-exploitation`.
- Use `windows-internals` for build-specific object/I/O context, `driver-comm` for IOCTL protocol design, `kernel-callbacks` for callback ownership, and `windows-driver-0day` for a confirmed driver vulnerability.
- Use `byovd` for third-party vulnerable-driver operations, `exploit-dev` for a proved primitive, and `hypervisor-dev` for a custom VMM boundary.

## Verification checklist

- [ ] Documented versus unexported/version-pinned dependencies are explicit
- [ ] Device ACL and every IOCTL method/access/length contract are tested
- [ ] PnP, power, cancellation, removal, and partial-failure unwind paths are covered
- [ ] IRQL, request, reference, MDL, allocation, and callback ownership are balanced
- [ ] NX pool, SAL, `/W4 /WX`, Code Analysis, signing, and HVCI results are recorded
- [ ] Driver Verifier passes malformed-I/O and repeated lifecycle tests
- [ ] KD crash triage and exact SYS/PDB/build evidence are preserved
