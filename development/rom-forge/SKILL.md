---
name: rom-forge
description: "Authors and compiles Puck cartridges (puck.cartridge.v1, *.cgb.puck, *.dmg.puck, *.agb.puck, forge.play, forge.open, puck compile --validate), native compilers, cost. Emulator core is gaming-bricks."
---

# ROM documents and native compilers

A map of cartridge authoring: where it lives, the contracts that bite, and how
to see a cartridge run. When this file and the code disagree, the code wins and
this file is corrected in the same change.

## Where things live

| Thing | Where |
|---|---|
| The `puck.cartridge.v1` model, validation, canonicalization, the `CartridgeDraft` editor, `ICartridgeCompiler`, the cost model | `src/Puck.GamingBricks.Forge` (`CartridgeDocuments`, `CartridgeValidation`, `CartridgeCost`, `CartridgeLimits`); its README has the source contract |
| The cartridge `.puck` vocabulary | `src/Puck.GamingBricks.Transpiler` |
| Native SM83 compiler for the cgb and dmg targets (code, 2bpp tiles, maps, palettes or shade registers) | `HgbCartridgeCompiler` in `src/Puck.HumbleGamingBrick.Forge` |
| Native AGB compiler (Thumb code, mode-0 4bpp graphics) | `AgbCartridgeCompiler` in `src/Puck.AdvancedGamingBrick.Forge` |
| Shared audio compilation | `AudioDocumentCompiler`, `ApuNotePeriod` in the shared forge package; `TuneRom.Build` for world audio |
| Boot ROMs | `BootRomBuilder`, `BootDivPrediction`, `BootRomLayout` in `Puck.HumbleGamingBrick.Forge`; the native ARM7TDMI firmware in [`Puck.AdvancedGamingBrick/Firmware`](../../../src/Puck.AdvancedGamingBrick/Firmware/README.md) |
| The in-engine console | `src/Puck.World/ForgeCommandModule.cs` (`forge.new/open/show/set/remove/undo/check/build/save/export/play`) |
| Shipped sources | `worlds/debug/cartridges/<target>/*.<target>.puck` (one folder per target, `cgb/`, `dmg/` and `agb/`, which a world lists in a machine's `contentFolders`), authored source only; `shared/` holds the modules several targets import, each declaring `schema: "puck.cartridge.v1"` so a world-source walk of the package never takes it for a world module |

Both compilers consume the same rules, variables, sprites and input conditions.
Source data determines behavior: never add a game-name switch or copy gameplay
into a C# template. `Puck.GamingBricks.Forge` depends on Abstractions, Assets and
`Puck.State`, never on World.

## From source to a running cartridge

1. Edit the `.puck` source.
2. `puck compile <name>.cgb.puck --output .claude/scratch/<lane>-cartridge.cartridge.json --validate`.
   `--validate` runs `CartridgeDocuments.Validate` over the lowered JSON;
   lowering alone proves only that the source was well formed.
3. In a running `Puck.World`, `forge.open <file>.cartridge.json` loads the
   compiled JSON as the console's draft, then `forge.play <screen-index>
   <file>.cartridge.json` hot-loads the draft into a screen. `forge.open` reads JSON only; machine content binding accepts authored `.puck`
   sources directly.
   `forge.play` needs a draft first (`forge: create or open a draft first`
   otherwise), and its path is an output: it writes the draft's canonical source
   there, then inserts it, and refuses a path not ending in `.cartridge.json`.
   A world screen whose `source` is a machine may instead name the
   `.puck` source as its `contentPath`; its content provider resolves imports
   and compiles the source at bind.
4. Look at it with `world.screenshot`. Cartridges are verified in a
   world, never in a bespoke driver.

`puck decompile <name>.cartridge.json --output <name>.cgb.puck` turns a document
back into source; the source it writes compiles back to the same bytes.

The owner's ruling treats cartridge JSON twins as derived caches: never commit
them or compare a run against them. Commit the authored source, compile when
needed, and keep semantic compile/decompile round trips over freshly compiled
documents. The machine content provider accepts source directly; the forge
console still opens a compiled JSON draft.

`forge.play <screen> <path>` saves the source and inserts it through the
screen's named machine (`WorldMachineCommandModule.InsertContent`); a screen
with no declared machine refuses. The path must be a file in one of that
machine's `contentFolders`, as every mount must, and the play needs Control
over the screen and the machine. Failed draft edits leave the draft intact; check, save, build,
export and play always validate.

## Contracts that bite

- **Cartridge rules admit what world rules refuse.** `repeat <n> as <name> { }`
  with `break`, call-form gates (`key(<button>, held|pressed|released)`) and
  every compound assignment are legal in a cartridge rule. World rules also
  admit compound assignment; loops and cartridge call-form gates are
  **PUCK037** and **PUCK038** there. `key(...)` is a gate only,
  not an operand. A `repeat` index name must be a declared variable.
- **Rule bodies are step trees** (`set`/`if`/`repeat`/`break`/`map`/`blit`/
  `play`/`stop`/`save`/`load`). An operand is a `Puck.State.ExpressionProgram`;
  `CartridgeExpressions.Reads` is the admitted operation subset and anything
  outside it is refused at its own spelling.
- **Targets differ; validation says how.** cgb, dmg and agb; byte and two-byte
  state; no ROM banking. Consult the validator before calling a feature
  portable. The light sensor `$light` exists only on `cgb`.
- **Colour is per-palette:** up to 8 palettes on cgb and 16 on agb,
  `mapPalettes` per background cell, a sprite picks an object palette. The dmg
  target validates like cgb but shades monochrome: every cell from the first
  background palette whatever it selects, a sprite from the first or second
  object palette by its palette's low bit, each colour reduced to one of four
  shades by its luma (`CartridgeGraphics.MonochromePalette`); a fade is a
  table of shade registers. A dmg image runs at single speed, so it sustains
  half the cgb work per frame (`CartridgeCostProfile.Monochrome`).
- **One game, several targets: a shared module.** A cartridge source may
  `import` a `.puck` module; its templates and constants come in
  (`CartridgeDocumentEmitter.LowerSource`, which `puck compile`, the language
  server and the round-trip test use), never rows. The game lives once as a
  template in `worlds/debug/cartridges/shared/` (`tetromino.puck`), and each target's source
  imports it, declares `target` and `palettes`, and calls it. A module contributes no standalone document.
- **A Color-only image cannot run on the DMG.** The cgb image arms the speed
  switch and executes STOP, which parks a monochrome processor until a key is
  pressed, and it writes palette memory and video bank one, which the DMG does
  not have. Port the source to `target: "dmg"` instead.
- **Map writes land a frame late on both targets:** they queue and drain in the
  next vertical blank. Validation bounds a frame's map writes to the queue's 24
  entries.
- **A sound is a music track or a one-shot effect.** A track is one to four
  voice parts, one to a channel, and validation refuses an effect on any voice
  a track occupies, since the effect would cut that part off. An effect may sit
  only on the pulse-1, noise or wave voice (never pulse 2), so with music on
  pulse 1 and pulse 2 the choices are an effect on noise or wave, or moving the
  music part off pulse 1 and the effect onto it.
- **Keep the two sound drivers in register sync.** Stream step widths are
  `duration` plus five register bytes for pulse one and wave, four for pulse two
  and noise; `AgbSoundDriver` maps the same registers to the AGB's legacy sound
  ports.
- **Saves.** `AgbSaveModule` needs its identifier text in the image or nothing
  persists; saves persist every byte.

## Cost is measured, never estimated

`CartridgeCost` prices a document in abstract work units against
`CartridgeCostProfile`'s per-target weights; `CartridgeDocuments.Estimate`
reports the frame bound and nothing refuses on it. Cost is advice, never a gate:
do not add a cost refusal, because the one hard refusal is capacity
(`CartridgeCapacityException`, an image that outgrew its machine). Weights come from
`puck cartridge-cost`, which boots `CartridgeCostMeasurement`'s probe documents
on both machines. Never hand-count an emitter's instructions into a weight or
adjust a weight to make a document fit; a new primitive is measured by adding
its shape to `CartridgeCostMeasurement.Shapes`. An unmeasured primitive prices
as `CostBound.Unmodeled`, which poisons the whole estimate. Never compare unit
totals across targets. A blit repaints with the display off, so frames stop
advancing while it runs; `CartridgeLimits.BlitCellCount` bounds its size.

## Boot ROMs

`BootRomBuilder.Build(ConsoleModel)` emits each revision's boot program. The
handoff counter (`BootDivPrediction`'s tables) is the contract, pinned from
outside by the `boot-rom-handoff` Post stage against the mooneye `boot_div-*`
cartridges; never move a table value to make a boot agree with it. The builder
solves its straight-line tail against the emitted image; never hand-count
instruction timings into its constants. Runtime packages embed generated images
(`HgbFirmware.GetImage`) and never reference Forge. Regenerate with
`puck firmware hgb --output <dir>` (or `puck firmware agb`) and check the bytes
with `--verify`, which compares without writing.

## Seeing it work

- Compile a cartridge and play it in a world (above). For World integration,
  drive the real host over stdin (`puck-world`); a build alone is not a play
  test.
- The cartridge suites are `tests/Puck.AdvancedGamingBrick.Forge.Tests`
  (`CartridgeCompilerTests`, `CartridgeMemoryTests` and the per-feature
  `Cartridge*Tests` run cartridges on both real emulators),
  `tests/Puck.GamingBricks.Transpiler.Tests` (the round trip) and
  `tests/Puck.HumbleGamingBrick.Forge.Tests` (boot ROM and bundle container).
  Run them when they reach the change: `dotnet build <project> -c Release -nodeReuse:false`, then `dotnet test <project> -c Release --no-build`.
- **Settle out of OAM DMA before reading the bus.** A fixed stepping boundary
  can land inside OAM DMA, where WRAM reads 0xFF. Every SM83 verifier calls
  `VerifyMachineSettle.SettleOutOfOamDma` after stepping frames; use
  `Framework.VerifyMachineDriver`, which already does.
- **Wait on the observable fact, not a duration.** `RunFramesUntil` advances
  until a condition holds and fails at a frame cap. Reach a shared starting
  position once and hand it out with `VerifyMachineDriver.Snapshot`/`Restore`.

[references/backend-contracts.md](references/backend-contracts.md) holds memory
addresses, register bits and the native compilers' instruction-level behavior.

## Route adjacent work

| Skill | Route there for |
|---|---|
| `puck-dsl` | `.puck` grammar, the compile/lint/format verbs, PUCKnnn diagnostics. |
| `gaming-bricks` | Emulator core behavior and the Post batteries. |
| `puck-world` | Driving the World over stdin; screens and authority. |
