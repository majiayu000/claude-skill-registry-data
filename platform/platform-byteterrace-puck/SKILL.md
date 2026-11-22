---
name: platform
description: "Maps Puck's OS seams (Puck.Platform, .Windows, .Linux): native windows, Win32/Wayland/XCB, displays and VRR, precision waits, memory, clipboard, camera and desktop capture, probes, HID transports."
---

# Platform

A map of where Puck meets the operating system. Three projects, one shape:

- **`Puck.Platform`** holds the OS-neutral contracts and the pieces that need
  no OS code: window, clipboard, camera, image-capture and audio-render
  contracts, camera discovery polling, the unmanaged allocator, probe
  readings and kernel sockets, null fallbacks and the declining recording
  factories.
- **`Puck.Platform.Windows`** implements them over Win32, Media Foundation,
  Windows Graphics Capture, WASAPI, Raw Input, HID, XInput and GameInput.
- **`Puck.Platform.Linux`** implements windows over Wayland and XCB and
  registers null or declining services for everything else.

A composition root picks one platform per seam with one
`OperatingSystem.IsWindows()` branch (`WorldBootComposition`, and
`WindowsPresentationRegistration` or `LinuxPresentationRegistration` in the
`Puck.Launcher.Windows` and `.Linux` projects). The project READMEs
([neutral](../../../src/Puck.Platform/README.md),
[Windows](../../../src/Puck.Platform.Windows/README.md),
[Linux](../../../src/Puck.Platform.Linux/README.md)) are the developer
reference. When this file and the code disagree, the code wins and this file is
corrected in the same change.

## Find the owner by what you need

| You need | Owner | Read |
|---|---|---|
| A native window, its events and its surface | `INativeWindow`, `INativeWindowFactory`, `INativeWindowBackend`; `Win32NativeWindow`, `WaylandNativeWindow`, `XcbNativeWindow`; `ConfiguredNativeWindow` as the headless stand-in | [neutral README](../../../src/Puck.Platform/README.md#what-lives-here) |
| Which display kind to open on Linux | `NativeDisplayEnvironment`, `NativeDisplayKindSelector` (environment variables only) | [neutral README](../../../src/Puck.Platform/README.md#what-lives-here) |
| Variable refresh range, display timing, colour space, keeping the display awake | `IDisplayTimingInfo` on `Win32NativeWindow` (`Win32NativeWindow.Vrr.cs`), `EdidVariableRefreshParser`, `Win32DisplayColorSpaceProbe`, the display power request in `Win32NativeWindow.DisplayPower.cs` | [host pacing](../../../docs/reference/hosting.md#host-pacing) |
| Wait until a deadline without spinning or raising timer resolution, or until an event ends the wait early | `IPrecisionWaiter`: `Win32PrecisionWaiter` over `Win32HighResolutionWaitableTimer` (`AddWindowsPrecisionWaiter`) or `LinuxPrecisionWaiter` over `clock_nanosleep` (`AddLinuxPrecisionWaiter`), one container singleton the World's composition root registers for every shape and the Linux silo registers for its pacer, consumed by `HostWaits.Until` and by `HostWaits.Pace`, the pacer's serviced wait, which sleeps on the timer and the pump thread's wake in one operating-system wait | [below](#play-nice-with-the-host) |
| Unmanaged memory | `IAllocator`, `MimallocAllocator`, registered by `AddPuckAllocator` | [neutral README](../../../src/Puck.Platform/README.md#what-lives-here) |
| Clipboard | `IClipboardService`: `Win32ClipboardService`; `NullClipboardService` on Linux | [neutral README](../../../src/Puck.Platform/README.md#what-lives-here) |
| Mouse, keyboard and pointer lock at the OS boundary | `Win32NativeWindow` messages, `Win32RawInput` (relative motion per mouse), `Win32PointerLock`, `WindowInputQueue` | [pointer input](../../../src/Puck.Platform.Windows/README.md#pointer-input) |
| Pads and HID devices at the transport | `WindowsInputTransports.CreateGamepadManager` over `Win32HidDeviceSource` and `Win32XboxAcquisitionSource` (XInput, GameInput) | `input` |
| Device lights | `ILampArrayDevice`: `Win32LampArrayDevice` | [abstractions](../../../docs/reference/abstractions.md) |
| A webcam's frames, CPU pixels or shared GPU textures | `ICameraCaptureService` (`EnumerateDevices`, `TryOpenPixels`, `TryOpenShared`) → `ICameraGraph`; `Win32MediaFoundationCameraService`, `Win32CameraGraph`'s MTA worker, `Win32D3D11CameraFrameConverter`; discovery polling in `CameraDeviceScanner` | [camera capture](../../../src/Puck.Platform.Windows/README.md#camera-capture) |
| A desktop or another window's pixels as a feed | `INativeImageCaptureService`: `Win32NativeImageCaptureService`, `Win32GraphicsCaptureFeed` | [Windows README](../../../src/Puck.Platform.Windows/README.md#contents) |
| A passthrough screen that forwards input to a desktop window | `Win32DesktopPassthrough`, `Win32PassthroughWindow` | [device input](../../../docs/reference/input.md) |
| A probe: a kernel over camera, strobe or rendered frames | `ProbeReading`, `PublishBuffer<ProbeReading>` (the shared latest-value handoff, whose readers never wait), `IProbeKernelHost`, `ProbeKernelRequest`; `Win32ProbeKernelBench`, `Win32RenderedProbeKernelHost`; `ProbeTrackPlayer` replays recorded readings | [neutral README](../../../src/Puck.Platform/README.md#what-lives-here) |
| The audio output device | `IAudioRenderDeviceFactory`: `WasapiAudioRenderDeviceFactory`; none on Linux | `media` |
| Video encoders, loopback and microphone capture | `IVideoEncoderFactory`, `IAudioCaptureSourceFactory`: `MediaFoundationVideoEncoderFactory`, `WasapiAudioCaptureSourceFactory`; declining factories on Linux | `media` |

## Registration shape

- `PlatformWindowingServiceRegistration.AddPlatformWindowing` registers only
  the neutral pieces (display probe, platform support, window factory). Each
  platform package adds one method per seam:
  `WindowsPlatformServiceRegistration.AddWindowsPlatformWindowing`,
  `AddWindowsCameraCapture`, `AddWindowsRecordingPlatform`,
  `AddWindowsAudioRender`, `AddWindowsPrecisionWaiter`, and the Linux
  equivalents on `LinuxPlatformServiceRegistration`
  (`AddLinuxPlatformWindowing`, `AddLinuxCameraCapture`, which registers the
  null camera and image-capture services today, `AddLinuxRecordingPlatform`).
  A new backend implements the contract in its platform project and replaces
  the null service in that platform's registration method.
- A method that constructs a `[SupportedOSPlatform("windows")]` type carries
  the attribute itself, so CA1416 makes the caller guard with
  `OperatingSystem.IsWindows()`. The guard lives in the composition root,
  never inside a platform project.
- `Puck.Platform.Windows` stays `net11.0`, like `Puck.Platform`, so the
  annotations keep firing. `WindowsCaptureProjection.targets` re-declares the
  WinRT projection at every entry point that references it, on Windows hosts.
- A seam with no backend registers a null or declining service that answers
  with a reason (`NullCameraCaptureService`, `DecliningVideoEncoderFactory`),
  never a missing service a caller must guess about.

## Play nice with the host

AGENTS.md's ruling applies here first: Puck uses the host's threads, waits,
timers and virtual memory, and never spins in place of a wait or raises
process-wide timer resolution. In this area that means:

- Wait on `IPrecisionWaiter`. `Win32HighResolutionWaitableTimer` uses
  `CREATE_WAITABLE_TIMER_HIGH_RESOLUTION`, which wakes within about half a
  millisecond without `timeBeginPeriod` and without spinning;
  `HostWaits.Until` re-reads its clock after each wait and falls
  back to a one-millisecond sleep only where no waiter is registered (an OS
  too old for the timer, a silo started on Windows, a test). A host that can
  register one does, so no shipped path leans on the sleep, which lasts a
  whole system tick on Windows. A busy loop on a stopwatch is a defect,
  however short.
- Work the pump thread should take up while it waits between frames registers
  with the door (`HostWaits.Serve`) and is woken through its `WaitService`;
  the pacer's wait (`HostWaits.Pace`) then waits on the timer and that wake
  together (`IPrecisionWaiter.TryWait` with a wake). A service that asks to
  run again is run no sooner than `HostWaits.LeastServiceDelay`, so a serviced
  wait sleeps between runs. Only the pacer's form services: a wait inside an
  iteration never re-enters a service.
- Swap-chain waits pace a windowed host ([host pacing](../../../docs/reference/hosting.md#host-pacing));
  the timer only bounds what the swap chain cannot.
- Camera graphs own their native objects on one MTA worker thread, joined with
  a bound on disposal; camera scans run at most one at a time on a worker and
  hand back completed snapshots without blocking the caller.
- The window holds a display-required power request while open, because a
  powered-off display stops the compositor retiring presents.

## Contracts that bite

- **An empty camera list means no cameras.** `EnumerateDevices` returns empty
  only when the machine has none; a failed scan throws
  `InvalidOperationException`, so a caller never reads a failed scan as every
  camera unplugged.
- **A successful open is usable.** A pixel open has already published a frame
  from every stream; a shared open has validated native GPU input. A shared
  ring's consumer acquires a slot until its GPU submission retires, and the
  camera drops a frame rather than overwrite a texture still being sampled.
- **Relative mouse motion is never integrated into a cursor estimate.** Raw
  Input supplies per-mouse deltas; the system cursor supplies positions and
  buttons.
- **An agent's World opens no physical device.** `--devices none` drops every
  OS event before a seat; never inject real input to test
  ([puck-world](../puck-world/SKILL.md#an-agents-world-opens-no-physical-device)).
- **A device or OS protocol is independent work.** Consult several
  independent sources (vendor documentation, kernel drivers, other open
  implementations), cite each and note where they disagree (AGENTS.md).

## Where each contract is enforced

| Contract | Enforced by |
|---|---|
| Windows-only code runs only behind an OS guard | CA1416 over `[SupportedOSPlatform]` on the registration methods |
| `Puck.Platform.Linux`'s closure has no Windows dependency | the `Puck.Platform.Linux` lane profile in `build/Architecture.props` (`puck architecture`) |
| A failed camera scan is distinct from an empty one | `ICameraCaptureService.EnumerateDevices` throwing; `CameraDeviceScanner` keeping failures apart from empty lists |
| One waiter per timer, no spinning | `Win32HighResolutionWaitableTimer` (one waiter at a time, re-armed per wait) |

## Open gaps

- **Linux has no camera, desktop-capture, audio-render, video-encoder,
  audio-capture or clipboard backend**, and its windows hold no display
  request (Wayland's idle inhibit, X11's screensaver suspend). Windowed
  Wayland and XCB behaviour has not been run on real Linux hardware.
- **Duplicates recorded in the refactoring packet:** camera plane validation
  and L8/BGRA packing (`Win32FaceAuthenticationCameraGraph.cs` beside
  `CameraFramePacking`)
  ([refactoring campaign](../../../docs/plans/open-items.md#refactoring-campaign)).
- A reading taken while the compositor is not composing still looks like a
  slow frame ([open items](../../../docs/plans/open-items.md)).

## Verify

- Build what you touched: `dotnet build src/Puck.Platform.Windows -c Release`
  or `src/Puck.Platform.Linux`; a Linux change also gets the WSL2 build the
  [Linux launcher README](../../../src/Puck.Launcher.Linux/README.md) gives,
  and says what it does not prove.
- Laws: `tests/Puck.Platform.Windows.Tests` (camera enumeration and pixel
  delivery skip on a machine with no colour camera), and the host-loop laws in
  `tests/Puck.Launcher.Tests` (`OffscreenBoundaryLawTests` drives a manual
  `IPrecisionWaiter`).
- A window, a display, a camera or pointer lock is a windowed World, a GPU leg
  (`verification`); hand it back as a verification request unless your brief
  grants it.

## Look-alikes

- Host pacing decisions (swap chain, timer grid, catch-up bursts) belong to
  `Puck.Launcher` and the hosting reference; this area only supplies the waits
  and display facts they read.
- `Puck.Input` turns transports into `InputSignal`s and binds them (`input`);
  this area only acquires devices and window events.
- Camera capture feeds screens and probes; `capture.*` records the game
  (`media`).

## Route adjacent work

| Skill | Route there for |
|---|---|
| `input` | Gamepads, HID protocols, haptics, `InputArbiter`, window input mapping and bindings. |
| `media` | The audio device's mixer and director, recording sessions, encoders as the recording graph uses them. |
| `rendering` | Swap chains, presenters, the frame pacer, shared GPU textures a camera ring feeds, the camera conversion shader. |
| `puck-world` | Screens that show a camera or desktop feed, probes rows, booting a windowed World. |
| `dotnet-performance` | Allocation and interop cost on a platform hot path. |
| `verification` | GPU legs for windowed checks, the private CLI copy. |
