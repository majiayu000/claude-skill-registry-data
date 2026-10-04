---
name: netcode-readiness
description: Keeping the single-player build ready for multiplayer without building multiplayer yet — the server-authoritative boundary, serializable state, input as commands, entity ownership, and what is cheap now versus expensive to retrofit. Use when designing any new system, when adding state, or when tempted to read input or wall-clock time from inside game logic.
---

# Netcode readiness

We ship single-player vs AI first. We do **not** build a server, netcode, or
matchmaking now. But the shape of the simulation is decided now, and a few
constraints kept from day one are the difference between "add multiplayer" and
"rewrite the game".

This skill is a short list of those constraints. It is not a licence to build
speculative networking infrastructure — if you find yourself writing a transport
layer, stop.

## The model we're targeting

**Server-authoritative with client prediction and reconciliation.** Not deterministic
lockstep, and not rollback.

Why: Havok is a WASM physics engine without a guarantee of bit-exact reproducibility
across platforms and versions. Lockstep and rollback both require bit-exact
simulation on every peer; a single ULP of divergence compounds into completely
different world states. Server-authoritative snapshots tolerate small divergence by
design — the server's state simply wins, and clients correct toward it.

Consequences worth internalising:
- The server will run the same simulation code we're writing now, headless, in Node.
  This is the same requirement the `game-testing` skill already imposes, so it costs
  us nothing extra — but it means the sim must never require a browser API.
- Clients predict locally and reconcile when the authoritative state disagrees.
  Reconciliation needs to be able to *replay* recent local inputs against a corrected
  state, which is why inputs are stored as an ordered, replayable sequence.
- Physics divergence is expected and fine. Design so a small positional correction is
  visually smoothed, never snapped.

## The five constraints

**1. Game state is fully serializable.**
Plain data — numbers, strings, arrays, plain objects. No class instances with
behaviour, no closures, no `Map` keyed on object identity, no references to Babylon
nodes or Havok bodies. If `structuredClone(state)` wouldn't round-trip it, it doesn't
belong in state. This is already required for save games and golden-replay tests.

**2. Input is a command, not a read.**
Game logic never queries a keyboard, touch, or gamepad API. Each tick receives an
input command object (`{steer, throttle, brake, handbrake, ...}`) produced by the
platform layer. Commands are values: sequenced, serializable, loggable, replayable,
and — later — sendable over a wire. This one constraint is what makes prediction and
reconciliation possible at all.

**3. Time comes from the tick, never the clock.**
No `Date.now()`, `performance.now()`, or `requestAnimationFrame` timing inside game
logic. Durations are tick counts or accumulated `dt` passed in. A cooldown measured in
wall-clock time cannot be reconciled or replayed.

**4. Every entity has a stable id and an explicit owner.**
Ids are assigned from a seeded counter in state, not from a random source or an array
index. Every entity carries an owner field — currently always the local player or
"server" (the AI), later a connection id. Adding an owner concept later means touching
every system; adding it now costs a field.

**5. Randomness is seeded and lives in state.**
The PRNG's position is part of game state and advances only inside the simulation.
Never `Math.random()`. This keeps world generation and AI decisions reproducible for
tests today and consistent between server and client later.

## Cosmetic state is usually not cosmetic

Before putting something in the view because it "only affects how it looks", ask
whether another player would benefit from seeing it. In a pursuit they usually
would, and that makes it simulation state.

Brake lamps are the clearest case: a chasing player reading them to anticipate a
corner is real information, not decoration. The same goes for a boot standing
open, a siren, or damage. All of it is plain data, all of it replicates, and all
of it has to survive a save — so it belongs in `GameState`, driven from the
simulation, with the view merely reading it.

Store it as a continuous value where the thing has a duration (a lamp fading, a
panel swinging) rather than a boolean the view has to animate. The animation then
replicates too, instead of every client inventing its own.

## Cheap now vs expensive later

**Cheap to keep now (do these):** the five constraints above; keeping the sim free of
browser APIs; keeping systems as pure functions of state; a clean `step(state, input)`
entry point.

**Expensive to retrofit (which is why we do the above):** removing ambient time and
input reads from dozens of systems; making a deep object graph serializable;
introducing entity ownership; separating simulation from rendering after they've grown
together.

**Do NOT build now:** transport, serialization wire formats, delta compression,
interest management, lag compensation, matchmaking, lobbies, accounts, anti-cheat.
All of these are additive once the constraints above hold, and all are wasted work
before there's a game worth playing.

## What a snapshot cannot carry

A snapshot holds transforms and velocities. It does **not** hold Havok's internal
solver state — contact caches and warm-start impulses — and there is no way to
extract them. Restoring therefore restarts the solver cold, and a restored run
diverges from an uninterrupted one: slowly at first, then chaotically, as any
contact-rich nonlinear system does. Measured on the current car, roughly a
centimetre of position over a second of continuation.

Two consequences:

- This is the concrete reason lockstep and rollback are off the table, beyond
  the general point about Havok not being bit-exact across platforms. Even on
  one machine, in one process, a restore does not reproduce exactly.
- **Never write a restore test as a per-number epsilon.** Such a test measures
  chaotic amplification, and its epsilon has to be retuned every time the car's
  mass or geometry changes — at which point it is testing the tuning, not the
  restore. Assert a short horizon and a physical bound instead: the car is
  within a centimetre a second later. Keep the exactness assertion for the
  serialisation round-trip itself, which *must* be lossless.

## The one test that protects this

A test that runs the simulation headless in Node — no browser globals, no DOM, no
Babylon — for a scripted input sequence, snapshots state with `structuredClone`,
serializes it to JSON and back, and continues the run to the same result.

If that test passes, the simulation is server-ready. If it fails, it names exactly
which constraint has been broken. Run it in CI.

## Review checklist for any new system

- Does it read input, time, or randomness from anywhere but its arguments and state?
- Is everything it adds to state plain, cloneable data?
- Do new entities get stable ids and owners?
- Would it still run in Node with no DOM?
