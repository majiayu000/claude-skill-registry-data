---
name: vehicle-physics
description: Vehicle simulation and driving feel — raycast suspension, tyre grip and slip, steering, braking and handbrake, drift, collisions and damage, and the tuning workflow. Use when building or changing how cars drive, when a car feels wrong (floaty, twitchy, understeery, slow to respond), or when adding a new vehicle class such as a police cruiser.
---

# Vehicle physics and driving feel

Driving feel is the game. A cops-and-robbers chase is only tense if the car is
enjoyable to control, so this system gets more iteration than anything else.

## Model: raycast vehicle, not rigid-body wheels

Use a single rigid body for the chassis plus four downward raycasts for wheels. Do
**not** simulate wheels as constrained rigid bodies — it's slower, less stable, and
much harder to tune. Every mainstream driving game uses raycast vehicles.

Per wheel, per tick:
1. Raycast down from the wheel's mount point, up to suspension rest length + travel.
2. No hit → wheel is airborne; no suspension or tyre force, and steering authority drops.
3. Hit → compute **suspension force** along the contact normal:
   `F = k * compression - c * compressionVelocity`, clamped to >= 0 (suspension pushes,
   never pulls) and clamped to a max to survive big landings.
4. Compute **tyre forces** in the contact plane: longitudinal (drive/brake) and
   lateral (grip), each limited by the friction circle (see below).
5. Apply all forces to the chassis at the contact point — that's what produces weight
   transfer, body roll, and dive under braking for free.

## The friction circle

The single most important concept for feel. A tyre has one total grip budget, shared
between turning and accelerating/braking:

```
sqrt(F_long² + F_lat²) <= mu * F_normal
```

Compute both desired forces, then scale both down if they exceed the limit. This one
rule gives you, without special-casing: understeer when accelerating into a corner,
oversteer when braking mid-corner, loss of steering under full throttle, and drift.

`F_normal` comes from the suspension, so weight transfer feeds grip automatically —
the front tyres grip more under braking, the rears under acceleration.

## Tyre slip

Lateral force is a function of **slip angle** (angle between wheel heading and actual
velocity direction); longitudinal force is a function of **slip ratio**. Both curves
rise steeply to a peak and then fall off — the falloff after the peak is what makes a
car break traction and what makes drifting controllable.

Don't implement full Pacejka unless you need it. A curve that rises linearly to a
tunable peak and then decays to a tunable sliding-friction value is enough and is far
easier to tune. Keep the curve in the tunables module as named points.

## Tunables

Every one of these lives in the tunables module with units in the name, and none of
them appear as literals in logic:

| Group | Parameters |
|---|---|
| Chassis | mass, centre-of-mass offset (lower and slightly rear = stable), inertia |
| Suspension | rest length, max travel, spring rate, damping (separate bump/rebound), anti-roll |
| Tyre | peak grip coefficient, peak slip angle, sliding grip, per-axle grip bias |
| Drive | torque curve, gear ratios (or simplified direct drive), drive layout, top speed |
| Brakes | brake torque front/rear, handbrake torque (rear only), ABS on/off |
| Steering | max angle, speed-sensitive reduction, input smoothing rate, self-centring |
| Assists | traction control, stability assist, drift assist — strengths, all tunable to 0 |

**Centre of mass is the highest-leverage single value.** Too high and the car rolls
and flips; too far forward and it won't rotate. Tune it before anything else.

## Feel targets for this game

- **Arcade, not simulation.** The fantasy is a movie car chase. Grip levels above
  realistic, forgiving recovery from slides, no stalling, no clutch.
- **Speed-sensitive steering** is essential. Full steering lock at 120km/h is
  undriveable on a touchscreen.
- **Input smoothing** matters more than on a wheel or stick, because touch input is
  binary. Ramp steering toward the target angle at a tunable rate rather than snapping.
- **Handbrake turns must work and be reliable** — it's the core chase verb. Handbrake
  cuts rear longitudinal grip and reduces rear lateral grip; the car should rotate
  predictably, not spin uncontrollably.
- **Airtime should be survivable.** Cap angular velocity in the air and apply gentle
  auto-levelling, or every jump ends on the roof.
- **Cop cars differ by tuning, not by different code** — heavier, more top speed, less
  agile. One vehicle system, several tunable profiles.

## Collisions

- Chassis collides as a simplified convex shape, never the visual mesh.
- Impacts scrub speed and impart rotation, but should not stop the player dead — a
  full stop from a glancing wall hit ends chases and feels awful. Tune restitution
  and add glancing-blow deflection.
- If damage exists, it modifies tunables (grip, max speed, steering) so it's felt
  rather than merely displayed.

## Tuning workflow

1. Change values only in the tunables module — never logic.
2. Use a dev-only tuning overlay (sliders bound to the tunables) to iterate live.
3. Test on a flat plane first, then a slope, then the real city.
4. **When it feels right, write a golden-replay test** capturing that behaviour: a
   fixed input script, asserting tolerance-bounded position/velocity at checkpoints.
   This is what stops a later physics change silently ruining the handling.

## Diagnosing bad feel

| Symptom | Usual cause |
|---|---|
| Floaty / bouncy | Suspension damping too low, or spring rate too high for the mass |
| Rolls over easily | Centre of mass too high; add anti-roll |
| Won't turn (understeer) | Front grip bias too low, or steering angle reduced too aggressively with speed |
| Spins constantly (oversteer) | Rear grip too low, or centre of mass too far rearward |
| Twitchy on touch | No input smoothing, or no speed-sensitive steering |
| Sticks to walls | Restitution too low and no deflection handling |
| Vibrates at rest | Suspension spring/damper stiff relative to timestep; check resting-contact test |
