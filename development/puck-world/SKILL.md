---
name: puck-world
description: "Maps Puck.World: .puck worlds, rules, grants, console verbs, extensions, the live MCP World. Use to run or verify a World change (stdin script, stale binary, headless run) or debug a refusal."
---

# Puck.World

A map of the World: where each part lives, the contracts that bite, and how to
run it. Each project's README is the developer reference; the files under
`references/` hold each subsystem's contracts. When this file and the code
disagree, the code wins and this file is corrected in the same change. Treat
counts and inventories here as snapshots and check them against the tree.

Creation authoring (shapes, profiles, panels, folds, contact tuning) belongs to
`sdf-authoring`; the `.puck` language core to `puck-dsl`; the renderer to
`rendering`.

**Bare-metal hosting.** Puck's own freestanding runtime and platform host are
the target; do not propose hosting stock .NET as a fallback. Treat missing
contracts as porting work in that host or the engine
([owner ruling](../../../docs/decisions/runtime-and-delivery.md#the-runtime)).
The archived BareMetal experiment remains read-only prior art.

**One live world.** The debug world, the asset package `worlds/debug/` (entry
`debug.puck`, basis `avatars/moth`), is the only live world, with the
garden (`garden.puck`) and the night field (`night.puck`) its painting wing's portals open onto
(`paintings.puck`, in the gallery hall); `debug.md` and `paintings.md` beside them are the
portal demo and its inspection verbs. It boots on the Moth's seat chase
camera: the first authored `views` layout is what a boot shows, and the Moth's
is `play`, followed by inspection layouts (`three-quarter`, `front`, …) that
`view.override layout <name>` selects. The Moth basis (`avatars/moth.puck`)
authors the body, its motion programs, its camera (`seatControl`,
`seatRig "moth-camera"`); the standard's `camera.puck` supplies shared feel and boom limits. A new rule or feature for
the live world goes in `debug.puck` (or a scratch `.puck` world booted with
`--world`). Every other world (the island
`puck.world.json`, its districts, the games) and their canary, parity and
verdict fixtures are quarantined under `experimental/`; do not boot, repair or
retarget them, and read the references' mentions of them as prior art
([decision](../../../docs/decisions/engine-design.md#one-live-world-while-the-campaign-runs)).

## Live state reads and writes

**The standard is authored.** `worlds/standard/standard.puck` composes the
optional controls and skin. Shared cursor, icons, binding-bar designs, pages
and wheel belong there; the debug world's Go/Tour pages and Places ring refine
it in `worlds/debug/controls.puck`. The garden and night field import the
standard directly. Add mechanisms to the engine and concrete design to the
standard, with avatar tuning and rig animation in the avatar document. Authors
override rows by id in the importing document's own body, or replace/omit the
package through the existing composition path; do not copy a second standard
into a world. [The package README](../../../worlds/standard/README.md) owns the
import and override examples.

**Replay one scope while the world lives on.** An authored `replays` row names its
document rows, stable body ordinals, input principals, control row and timed
input program. `WorldScopedReplayRuntime` captures its starting arena columns and
body continuations and the rule/interaction latches of compiled writers to those
rows or bodies (plus their rule-group progress), records accepted addressed mutations plus body commands and
intents, and compares every replayed tick with that live recording. It uses
`StateArena.CaptureScope`/`RestoreScope` and `AddRowTo`, and the population's
existing continuation codecs: exporting and reloading cell values alone loses
ring/draw cursors. Its derived tape belongs to the authority checkpoint and
authoritative hash. `replay.scope` is operator read-back and next-tick control;
it never invokes `world.load` or masks other seats. The first completed drive
derives the tape, later drives verify it. Field, vector, timed and pool rows need
a wider continuation boundary and are refused, as do decision rules and undo or
partially owned rule groups. Body-effect ownership walks nested arms, literal body
keys and compiled placement domains. Shared or unbounded live body targets in a
selected continuation are refused; a standalone level rule carries no edge latch.
Scope restoration validates the complete row/body
inventory before mutation; starting images are privately copied and digested.
Persisted tapes must have a complete expected hash sequence or a consistent
active recording, with ordered, scoped inputs. Hot scope observers enumerate
`ScopedReplaySpan`; an inactive scope must allocate zero bytes per steady tick,
and a warmed active scope hash must allocate zero bytes. Keep closure-bearing
rebinding in the slow method after the compiled-array identity check.
Scope rules must read local facts: `physics(quiescent, "chess-demo")` restricts
the existing census to that scope's bodies. The second argument can also name a
keyed placement roster; its cell values do not filter membership. A state row
and replay scope sharing that name are ambiguous and refused. Both selections
require rigid bodies to rest uncarried, while the global `physics(quiescent)`
couples a table to unrelated rigid bodies. The debug world's idle example
and its game-score citation are in [chess.md](../../../worlds/debug/chess.md).
See [replay](references/replay.md#scoped-live-replays) for the control cells.

A debug-based table fixture keeps `documentId: "debug"` when it expects the
debug world's same-world portals to remain in its boot instance. Giving it a
different identity can open another `debug` instance through a return portal;
machine overrides in the fixture do not stop that other instance's machines.

A debug-based fixture none of whose claims reads a machine imports
`stopped-machines` (`worlds/debug/stopped-machines.puck`): every device stays
mounted and engageable but the host does not advance it, so the scenario does
not pay for emulating cartridges it never reads. Emulation and continuation
hashing are most of a debug scenario's tick cost. A fixture that reads some
machines stops the rest by name (`machine-debugger-tests.puck`), and a machine
added to the debug world is added to that fragment.

The arena is the live gameplay store. `WorldServer.Definition` holds declarations
and seeds; use `ExportDefinition()` only at an explicit snapshot/edit boundary.
Runtime value readers use `WorldStateReader` bound to the live arena, and
publication carries journal changes without rebuilding document rows. Rules,
bound addon batches and host cell commands share the grant-checked transaction.
Every untrusted read and delivery checks `WorldStateDisclosure` again; caching
a bound address never caches permission. Responses, deals and tenure are
placement projections. Checkpoints snapshot arena columns directly.

## Diagnostic reports and pins

Scripted camera framing uses `view.recenter [player]` (1-based), which resets
the live orbit and boom and answers without devices. `player.look.recenter` is a
held input binding with no text answer; it is not an operator reset.


`world.debug-view report colliders --json` and `world.debug-view report contacts
--json` are core commands: they run with the view off and in a headless host.
Coverage is serialized once at the report root; a picked finding carries its own coverage. Unknown coverage is a result, never a clean bill of health. Headless checks
compare the effective analytic colliders and retained support solves with the
authored solid field; rendered checks additionally require matching retained
opaque meshes. Dynamic supports and interpolated body poses without an exact
solver witness remain unknown. Rigid contacts retain a loaded manifold point;
snap reach is informational and never a hover tolerance.

Enable `world.debug-view colliders|contacts [focus|pins-only]` for the primary
view. `world.view.pick primary finding <id>` reads a retained causal record
even while its diagnostic view is off or another is active; run `report` first
to populate findings. `primary` resolves to the first seat's rendered instance
(`world` before presentation); explicit instance names and the normalized
`[<view-or-instance>] <x> <y>` pick form work too, and a pick with no view
addresses `primary` (`world.view.panes` names the presented view).
`world.debug-view goto <id>` requests an operator camera pose only. Reports
share stable cause IDs, current measurements, precision budgets, source
stamp/creation/node/operation and tick lifetimes. Changed reports enter
`host.log category world.debug-view.colliders` or `.contacts`, debounced.
See [scene diagnostics](../../../docs/reference/commands.md#scene-diagnostics)
for capture names and current coverage boundaries.

## The live World is shared

The `puck` MCP server is the agents' own debugging instrument (the owner's
ruling): agents fix and improve it as ordinary work, without asking first,
within reason, keeping it lean in what it returns and complete in what it
reports.

The World the owner pairs in runs the main
checkout's build and sources, not a worktree's. Reach it through the `puck` MCP
tools (in Claude, ToolSearch `select:mcp__puck__puck_adapter,mcp__puck__puck_worlds,mcp__puck__puck_world_start,mcp__puck__puck_world_start_wait,mcp__puck__puck_world_stop,mcp__puck__puck_exec,mcp__puck__puck_capture_frame,mcp__puck__puck_state_vector_write`):
`puck_worlds` lists the running Worlds, and `puck_exec`, `puck_capture_frame`
and `puck_state_vector_write` take a `world` argument (attachment id or
process id) that reaches exactly that World; name it whenever more than one
runs. Reads and captures are free. A mutation (`world.row.set`, `world.reload`,
`body.*`, `player.*`, `view.override`) changes what the owner sees: make one
only when the task allows it, and restore what you changed.

To run your own edits, start a World with `puck_world_start` (`checkout`: your
worktree's absolute path; `windowed: true` only for a granted GPU leg). The
call returns `pending` and a `startId` promptly. Poll `puck_world_start_wait`
with that id. A contended multi-lane GPU run can set `timeoutSeconds: 7200`:
the admission deadline includes compilation, the fair GPU queue and attachment,
so the former thirty-minute maximum expired behind other verification batches.
This extends queue admission, not the lane's twenty-minute running-World batch.
Each wait defaults to 20 seconds; `timeoutMs` allows up to 120000 in one
call, so a cold build needs few polls. Never repeat the start while pending. A pending
answer names its `stage` (`building` the World from the checkout's sources, `gpu-lease`,
or `booting`, with the World's last stderr line in `output`) and the seconds `elapsedSeconds`
since admission. A cold build continues between calls and across adapter updates.
`cancel: true` on the wait cancels an unfinished start. A cancelled poll only
ends that poll. Session shutdown cancels starts and stops its Worlds.
The tool resolves the World build of the checkout's current sources from the same
content-keyed store `puck test` and `puck canary` use, building it first when
no run has built that source state (an unchanged tree reuses its build), so it
never boots a binary older than the sources and documents you edited; a
failed build refuses the start with its first errors. Builds of different source
states queue on the machine's `build` lease, one at a time, and `backend: vulkan`
builds with SPIR-V (a separate build in the store) and passes `--backend vulkan`,
which the default Direct3D 12 build refuses. Its build is not the
worktree's `bin/Release`, so no manual build is needed first. Never hand-write that boot
line: the tool passes `--devices none` ([the ruling](#an-agents-world-opens-no-physical-device)),
a state directory of its own and `--control`, takes and holds the GPU lease
for a windowed World. A completed wait returns its `processId`. Name that World on
every call, read its stdout and stderr with `host.log` (`host.log category
sdf.mesh-bake`, `host.log since <seq>`, `host.log ticks <from>..<to>`), and end
it with `puck_world_stop`, which refuses any World the adapter did not start.
The World runs from the store's build, which holds it while the World runs and
leaves your `bin/Release` free to rebuild
([references/hosting-and-release.md](references/hosting-and-release.md)).

Codex discovers these tools through the session's tool inventory (search for
`puck`); its repository MCP configuration uses the same launcher as Claude.
A Codex lane launched with `--sandbox read-only` sees none of them; it needs the
default profile or `workspace-write`
([orchestration](../orchestration/SKILL.md#launch-capabilities)).
Antigravity names the same server `puck_operator` (its workspace plugin `puck`
registers the server `operator`), so its tools appear as `puck_operator/*`; it
loads their schemas lazily, so its brief says to read each tool's schema first
(orchestration, same section).
Use the tools directly before writing a stdin process wrapper.
The hook installs completed CLI builds through the launcher's signed local
development channel under `.claude/mcp-install`. A persistent front follows
activated builds without reconnecting the client; earlier backends retain
their World processes and route their stops until those Worlds and pending
starts end, then retire once their in-flight calls finish. Session shutdown
drains every remaining backend. Rebuild
`src/Puck.Cli` to publish adapter changes, then use `puck_adapter` to inspect
the answering backend's module id and installed directory. No publisher key,
Azure release or application-copy staging is involved. The main checkout's
`.claude/mcp-install` serves every session on the machine, the lead's
included: a lane proving an adapter change publishes into an install root in
its own worktree (`puck mcp --prepare-install --install-root <worktree>/.claude/mcp-install`)
and runs that front, never the main checkout's: activating an unfinished
adapter there breaks every session's tool results until `current` points back at
`last-good`. The stub counts each launch of a pending
version and rolls back after three unproven ones, and a client's protocol probe
plus its connect launch the front twice, so the front and its worker both clear
the health marker as they start. A build the stub rolled back has spent its
replay sequence: `--prepare-install` then keeps the installed version and says
`kept …`, and rebuilding `src/Puck.Cli` publishes a newer one.

`puck_exec.command` also accepts a newline-separated script: at most 64
nonblank, noncomment lines and 8192 characters total. The entire script reaches
one text session together. Each line waits for the preceding settlement, so
successive Simulation lines apply on adjacent ticks; include `world.wait` to
space them further. Reads see earlier writes. Scripts continue after refusals;
inspect the per-line `commands` array (one-based source `line`, `status`, and
`output` or `data`, plus flags when true; the command text is not echoed, since the
line number names it, and top-level `output` and `data` are omitted on scripts). A
script that ran is a completed call even when a line was refused (an unknown verb
included): its text names each refused line and why, and the aggregate `status` is
`refused`. A result names its `world` (attachment and process id) only when the
call named none. `timeoutMs` covers the entire script. Cancellation discards
queued lines but may leave dispatched changes; inspect before retrying.
Results expose native JSON output as `data` in place of `output`, including each
script line's `data`; null and false fields with documented defaults are omitted,
and `content[0].text` carries a short status so no payload is serialized twice.
`world.at --json` returns the completed tick and arrays of pending and ran lines
with tick, command, status and output. Use `world.at` for absolute ticks or
several commands at the same tick, and a multiline script for an ordered
command/wait/read sequence.

Keep reads lean: a large answer (`world.affordances`, `world.grants`) is narrowed
by `puck_exec`'s own filters, which never change what the command does and apply to every
line's answer: `lines` (one-based ranges such as `1-20,40`), `match` (lines containing a text,
ignoring case), `fields` (keys of `key=value` answers, or property names anywhere in a JSON
answer) and `maxBytes` (a cut ending in an explicit mark, with `truncated` set). `world.view.camera` answers a compact line (`full` for every
field, a key list for chosen ones), `help <prefix>` answers one synopsis line per
verb (`help --full <prefix>` for the whole text), and a sampling loop belongs in
one script rather than one call per sample. `world.view.pick <view> <x> <y>`
holds its call until a rendered frame answers, a paused World included; a view that
renders no frame is refused as unanswered when the call's deadline passes (10 seconds in a piped
session, where the refusal prints on stderr after the `pending` line on stdout), and neither hover nor a hover's
release replaces a waiting pick or erases its answer before the asking call reads it. A command text
with a newline is a script (`commands`, `isError` false); one without is an ordinary command whose refusal is `isError`.

## The model

Everything is data. A versioned JSON document (`puck.world.definition.v1`)
describes what runs; the engine validates, simulates, renders and replays it
deterministically. The world is one bootable experience: durable configuration
is a document field, live operation is a console verb, and there is no
`--flag` mode and no environment-variable surface. **A baked C# constant is the
same violation as a flag:** if different worlds would want the value different
(a sensitivity, clamp, radius, timing, speed, which button arms a mode), it is
a document field in its first commit. Legitimate constants are capacity bounds,
representation and determinism constants, and math.

The console is the control plane: process stdin drives verbs, stdout and stderr
echo results, and the on-screen console is only a mirror of that pipe.

A world is authored in `.puck` source. `Puck.World.Transpiler` (the world
vocabulary, a peer of the cartridge vocabulary over the `Puck.Transpiler` core)
lowers it to the same JSON. `PuckWorldLoader.TryResolveWorld` compiles a
`--world <x>.puck` path in memory through `WorldCompileCache` before composing
and validating it exactly like a JSON boot, and `world.reload` recompiles it
from disk. A world source has no committed JSON beside it; the build compiles it
into its output. Every construct of the world vocabulary is described once in
`src/Puck.World.Transpiler/Vocabulary/`, and `puck vocabulary` generates
[the inventory](../../../docs/reference/world-vocabulary.md) from it.

A rule is a `when` gate, a trigger `mode`, an optional `forEach`, and effect
statements. A deadline is a cell holding a due tick: `schedule` writes it and a
later rule gates on `$tick >=` it (the Moth's `boot-boost-*` and `blink-*` rules
are the live pattern), never a remainder decremented each tick:

```text
state {
  world {
    table armed { "0" = 1 }
    table cooldownEnd { "0" = 0 }
    table stale { "0" = 7 }
  }
}

rule "cooldown-arm" {
  when armed[$each] == 1
  mode: Edge
  forEach: armed
  schedule cooldownEnd[$each] in 2s   // scheduleState: Write of the due tick, folds as UpsertStateCell
}

rule "cooldown-expire" {
  when armed[$each] == 1 and $tick >= cooldownEnd[$each]
  mode: Level
  forEach: armed
  remove stale[$each]                 // removeStateCell: Remove, folds as RemoveStateCell
  armed[$each] = 0
}
```

`puck compile <file> --validate` compiles that source and runs the boot
validator over it. Every effect writes the tick's `StateArena` through the rule
frame and folds into an existing state mutation kind, never a path of its own;
the full effect table is in
[references/mutations.md](references/mutations.md#rule-effect-sugar-puck--state-mutation-kind).
`world.row.set` edits a live document row; it is not the way to author a new
rule. Grammar, units and the compile/lint verbs belong to `puck-dsl`.

## Projects

| Project | Owns |
|---|---|
| `src/Puck.State` (+ `.Generators`, `.Topology`, `.Rules`, `.Search`, `.Vectors`) | The state and rule engine beneath the document, with no world concept: sections, rows, cells, the expression IR, `StateArena`, the rule compiler |
| `src/Puck.World.Schema` | What a world is: `WorldDefinition` and its section records, `WorldDefinitionValidator`, serialization, document-embedded wire vocabulary (`PlayerIntent`, `WorldGrant`) |
| `src/Puck.World.Protocol` | What a world says: `WorldCommand`, `WorldMutation`, `SubmissionEnvelope`, `WorldSnapshot`, `IServerLink`, `WorldStateMirror` (every presentation read of state), the adjacency family |
| `src/Puck.Networking` | The wire substrate: `FrameCodec`, `WireReader`/`WireWriter` |
| `src/Puck.World.Server` | The authoritative simulation: `WorldServer` (the tick, the journal), `WorldGrants`, `WorldPopulation`/`WorldBody`, `WorldEngagement`, `WorldReplayTape`, `WorldHistory`, `WorldOutputHub` |
| `src/Puck.World.Console` | Server-side console modules (`world.grant`, `world.row`, `world.state`, `world.wait`, `replay.*`, `world.history`) |
| `src/Puck.World.Addons` | The scripting-guest addon host |
| `src/Puck.World.Machines` | The engine-neutral screen-machine host (`WorldMachineHost`, `WorldMachineCatalog`) |
| `src/Puck.World.Client` | The presentation seam: `WorldClient`, `SeatController`, `WorldSeatBindings` (over `Puck.World.Vocabulary`'s `WorldAffordances`), `WorldCameraRigCompiler`, `WorldFramePresenter`, the stamp pool. References Protocol, never Server |
| `src/Puck.World.Vocabulary` | The input vocabulary a world document is validated against (`WorldAffordances`), below Client |
| `src/Puck.World.Transpiler` | The world `.puck` vocabulary: `WorldCompiler`, `WorldCompileCache`, `Vocabulary/` |
| `src/Puck.World.Authoring` | The embedded content families (`puck.creation.v1` `CreationDocument`/`CreationCanonicalizer`) and the sculpting library |
| `src/Puck.World` | The sole composition root: `Program.cs` (every host flag), `PuckWorldLoader`, audio, the screen binder; it ships no world (the debug world is the package `worlds/debug/`) |
| `src/Puck.World.Silo` | The hosted multi-world silo (Orleans activation lifecycle only; game traffic rides the World's own wire) |
| `src/Puck.World.Browser` | The engine in a browser tab: a `browser-wasm` publish of Schema, State and the `.puck` toolchain |
| `src/Puck.World.AgentBridge`, `.AgentHarness`, `.AgentHarness.Azure`, `.Azure`, `.Embeddings` | Optional extensions (agent participants, Azure resource operations, text embeddings); no base world project references them |

`build/Architecture.props` enforces the layering (`PUCKARCH` diagnostics):
Schema never references Protocol or Server, Server knows nothing about
rendering or input, Client never references Server.

## Contracts that bite

**Native capture stays (owner ruling).** Gameplay video/audio clips and microphone
input are product capabilities even without a current world caller. Keep the
windowed `capture.start/status/stop` surface, `--recording`, recording document
loader/format, Windows encoder and loopback/microphone capture, and Linux
factories/registration. Capture and deterministic `replay.*` serve different
outputs; scheduler consolidation does not remove capture. Headless Worlds do
not compose these capture verbs. See [recording](../../../docs/reference/recording.md).

**Determinism.** No wall clock, RNG or float in simulation state; fixed point
from `Puck.Maths`. The simulation rate is a document field
(`WorldDefinition.Simulation.RateHz`, dividing 50400 exactly, default 30). Every
entity advances on the server from a `PlayerIntent`; poses never come from
outside. A deliberate correction to logic is expected to change replay hashes.
Client code is presentation: floats are fine there and nothing feeds back.
A `probes` row plays on the wall clock, so an `axis` binding (a probe channel
into the input router) makes every test world that imports it refuse
`puck test --reproduce`; the debug world's `beacon` probe (`probe-beacon.puck`)
uses `parameter` bindings, which write presentation only.

**The acting principal.** Every mutating ingress consults the acting principal
before any mutation. The ingress stamps identity (`SubmissionEnvelope.Principal`
on the wire, `CommandContext.Principal` for console text); handlers read
`context.Principal` and never construct a principal, which would launder an
identity. A refusal distinguishes what a grant composes from whether the subject
is legitimate for the actor. Client code never mutates local state before the
server's verdict. Trace the acting principal stamped at ingress when debugging
a refusal; constructing a `Principal` in a test bypasses the path under investigation.
[references/authority.md](references/authority.md)

**A toast narrates a player's own act.** `WorldToastPolicy` decides from the
echo's acting principal: a `Console`-stamped write or grant (stdin, an MCP or
control attachment, a sweep or schedule prelude, a session screen's admission
grants) reports through the console row, stderr and `host.log`, never the
toast. `world.hud toast` reads the toast store in any shape
([HUD](references/hud.md#verbs)).

**Read through the caller's disclosure.** A console read-back reads the
`WorldStateReadView` its acting principal is minted
(`IWorldConsoleAuthority.ReadView`), never `WorldServer.Definition` directly.

**One pipeline for change.** A `WorldMutation` buffers through the ordered
domain, drains FIFO at the tick boundary, composes a candidate, revalidates the
whole document, capacity-checks, swaps atomically, journals and delivers. Rule
effects write the tick's `StateArena` and publish once at the end of the tick.
Rendering derives from the delivered definition. The step order and the
add-a-kind procedure: [references/mutations.md](references/mutations.md).

**Paths resolve beside the document** that names them (`WorldDocumentPaths`);
shipped engine content resolves through `PuckPaths.Shipped`.

**An import names; the named file decides what it brings.** `import "skies"`,
never `import "skies.puck"` (PUCK121). A module library (a source emitting no
document) hands its `let`s and templates to the compile; anything else is a
document composed into the importer at load. A library imports only libraries
([composition](references/documents-composition.md#document-composition-basis-and-imports)).

**A composed console operation is a `commands` row, not a C# verb.** The
owner's ruling: console commands are easy to author and compose for safe
operations, without C# work for each. A document's `commands` section names a
command (`debug.go`), its typed parameters and the console lines it runs; the
registry answers it beside the engine's verbs (`help`, bindings, wheel
sectors, `run <name>`) and `world.reload` swaps the set. It runs each line
under the caller's own principal and session policy, calls only what a binding
may name, and never takes an engine verb's name
([reference](../../../docs/reference/commands.md#document-authored-commands);
code: `Puck.Commands/AuthoredCommand.cs`, `CommandRegistry.Authored.cs`,
`Puck.World.Schema/WorldConsoleCommand.cs`). Write a C# verb only for what no
composition of existing verbs expresses. The debug world's `places.puck`
(`debug.go <place>`) is the live example. Adding, renaming or changing the
bindability or audience of a C# verb owes `puck verbs` (regenerates the
catalog `puck compile --validate` checks authored commands against).

**Narrate through the hub.** Server never writes to `System.Console`; every line
is a `WorldOutputHub.Narrate` call, bound to stderr (or stdout for answers) by
the composition root.

**Mint generated names through `GeneratedName`** (`$` inside a document, `~` in
a path), never by concatenation.

**The screen binder's device work lives in `WorldScreenBinder.Device.*`**, the
prefix `build/CoverageHardwareOnly.txt` lists: what needs a GPU device or its shared
resources, the frame presenter, the render graph's running instances, or a
camera or capture handing over frames. `WorldScreenBinderLawTests` reaches every
line of the other binder files on the CPU, so a binder member that needs no
device lands there with a test.

**Adding an authorable feature owes, in one change:**

1. Search `src/Puck.World.Schema` for existing vocabulary first; the value
   often exists already. A camera tunable belongs to the seat camera path:
   framing and pitch limits in `views.seatControl` and the camera program's ops
   (`views.seatRig`), input feel in `seatDefaults.seatCameraFeel`
   (`WorldSeatCameraFeel`: optional `clearanceMode` override, pointer `yawSensitivity`/`pitchSensitivity` in
   radians per pixel, `stickLookRate`, inversion, gyro; absent means zero
   response). A seat reads the feel of the document that owns it: the world's
   for an unclaimed seat, the claiming identity document's own
   `seatDefaults.seatCameraFeel` for a claimed one. So a value for one seat (one
   player's preference, which travels with them) belongs in that identity
   document, and a value in a world's basis changes every world built on it.
   Its console row path is `playerDefaults.seatLook` and its read-back is
   `world.view.camera`.
2. Author the value as a document record with a default that preserves today's
   behavior. Behaviour is an operation, or an operation's parameter, in the
   program vocabularies (the owner's ruling): body movement in
   `bodyMotionPrograms` (the program carries its ops' parameters, as `target`
   and `planarTarget` do), camera framing and smoothing in the camera program's
   ops. Never add a knob to a kit or tuning record beside them; where a
   hard-coded behaviour blocks a program from expressing something, move it
   into an op the program authors.
3. Validate it in `WorldDefinitionValidator`, refusing by name.
4. Sweep the shipped worlds; parsing is strict and refuses unmapped members.
5. Add a read-back verb that echoes the decision (`world.why`, `world.grants`,
   `world.status`, `world.hud` are the pattern).
6. Fold any derived cost into `world.budget`.

Then regenerate with `puck schema` (JSON Schemas, the dashboard types and
`WorldModelShape.generated.cs`); never hand-edit those outputs.

## Running it

`host.frames` reads both windowed and headless host iterations. A headless `--unpaced` run takes one fixed tick
per iteration, so `world.wait 1` followed by `host.frames 1` isolates that tick's simulate time; warm the ordinary
simulation first when measuring a guest's first write separately from whole-engine cold boot. Check the reported
step count. In a paced run the pump can drain a released command between steps of the current iteration, while
`host.frames` reads only completed iterations: an echo immediately before the reading need not belong to that row.
Use the unpaced recipe for individual ticks; its machine-queue backpressure still contributes to simulate time.
Rendered phases are zero.

A World you drive call by call is a `puck_world_start` World
([above](#the-live-world-is-shared)). A whole script piped through stdin, with
its streams captured, is this recipe:

```text
dotnet run --project src/Puck.World -c Release -- --world worlds/debug --devices none --exit-after-seconds N --state-dir <tmp> < script.txt > out.log 2> err.log
```

### An agent's World opens no physical device

The owner's ruling: any World an agent boots passes `--devices none`; a World the
owner asked to play in passes `--devices all` explicitly, and the
`world-devices` hook refuses a boot that names neither. Without the flag
a windowed World opens every physical controller (GameInput, XInput, HID pads)
and keeps reading them while its window is in the background, so the owner's
pad presses drive the agent's test World (one boot opened the owner's Xbox pad
as player 1). Focus gating is rejected: the owner's whole-desktop feature needs
the pad read while another window is in front, so the default stays `all`, and
the choice is the operator's per run, never a document member (a document must
not decide whose hardware a run reads). `--devices none` opens no pad, registers
no gamepad manager, arbiter or capture, and drops every OS key, text and pointer
event the window receives before a seat sees it
(`WorldWindowInputFilters.ConsumesEveryEvent`). A framed desktop screen claims no
system-wide hotkey either (`WorldSourcePassthrough.ClaimsSystemChord`), so the
owner's Control+Alt+Escape never reaches the World. stdin, the console,
`player.signal`, `body.*`, schedule rows and MCP still drive the World. The
boot says `[world.host] physical input devices are off` on stderr; a stderr with
a `[gamepad]` or `[gameinput]` line means the flag was missed. A headless or
offscreen boot opens no device either way, and the flag is harmless there. The
verbs that boot a windowed or offscreen World for you (`puck canary`, `puck
parity`, `puck counters`, `puck verbs`, `puck docs citations`, `puck bench
startup`) pass it themselves (`WorldDevices.NoneArguments`). The owner's own World
(`.claude/launch.json`'s `debug-world`) explicitly passes `--devices all`. Never inject real input to
check the flag: the owner may be holding the pad.

- **The edit loop is hot reload.** The owner's C# loop runs the World under
  `dotnet watch` with the edited projects unoptimized
  (`--property:PuckHotReload=Puck.World.Client`, comma-separated; never `-p:`,
  which `dotnet watch` reads as `--project`): a body edit applies in under a
  second and prints `[world.hot-reload] applied revision N`, a rude edit
  rebuilds and reboots, and an edit to an unlisted project is refused until the
  watch restarts ([edit to running](../../../docs/development/contributing.md#edit-to-running)).
  A cache holding a product of code compares `CodeRevision.Current`
  (`Puck.Abstractions`) or keeps its entries in a `CodeDerivedTable`, and
  derives again when it moved; a persisted product folds
  `CodeRevision.AppliedTo` (over the types it reads) into its identity. A new
  such cache does the same. Laws that apply an update call `AppliedCodeUpdate`
  (`tests/Shared`) inside `AppliedCodeUpdateCollection`, which runs alone. An
  agent's verification still boots a fresh World.
- **Build first.** A failed build leaves the previous binaries in place, so a
  run after it exercises old code and shows nothing about the change, however
  well it behaves. The change is not verified until the build exits 0 after the
  last edit and the same script, rerun through this recipe with its own
  `--state-dir`, shows the behavior. Report what ran (build, command, script,
  what it showed); the commit body carries it.
- **Keep a windowed World's life short.** A windowed debug World holds about
  5.5 GB of working set and 8.5 to 10.5 GB of private bytes once booted, most
  of the working set the baked meshes' managed arrays and the irradiance
  scene's hierarchy (at about 30 million static triangles, about 1 GiB of mesh
  indices, normals, positions and triangle materials and about 0.55 GiB of
  hierarchy nodes and leaf order, by a ClrMD heap walk); read it with `host.memory` (`host.memory collect` for the reachable
  managed part) beside `Get-Process`. Several GB of those private bytes are the
  device's own heaps mapped into the process (write-combined pages with no
  residency), not system memory. Two windowed Worlds and a couple of builds
  still strain a 32 GB machine. Boot, pose, capture and stop in one
  batch of under 10 minutes; tune light values on a headless World or with
  `world.reload` inside a batch, never by holding a World open between steps.
  Arm a whole batch with `world.rate pause`, `world.at` scripts at absolute
  ticks and `world.rate resume`, since the World steps on between calls.
- `--exit-after-seconds` of 0 or less disables the auto-exit; absent uses the
  document's `host.exitAfterSeconds`. `--world`
  is required: a package folder (its `manifest.json` names the entry), a
  `.puck` source or a JSON document; without it the boot refuses. `Program.cs` parses the full flag surface;
  host flags are deployment overrides of the document's `host` section.
- `--state-dir <dir>` gives a hermetic state root; parallel runs each need
  their own.
- **Presentation modes** (`host.presentation`): windowed, `offscreen` (GPU
  composition to images, what `puck parity` boots) and `none`
  (`HeadlessWorldSimulation`, full authority, no GPU, so no capture). The Moth
  basis authors `Windowed`, so the debug world boots windowed. `--headless`
  (or `--headless true`) forces `none` for one run and `--headless false`
  forces windowed; offscreen is a document's `host.presentation`. Check the
  effective mode, overrides included.
- **Sharing the GPU.** A run whose effective mode is `none` uses no GPU: while
  another session holds the GPU grant for a parity, counters or windowed leg, it
  may run beside that leg with its own `--state-dir`, as may builds and other
  CPU work. Windowed and offscreen runs are GPU work and wait for the grant and
  an idle GPU (`puck host load` prints `GPU busy` or `GPU idle`). A process
  search of your own matches its own command line, so exclude it before
  concluding another job is running
  ([verification](../verification/SKILL.md#what-uses-the-gpu)).
- **Capture both streams.** Read-back answers land on stdout; refusals,
  narration, boot lines, capture announcements and `[world.mutation: …]`
  echoes land on stderr. A World you did not launch keeps its newest 4096
  lines of both in a ring that `host.log` reads over an attachment, each as
  `#<seq> t<tick> out|err <line>`; filter with `category <prefix>`, `text
  <word>` (quote several words), `stream err`, `ticks <from>..<to>`, `since
  <seq>` and `last <n>`.
- **Narrow a large read.** An MCP result carries 1 MiB, and `world.counters gpu`
  alone passes that in a world with many render-graph instances. Ask with
  `summary`, `node <name>`, `pass <label>` or `counter <prefix>` (they combine;
  [the rendering skill](../rendering/SKILL.md#performance-and-cost) names the
  forms), and a source name (`world.counters state`) for the rest.
- **The drain barrier.** A following immediate verb waits for pending
  simulation traffic, so write-then-read pairs need no polling.
  `world.wait <ticks>` holds the issuing session; a windowed script that reads
  rendered work waits on `world.wait ready <seconds>`, one that reads the baked
  frame (every residency's mesh-path bake done) on `world.wait bakes <seconds>`,
  and one that reads a capture on `world.wait captures <seconds>`. Each form needs its seconds deadline: a
  bare `world.wait ready` is refused as not a tick count, and the script then
  runs on without waiting. End a script with `quit`. Blank lines and `#`
  comments are skipped.
- **Encoding.** Pin `[Console]::OutputEncoding` and `$OutputEncoding` to UTF-8
  without a BOM (`[System.Text.UTF8Encoding]::new($false)`): a BOM written into
  piped stdin corrupts the first command.
- **Indexing.** `body.*` verbs and `world.grant body:<n>` take the 0-based
  entity index; `player.*` verbs take 1-based seat numbers.
- **Screenshots arm, they do not capture.** `world.screenshot <path.png>`
  echoes `pending` on stdout; the file is announced on stderr
  (`[capture] … -> <path>`). Fence a frame with `world.wait` before reading it.
  Compare windowed captures by changed-pixel count: outside the tick-exact
  procedure below two are never byte-identical, and inside it stills of one
  tick in fresh Worlds are, but for a 1-level residue on a few pixels.
- **A capture is a settled still unless asked otherwise.** The ordinary capture
  (`world.screenshot`, `puck_capture_frame`) holds presentation and lets
  temporal views converge, so it never shows flicker, ghosting or trails. For
  those, read what the display presented: `puck_capture_frame` with
  `mode: "presented"` and `frames: 8` (optionally a `region`), or
  `world.screenshot <path.png> presented 8`, which report each frame's changed
  pixels and luma change against the one before
  ([console](references/console.md#settled-stills-and-presented-bursts)).
- **Patrol an area to see the body.** `world.patrol <x0> <z0> <x1> <z1> <step>
  [yawDegrees|-] [settleTicks] [y|-]` on a windowed World poses body 0 at each grid
  point of its current level (`y` names another level's floor height) and picks the centre of the first seat's rendered view
  (more pixels about it where the centre misses the body). It answers with the tick
  its `world.at` script ends at; `world.wait until <tick>`, then `world.patrol` gives
  a summary and a line per flagged point (`OFF BODY`, `OCCLUDED` by an exhibit, `NO
  ANSWER`, `STALL`), `world.patrol all` every point. A pick names `body=<index>` for a
  body and `placement=<id>` for a placement (a pick answer also names `prototype=` and the
  `materialName=` palette entry). `world.patrol stop` clears every armed
  `world.at` line, not only the patrol's.
- **Capture motion on exact ticks.** `puck motion` does it for the Moth in one
  command (scenario file `worlds/debug/motion.scenarios.json`, contact sheets,
  `--reproduce`); the rest of this item is the procedure under it. Calls over MCP land wherever the World
  has stepped to, so a script whose inputs and stills must land on exact ticks
  is armed in one line with `world.at` and waited for with `world.wait until
  <tick>`; `world.lockstep on` makes a windowed World's presentation repeat
  with the ticks, and `view.reseed <body>` beside a `body.pose` restarts its
  gait. Every settled still names its tick and state hashes
  (`[still] … tick= hash= pose= shown=`), and `slots` writes each viewport of a
  multi-camera layout. The procedure and what repeats:
  [tick-exact debug capture](references/schedules-and-tests.md#tick-exact-debug-capture).
- **A denial check needs a control.** Pair it with an actor who holds the grant
  and succeeds, and keep actor and target different (every seat is seeded wide).
  For a fixture whose other player's row is `state:players$other`, inspect
  `world.why peer:1:1 edit state:players$other`; the peer must be admitted and
  must not own that target. Trace the actual ingress-stamped principal too.
- **Pixels are not a replay proof.** `replay.verify` MATCH proves the hashed
  authoritative state trajectory, not the HUD or the image
  ([references/replay.md](references/replay.md)).
- `puck test <source>` boots each `.puck` `test` block headless and prints one
  verdict per line ([references/schedules-and-tests.md](references/schedules-and-tests.md)).
  A scenario is for an invariant that running cannot show: a replay or
  reproduction, an exact fixed-point or timing result, a refusal or atomic
  rollback and its control, an input release barrier, a body or register
  crossing documents, or a rule edge case only a constructed position reaches.
  A feature or exhibit (a lift's schedule, a lever's values, a companion's
  flight, a tool's report) gets no scenario by default, and a brief asks for one
  only by naming its invariant; a feature is shown by
  running it, and the debug world's sweep is its signal
  ([decision](../../../docs/decisions/engine-design.md#the-debug-world-is-the-engines-instrument)):
  `puck sweep` reads the tools, reports, budgets and counters on a headless
  World (booted with `--paused` before its first tick and held between calls,
  so its ticks repeat), `--tour` (or `--attach <world>`) the rendered signals
  and the capture tour (each still pinned to a named tick, lockstep on,
  framing and reseeding pinned beside the motion with `world.at`, and every
  eventual answer checked), and a new signal or tour stop is a row of
  `worlds/debug/sweep.json`. `--cache-dir` lets fresh owned Worlds share a
  writable lane scratch cache; omitted, it uses the per-user cache. Cache work
  counts are recorded, while exact boot comparisons select cache-independent
  counters. Whatever it could not measure
  (a closed attachment, a spent `--timeout`, a metric a rule reads that the
  answer lacks) is reported unmeasured and fails the run like red
  ([CLI reference](../../../docs/reference/cli.md#puck-sweepthe-debug-worlds-sweep)).

After an attached sweep tour, check `body.where 0` and `world.rate` before another
reproduction: the tour leaves authority paused and the seat in its final
destination (the night field in the debug plan), rather than the boot world.
An unqualified `body.pose` then moves that destination's body.

`WorldPoseInterpolation` preserves identical snapshot positions exactly and
normalizes identical orientations without blending them. Weighted endpoint sums
can move equal floats as presentation alpha changes; local, neighbour and session
body consumers share this guard so stopped attachments stay still.

Verify game behavior by running the game (`AGENTS.md` rule 3). Write a test only
where running cannot show the behavior. Standalone runners, record directories
and `--validate-*` flags are banned.

Smoke session:

```text
printf 'world.status\nbody.where 0\nworld.grants console\n' |
  dotnet run --project src/Puck.World -c Release -- --world worlds/debug --devices none --exit-after-seconds 6 --state-dir "$TMP/puck-state"
```

## Subsystem index

| Working on | Read |
|---|---|
| Document schema, serialization, validators, profiles, binding layers, capacity constants | [documents.md](references/documents.md) |
| Tick order, mutation kinds, journal and undo, rule sugar lowering | [mutations.md](references/mutations.md) |
| Grants, principals, verdicts, budgets, refusals, `world.why` | [authority.md](references/authority.md) |
| `SubmissionEnvelope`, the one queue, completions, echo routing | [ordered-domain.md](references/ordered-domain.md) |
| HUD schema, overlay reservation, bindings, HUD verbs | [hud.md](references/hud.md) |
| Camera rigs, seat control and seat camera feel, layouts, `world.view.*` and `view.override` | [views.md](references/views.md) |
| Boundaries, federation, handoff, crossing logs | [adjacency-and-federation.md](references/adjacency-and-federation.md) |
| `body.engage`, control applications, sitting at a tabletop (board `engage`, `board(pointer, …)` and its seat reads, the board view), machines, a machine's `contentFolders` (shipped and local, which may be absent), `machine.swap`, a folder's local boot default (`folder.json`, `machine.default`, `preferFolderDefault`), the debug world's device row | [engagement.md](references/engagement.md) |
| Join, leave, park, resume | [session-lifecycle.md](references/session-lifecycle.md) |
| The replay tape, verify semantics, `world.history` | [replay.md](references/replay.md) |
| Addon rows, mount transaction, channels, fuel | [addons.md](references/addons.md) |
| Command modules, routing, output contract, screenshots | [console.md](references/console.md) |
| Render validation, stamp capacity, rigid/carry/tether facets | [documents-render.md](references/documents-render.md) |
| Navigation, the tabletop primitive, records and pools | [documents-state.md](references/documents-state.md) |
| Boot-only sections (gravity, portals, simulation rate, references), `basis`/`imports` composition, the validator, serialization, the sculpting library | [documents-composition.md](references/documents-composition.md) |
| How a body's look animates: creation drivers, swings, effectors and look followers, all read in `WorldCreationInstances.PackTransforms` (presentation only); the moth's turning, directional gait and stepping feet are authored there, never in client code | [documents-composition.md](references/documents-composition.md), [sdf-authoring rig](../sdf-authoring/references/rig.md#how-the-moth-moves) |
| Extensions (`IPuckExtension`, `PuckExtensionSet`, installed `extensions/<name>/<name>.dll`), agent participants, the silo, MCP, release | [hosting-and-release.md](references/hosting-and-release.md) |
| `captures`, `schedule`, verdict rows, `puck test` | [schedules-and-tests.md](references/schedules-and-tests.md) |

## Limits worth knowing

- Rigid creation copies share one local bake and palette. Each live copy owns one root transform and one draw; articulated creations add only independently moving part slots. Storage grows from the live world, without a fixed registration or per-creation shape budget. Catalog geometry emits only for looks in use, with detail chosen by projected size. The actual render envelope, GPU draw/vertex counters, baked groups and resident bytes describe the cost. Scope depth is 4, screen bindings 32 and bounded volumes 64; representation overflow refuses explicitly.
- XInput caps at four pads locally; HID pads are uncapped.
- The debug world uses the analytic contact provider (`collision.requirements`
  empty): spheres, circular cylinders and Boxes have surface contact. A Box
  collides with its authored `rounding` (sharp without one); chamfered Boxes use
  their exact lifted-profile support map, including deep bevels and the
  cap/profile corner. Superellipsoids use their Lp surface (the chair seat
  and back are exponent 4, not Boxes). Rounded/chamfered circular rims use
  contained cylinder cores with a computed inward-error bound; diagnostics
  name errors within it as known approximations, red beyond it, and never
  apply that bound to outward error. Other finite primitives use
  oriented bounds. A creation with relief (`noise`) collides as its drawn
  surface: one field collider per copy over the creation's own fixed-point
  program, the valley's walls included
  ([sdf-authoring](../sdf-authoring/references/shapes.md#contact-admission)).
  The Moth's capsule has a 0.35 m radius and is 2.06 m tall;
  sharp and rounded boxes use closest segment/box features. Lateral edge/rim
  approach requires enough step height to clear the local touched edge plus
  its fillet radius, never the distant apex of a tilted ramp; an edge witness
  at or below the pre-move foot remains walkable support;
  resting and falling still meet the rounded surface. Every
  boolean carve in an unrelieved analytic creation collides as the uncarved
  shape; relieved field colliders retain the authored blends. Build a doorway,
  window or stairwell as a union of boxes around the opening, never a
  subtraction, and keep 2.4 m of headroom over every tread and landing (her
  height plus the 0.3 m step-up raise). `worlds/debug/hall.puck` is the
  worked building: switchback stairs of 0.25 m risers, slabs holed by unions,
  and a lift.
- Input has independent budgets of 32 numeric axes and 64 packed buttons. The
  debug modules import one vocabulary in `worlds/debug/inputs.puck`; chess uses
  shared `confirm` and `cancel`, independently of machine `select`. Resolve
  names through `WorldChannelTable`: a declaration index is not a storage
  address. Target-register reach has its own mask and budget. Relative input
  shares the numeric bank as Q32.32 displacement: use the table's typed reader,
  never a held-level reader. The host accumulates samples and drains once per
  routed tick; rules read a Q48.16 projection with authoritative fractional
  residue. Binding compilation must receive the routed channel shapes.
  [Input channels](../../../docs/decisions/input-channels.md) owns this model
  and its authoritative modes, release barrier and timed history.
  Switching modes releases by default; declared same-meaning holds and toggles
  may continue, while changed meanings and transition edges never cross the
  epoch barrier.
- A kit whose collider differs from the body's last one (a kit `select` by a
  body register: the suit, noclip) steps the body to the nearest pose up its
  axis or along world X or Z where the new volume is not embedded
  (`WorldBody.EscapeEmbedding`), never down: the ordinary solve's shallowest
  push from deep inside a box can be down through the floor. The debug world's
  noclip (`worlds/debug/noclip.puck`) is a collider-less free-flight kit
  selected through the `form` register (suit + 2 × noclip).
- A moving floor is an attached solid placement riding a body (`attach` plus
  `solid`, analytic provider only); a body grounded on it rides its translation
  and yaw through the same narrowphase and slope test as ordinary contact.
  `motion.groundSnap` follows downward surfaces within an authored reach;
  jump and launch operations release grounding. The gallery
  lift moves its car body with a rule that `poseCell`s it along a box topology
  of 1/16 m layers each tick, so its speed and floor stops are exact.
  Its numeric attachment index must track population capacity and import order:
  the gallery shares `galleryPopulation` between its capacity and lift body,
  which is immediately below the companion imported ahead of it.
  A stale index can attach the platform to a different inhabitant while the
  placement-keyed car still moves; inspect `body.where` before changing physics.
- An attached placement can also `respond` to state: the shown prototype and
  its colliders swap while its attachment stays intact. The lift's car doors
  and indicator use this; `inhabit` and `faceSources` still refuse `respond`.
- A moving carrier or a solid response swap wakes only the parked rigid bodies
  whose bounds, grown by the contact reach (two contact skins) and the rigid
  support probe's travel, meet the box its changed colliders cover; any other contact-field
  change wakes every one. A ride or a door that lags the tick shows as
  `world.counters physics.bodies` advances per tick far above the idle count
  ([server README](../../../src/Puck.World.Server/README.md)).

## Route adjacent work

| Skill | Route there for |
|---|---|
| `puck-dsl` | `.puck` grammar, modules, units, the compile/lint/format verbs, PUCKnnn diagnostics. |
| `sdf-authoring` | Creation shapes, materials and rigs. |
| `rendering` | The renderer and SDF VM the frame source feeds. |
| `gaming-bricks`, `rom-forge` | Emulators behind engaged screens; cartridges. |
| `maths-usage` | Fixed-point primitives on simulation value paths. |
| `verification` | The landing bar, the private CLI copy, GPU grants and flake-versus-failure. |
