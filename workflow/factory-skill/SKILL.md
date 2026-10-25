---
name: factory
description: Turn a one line description of a factory ("a line that makes 2,000 e-bike motors a day", "a bakery that bakes 10,000 croissants an hour", "a battery cell gigafactory") into a single self-contained HTML page with a live 3D tilt-shift miniature of that factory, driven by a real discrete event simulation (stations, cycle times, batches, finite buffers, shifts, breakdowns, scrap) with a live HUD for throughput against target, takt, utilization, WIP, lead time and the bottleneck, where clicking a station lets you add a machine or change a cycle time and watch the bottleneck move. Use it whenever someone wants to see, size, explain or pitch a production line, plant, assembly line, process or factory, asks "how many machines do I need", "where is the bottleneck", "can this line make N a day", wants a factory simulation or digital twin demo, or describes a product and a volume, even if they never say "simulation".
---

# Factory

**Describe a factory in one line. Claude builds it as a live 3D simulation you can run.**

The page is a model factory on a table, seen through a tilt-shift lens: a cut-away hall with
the line inside, machines that move while they work, product flowing on conveyors, people, forklifts, a
truck yard. Under it runs a discrete event simulation. Every number on screen comes from that
simulation, never from a script: the throughput, the utilization bars, the WIP, the pulsing red
outline around the bottleneck. When someone adds a machine at the bottleneck, the simulation gets
one more server, the conveyor in front of it drains, and the outline moves to the next constraint.

## The one rule that matters

**The simulation is the explanation, so it has to be true.**

- Cycle times, batch sizes, dwell times, breakdown rates and yields come from how the real process
  works. Use the numbers a process engineer would recognise and say in `note` where they come from
  ("18 min at 180 C", "51 slots, 3 needle head"). When you have to estimate, say "typical".
- Machine counts come from the sizing rule, which the page prints in the inspector:
  `machines = CEIL(rate_in x cycle / (batch x availability x target utilization))`.
- Throughput, utilization and the bottleneck come out of the simulation. Never tune inputs to make
  a nicer result. If the first line misses its target, that is the finding: report it, show it, and
  let the user fix it with the slider.

## Workflow

Run `date` at the start. A factory takes 10 to 25 minutes.

1. **Read the line.** Pull out the product, the volume and the time unit. Fill in what is missing with
   stated assumptions: shifts (2 x 8 h unless the process runs around the clock, like cells,
   chemicals or glass), the product variant ("250 W rear hub motor"), the scope ("the canning hall,
   from bright tanks to pallets"). Say them in one short paragraph before building.
2. **Route.** Write the real process route as 6 to 10 stations, in flow order, with branches where
   sub-assemblies are made in parallel and joined (stator + rotor + housing into motor assembly).
   Each station: what happens, the machine that does it, the cycle time per unit or per batch, the
   batch, MTBF/MTTR if it is a machine that breaks, yield if it is a test or inspection.
   `references/process.md` has typical numbers for common processes and how to pick them.
3. **Pick the token.** One token is one unit unless the line is fast. Choose `perToken` so one token
   leaves the line every 5 s to 2 h (a tray of 40 croissants, a case of 24 cans, a tray of 96 cells).
4. **Write `spec.js`** (schema below). Start from the closest example in `examples/`.
5. **Check it headless.** `node scripts/check.mjs spec.js`. It sizes the line and runs 5 production
   days of the same engine the page runs, and prints per station: machines, capacity per day, busy,
   down, blocked, starved, failures; then the forecast and the bottleneck. Read it like an engineer:
   - Does each machine count look like a real plant? 446 proofer slots is right (4 chambers of 120);
     40 laminators is a wrong cycle time.
   - Is the bottleneck plausible? Long dwell steps and machines with poor availability usually are.
   - Fix mistakes in the inputs (a wrong unit, a batch you forgot). Do not fix the result.
6. **Build.** `node scripts/build.mjs spec.js <out>.html` writes one file of about 1 MB with three.js,
   the runtime and the spec inlined. It opens from disk with no server and no network.
7. **Look at it.** `node scripts/capture.mjs <out>.html shot.png --query "assemble=0"` (needs
   Playwright) and read the PNG. The line should fill the frame, every station should have its
   machines, product should be on the conveyors, the HUD should show a throughput. Zero console errors.
8. **Answer** with the file path, the forecast against the target, the bottleneck and why, the sizing
   of the bottleneck station, and one what-if to try ("add a third winder: the forecast goes from
   1,943 to 2,0xx a day and the constraint moves to EOL test"). Run that what-if through
   `check.mjs` (edit `servers` on a copy) before you quote it.

## Spec

```js
FactorySkill.define({
  id: 'ebike-motors',                        // file name
  prompt: 'a line that makes 2,000 e-bike motors a day',  // the user's line, typed into the page
  title: 'E-bike hub motor line',
  product: { name: 'motor', unit: 'motors', perToken: 1 },
  demand: { perDay: 2000 },                  // or perHour, or perWeek (5 days)
  calendar: { shifts: 2, hoursPerShift: 8, startHour: 6 },
  sizing: { targetUtil: 0.85 },              // planned utilization for the sizing rule
  release: 'capacity',                       // 'capacity': raw material always there (find the max), 'takt': released at demand
  seed: 11,
  stations: [
    { id: 'stamp', name: 'Lamination press', machine: 'press', ct: 22, cv: 0.04, buffer: 8,
      mtbf: 6 * 3600, mttr: 25 * 60, input: 'coil', stage: 'stack', note: '64 laminations at 180 strokes/min' },
    { id: 'wind', name: 'Needle winding', machine: 'winder', ct: 150, after: ['stamp'], stage: 'wound' },
    ...
  ],
  stages: { coil: { shape: 'coil', color: '#8d949b' }, stack: { shape: 'ring', color: '#6f7780' }, ... },
})
```

Station fields:

| field | meaning |
|---|---|
| `id`, `name` | key and the name on the plate and in the HUD |
| `machine` | a kit machine (table below) or an alias such as `lathe`, `proofer`, `pasteurizer`, `seamer` |
| `ct` | seconds per cycle per machine; with `batch` it is the time for the whole batch |
| `cv` | coefficient of variation of the cycle (lognormal). Automatic 0.02 to 0.06, manual 0.1 to 0.2 |
| `batch` | units taken and released together (a chamber oven, a mixer, a TVAC) |
| `perMachine` | units one physical machine holds at once in continuous flow (tunnel oven, spiral, proofer, formation rack). The DES gets that many servers per machine with `ct` = dwell time |
| `servers` | `'auto'` (default, sizing rule) or a number of machines (times `perMachine`) |
| `buffer` | capacity of the input buffer (each input of a join has its own) |
| `mtbf`, `mttr` | mean busy seconds between failures and mean repair seconds (exponential) |
| `yield` | fraction good; the rest is scrapped at this station |
| `after` | predecessor ids. Default: the previous station. A station with `input` starts a new branch |
| `input` | the raw material stage a branch starts from |
| `stage` | the product stage this station outputs (looks up `stages`) |
| `note` | where the numbers come from, shown in the inspector |
| `variant`, `color`, `accent`, `length`, `radius`, `height`, `fill`, `web`, `glow` | looks |
| `operators`, `reserve`, `at: [col, row, dir]` | people beside machines, spare floor slots, manual grid placement |

The model is a tree into one last station (the sink): every station feeds exactly one next station.

## Kit

Machines (real scale, metres) in `runtime/kit.js`:

| machine | looks like | kind |
|---|---|---|
| `cnc` | machining centre, window, moving spindle, chip conveyor | side |
| `press` | press with ram and flywheel, coil feeder; `variant: 'magnetizer'` | side |
| `winder` | needle winder, spinning table, wire spools | side |
| `robot` | fenced 6 axis arm cell; `variant: 'weld'` adds arc and sparks | side |
| `bench` | assembly bench with an operator, bins, tool balancer | side |
| `tester` | test rack with screens and a clamp fixture | side |
| `oven` | chamber oven with racks (batch); `variant: 'proofer'` | side |
| `mixer` | spiral or planetary mixer with turning bowl | side |
| `filler` | rotary filler / seamer in a glass enclosure | side |
| `formation` | racks with blinking channels (formation, ageing, burn-in) | side |
| `tank` | stainless tank with agitator, ladder, piping | side |
| `laser` | laser cell with glowing window | side |
| `turntable` | calibration turntable with camera tripods | side |
| `cage` | flight / function test cage; the unit lifts while tested | side |
| `bay` | integration bay with gantry crane and technicians; `variant: 'cleanroom'` | side |
| `chamber` | thermal vacuum / autoclave vessel with a round door (batch) | side |
| `kitting` | shelving with bins and a picker | side |
| `stacker` | high speed stacking / winding head | side |
| `cell` | generic enclosed process cell (anything else) | side |
| `tunnel` | tunnel oven, dryer; `variant: 'pasteurizer' | 'washer'` | inline |
| `spiral` | spiral cooler / freezer / proofer tower | inline |
| `rollers` | sheeter, laminator, `variant: 'calender' | 'slitter'` | inline |
| `coater` | roll to roll coater with drying oven | inline |
| `smt` | printer + pick and place + reflow | inline |
| `vision` | inspection arch over a belt | inline |
| `packer` | case packer / flow wrapper | inline |

Product shapes for `stages`: `ring wound rotor hub disc coil box crate tote croissant tray dough sheet
can sixpack bottle cell pouch roll module pack pcb frame drone satellite bus sneaker bag puck`.
Each takes `color` and `scale`; `tray` takes `item: 'croissant' | 'dough'`.

A process with no fitting machine: use `cell` with a `glow` colour, or define one in the spec file
before `define` (guarded, so `check.mjs` can run the file without a browser):

```js
if (FactorySkill.Kit) FactorySkill.Kit.def('kiln', (o) => {
  const K = FactorySkill.Kit, { g, M, body, acc } = K.sideBase(o, 3, 2.4)
  K.box(g, 3, 2.2, 2.2, body, 0, 0, 0)                 // K.box(parent, w, h, d, material, x, yBottom, z)
  const door = K.live(K.group(g, 0, 0, -1.1))          // parts that move live in K.live groups
  K.box(door, 1.4, 1.6, 0.08, acc, 0, 0.3, 0)
  return K.finish({ g, kind: 'side', w: 3, d: 2.4, h: 2.4, entry: K.V(0, 0.9, -1.3),
    work: K.workFixed(0, 0.9, 0), anim(s) { door.position.y = s.state === 'busy' ? 0 : 1.4 } }, o, [1.2, 2.2, -0.9])
})
```

`references/kit.md` has the whole API (materials, parts, people, vehicles, `work(i, p)` for units that
move through a machine).

## The page

- Opens on the assembled factory, already 3 production hours in (more for slow lines) so buffers hold
  WIP. `?intro=1` types the prompt and assembles the factory station by station first.
- HUD: throughput per day over the last 4 h against the target, a sparkline per production hour,
  takt, WIP, lead time, the bottleneck card, one bar per station split into busy, blocked, starved and
  down. The bottleneck station gets a pulsing red outline on the floor; nothing else is labelled.
- Click a station (or its row) for the inspector: machines with minus and plus (spare floor is
  reserved), cycle time and buffer sliders, the sizing formula with its numbers, MTBF/MTTR, failures,
  scrap, and a 3 day forecast of the changed line from the same engine.
- Speed buttons scale production time; the clock shows day, time and shift.
- `?film=1` stops the clock: `window.__film.step(dt)` renders one frame. `window.factory` exposes
  `select(id)`, `setMachines(id, n)`, `setCT(id, s)`, `setBuffer(id, n)`, `camTo({az, el, dist, target}, s)`,
  `stationCenter(id)`, `forecast()`, `sim`, `world`.
- Other URL options: `speed`, `seed`, `release=takt`, `select=<id>`, `ui=0`, `assemble=0`, `ao=0`.

## Look

Tilt-shift miniature photography, not a CAD view: warm sun with soft shadows, ambient occlusion, a
narrow band of focus with heavy blur above and below, saturated warm grade, vignette, grain. The
factory sits on a diorama base on a table: cut-away hall (back and left walls full height, front and
right cut low with the section face coloured), racking along the back wall, clutter on free floor,
truck yard, parking, trees, a sign. Machines are cream with one accent colour per station.
`references/look.md` explains each choice and what to keep when you extend it.

## Verify like a critic

- `check.mjs` numbers match the HUD after a few hours (the HUD window is 4 h, so it is noisier).
- Every station shows its machines; nothing floats; tokens sit on belts or in machines.
- At the bottleneck the input buffer is full and machines upstream show amber (blocked); downstream
  rows show grey (starved). If not, the bottleneck is downtime driven: say so.
- Add a machine at the bottleneck in the page: the forecast line updates and the outline moves within
  about an hour of production time.

## Files

| path | what |
|---|---|
| `runtime/des.js` | the simulation engine and the sizing rule (pure, runs in Node and the browser) |
| `runtime/kit.js` | machines, products, people, vehicles |
| `runtime/world.js` | layout, hall, conveyors, token placement from simulation state |
| `runtime/look.js` | renderer, light, AO, bloom, tilt-shift, grade |
| `runtime/app.js`, `runtime/hud.css` | page, HUD, inspector, film hooks |
| `vendor/three.bundle.js` | three.js r185 and the addons used (MIT) |
| `scripts/check.mjs`, `scripts/build.mjs`, `scripts/capture.mjs` | headless run, build, screenshot |
| `examples/*/spec.js` | six factories made with this skill, each with its built page |
