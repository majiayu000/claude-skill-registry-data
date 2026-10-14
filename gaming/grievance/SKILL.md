---
name: grievance
description: Read a grievance capture from sector-unity-proto — the F9 debug key that records what the screen actually showed when something looked wrong. Use when the user says a grievance/capture is waiting, refers to "that thing that looked wrong", describes a visual or motion complaint in prose ("it zoomed by me", "the planet is tiny", "it whips past"), or asks what the last capture showed. Also use before answering any question about on-screen size, position, or motion in this project — the capture is ground truth, memory is not.
---

# Grievance

A grievance is a measurement of a complaint. The user presses a key when the screen looks wrong. The game writes what it was actually showing. You read numbers instead of guessing from prose.

## The keys

| Key | What it records |
|---|---|
| `F9` | One frame: `frame.png` + `state.txt` |
| `Shift+F9` | The same, plus `motion.txt` — 60 frames, one second |

Source: `Assets/_Project/Proto/Diagnostics/GrievanceCapture.cs`. It self-registers, so it needs no scene setup. It only works in play mode.

## Where captures live

```
<repo>/Logs/grievance-<yyyyMMdd-HHmmss>/
├── frame.png     the game view
├── state.txt     cameras, ship, every catalog body
└── motion.txt    the body rows again, per frame (Shift+F9 only)
```

Find the newest:

```bash
ls -dt Logs/grievance-* | head -1
```

## How to read one

Do these in order. Stop when the numbers answer the question.

1. **Read `state.txt` first.** It is small and it carries the answer most of the time.
2. **Look at `frame.png`** only when the complaint is about appearance, not number. A size or position complaint is already in `state.txt`.
3. **Read `motion.txt`** only when the complaint contains a verb — whips, drifts, jumps, lags, zooms. A static complaint does not need it.

### What each row means

```
camera IsoCamera ortho=True size=21.0 ...
```
`ortho=True` means screen size ignores distance (P-DIVIDE). `ortho=False` with a `fov` means screen size doubles for every halving of distance. If a body grows on approach and the user did not want that, this row is the cause, not the symptom.

```
body Ceres dist=3,748 km bearing=41.200 deg screen=(1204,560) 130 px VISIBLE
```
- `dist` and `bearing` are truth, from the double-precision world model.
- `screen` and `px` are what the player saw, from `WorldToScreenPoint`.
- No `screen=` field means no `Scenery <name>` object exists for that body.
- No `VISIBLE` means it projected off-screen or behind the camera.

### Motion

`motion.txt` repeats the body rows per frame. Diff a column to get a rate. Bearing slew is `v / range`, so it diverges as range goes to zero — a large per-frame delta at small `dist` is that singularity, not a bug in the mover.

```bash
grep 'body Ceres' Logs/grievance-*/motion.txt | awk '{print $5}'
```

At 60 fps, `delta x 60` is degrees per second. The screen is about 8 px per degree at fov 100 on a 2560-wide view, so `deg/s x 8` is pixels per second.

## Rules

- Quote the number from the capture. Never restate the user's prose back as a finding.
- One capture is one frame of one session. It shows what happened, not why.
- When the capture disagrees with what you expected, the capture is right.
- When no capture exists and the complaint is visual, ask for one before diagnosing. `F9` costs the user one keypress and saves you a wrong hypothesis.
- Captures accumulate. Delete old ones only when the user asks.

## Handoff

A grievance answers item 3 (LEDGER) and item 4 (CAUSE) of a `premise-lock` block. Move the numbers straight into the ledger as `VERIFIED`, with the capture path as the evidence. Do not re-derive them later from memory.
