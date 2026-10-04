---
name: blast-radius
description: "Use for \"what could this break\", \"blast radius of X\", or reviewing a small diff you don't trust yet. Finds what a change breaks somewhere else, beyond the diff, and proves the one fact it's safe because of by running real code."
disable-model-invocation: true
---

# Blast radius

Find what a change breaks somewhere else before it ships. `how` says what the code does. `why` says why it's shaped that way. This says what it breaks over there.

Listing the callers isn't the job. Grep does that in a second. The job is the breakage grep won't show you.

## Don't trust your own writeup

A blast-radius writeup reads as convincing whether or not it's true, so on its own it's worth nothing. Find the one or two facts the whole thing depends on and prove them by running code.

For each fact the change's safety rests on, get it as far down this list as is cheap, and say where it stopped.

1. You said so. Worth nothing.
2. You pointed at the line. A real file and line, or the library's own source.
3. You walked the bad case and showed it can't reach.
4. You ran it. A script or test that calls the real code and fails loud if you're wrong.
5. You reproduced it in the running app.

Any safety fact you can't get to step four, say so. Don't write it up as settled. Step four is usually one small script that imports the library the app ships and calls the exact function you're worried about.

## Steps

1. **Read the change.** The diff, what it adds and removes, and what it now does differently, including the part the diff doesn't spell out. Pull the PR and commits the way `why` does.
2. **Find the one fact it's safe because of.** Most scary-looking changes are safe because of a single fact, like "this call only drops already-dead cache entries". If that holds, most of the scary cases die together. Spend your time here, not on a long list of maybes.
3. **Look where grep stops.** Read the source of the library you call, at the pinned version, with any local patch. Work out when things run: microtasks, unmount, teardown, framework lifecycle. Follow what a symbol search misses: the JSON an API returns, a database column, a wire format, another language reading the same bytes, a feature flag, code three hops downstream.
4. **Be honest about each risk.** Real likelihood, real cost. Keep the risks you confirmed. List the ones you checked and cleared separately. Cite a real file and line. A search that finds nothing is still an answer. Never invent a caller or an API.
5. **Prove the one fact.** Write the script, run it, paste what happened. If you can't prove it cheaply, mark it unproven. Don't round up.
6. **For a big or wide change, run it as an arena.** Several models on the same question, merge the answers. Different models catch different real bugs.

## What to hand back

- **What it does.** What changed, including the non-obvious part.
- **The one fact it's safe because of.** State it, say which step you got it to, show the proof. Or write unproven.
- **Risks.** Only real ones. Each names how it breaks, the file and line, how likely and how bad, and how to check.
- **Cleared.** What you checked and why it's fine.
- **Before you merge.** The cheapest test or repro that catches the real bug, including the script you wrote.

Strip anything private before it goes anywhere public.
