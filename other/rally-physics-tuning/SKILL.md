---
name: rally-physics-tuning
description: Change Gravel Rally handling - car physics parameters, tyre/surface grip, suspension, drivetrain, driver assists - and validate with the regression and autopilot tests. Use when the user says the car feels wrong (spins, understeers, floaty, rolls, slow, too grippy) or asks for physics changes.
---

# Rally physics tuning

Code: `src/games/rally/physics/` (DOM-free). Model, tuning table, tyre / set-up design, numbers and open work: `src/games/rally/PHYSICS.md` (update its tables when numbers move).
Conventions: body +Z forward, +Y up, **+X left**; steer input +1 = right; 240 Hz fixed step.

## Where things live

- Per-car numbers: `cars/<id>/<id>.ts` -> `physics` (mass, COM height, axles: spring/damper/travel/antiRoll/
  grip/forceHeight, `brakes`, engine torque curve, gearbox, drivetrain split + diff locks, aero).
  Ride height is preserved automatically when springs change (mount computed from static load).
- Surfaces: `physics/surfaces.ts` (`mu`, `slide`, `peakSlip`, `peakAngle`, `rolling`, `bump`, `rough`).
- Water: `Vehicle.waterPass` (tyre + body drag, flooded intake), fed by `GroundProvider.waterLevel`;
  `tests/rally/water-physics.test.ts` prints dry / shallow / deep acceleration per car.
- Tyre size + suspension set-ups: `CarPhysicsDef.tyres` (sizes per compound + axle; each rolls on `axleRadius`, gearing on `drivenRadius`) and `setups` / `setup`
  (`deriveSetups`, `applySetup`, `compliance` in `physics/car-setup.ts`); the per-car grip layers live in `physics/car-tyres.ts`
  (`carSurfaces`). Build the `Vehicle` from `applySetup(def, id)` + `setTyre(id)`; tests: `car-setup.test.ts`, `car-matrix.test.ts`.
  Retuning springs changes the compliance (and so the grip match) by itself - keep damping ratios 0.25-0.8 and a car's range
  (Skoda Rally wide, Zastava soft half, Bimmer stiff half).
- Gearing presets: `physics/gearing.ts` (`CarPhysicsDef.gearings` = short / medium / long final drive, race cars only;
  `applyGearing` after `applySetup`; `topSpeed` = the setup screen number; `MapDef.gearing` = a stage's recommendation;
  `Autopilot.maxSpeed` lifts the 151 km/h cap to measure top speed). Tests: `gearing.test.ts`.
- Tyre types: `physics/tyres.ts` (five tyres in three families: `tarmac` / `tarmac_hard`, `mixed`, `gravel_hard` / `gravel`;
  the ids `tarmac` and `gravel` are the soft compounds; per-tyre multipliers on the surfaces; `Vehicle.setTyre`, `null` = raw
  surfaces so `vehicle.test.ts` bands stay put). Grip / feel of a tyre = edit its table there; ranks are checked by
  `integration-tests/rally/tyres.test.ts`. A new surface needs an entry in every `TyreDef.grip`. Sizes, brake kit, rim and tread
  follow the family (`TyreSize` per `byCompound[family]`); a car's class of rubber is `TyreSize.grade` (rally 1, road 0.82,
  slick 1.12).
- Tyre temperature: `physics/tyre-temp.ts` (heat / cooling constants, grip curve), windows in `TyreDef.temp`, air and road per stage, season and time
  of day (`StageDef.temps`, valid at the stage start; the air falls 6.5 K/km with `setClimate`'s `refHeight`). Only runs with `Vehicle.setClimate` (game); tests without it keep the reference numbers.
  Tests: `tests/rally/tyre-temp.test.ts` (feel targets), `integration-tests/rally/car-matrix.test.ts`.
- Brakes: `CarPhysicsDef.brakes` / `gravelBrakes` (type, size, pad class, `clamp` force; `physics/brakes.ts`), torque acts on the
  wheel's effective inertia, disc temperature + pad fade only with a climate. Tune `clamp` until the torque limit sits ~10 %
  over the tyre's best decel (`tests/rally/brakes.test.ts`).
- Tyre model: `physics/tire.ts`. Rigid body / suspension / contacts: `physics/vehicle.ts`.
- Driver aids: `Vehicle.tractionControl` (traction term: slip ratio held at 0.6 x the surface's peak; stability term: combined slip; `T` in game), `Vehicle.abs` (per-wheel
  anti-lock on the foot brake, `B`; `physics.noAbs` = not fitted), `autoReverse`, keyboard steering ramp / speed limit /
  counter-steer allowance in `game/input.ts`. Each aid has a `RallySettings` flag + an Options row hidden when not fitted.

## Workflow

1. Reproduce with numbers, not vibes:
   - `npm run test -- tests/rally/vehicle.test.ts` prints 0-100, 100-0, top speed, lateral g per surface.
   - `integration-tests/rally/handling.test.ts` = whole-car handling (ramp / step steer, lift / power / brake mid-corner, handbrake,
     slalom, keyboard lock, braking, drops, ruts) per car x tyre x set-up x surface; `HANDLING_FULL=1` all set-ups,
     `HANDLING_OUT=x.json` dumps every number. To try a change without editing a car, pass a modified def
     (`Cfg.def`) or a Vehicle patch (`Cfg.patch`) to the manoeuvres in `handling-harness.ts`. Last review notes
     (local only, git-ignored): `sources/cars/HANDLING-REVIEW.md`.
   - In game `/games/rally/?car=<id>&spawn=pad&mute=1` (always `mute=1` when testing; AGENTS.md "Sound while testing"): `F2` telemetry (per-wheel load, compression, slip ratio/angle,
     Fx/Fy, surface), `F4` force vectors + hull.
   - For a specific stage spot: `?spawn=<metres along road>`.
2. For behaviour over a whole stage write a throwaway trace test (see git history / the pattern in
   `integration-tests/rally/stage.test.ts`): run `Autopilot` + `Vehicle` headless and log speed, sideslip
   (`atan2(v·right, v·forward)`), `up.y`, wheel loads every 0.05 s around the event. Delete it afterwards.
3. Change one knob at a time (table in the rally DETAILS.md). Keep surface `bump` wavelengths long - short bumps
   become damper spikes because wheels are single rays with no unsprung mass.
4. Validate: `npm run test` (`vehicle.test.ts` bands) and `npm run test:integration:rally` (`stage.test.ts`: every car finishes every map,
   `up.y` stays > 0.5). If you intentionally change a band, update the test and say why.
5. Feel-check on keyboard AND (if available) gamepad.

## Lessons already learned

- "The car can't turn into corners" was the front wheels locking under braking - ABS (`Vehicle.absPass`, `B`) fixed it.
  A grip-aware keyboard / pad steering limit and a front-grip / softer-diff retune were tried first, felt wrong to the
  player and were dropped: check braking (`straight`, ABS off via `Cfg.patch`) before touching steering or grip.
- Auto gearbox decisions use ground speed, not wheel speed (wheelspin caused gear hunting).
- Handbrake declutches the rear (otherwise reflected engine inertia stops the wheels locking).
- Flimsy props must not be solid colliders (a 6 cm post stopped the car dead at 95 km/h).
- Rear-biased AWD at full throttle mid-corner power-oversteers; the stability part of TC handles keyboard play.
- TC stability on driven FRONT tyres uses a high threshold (2.0 vs 1.15 rear): past their peak they understeer, and
  cutting power there bogged the Skoda Rally / Zastava mid-corner; keyboard lock (`keyboardSteerLimit`) stays near the
  peak-grip steering - check both with `handling.test.ts` (keyboard lock rows) when touching either.
- Crests in corners unload the tyres (loads can drop to ~40%) - a real hazard; place jumps on straights.

## Bump the times version (last step)

A handling change to one car bumps its `CAR_TIMES_VERSIONS` entry in `game/stage.ts`; a shared physics change (tyres, surfaces, drivetrain model, assists) bumps every released car (`hideInProd` cars stay at 1, a test checks). Bump only when the user says we are making a build; until then say in the PR
which cars changed (AGENTS.md "Rally times versions"). Old times stay below the new ones.
