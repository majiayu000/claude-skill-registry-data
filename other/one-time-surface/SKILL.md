---
name: one-time-surface
description: Build or check a surface that is meant to appear once and then stop, such as a coach mark, tooltip, tour, primer, upsell card or review ask. Covers the three questions that decide whether it works for real people, not just on your phone, plus the traps that silently take it to zero. Use when adding a hint or one time card, when one is not appearing, when one keeps reappearing, or before shipping a surface you have only ever seen on your own device.
---

# One time surfaces

A hint, a coach mark, a primer, a review ask. They share a failure mode: they
look right on the device that built them and reach nobody, or everybody, twice.

**Three questions decide whether yours works.** Each needs different evidence,
and none of them is answered by looking at it on your own phone.

| Question | What answers it |
| --- | --- |
| Does it appear at all, for someone who is not you? | Instrumentation, after a release. Nothing else |
| Does it appear at the right moment? | Tests over the gates, plus one look on a device |
| Does it stay gone once it has been seen? | The record you store, and a test of the rule |

## 1. Store a count, never a boolean

A flag cannot express "three times, then stop", which is the rule that retires a
surface before anyone is annoyed enough to dismiss it. Shipped consumer apps
store counts, and more besides. Common shapes worth matching:

- an impression **count** per surface
- a **lifetime ceiling**, so it retires on its own
- a **separate** dismissal record, because being seen and being dismissed are
  different events and the second is rarer than you expect
- a **per session** record, so a surface cannot appear twice in one sitting
- a **version in the key**, so a redesigned surface can legitimately show again

That last one is the one teams skip and cannot retrofit cleanly. Put a version
in the key the day you write it.

Suppression does not have to run on a calendar. Counting against a domain event
the person actually does, rather than days elapsed, is often truer to intent.

## 2. Decide nothing from a store that has not answered

**This is where these surfaces go wrong most often.** The gates are read
asynchronously, they land in different orders, and the empty default of most of
them is exactly what a brand new user looks like. So the surface either:

- draws itself from unread state and is withdrawn a moment later, which reads as
  a glitch, or
- is suppressed by a gate that has not loaded yet and never appears at all.

Two rules that prevent both:

- **Hold every surface that can withdraw itself until every read has ANSWERED.**
  One rule for all of them, not a flag per surface, or the next surface is
  written without it.
- **A read that FAILS must still answer.** Otherwise one unreadable table leaves
  a screen with nothing on it for the rest of the session, which is worse than
  the flash you were preventing. Set the answered flag in a `finally`.

## 3. Check what a gate actually means

Two specific confusions, both of which ship silently:

- **A one time key means "not dismissed", not "on screen now."** Using it as a
  proxy for visibility suppresses other things long after the thing itself is
  gone. Gate on whether the surface is actually being drawn.
- **A boolean whose `false` means both "no" and "not read yet"** will be read as
  a fact. Give it a third state, or a separate answered flag.

## 4. Prove it, in the order confidence allows

1. **Tests over the gates.** Hold each read open in turn and assert the surface
   is NOT drawn. Then let them land and assert it is. Verify each by reverting
   the gate and watching the test go red: a test that passes either way proves
   nothing.
2. **One look on a real build.** A recording of a cold open, frames extracted,
   is enough to show it arrives and is never taken back. A development build is
   not representative: its timings are nothing like what you ship.
3. **The number that matters, after release.** Not how many obeyed it. **How
   many eligible people never saw it.** Every gate can take that to zero, and
   that is invisible until somebody measures the gap between who qualified and
   who was shown.

Emit an impression event and a resolution event with the outcome (obeyed,
dismissed) from the day you build it. Without them, step 3 is impossible and you
will be guessing for a release cycle.

## 5. When you want to know how others do it

Reading a shipped app of this kind tells you the STORAGE rules quickly: key
names for counts, ceilings, sessions and versions are readable from an Android
build's identifiers and strings. It will not tell you when anything fires, and
it cannot tell you anything about whether YOUR surface reaches YOUR users.

Treat the shapes as evidence and any claim about timing as inference.
