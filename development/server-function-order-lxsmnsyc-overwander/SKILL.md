---
name: server-function-order
description: A server function is addressed by its place in its file, and only the build guard keeps a tab from another build from calling the wrong one. Applies whenever adding, removing, moving or changing the parameters of a function whose body opens with 'use server', and whenever touching the build guard or anything that calls the server outside `fetch`.
---

# Server functions and the build guard

In a production build, SolidStart names every `'use server'` function by its file and its position in that file (`<file hash>-<index>`). The function's name is not part of it.

A tab loaded before a deploy keeps calling those positions, with the arguments its own build sends. When a function moves, that tab would call whatever sits in its slot now. This happened twice before the guard was strict:

- A new parameter at the front of the position save shifted every argument, so a player's chunk X was read as a step count and they were moved to 0,0.
- Three claim-list functions merged into one moved the nest and phenomenon claims up two slots.

## The guard

A tab names its build on every server call (`src/utils/stale-build.ts` wraps `fetch`), and `src/middleware/index.ts` refuses any server call that does not name the live build, before any function runs. The tab reloads on the refusal. A call that names no build is refused too.

Because no call from another build ever reaches a function, server functions may be added, removed, reordered or given new parameters like any other code. A function nothing calls any more is deleted rather than kept for its slot.

## The rules

- **Never weaken the guard.** Letting through a call that names no build, or another build, brings back every hazard above.
- **Every server call goes through `fetch`.** SolidStart's client looks `fetch` up when each call is made, so the wrapper covers it. Anything that reaches `/_server` another way (a `<form action>` posted without JavaScript, `navigator.sendBeacon`, a worker) sends no build header and is refused, so it needs the header added or a different route.
- **The guard must be installed first.** `guardServerCalls()` runs in `src/entry-client.tsx` before the app mounts; a call made before it would be refused.

## Checking a change

For a change to the guard, run `test/utils/build.test.ts` and `test/utils/stale-build.test.ts`. For a new way of calling the server, check in the browser's network panel that the request carries the `X-Build` header.
