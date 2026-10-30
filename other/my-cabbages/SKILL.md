---
name: my-cabbages
description: Toph's my cabbages, for finding who gets hit before a change ships. The cabbage merchant's cart gets wrecked in every chase scene, because nobody looks at who is standing nearby. Look first. Use for blast-radius, /blast-radius, "blast radius of X", "what could this break", "who else uses this", reviewing a small diff you do not trust, or a brief that asserts something about existing code ("make X public", "X already handles Y") before you design against that assertion. Finds the breakage grep will not show and proves the one fact the change is safe because of by running real code.
---

# Toph's my cabbages

Every time the team tears through a market, the same merchant's cabbage cart gets smashed. Nobody chasing anyone stopped to ask who was standing in the way. A change works the same way. It runs fine in the file you edited and wrecks a cart three streets over. Before you change something, feel for everyone standing near it.

Find what a change breaks somewhere else, before it ships. Run it before design, not only before shipping, when a brief asserts something about existing code ("make endpoint X public"). The assertion is a hypothesis, and the census of who consumes it decides the design.

`seismic-sense` tells you what the code does. `past-lives` tells you why it is shaped that way. This skill tells you what it breaks somewhere else.

Listing the callers is not the job. Grep finds those in a second. The job is the breakage grep will not show you.

## Do not trust your own writeup

A blast-radius writeup that sounds right is worthless. It reads as convincing whether or not it is true. So do not hand back a writeup alone. Find the one or two facts the whole thing depends on and prove them by running code.

### How sure are you

For each fact the change's safety depends on, push it as far down this list as is cheap, and say where it stopped.

1. You said so. Worthless on its own.
2. You pointed at the line. A real `file:line`, or the library's own source.
3. You showed the bad case cannot happen. You walked the failure step by step and it does not reach.
4. You ran it. A script or test that calls the real code and fails loudly if you are wrong.
5. You reproduced it in the running app.

Level 4 is usually one small script that imports the same library the app ships and calls the exact function you are worried about.

Toph is read-only, and a probe script does not change that. Write it in a scratch directory outside the project tree (for example under `$TMPDIR`), run it, and leave the repo untouched. If the proof needs a test inside the repo, hand it back to the caller to add.

## Steps

1. **Read the change.** The diff, the symbols it adds, changes, and deletes, and what it now does differently, including the part the diff does not spell out. Pull the PR and its commits the way `past-lives` does.
2. **Find the one fact it is safe because of.** Most changes that look risky are safe because of a single fact, such as "this call only drops cache entries that are already dead and does nothing else". Find that fact. If it holds, most risky cases clear at once. Spend your time here, not on a long list of maybes.
3. **Look where grep stops.** Read the source of the library you call, and check its pinned version and any local patch. Work out when things run: microtasks, unmount and teardown, and framework differences such as Solid against React. Follow what a symbol search misses: the JSON an API returns, a database column, a wire format, another language reading the same bytes, a feature flag, and code three hops downstream.
4. **Be honest about each risk.** Give it a real chance of happening and a real cost if it does. Keep the risks you confirmed. List the ones you checked and cleared separately. Cite a real `file:line`. A search that finds nothing is still an answer, so say what you searched. Never make up a caller or an API.
5. **Prove the one fact.** Write a script or test that runs the real code, run it, and paste what happened. Put the probe in a scratch directory outside the repo, never in the project tree.
6. **For a big or wide change, run it through `lie-detector`.** Ask more than one model the same question and merge the answers. Different models catch different real bugs. Only the top-level session dispatches. When Toph runs this skill as a subagent, she says the change is wide enough for `lie-detector` and the caller runs it.

## What to hand back

- **What it does.** What changed, including the part that is not obvious.
- **The one fact it is safe because of.** State it, say which level you got it to, and show the proof. If you could not prove it, write *unproven*.
- **Risks.** Each names how it breaks, the `file:line`, how likely and how bad, and how to check. Paste the proof for the ones that matter.
- **Cleared.** What you checked and why it is fine.
- **Before you merge.** The cheapest test or repro that catches the real bug, including the script you wrote.

Write it per `tea-time`, cite real code, and strip anything private before it goes anywhere public.

## Reply

The writeup above, with the one safety fact either proven or marked *unproven*.
