---
name: fix-the-root-cause
description: Use when fixing any bug, especially one that surfaces far from where the bad state was created.
---

## The rule

The place a bug shows up is rarely the place it comes from. Patching the symptom at the surface leaves the real cause free to break something else next week. Find the layer that produced the bad state and fix it there.

This sharpens superpowers' systematic-debugging: that skill finds the bug; this one decides which layer the fix belongs in.

## Fires when

Any bug fix, especially a crash, a null, a corrupt value, or a wrong result that shows up far from where the data was created.

## How to apply

Trace the bad value back to where it was born, not just where it blew up. Ask "what let this state exist in the first place?" and fix that.

A guard at the call site is fine as a seatbelt, but it isn't the fix if something upstream keeps handing out broken state.

## Worked example

A page crashes on `user.address.city` because address is null. The symptom fix is a null check on the page. But the real cause is the user loader, which returns a half-built user when a join fails, so any page that touches address is one click from the same crash. Fixing the loader to either return a complete user or fail loudly kills the whole class of crashes. The null check alone just moves the next crash to a different page.

## Red flags

| Thought | Reality |
|---|---|
| "A null check here makes it stop crashing" | It stops this crash, not the cause. |
| "The bug is on this page" | The bug is wherever the bad value was made. |
| "I'll patch the symptom now and fix it properly later" | Later rarely comes, and the bad state keeps spreading. |
