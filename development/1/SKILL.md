---
name: loto-interaction-mechanics
description: Use this skill whenever building, modifying, or debugging any part of the LOTO 7-step simulation — step gating, valve interaction, hasp alignment, padlock sequencing, grab mechanics, pressure validation, or completion logic. This is the authoritative tolerance and physics contract. Do not invent values. Do not approximate thresholds. Always load this skill before writing any LOTO interaction code.
---

This skill is the single executable reference for all LOTO simulation interaction logic in the Myelin platform. Every threshold, formula, and constraint here is non-negotiable. Do not substitute values from general physics intuition or prior training. Read this file first. Build from these numbers exactly.

---

## Step Sequence and Gating Rules

The LOTO pathway is a strictly ordered 7-step sequence. A step may not be attempted until all prior steps have passed validation. There is no skip logic, no shortcut path, and no optional ordering.

| Step | Action | Validation Gate |
|------|--------|-----------------|
| 1 | Notify affected personnel | Presence-confirmed state flag only — no physics validation |
| 2 | Isolate energy source (valve turn) | Rotation within π/2 ± 0.05 rad of closed position |
| 3 | Apply hasp to valve stem | Hasp centroid distance to stem snap point < 0.02 m |
| 4 | Apply padlock through hasp | Lock body orientation within ± 0.08 rad of valid axis; shackle engagement confirmed |
| 5 | Attempt start (test) | Start interaction registered; system confirms no activation |
| 6 | Verify zero energy (pressure check) | Residual pressure reading < 0.1 bar |
| 7 | Perform task; confirm completion | All steps 1–6 passed; completion interaction registered |

Step 7 gates the post-simulation state transition. No completion event may fire unless all prior step pass flags are true in the session state object.

---

## Valve Interaction — Step 2

### Torque Curve

Apply the following torque resistance values across the valve rotation arc. These are not uniform — resistance varies by phase.

```
torqueCurve = [8.2, 3.1, 11.8]  // Nm, sampled across rotation phases
```

Phase 1 (initial break-loose): 8.2 Nm
Phase 2 (mid-rotation, reduced friction): 3.1 Nm
Phase 3 (near-closed, seat engagement): 11.8 Nm

Interpolate between phases proportionally to current rotation angle. Do not apply a flat torque value.

### Rotational Validation

Pass condition: `Math.abs(currentAngle - targetAngle) <= 0.05` where `targetAngle = Math.PI / 2`

End-state snap behavior: when the angle enters the tolerance window, snap to exact target and lock rotation. Play the torque-click audio cue (4200 Hz). Disable further rotation input on this object.

### Pressure Model

Residual system pressure is a function of valve angle:

```
pressure = 10 * Math.exp(-angle * 0.5)  // result in bar
```

This value must be computed in real time and surfaced to the pressure gauge readout. It is also the value checked at Step 6.

---

## Hasp Interaction — Step 3

Pass condition: distance from hasp centroid to valve stem snap point < 0.02 m

Alignment feedback progression:
- Distance > 0.10 m: no feedback
- Distance 0.05–0.10 m: show proximity indicator (visual only)
- Distance < 0.05 m: activate alignment guide overlay
- Distance < 0.02 m: trigger snap-to-point, play connector-snap audio (1850 Hz), register step pass

Squeeze requirement: the grab must maintain continuous hold through the snap event. A released grab before snap does not register.

---

## Padlock Interaction — Step 4

Orientation validity: lock body must be within ± 0.08 rad of the valid insertion axis before shackle engagement is permitted.

Shackle engagement sequence:
1. Confirm hasp hole alignment (derived from Step 3 snap state)
2. Confirm orientation within tolerance
3. Register shackle-through event on contact
4. Play spring audio cue (1200 Hz) on engagement
5. Set lock state to CLOSED; disable removal interaction

---

## Grab and Manipulation Baseline

These values apply to all grab-capable objects in the LOTO simulation unless an object spec overrides them explicitly.

```
reach         = 0.4    // m — maximum grab distance from hand origin
grabRadius    = 0.03   // m — sphere radius for grab detection
maxForce      = 25     // N — maximum applied interaction force
```

Collision-based grab (when hand tracking is active):
```
overlapThreshold  = 0.015   // m
palmRadius        = 0.08    // m
fingerCapsuleR    = 0.012   // m
```

Grip ramp: interpolate grip strength from 0 to 1 over 0.2 seconds on grab initiation. On release, apply controlled damping — do not snap to zero.

---

## Step 6 — Zero Energy Verification

Read the live pressure value from the pressure model. Display on pressure gauge with a readable numeric readout and a colored indicator band.

Pass threshold: `pressure < 0.1` (bar)

If pressure >= 0.1 at time of verification attempt: show failure feedback, do not advance, log the failed attempt with the current pressure value and timestamp.

If pressure < 0.1: register step pass, play confirmation audio, advance to Step 7 gate.

---

## Step 7 — Completion and Task Gate

Completion may only fire when:
- Steps 1 through 6 all carry `passed: true` in the session state
- The task completion interaction has been performed

On completion:
- Emit a `LOTO_COMPLETE` telemetry event with the full step pass trace
- Trigger the post-simulation UI transition
- Do not allow the simulator to return to an incomplete state without a full session reset

---

## Audio Cue Reference

| Event | Frequency | Notes |
|-------|-----------|-------|
| Valve creak (rotation start) | 400 Hz | Short transient, material-realistic |
| Spring engagement | 1200 Hz | Padlock shackle event |
| Connector snap | 1850 Hz | Hasp alignment snap event |
| Torque click (valve closed) | 4200 Hz | End-state confirmation |

All audio must be triggered by the specific interaction event, not by proximity or animation frame. Use Web Audio API. Do not use HTMLAudioElement for latency-sensitive cues.

---

## Failure State Handling

Any step failure must:
1. Display clear visual feedback identifying which tolerance was not met
2. Log the failed attempt with step ID, measured value, required threshold, and timestamp
3. Return interaction control to the learner for retry
4. Not reset prior passed steps unless a full session reset is explicitly triggered

Failure feedback must be readable under both bright and low-contrast scene lighting.

---

## What Not To Do

- Do not invent or approximate torque, distance, or pressure values
- Do not allow step skipping under any condition
- Do not fire completion without validating all prior step flags
- Do not request camera access without an explicit user gesture (see camera-permission-flow skill)
- Do not flatten the torque curve to a single constant
