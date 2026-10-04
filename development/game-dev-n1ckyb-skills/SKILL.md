---
name: game-dev
description: Build and change gameplay features in this project — entities, game loop, input, physics, rendering, state, and content/data. Use when adding or modifying anything the player sees, controls, or interacts with, when wiring new systems into the loop, or when tuning feel (handling, timing, camera, feedback). Not for test authoring (use game-testing).
---

# Game development

Guidance for writing gameplay code in this repo. Read `docs/architecture.md` and
`docs/game-design.md` if they exist before starting — they are the source of truth for
the current design; this skill is the source of truth for _how_ to build against it.

## Project specifics

- **Game:** `drive-evird` — free-roam 3D driving, cops vs robbers. Player picks a side.
- **Engine / stack:** Babylon.js + Havok physics (WASM), TypeScript, Vite.
- **Renderer:** WebGPU where available, automatic WebGL2 fallback. WebGL2 is the
  baseline — never ship a feature that only works on the WebGPU path.
- **Run the game:** `npm run dev`
- **Primary target:** iOS Safari as an installable PWA. Desktop browsers are a
  development convenience, not the target — a change that is only ever verified on
  desktop is not verified.
- **Frame rate:** 60fps target, 30fps hard floor on the oldest supported device.
- **Simulation rate:** fixed 60Hz.
- **Multiplayer:** single-player vs AI first, built server-authoritative-shaped.
  See the `netcode-readiness` skill — this constrains how state is written.
- **World:** seeded procedural endless city. See the `procedural-world` skill.

## Route-following alone drives cars into walls

A path is a centreline. A car that ran wide on a corner is no longer on it, and
following the path from where it now stands means driving through whatever it
ran wide into. No amount of better path-following fixes this, because the path
is not the problem.

Three forward raycasts — left, ahead, right — are enough. Steer away from the
closest hit in proportion to how close it is, toward whichever flank has more
room, and cap speed by the free distance ahead. Cast from _ahead of_ the car's
centre and above the ground, or the rays start inside its own chassis and every
one reports zero.

Two details that decide whether it works:

- **Add avoidance to the path steering, do not replace it.** A car that abandons
  its route the moment it sees a wall stops making progress; one that edges clear
  while still trying to go where it was going recovers.
- **Break ties deterministically.** Equal room both sides, decided randomly, makes
  a car flip side every tick in a corridor and go nowhere. Always pick the same
  way.

Keep the raycasting outside the controller — have the world fill in a small
"what can I see" struct and pass it in. The controller stays pure and every
steering decision stays testable with no physics world at all.

## Several pursuers is not one pursuer three times

Route every unit to the same point and you get a conga line down one street. Two
changes turn that into a team, and neither needs a real assignment algorithm:

- **Intercept rather than chase.** Aiming where the target _is_ means arriving
  where they _were_ — it looks like being towed. Aim at a predicted position,
  capped so a fast target does not send everyone to the horizon, and degrade to
  plain pursuit when the target is stationary rather than dividing by zero.
- **Give units different jobs by index.** One intercepts; the rest aim well ahead
  of the target and to alternating sides, so they arrive from different streets
  and the player is squeezed instead of followed.

Assert it: no two units aiming within some distance of each other. That test
fails the moment someone simplifies the targeting back to "everyone goes to the
player".

## Driving an AI car along a path: the four things that actually break

All four cost a debugging round here, none is obvious, and each looked like a
different bug than it was.

1. **Project onto the path, not onto the nearest waypoint.** With junctions 90 m
   apart, a car 30 m along a leg still has the start as its nearest _waypoint_,
   so the lookahead is measured from behind it, the aim sits behind the car, and
   it orbits a fixed point at full lock — covering hundreds of metres while its
   displacement stays under twenty.
2. **Do not look past a sharp corner, and do release the clamp on arrival.**
   Aiming through a right-angle junction takes the racing line diagonally across
   the corner, which in a city is through the building on it. But a clamp that
   never releases pins the aim to a waypoint the car is already standing on, and
   it creeps there forever. Clamp beyond a few metres; release inside them.
3. **Plan speed from the route ahead, not from the bearing to the aim point.**
   Deriving curvature from the bearing breaks the moment the aim is clamped at a
   corner: pointing straight at a junction reads as "no curvature", so the car
   accelerates into every turn it is about to make. Scan forward for turns and
   work back through a braking distance — which is also what a driver does.
4. **A speed profile is worth nothing if the controller does not follow it.** The
   brake gain here was a divisor of eight, so being 0.3 m/s over the planned
   limit produced four percent brake. The plan was right and completely ignored.

And one that generalises past driving: **anchor a path at the agent, not at the
nearest node.** Snapping both ends of a route to graph nodes teleports the path's
origin onto the network, so an agent that has been knocked off it is told to
follow a road it is not on. Prepend its own position — but only when it is
meaningfully off, because a near-zero-length leg has a meaningless bearing, and
anything reading angles off that path will see a hairpin that is not there.

## Non-negotiables

1. **Simulation is separate from presentation.** Game state and the rules that
   advance it must not import rendering, audio, or input libraries. Rendering reads
   state; it never mutates it. This is what makes the game testable headlessly and
   what keeps a later engine or renderer swap from becoming a rewrite.
2. **The simulation is deterministic.** Same initial state + same input sequence +
   same tick count → identical resulting state, every run. That means:
   - Never call a global/ambient clock inside simulation code. Time arrives as a
     parameter (`dt`, or a tick index).
   - Never use an unseeded RNG. All randomness comes from an explicit seeded
     generator carried in game state.
   - No iteration over unordered collections where order affects the result.
3. **Fixed timestep for simulation.** Advance the simulation in fixed increments and
   accumulate leftover real time; render at whatever rate the display allows and
   interpolate between the last two simulation states. Variable-`dt` physics produces
   frame-rate-dependent behaviour and irreproducible bugs.
4. **No gameplay constants inline.** Speeds, accelerations, cooldowns, damage,
   spawn rates, and thresholds live in one tunable data module or data file, named
   and unit-suffixed (`MAX_SPEED_M_PER_S`, not `maxSpeed`). Tuning must not require
   hunting through logic.

## The game loop

The canonical shape, whatever the language:

```
accumulator += realElapsed  (clamped to a max — never let a long stall spiral)
while accumulator >= FIXED_DT:
    input.snapshot()            # sample once per tick, not per system
    world.step(FIXED_DT, input) # pure-ish: state in, state out
    accumulator -= FIXED_DT
render(world, accumulator / FIXED_DT)   # alpha for interpolation
```

Clamp `realElapsed` (e.g. to 0.25s). Without it, one slow frame queues dozens of
catch-up ticks, which take longer, which queues more — the spiral of death.

## Adding a system

A system is a function over game state, run at a known point in the tick. When adding one:

- Decide its **order** in the tick explicitly and write the reason down next to the
  registration. Ordering bugs (input read after movement, collision resolved before
  integration) are the most common and most confusing class of gameplay bug.
- Give it the **narrowest slice of state** it needs. A system that takes the whole
  world is a system nobody can reason about.
- Make it **idempotent per tick** — no accumulated side effects outside game state.
- Add it to the headless test harness in the same change (see the `game-testing` skill).

## Entities and state

Prefer plain data for game state — structs/records/arrays — over deep object graphs
with behaviour attached. Reasons that actually matter here: it serialises for free
(save games, replays, test fixtures), it diffs readably in failing tests, and it
keeps update order in the systems rather than smeared across methods.

Give every entity a stable id. Never hold raw references across ticks where an
entity can be destroyed — hold the id and resolve it.

## Feel

Feel is a first-class requirement, not polish. When implementing player-facing
mechanics, budget for these from the start:

- **Input responsiveness.** Sample input every tick; never drop a press that lands
  between ticks (latch presses, consume them in the tick).
- **Forgiveness windows.** Coyote time, input buffering, and generous hit windows
  make a game feel fair. They are gameplay logic, so they are tunable constants and
  they are tested.
- **Feedback on every action.** Every player action needs an immediate readable
  response — visual, audio, or haptic. An action with no feedback reads as a bug.
- **Camera is a system.** It has its own state, smoothing, and constraints. It is
  not a value computed inline during render.

Tune by changing constants and playing, not by rewriting logic. If tuning requires a
code change beyond a constant, the constant is in the wrong place.

## Performance

Profile before optimising; state the measured number in the commit message. Beyond
that, the rules that pay off in games specifically:

- **Don't allocate in the hot loop.** Per-frame allocation is the usual cause of
  frame-time spikes. Reuse buffers; pool short-lived entities (projectiles, particles).
- **Broad-phase before narrow-phase.** Never run pairwise collision over all entities.
- **Batch draw calls.** Group by material/texture/shader; sort once, not per object.
- **Budget in milliseconds, not percentages.** At 60fps you have 16.6ms total. Know
  what each system costs.

## Assets and content

Content (levels, tracks, enemy tables, tunables) is data, loaded and validated at
startup with a clear error naming the offending file and field. A malformed content
file must fail loudly at load, never silently produce a broken game state.

## Split UI into a pure half and a DOM half

The test config uses `environment: 'node'` deliberately — it is what makes a stray
`document` in `src/sim` fail the run — so a DOM module is untestable by construction.
Do not reach for jsdom to fix that. Move every *decision* into a pure sibling and
leave only presentation behind: `session.ts` decides what a session is (seed parsing,
option validity, URL-versus-storage precedence) and `menu.ts` only draws it.
`control-layout.ts` is the same shape.

The payoff is immediate. Writing those tests first found two bugs in a seed parser
that read fine:

- A "fold" for over-long hex that was **truncation wearing a fold's comment** —
  `(value * 16 + digit) >>> 0` drops the high digits, so every seed sharing its low
  eight collapsed onto one city.
- A **decimal branch that was unreachable**, because an all-digit string is valid hex
  and the hex rule ran first. Removing it was the fix; supporting both would make
  `12345678` mean two different cities.

Inject the impure edges rather than importing them — `resolveSession(params, read)`
takes a storage reader, so nothing touches `localStorage`, which throws outright in
private browsing and cannot be imported at module scope in a node test at all.

Then mutation-test: invert the precedence order, make the parser return a constant,
turn a membership check into a range check. All four bit here; a suite that does not
is measuring nothing.

## Shell footguns in this environment

`pkill -f "<pattern>"` matches **your own shell's command line**, which contains the
pattern you just typed. `pkill -f "vite preview"` killed the agent's shell three times
before the cause was obvious — the symptom is an exit code and no output, which reads
like the command failing rather than the shell dying. Kill by PID from `pgrep`, or
match on something the invoking command line cannot contain.

Spawning a dev server through `npx` leaves it running: `npx` puts two shell processes
between you and the server, so killing the child on exit orphans the grandchild that
holds the port. Resolve the tool's own entry instead —
`require.resolve('vite/package.json')` then its `bin` — and let it pick a free port
rather than pinning one. `tools/smoke-prod.mjs` has the full reasoning; every new tool
should copy it rather than rediscover it.

## Adding a system that owns a quantity something else hardcoded

When heat took ownership of how many pursuers exist, three things broke that had
nothing to do with heat, and each one is the same shape: something else was the
de-facto owner and nobody had said so.

- **Tests that add their own entities.** A test placing three cops had them
  withdrawn on the first tick. That is correct behaviour and a genuinely
  surprising API, so make the new owner's rule reachable from a test — a tuning
  override on `createWorld` — rather than leaving tests to fight it.
- **The shared RNG.** Spawning drew from `state.rng`, which advanced it by a
  different number of steps depending on how the chase went. Still
  deterministic, but it couples every later draw to the pursuit's history, and
  it broke a determinism test that assumed stepping left the generator alone.
  Derive placement from `deriveSeed(rootSeed, ...)` like the city does.
- **A test whose premise quietly expired.** "The rng is untouched after 60
  ticks" was only ever true because no world had an AI in it. Assertions that
  encode an absence go stale silently the moment the absence ends.

And one design rule the tests forced out: **do not remove an entity the player
can see.** Culling a pursuer on the tick heat drops deletes a car from the
mirror mid-corner, which reads as a glitch rather than as the pursuit easing
off. Withdraw only beyond the distance where it is already out of sight.

## HUD readouts must have a source

A dense genre HUD invites filling the corners with plausible numbers. Every
placeholder gauge is a future bug report, and an inert one is worse than a
missing one — a nitro bar that does nothing looks exactly like a nitro bar that
is broken. If a readout has no system behind it, either build the system or
leave the slot empty and say so.

Where a readout is *derived* rather than simulated, say which in the module
docstring. The gear indicator here is computed from speed on the way out, and
`gearbox.ts` opens by stating that it is a readout and not a drivetrain —
because the next person to touch it will otherwise assume real ratios exist and
tune against them.

## Definition of done for a gameplay change

- Simulation still runs headless and deterministically.
- New/changed tunables are in the tunables module with units in the name.
- Tests added per the `game-testing` skill.
- Ran the game and confirmed the change reads correctly to a player — state that you
  did, and what you observed.

## Perfect information is what makes an AI un-tunable

An agent that reads the player's live position every time it re-plans has no
state in which it is uncertain. That sounds like a strong AI and is actually a
cage: there is nothing for cover, darkness, distance or a clever route to take
away, so the only difficulty lever left is raising a speed — and speed alone
reads as the game cheating.

Give it a **belief** instead: a last known position, a last known heading, and
how long ago it was confirmed. Then the interesting levers appear on their own —
how far it can perceive, how long it keeps driving to a stale answer, how widely
it searches after that. The hardest tier stops being the fastest one and becomes
the one still looking in the right place after you have gone.

Three things this gets wrong if you are not careful, all found the hard way:

- **The initial belief must not be empty.** Units dispatched to a suspect were
  told where to go. Starting from "no idea" means a player who never moves is
  never found, which is not stealth, it is a round that cannot end.
- **A search must not widen past what the agent can perceive.** If it can spread
  90 m from the last known point but only see 70 m, a target that simply stayed
  put is standing in the one place the search has left — and the agent orbits
  outside its own detection range forever.
- **Believing a heading and acting on it are two decisions.** Keep the last
  heading through a stop, so a car rocking on its suspension cannot rewrite it —
  but do not *use* it below walking pace, or every unit cuts 150 m ahead of a
  parked car to a corner it will never turn.

And make the rule asymmetric where the fiction is asymmetric. "They always know
on a lit street, and only nearby on a dark one" is both better fiction and far
easier to reason about than a symmetric radius — and it means the feature can
only ever make the game harder in the place it was meant to.

