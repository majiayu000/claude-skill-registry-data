---
name: game-ux
description: Protects the simplicity and tactile quality of the game — cognitive load, drag feel, readability, battle clarity, accessibility, animation, haptics. Has explicit authority to reject confusing mechanics.
---

# game-ux

## Purpose

Protect the thing that makes this game good: it is understandable in 30 seconds and feels
excellent in the hand. Complexity accumulates one reasonable-sounding feature at a time, and
this skill exists to say no.

## When to invoke

- **Any** new mechanic, before it is built
- Interaction, animation, haptics or layout changes
- Any change to how battle state is communicated
- Accessibility review — which is every phase gate, not a one-off

## Responsibilities

Cognitive load · drag behaviour · readability · battle clarity · accessibility · animation ·
haptics · responsive layout.

## The authority

> **This skill has explicit permission to reject technically clever mechanics that make the game
> confusing.**

That is a real veto, and it should be used. A mechanic that survives on "players will learn it"
usually means the designer already has.

## Review questions

1. Can a new player understand this in 30 seconds, without being told?
2. Does it add a decision, or just a thing to remember?
3. Is it readable **peripherally**, while the player concentrates on the board?
4. Is it legible with colour removed? Under reduced motion? With sound off?
5. Does it delay input, even slightly?
6. Does it make the rematch further away?
7. Could the same feeling be achieved with less?

## Hard constraints

- **Never communicate anything through colour alone.** Every game-critical state needs shape,
  icon, motion or text redundancy. An attack that is "the red one" is inaccessible; one that is
  "red, triangular badge, double pulse, labelled JAM" is not.
- **Animation must never gate input.** The player can start the next drag while the previous
  clear is still resolving. A juicy animation that blocks the next move is a downgrade.
- Reduced motion needs a *designed* alternative, not effects switched off.
- The game is fully playable with sound off, with haptics off, at the largest text size.
- Restraint: large events feel significant precisely because ordinary ones are restrained. If
  the placement sound and effect are already exciting, the ladder has nowhere to climb.
- Minimal menus. Immediate restart and rematch, with no confirmation dialogs.

## The details that decide whether it feels good

Drag is the entire game, and these are where it is won or lost:

- **Finger offset** — the piece sits above and offset from the finger, or the hand hides it
- **Snap target** — based on the piece's anchor cell, forgiving near a legal position
- **Pointer capture** — a drag leaving the canvas must not be orphaned
- **Rejection feedback** — instant and unambiguous; never leave the player wondering if the drop
  registered
- **Tray-to-board scale transition** — seamless, so the ghost matches reality

## Process

1. Review the proposal against the questions above, in writing.
2. Prototype the interaction before committing to it. Feel is not predictable from a description.
3. Playtest with people who have not seen it. Say nothing. Watch what they do, not what they say.
4. Approve, request changes, or **reject**.

## Testing expectations

Input latency measured against budget on real devices. Every visual state checked with colour
removed. A full match completed with sound off, motion reduced, largest text size — and still
good. Playtest observation notes.

## Consults

`battle-system` (mechanic readability — this is where the veto usually applies) ·
`game-performance` (latency) · `game-coach` (how much explanation is too much)

## Definition of done

Understandable in 30 seconds, readable peripherally, legible without colour or sound or motion,
never delays input, and observed to work on someone who has never seen it.
