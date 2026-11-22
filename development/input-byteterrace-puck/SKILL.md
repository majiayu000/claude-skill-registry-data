---
name: input
description: "Maps Puck input: channels, inputModes, sub-tick ingress, tap/hold/chords/sequences (inputPatterns), bindings and overlays, the always-active plane, devices, haptics. Grammar: puck-dsl."
---

# Input

A map of how a physical press becomes authoritative semantic input and what
judges it. Input has two layers, and most mistakes come from picking the wrong
one:

- **The host's physical layer.** `Puck.Input` reads devices and window events;
  `Puck.Commands`' `InputRouter` resolves each source through the composed
  binding profile (pages, chords, toggles, wheels, activators) per seat. It is
  presentation-side: it never decides a rule, and its gesture state is not
  replayed authority.
- **The authority's semantic layer.** `WorldInputRuntime` and one
  `WorldInputOwner` per admitted seat or session hold modes, epochs, timed
  event history and pattern matches. Rules read it; checkpoints, hashes and
  replay carry it.

[Input channels](../../../docs/decisions/input-channels.md) owns the model and
its reasoning; [commands](../../../docs/reference/commands.md) and
[device input](../../../docs/reference/input.md) are the human references;
[references/bindings.md](references/bindings.md) holds the binding composition
contracts. When this file and the code disagree, the code wins and this file
is corrected in the same change.

## Find the owner by what you need

| You need | Owner | Read |
|---|---|---|
| Name an action and give it a shape (button, axis, relative look, text) | `channels` rows → `WorldChannel`, `WorldChannelTable`; `ChannelShape` (`PlayerIntent.cs`); motion `ChannelRole`; shared names in `worlds/standard/inputs.puck` | [semantic names](../../../docs/decisions/input-channels.md#semantic-names-and-typed-values) |
| Decide which actions are live while walking, flying, seated or engaged, and what survives a switch | `inputModes` → `WorldInputModes`, `WorldInputCatalog` (one `WorldInputMapping` per allowed tuple), `WorldInputSelector`, `WorldInputOwner.Switch`; the debug policy is `worlds/debug/input-modes.puck` | [modes](../../../docs/decisions/input-channels.md#modes-are-simulation-state), [switching](../../../docs/decisions/input-channels.md#switching-releases-input) |
| The time of a press inside a tick, several presses per tick, typed text | `WorldInputProducer` → `WorldInputBatch` → `WorldInputRuntime.TryAdmit` → `WorldInputOwner.TryAdmit`; `WorldInputInterval`; `inputHistory` (`WorldInputHistory`) | [sub-tick time](../../../docs/decisions/input-channels.md#sub-tick-time-and-clocks) |
| Tell a tap from a hold; a double tap, a fighting motion, a simultaneous press, a buffered attack, a rhythm note | `inputPatterns` (`WorldInputPattern`, compiled by `CompiledWorldInputPattern.Compile`), matched by `WorldInputOwner.TryMatch`, read by `inputMatch`, consumed by `consumeInput` | [below](#press-release-tap-hold-chords-sequences-and-rhythm) |
| Drive a seat's controls from a program each tick, as a player at a pad would (a benchmark route) | `seatPrograms` rows (`WorldSeatProgram`: `move`, `turn`, `hold`, `pulse`, `tap`) evaluated by `WorldSeatDriver` in the tick-complete hook (`WorldTickScript.Ticked`) and submitted through the seat's ingress (`WorldTickScript.SubmitSeat`); `routes` rows say where to go. The driver is the seat's client: it reads only what the seat's authority delivered (`WorldSeatSenses`), in process or remote | [the benchmark plan](../../../docs/plans/benchmark.md#the-route-is-places-played-by-an-authored-seat-program-stage-4) |
| Map a key or button to an action or command; pages, chords, autorun toggles, wheels | `bindingOverlays` → `WorldBindingComposer.Compose` → `BindingProfile.Compile` → `PagedInputBindings` inside `InputRouter`, composed per seat by `WorldSeatBindings`; the standard's rows in `worlds/standard/controls.puck` | [bindings.md](references/bindings.md), [commands: bindings](../../../docs/reference/commands.md#bindings) |
| A control no page or overlay can take (the console key, the pause menu) | `IAlwaysActiveInputBindings`, implemented by `TerminalInputBindings` (`Puck.Launcher`) | [below](#the-always-active-plane-and-reserved-gestures) |
| Read a controller, keyboard or mouse; rumble, lights, adaptive triggers | `Puck.Input` (`GamepadManager`, `InputArbiter`, `GamepadCaptureSource`, `WindowInputMapper`, `InputSources`, `IGamepadOutput`); OS transports in `Puck.Platform.Windows` | [device input](../../../docs/reference/input.md) |
| A machine's buttons while a seat is engaged | the route's kit `pad` map (`WorldKit`, `WorldPadElement`) | [engagement](../puck-world/references/engagement.md) (`puck-world`) |
| Light the keyboard's keys from the world: the next key to press, the keys a page binds, a flash on an event | `keyLights` (`WorldKeyLightSection`) → `WorldKeyLightDirector` → `LightLegendComposer` → `LampLegendDriver` → `ILampArrayDeviceSource`; read-back `lights.state` | [dynamic lighting](../../../docs/reference/input.md#dynamic-lighting) |
| A game played by typing words | the standard's `typingPlay` and `typingFamily` (`worlds/standard/typing.puck`): a `Text` channel judged a character at a time against words authored as strings (`scalars(text)`) | [the press](../../../worlds/debug/press.md) |

## Semantic channels and typed values

- A world declares each action once in `channels`; modules, bindings, kits,
  rules, engagement maps and grants name it. The standard's shared vocabulary
  is `worlds/standard/inputs.puck`; world-specific actions stay in the world
  (the debug world's `suit.puck`, `noclip.puck`). Different meanings get
  different names: chess uses the shared `confirm` and `cancel`, independently
  of a machine's `select`. The engine
  knows only the motion roles (`ChannelRole`), never a genre's vocabulary.
- Each active input owner has 32 numeric slots (Q48.16 levels, or Q32.32
  `Relative` displacement) and 64 packed buttons, budgeted per allowed mode
  tuple; target registers have their own reach mask and spend none of it.
  `Text` is event-only and takes no slot.
- Resolve names through `WorldChannelTable` or the owner's published mapping. A
  declaration index is not a storage address, and a slot may hold different
  actions in different tuples. Read relative input with the table's checked
  `ReadRelative`, never a held-level reader.
- `Relative` input (mouse look) shares the numeric bank as Q32.32
  displacement: the host accumulates samples and drains them once per routed
  tick, rules read a Q48.16 projection whose fractional residue stays in
  authority state, and it is never kept across a switch, toggled, or used by an
  activator. Binding compilation must receive the routed channel shapes.

- **A seat in one token is `seat<n>`** (1-based, case-insensitive, `seat1`..`seat4`), parsed once by
  `PrincipalTokens.TryParseSeat`: principals and grantees, `world.hud seat<n>`, `audio.listener` and a scenario's
  `seat1:` labels. A grant subject `seat:<n>` is a different grammar (a `kind:value` subject, zero-based); a
  keyword argument (`screen.source ... seat <n>`) and a HUD binding path (`seat.<n>.position.x`) keep their own
  shapes.

## Modes and what survives a switch

- A family's selector reads authoritative state only: `ActiveKit`,
  `Engagement`, `BodyState` (a finite or range-partitioned register) or
  `SeatState` (`WorldInputModeSelectorKind`). Never a binding page, the camera
  layout or wall time. `player.mode` changes a `SeatState` family through
  `WorldCommand.SelectInputState`. Every family with a camera-targeting state also
  takes that authority path, even without an `inputModes` selector; the authority
  composes or dissolves the application and publishes the seat state together.
- The live set is the global names plus every selected, unsuspended state's
  names. `suspendedBy` suppresses a family by another's selection;
  `combinations` restricts the allowed tuples, checked on every transition.
- **A switch releases by default.** A family's `transitions` row keeps named
  actions (`conditionalKeep` adds tuple-conditioned ones); with several changed
  families an action must be kept by every one, so an engagement row with an
  empty keep wins. The barrier (`WorldInputOwner.Switch`) advances the epoch,
  consumes the edge that caused it, and admits fresh input from the next tick;
  a kept hold continues with no new press.
- A source the barrier released waits for neutral before it can act again, and
  the router reports a button's edge once. A seat whose registry is rebuilt
  (every crossing) misses a release the router dispatched elsewhere, so each
  tick the seat reports neutral for every waiting button its router reports up
  (`WorldSeatInput.AcknowledgeReleasedButtons`, from `WorldClient.SynchronizeInput`);
  a button held through a portal then works on its next press.
- A binding page or `contexts` row changes which binding group a seat uses,
  never simulation eligibility. Install the barrier with the firing's commit,
  before another rule reads channels ([bindings.md](references/bindings.md)).

## Timed ingress and sub-tick time

- The host quantizes each device event once to a simulation interval and a
  Q48.16 offset (`WorldInputInterval`) on the 50,400 Hz engine clock
  (`FixedTickConversion`). No wall clock reaches simulation.
- Producers send `Press`, `Release`, `AxisSample` and `Text` events; the
  authority derives `AxisCrossing` from `inputHistory.crossings` (thresholds,
  hysteresis, an optional `facingState`) and records `Cancel` for a reset hold
  (`WorldInputEventKind`).
- `inputHistory` sizes retention, ring capacity, events per step, lateness,
  calibration and the judged clock (`Capture` or `Admission`). An overflowing
  batch is refused whole and resets the owner into a new epoch; history is
  never truncated. Size it for the rate and sample density
  ([bindings.md](references/bindings.md)). A `forEach: $inputEvents:<owner>`
  rule binds only the step's events and is priced at `maximumEventsPerStep`
  plus the terminal cancellations (`WorldInputIteration.StepCapacity`); a read
  through `each` costs one record. A rule reading a literal owner's events or
  holds is scheduled on that owner's input version, so the due list leaves it
  alone on a tick the owner's history did not change (`WorldRuleHost.TryInputScope`).
- In a scenario, `seat1: player.signal <source> press at:<seconds>` places a
  press at a sub-tick offset; `keyboard.text` commits text as ordered Unicode
  scalar events.
- Calibration is a per-owner signed offset in seconds that the judgement adds
  to a press's captured time. `player.calibrate <seconds> [seat]` (bindable,
  and a scenario step) submits `WorldCommand.CalibrateInput`; the authority
  bounds it by `inputHistory.calibrationLimitSeconds` (zero when unauthored)
  and applies it at an epoch boundary. A refusal narrates on `input.refused`.

## Press, release, tap, hold, chords, sequences and rhythm

Pick the layer by who must agree on the answer:

| You want | Use | Not |
|---|---|---|
| A gesture the simulation judges, replays and consumes once: tap versus hold, double tap, a motion, a buffered attack, a note | an `inputPatterns` row, read with `inputMatch(owner, pattern)` and claimed with `consumeInput` | a binding activator, a chord row or `BindingChordTracker` held state, which are host-only and not authority |
| The newest edge of an action, its time or its age | `inputEdge`, `inputTime`, `inputAge(owner, name, kind, occurrence)` | comparing two tick images, which loses a press and release inside one tick |
| How long the current hold has lasted, including across a kept switch | `inputHeldSince`, `inputHeldPress`, guarded by a current held level | |
| A page or command while modifiers are held (trigger pages) | chord rows: `held` is a set, `chord` an ordered sequence ([bindings.md](references/bindings.md)) | |
| A host-side tap code that fires a command | `BindingActivatorDefinition` with `Mode: Tapped` and `TimeoutTicks` (engine ticks), tracked by `RowActivatorTracker` | |
| An action latched on (autorun, autofly) | a `mode: Toggle` entry or chord row on the channel | a new command or state register |

The pattern contract (`WorldInputPattern.cs`, `WorldInputOwner.Patterns.cs`):

- A row has ordered `steps` (a channel, an event kind, an optional raw value,
  crossing or `simultaneousGroup`, tolerance and tick gaps),
  `maximumDurationSeconds`, `maximumGapSeconds`, optional `bufferTicks`,
  `held` (binary actions that must be down now) and `consumptionGroup`.
  `Compile` refuses more than 64 rows, a row outside 1 to 16 steps, a duration
  beyond retention, a kind that disagrees with the channel's shape, and
  overlapping or non-contiguous simultaneous predicates.
- Matching reads only the current epoch, picks the earliest-ending match, then
  the latest start, then the lowest event ids. Within one consumption group an
  earlier row has priority: its match removes those events from later rows'
  candidates. A read never consumes; `consumeInput` claims the range only when
  the firing commits (the arm in `WorldRuleHost.Arms.cs` preflights
  `TryMatch`), and a refused firing claims nothing. Claims and cursors are in
  the checkpoint and hash.
- `worlds/debug/input-pattern-tests.puck` is the worked example: a crossing
  motion consumed by a rule, and a `bufferTicks` attack whose rule adds an
  `inputAge` guard.
- **Tap versus hold.** The tap is a pattern of a press then a release within a
  window shorter than the hold; the hold and the tap share one
  `consumptionGroup` so one press cannot be both. The pause menu's Menu button
  is specified this way ([hub plan](../../../docs/plans/hub-and-saves.md#11-menu-routing)).
  A pattern step matches events only, so no step means "still held after N
  seconds": today the duration goes in the rule (a press pattern whose `held`
  names the action, plus an `inputAge` guard like the buffered example's), not
  in the pattern's data. That composition is an inference from the matcher's
  code, not a run scenario.

## Bindings and overlays

- Layers compose base first: the engine's build layer
  (`WorldEditorBindings.Layer`), each world `bindingOverlays` row in order
  (a `when` gate that fails skips it), the seat profile's `bindings`, then
  live rebinds. `BindingProfile.Compile` is the one compiler; never copy it.
- An overlay replaces only the pages it declares; everything else stays the
  player's ([the owner's ruling](../../../docs/decisions/input-channels.md#an-overlay-replaces-only-what-it-declares)).
- Concrete designs (bar layouts, wheels, trigger pages, keys) are standard
  data: `worlds/standard/controls.puck` (`bare`, `play-wheel`, `pad-pages`),
  `pad-kit.puck`'s modifiers; the debug world refines them in
  `worlds/debug/controls.puck`. None belongs in engine code.
- `BindingVocabularyCheck.Validate` and `puck compile --validate` refuse an
  unknown source, an unknown or unbindable command and a mismatched value kind.
- Live surface: `player.bind`, `player.bindings` (leads with the group
  derivation), `player.signal`, `world.affordances`, `body.rig`,
  `body.channels`, `world.binding-bar`. `player.signal` drives the same binding
  path a device does, headless included.
- The router delivers every edge it synthesizes (an impulse's inactive twin, a
  cancellation from focus loss, reload or a map change) on the next tick
  ([commands](../../../docs/reference/commands.md#quick-start)).

## The always-active plane and reserved gestures

- `InputRouter` resolves `IAlwaysActiveInputBindings` beside the active page
  for every source. Today `TerminalInputBindings.Resolve` answers only
  `keyboard.backtick` (the `console` command). While the console holds
  terminal focus, signals enter through `InputRouter.CaptureFocusExempt`: only
  commands declaring `CommandInputScope.FocusExempt` dispatch and only the
  plane answers presses.
- Host-reserved gestures outside the binding profile: Control+Alt+Escape
  returns keyboard focus from a passthrough source (`SourceFocus`), and Escape
  closes an open console (`ConsoleInputSink`).
- Ruled but not yet built: the pad's Menu (`gamepad.start`) and Escape always
  reach the pause menu, and no binding may name them
  ([play decisions](../../../docs/decisions/play.md#the-game)). Nothing
  enforces it yet: `BindingProfile.Compile` refuses neither source, no `menu`
  verb exists, and the standard's `start` row binds `gamepad.start`. Hub plan
  step H4 owns it.

## Devices and haptics

- Acquisition feeds `GamepadManager`; `InputArbiter` drains it once per host
  frame; `GamepadCaptureSource` appends timestamped `InputSignal`s to the
  router; `WindowInputMapper` maps keys, text and mouse. Source ids come from
  `InputSources` and resolve case-insensitively (`InputSourceVocabulary`).
- An agent's World passes `--devices none`: no pad opens and every OS event is
  dropped before a seat (`WorldWindowInputFilters.ConsumesEveryEvent`), while
  scripted input still drives it
  ([the ruling](../puck-world/SKILL.md#an-agents-world-opens-no-physical-device)).
  Never inject real input to test.
- **Keyboard lamps are painted from the document.** `WorldKeyLightDirector`
  (`Puck.World.Client`) builds each local seat's `LightLegendState` every fixed
  step from its routed world's `keyLights` rows and the seat's active
  `BindingPageView`. A row's scalars (`lit`, `available`, `character`,
  `flashSignal`) read through the seat's `WorldStateLease`, so one keyed `$body`
  reads the seat's body as a haptic row's does. It composes the legend onto a
  reference board for `lights.state`, and
  publishes the keyboard-holding seat's legend to `LampLegendDriver`
  (`Puck.Input.Lighting`). The driver owns the device loop on its own thread:
  it opens `Win32LampArrayDeviceSource` at the first published legend, never
  on the pump, and is registered only by a boot that opens physical devices,
  so an agent's World paints legends and writes no lamp. A lamp check needs
  `--devices all` and a keyboard that exposes a HID LampArray.
- Output goes through `IGamepadOutput` (capability-gated; rumble is finite by
  contract). `WorldHapticDirector` evaluates world-authored `haptics` rows
  (`WorldHapticRow`) per local seat against each seat's routed
  `WorldStateMirror` (including `$body` keys via `WorldStateLease.Scalar`,
  bound to the body `WorldSeatBodies` names for the seat) and
  drives the seat's assigned pad via `PlayerRoster.TryGetSeatDevice` and
  `GamepadManager.TryGetOutput`; `haptics.state` echoes per-seat status.
  The haptic, key light and highlight directors share `WorldSignalEdges`
  (`Puck.World.Client`): one reading per row id, reporting `Changed` or `Rose`
  against the last, and a row's first reading only seeds it.
  Protocol work consults several independent sources and cites each
  (AGENTS.md); hardware evidence and owed runs are in
  [device input](../../../docs/reference/input.md#limits-and-hardware-evidence).

## Where each contract is enforced

| Contract | Enforced by |
|---|---|
| Names, shapes and the 32/64 budget per allowed tuple | `WorldInputCatalog` compilation and `WorldDefinitionValidator.Channels.cs`, `.Modes.cs` |
| A selector reads only finite authoritative state | the closed `WorldInputModeSelectorKind` and `WorldInputSelector`'s partition proof |
| A switch releases what no keep set names, and consumes its edge | `WorldInputOwner.Switch`, the one barrier door |
| A stale-epoch or malformed batch is refused atomically | `WorldInputOwner.TryAdmit` |
| A pattern is bounded and well-formed | `CompiledWorldInputPattern.Compile` |
| Consumption happens only on a committed firing | the `consumeInput` arm in `WorldRuleHost.Arms.cs` |
| A binding names known sources and bindable commands | `BindingVocabularyCheck` |
| Same input, same state | history, holds and claims in `WorldInputOwner.Checkpoint.cs`; `puck test --reproduce` |
| World `haptics` rows | `WorldDefinitionValidator.Haptics.cs` (unique ids, unit intensities, positive duration within `WorldHapticCapacity.MaxDurationSeconds`, `mode`/`signal` agreement, seat tokens) and `WorldValueDomainGuard` |
| Menu and Escape are reserved | nothing yet (H4) |

## Open gaps

- **A hold completes with no closing event.** A pattern stage is satisfied
  only by an event, so a hold of N seconds cannot be pattern data; a term
  satisfied by time with the action still held (or a tick event closing the
  stage) is the hub plan's H4 work.
- **The matcher runs only in the authority.** `WorldInputOwner` lives in
  `Puck.World.Server` and only `WorldRuleHost` calls `TryMatch`; the
  always-active plane runs no matcher, so a remote authority decides every
  pattern. H4 runs the one matcher on the plane over its local events.
- **Cartridge rumble is unwired.** `WorldHapticDirector` drives
  `IGamepadOutput.Rumble` from authored `haptics` rows
  (`worlds/standard/instrument.puck` pulses on the beat), while a cartridge's
  `IFeedbackMachine.MotorLevel` still has no consumer. Keep it: an unreached
  capability is wired, not deleted.
- **The lamp loop has not met a lamp array.** `LampLegendDriver` and the
  `keyLights` path are verified on the reference board only.
- The chat exhibit, the in-world computer's typing tutor, the owed hardware
  runs and the decision's raw-slot wording are in
  [the input packet](../../../docs/plans/open-items.md#input-channels).

## Verify

- Scenarios: `puck test worlds/debug/input-pattern-tests.puck --jobs 1` and
  the other `worlds/debug/input-*-tests.puck`; add `--reproduce` for a timing,
  history or continuity change. Typed text end to end is
  `worlds/debug/typing-tests.puck` (the standard's play alone) and
  `worlds/debug/press-tests.puck` (the press in the whole debug world).
- Genre sweeps: `puck sweep --plan worlds/debug/<plan>.sweep.json --world
  <source>` with the five plans the
  [genre check](../../../docs/decisions/input-channels.md#genre-check) lists.
- Unit suites: `tests/Puck.World.Server.Tests/InputPatternTests.cs`,
  `tests/Puck.Commands.Tests`, `tests/Puck.Input.Tests`.
- Look-alike: the document's `patterns` section (`CompiledPatterns`, the
  `$match` operand, `world.match`) matches words over board cells, not input
  history.

## Route adjacent work

| Skill | Route there for |
|---|---|
| `puck-world` | Running and verifying a World, engagement and kit `pad` maps, the seat camera's input feel (`seatCameraFeel`), rules and grants. |
| `puck-dsl` | `.puck` grammar, `let`/`for`, compile and lint verbs, PUCKnnn diagnostics. |
| `gaming-bricks` | An emulated machine's own pad registers and input timing inside the core. |
| `platform` | The OS side of a device: window messages, Raw Input, pointer lock, HID and Xbox transports, lamp arrays. |
| `maths-usage` | Fixed-point types for offsets, calibration and judgement windows. |
| `verification` | Leases, the private CLI copy, flaky versus failing scenarios. |
