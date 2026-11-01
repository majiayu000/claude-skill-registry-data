---
name: gaming-bricks
description: "Fixes Puck GB/GBC/GBA and NES/Famicom (HGD) emulators: CPU, PPU/STAT timing, APU, links, snapshots and Post batteries (--cosim, --filter). Cartridges: rom-forge."
---

# Gaming Bricks

Treat the GamingBricks as one deterministic machine family: a shared SM83
compatibility core covering every DMG/MGB/SGB/CGB/AGB hardware revision
(`src/Puck.HumbleGamingBrick`), plus the separate ARM7TDMI-based GBA-native core
(`src/Puck.AdvancedGamingBrick`). `src/Puck.Machines` holds what both share:
snapshots, the instance/fork/pool lifecycle, queued hosts, link groups. The Humble
Gaming Deck adds the NTSC NES/Famicom console on the same substrate; its master
tick is distinct from either handheld clock. Read its
[manual](../../../docs/emulation/hgd/README.md) and run
`Puck.HumbleGamingDeck.Post` for changes to that core. The current implementation
and its Post stages are authoritative; update stale skill guidance in the same
change.

## Core invariants

- Advance emulated state only from integer clocks and explicit inputs.
- Keep configuration in constructor parameters or CLI options, never environment
  variables. AGB diagnostic hardware/trace overrides live in `AgbMachineOptions`;
  preserve them across forks and include behavioral options in typed snapshot identity.
- Preserve direct embedding through the public synchronous `AdvancedGamingBrickCore`
  and `HumbleGamingBrickCore` APIs and default factory composition. The shared
  [Machine hosting runtime](../../../docs/emulation/shared/machine-hosting.md) owns
  the host contract; both Post `embedding` stages
  exercise it without a worker, renderer or audio device.
- Keep firmware identity separate from startup mode. `MachineBootMode.Fast` skips startup without discarding the
  selected image; AGB still executes runtime BIOS services from that image. Explicit low-level diagnostic inputs
  remain supported. Bundled images are generated ahead of packaging, never by a runtime-to-Forge dependency.
- Keep floating point and host timing beyond a one-way presentation seam.
- Express console differences through capability gates (a named question on
  `ConsoleModelExtensions`), not forked SM83 cores and not a revision switch inside
  `Sm83`, `Ppu` or `Apu`. A fix that needs no model question needs no gate.
- Preserve snapshot, replay, fork, and cross-machine link determinism.
- Keep every idle fast path exact: an absorbed quiet stretch, a display ticked
  alone, or a halted span leaves the state the reference stepping would.
  `ComponentClock`'s `absorbsQuietStretches: false` and single `Step` calls are
  the references; `ColourIdleEquivalenceLawTests` and
  `AdvancedIdleEquivalenceLawTests` compare them over the shipped cartridges.
  A ticked cycle withdraws both cached clock agreements, including the
  others-only bound: rejoining the display to a stale bound can skip a timer
  edge.
- External suites, co-simulators, Post stages and golden replays are evidence
  about the hardware model. A stage or replay that a better-sourced correction
  moves is updated with the correction.

## Contracts that bite

- **Lockstep presentation completes machine steps.** The World selects
  `IMachineRuntime.Advance` through `WorldMachineHost.SynchronousSteps` while
  `world.lockstep` is on. Ordinary presentation keeps asynchronous `Submit`.
  A source upload's publication number identifies the upload, not the native
  frame its worker finished: compare `WriteFrame`'s version and bytes when
  diagnosing screen or screen-light repeatability. Adding a GPU fence wait can
  hide a late worker frame without fixing its completion boundary.

Each is detailed in [references/hardware-and-oracles.md](references/hardware-and-oracles.md).

- **STOP and EI are oracle conflicts, not bugs.** `ExecuteStop` (`Sm83.Decode.cs`)
  consumes STOP's pad byte (PC+2) only when no interrupt is pending (`IE & IF`,
  independent of IME) and leaves it when one is latched. The SingleStepTests/sm83
  corpus models STOP as one byte and re-arms EI when IME is already set, so
  families `10` and `fb` are documented oracle-conflict skips in the `sst-sm83`
  stage, never silent exclusions. The Tier-A `sm83-stop-pending-interrupt` stage
  covers the pending edge; the acceptance `ei_sequence` ROM pins EI.
- **The GB PPU schedule is one coupled contract.** Mode transition, polled STAT,
  VRAM and OAM locks, the mode-0 interrupt, the LY-comparison pulse and the
  fetcher order move together. Never tune one lag constant alone, and never move
  the PPU onto SameBoy's dots: the decompositions are measured and refuted
  ([Refuted PPU schedule decompositions](../../../docs/emulation/hgb/post-and-conformance.md#refuted-ppu-schedule-decompositions)),
  and the screenshot corpus is the gate. Acceptance cases that pin it by name:
  `hblank_ly_scx_timing`, the `intr_2_*` family, `intr_1_2`, `stat_irq_blocking`,
  `lcdon_timing`, `lcdon_write_timing`.
- **Timer before serial at equal timestamps**, and serial edges follow the free-running
  DIV counter, never the moment SC is written (`link-churn` and `boot_sclk_align`).
- **A `--cosim` run under about 60 frames proves nothing** (the boot logo scroll
  dominates it). Give a CPU-stream comparison at least 120 frames and check that the
  record count differs per ROM before believing a clean result.
- **Know which AGB BIOS ran before blaming firmware.** Advanced Post
  diagnostics (`--render`, `--trace-crash` and the rest) boot the
  bundled Puck firmware unless `--bios` names another image, as a World does;
  only the battery runs the zeroed stub, where any SWI or IRQ runs off into
  zeroed BIOS memory. A hosted core or `AgbLinkSession` console that stops
  being able to run (Undefined or Abort mode, a fetch from a region with no
  code) throws
  `AgbExecutionFaultException`, which `machine.state` shows as `fault=`.
- **Every core's framebuffer is packed `0x00RRGGBB`** (`ITimeTravelMachineCore.Framebuffer`, red in bits 16-23;
  the advanced brick sets the alpha byte), because the queued worker repacks it for the World's screens in that
  order. A PNG or a hash of the image goes through `FramebufferRgba.Pack` (`Puck.Machines.Post`), never
  `MemoryMarshal.AsBytes` of the words, which spells blue first.
- **Snapshot layout is one list per component.** Every component lists its fields
  once in a `TransferState` (a Humble mapper's `TransferRegisters`). No file
  records the layout; a deliberate layout change raises `CurrentVersion` of
  `MachineIdentity` (Humble) or `AgbMachineIdentity` (Advanced).
- **Deck boards own offsets, not memory, and time from bus edges.** NROM,
  MMC1 (`HgdMmc1`) and MMC3 (`HgdMmc3`) keep every RAM byte, the battery save's
  layout and its snapshot order in one `HgdBoardMemory`; a new board does the
  same. Board timing comes only from `IHgdMapper.ObserveM2` and
  `ObservePpuAddress`: MMC1's consecutive-cycle write rule counts M2 falls, and
  MMC3's counter clocks on a PPU A12 rise after three whole low M2 cycles. A
  board's laws live in `BoardLawTests`, and its fixture joins
  `PostMachine.Fixtures`, which the determinism, fork and mid-instruction replay
  stages all run. A Deck cycle's transaction runs at the read point mid-M2 and
  its write lands as M2 falls, with the interrupt sample; the `blargg-suites`
  and `accuracy-coin` stages are the judge of Deck timing (owner ruling in the
  [Deck manual](../../../docs/emulation/hgd/README.md#how-accuracy-is-judged)),
  never another emulator or a game's look. A Deck program that clears the CPU's I flag inhibits the APU
  frame IRQ (`$4017 = $40`) first, or the shared IRQ line never drops.
- **GBA multiplayer SIOCNT has an unmodeled ready line.** `AgbSerialController.PackSioControl`
  does not derive the SD/SI bits from cable-partner presence, so a program that
  polls the ready lines to find a partner never sees one. No committed stage
  covers a partner-polling program; the Tier C `link-replay` and `link-churn`
  micro-ROMs poll IF with IME off. Implementing the bits adds a stage for it:
  derive them from the modeled `AgbLinkCable` partner, never from ambient state,
  update the reference, and close the gap in
  [open items](../../../docs/plans/machines-and-cartridges.md#open-items).
- **Tests never depend on a commercial ROM or a retail BIOS** (owner ruling). A
  stage, test or CI step runs on committed sources and the fetched homebrew and
  test-cartridge corpora, and a stage whose only input is a licensed image is
  deleted, not kept (a retail-BIOS control inside a stage runs only when `--bios`
  names one by hand). A commercial ROM or retail BIOS is a local, by-hand input to
  a diagnostic (`--render`, `--bios`) and stays out of the repository, its builds,
  packages, logs and commit messages. A
  world device boots one only as the owner's local default: the git-ignored
  folder's own `folder.json`, written by `machine.default` (`puck-world`,
  [engagement](../puck-world/references/engagement.md)), so nothing committed
  names it.

## Workflow

1. Identify the affected machine and capability: shared SM83 compatibility in
   `Puck.HumbleGamingBrick`, or native ARM7TDMI GBA in
   `Puck.AdvancedGamingBrick`.
2. Read the relevant hardware contract and inspect the current implementation,
   stage registry (`PostStages.cs` in each Post project), and Post README. Do not
   infer timing from names or old stage counts.
3. Make the smallest hardware-model change that explains the evidence. Keep
   clock conversions exact, event ordering explicit, and snapshots complete.
4. Show the change working by running the Post stages it reaches in Release
   (below), or by booting a cartridge that exercises it. Diagnostic flags
   (`--stat-trace`, `--render`, `--cosim`) explain a run; they are not a verdict.
   Add a self-checking stage only where running cannot show the behavior.
   No file records an expected outcome: a corpus ROM that fails today fails its
   stage on every run until the emulator is corrected, and
   [the machines plan](../../../docs/plans/machines-and-cartridges.md#open-items) tracks them.
5. Report the exact commands, selected stages and asset-gated skips.

## Test a hosted machine with the debugger

Start a headless worktree World with devices none and use the debug world's
[machine debugger](../../../worlds/debug/addons.md#machine-debugger). Set its screen,
body and hardware RAM range while run is zero, pose the driver beside the screen
from the host, then set run=1. It uses ordinary engagement and player input folding,
checks native progress, compares neutral/held RAM, restores a checkpoint, compares
two program traces, and swaps/ejects through provider operations. Read each machine's
summary and per-check ticks, host.log and machineDebuggerViolations; use world.addons
for last/peak/total fuel. Run=2 plays runtime segments; run=3 fuzzes a seeded window.
No game addresses or title knowledge belongs in this guest.

The debug world runs 30 world ticks per second, holding inputs across about two native
frames. Hash/probe reads drain workers; checkpoints preserve their rational cycle phase,
so these generic checks need no extra frame-stamped input seam. Every queued core
implements pure `PeekByte`/`PeekBytes` (AGB's reads bus inspection, including byte
lanes of 16-bit IO registers); the inherited default peeks zero and hides live RAM.
The focused hardware-access law checks nonzero bytes and native progress after restore.

The authored machine-debugger-tests.puck runs bundled diagnostic cartridges, with a
withheld-input responsive failure as a negative control. All default cartridges also
need a live headless pass: a diagnostic passing does not prove an arbitrary game handles
a particular button. Record from boot before any addon steps when investigating a
failure with replay.drive; the addon receipt and machine inputs reproduce the check.

## Run it

The batteries are CPU-only executables; none opens the GPU.

```powershell
dotnet run --project src/Puck.HumbleGamingBrick.Post -c Release -- --fetch-corpora
dotnet run --project src/Puck.HumbleGamingBrick.Post -c Release -- --filter <stage-text>
dotnet run --project src/Puck.AdvancedGamingBrick.Post -c Release -- --tier A
```

`--fetch-corpora` fills the pinned corpus cache once. Iterate with `--filter` or
`--tier`; Tier A needs no assets, Tier B runs over the fetched corpora, Tier C
covers serial, link and infrared exchange. A stage whose asset is absent skips
(`--require-assets` turns that into an infrastructure failure), and the report
lists every skip. Report stage and skip counts from stdout; exit 0 alone does
not prove a stage ran. Exit 0 is pass or skip, 1 a failed check (a corpus ROM that does
not pass included), 2 infrastructure. `tests/Puck.HumbleGamingBrick.Tests` and
`tests/Puck.AdvancedGamingBrick.Tests` run their battery with an empty corpus cache,
so CPU suites cover the self-contained stages (and the cores they check). The
`Puck.*.Post` harnesses are outside the 100% coverage denominator.

## Load references selectively

- Read [references/hardware-and-oracles.md](references/hardware-and-oracles.md)
  for clock and event ordering, serial and timer edges, snapshots, GB PPU
  timing, oracle conflicts, and the documented GBA ready-line gap.
- Read the
  [`Puck.Machines.Post` README](../../../src/Puck.Machines.Post/README.md)
  first when a change touches stage or verdict semantics rather than one
  brick's own context — the shared battery scaffold both Post projects close
  over: `PostBattery<TContext>`, `IPostStage<TContext>`, `PostVerdict`,
  `PostTier`, `HashDivergenceReport`, `CorpusManifest`, `CoreEmbeddingProbe`.
- Read the
  [Humble Post README](../../../src/Puck.HumbleGamingBrick.Post/README.md) for
  tiers, the corpus suites and their per-case result rules, BESS, `--dump-snapshot`,
  `--hash-divergence` and the co-simulation workflow.
- Read the
  [Advanced Post README](../../../src/Puck.AdvancedGamingBrick.Post/README.md)
  for current tiers, assets, ARM/GBA diagnostics, co-simulation normalization,
  and the accuracy workflow.
- For a rendered accuracy check rather than a Post stage, write a framebuffer with
  Humble Post `--render <rom> <out.png> [frames] [dmg|cgb|agb]` and compare it
  by eye or against a reference capture. The authored comparison worlds
  (`hgb-compare.puck`, `hgb-mirror.puck`) are quarantined under `experimental/`
  and are not run. No test, tool, or asset names a licensed image, not even as a
  default path.

## Route adjacent work

| Skill | Use when |
|---|---|
| [`maths-usage`](../maths-usage/SKILL.md) | Selecting or changing deterministic numeric primitives shared with emulator state. |
| [`maths-laws`](../maths-laws/SKILL.md) | Authoring law-suite coverage for a changed public `Puck.Maths` member. |
| [`content-search`](../content-search/SKILL.md) | Finding stage names, registers, opcodes, ROM identifiers, or timing constants textually. |
| [`symbol-analysis`](../symbol-analysis/SKILL.md) | Resolving semantic C# references, implementations, or rename and deletion safety. |
| [`puck-world`](../puck-world/SKILL.md) | Integrating an emulator into world/session behavior beyond the emulator-host seam. |
| [`rendering`](../rendering/SKILL.md) | The renderer, SDF and shaders that present a machine's framebuffer; the emulator itself has no GPU path. |
| [`rom-forge`](../rom-forge/SKILL.md) | Authoring or compiling the cartridge under test — `puck.cartridge.v1`, the `.puck` DSL, or the native CGB/AGB compilers, rather than the emulator core executing it. |
| [`verification`](../verification/SKILL.md) | The landing bar, building before testing, and reading a flaky versus failing leg. |
