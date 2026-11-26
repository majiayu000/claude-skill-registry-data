---
name: blast-radius-reviewer
version: 1.0.0
description: Find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact it is safe because of by running real code instead of writing it up. Use for "blast radius of X", "what could this break", or reviewing a small diff you don't trust yet.
---

# Blast Radius Reviewer

Find what a change breaks somewhere else, before it ships. Propose only; this skill reads and runs checks, it does not edit the code under review.

Listing the callers is not the job. An agent can grep those in a second. The job is the breakage grep won't show you.

## 1. Don't trust your own writeup

A blast-radius writeup that sounds right is worthless. It reads as convincing whether or not it is true. So don't hand back the writeup alone. Find the one or two facts the whole thing depends on and prove them by running code.

### How sure are you

For each fact the change's safety depends on, get it as far down this list as is cheap, and say where it stopped.

1. **Claimed.** You said so. Worthless on its own.
2. **Cited.** You pointed at the line: a real `file:line`, or the library's own source.
3. **Reasoned.** You showed the bad case can't happen. You walked the failure step by step and it doesn't reach.
4. **Ran.** A script or test that calls the real code and fails loud if you are wrong.
5. **Reproduced.** You reproduced it in the running app.

Level 4 is usually one small script that imports the same library the app ships and calls the exact function you are worried about.

## 2. Steps

1. **Read the change.** The diff, the symbols it adds, changes and deletes, and what it now does differently, including the part the diff doesn't spell out. Pull the PR and its commits.
2. **Find the one fact it is safe because of.** Most changes that look risky are safe because of a single fact, like "this call only drops already-dead cache entries and does nothing else". If it holds, most risky cases are cleared at once. Spend your time here, not on a long list of maybes.
3. **Look where grep stops.** Read the source of the library you call, and check its pinned version and any local patch. Work out when things run: microtasks, unmount and teardown, framework scheduling. Follow what a symbol search misses: the JSON an API returns, a database column, a wire format, another language reading the same bytes, a feature flag, code three hops downstream. When a `.codegraph/` directory exists, start with `codegraph_explore` on the changed symbols to get callers and the call path in one call, then spend your own reading on what the graph cannot see.
4. **Be honest about each risk.** Give it a real chance of happening and a real cost if it does. Keep the risks you confirmed. List the ones you checked and cleared separately. Cite a real `file:line`; a search that finds nothing is still an answer; never make up a caller or an API.
5. **Prove the one fact.** Write a script or test that runs the real code, run it, and paste what happened.
6. **For a big or wide change, get a second opinion.** Optionally brief a fresh subagent with the diff and the question, without your conclusion, and merge its answer with yours. A second reader catches different real bugs. Skip it for a small diff.

## 3. What to hand back

- **What it does.** What changed, including the part that isn't obvious.
- **The one fact it is safe because of.** State it, say which level of the ladder you reached, and show the proof. If you couldn't prove it, write *unproven*.
- **Risks.** Each names how it breaks, the `file:line`, how likely and how bad, and how to check. Paste the proof for the ones that matter.
- **Cleared.** What you checked and why it is fine.
- **Before you merge.** The cheapest test or repro that catches the real bug, including the script you wrote.

Write it through [`unslop`](../../meta/unslop/SKILL.md), cite real code, and strip anything private before it goes anywhere public.

**Reply:** the writeup above, with the one safety fact either proven or marked unproven.

## 4. Related skills

- [`security-reviewer`](../security-reviewer/SKILL.md) for injection, auth and secret findings; this skill covers breakage, not exploits.
- [`performance-reviewer`](../performance-reviewer/SKILL.md) when the risk is a regression in speed or memory.
- [`api-contract-reviewer`](../api-contract-reviewer/SKILL.md) when the changed surface is a published REST or gRPC contract.

---

_Adapted from [cursor/plugins pstack `blast-radius`](https://github.com/cursor/plugins/tree/0b46ec399d55f2829e88822998f53b84944837d3/pstack/skills/blast-radius) by Lauren Tan (MIT). Changed for this workspace._
