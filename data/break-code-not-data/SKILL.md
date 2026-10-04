---
name: break-code-not-data
description: "Use during planned rewrites and migrations with clear phases. Aim at the end state instead of keeping every step working with throwaway compatibility code. Code in your branch can break between phases. Anything persisted or deployed never does."
disable-model-invocation: true
kind: principle
---

# Break code, not data

In a planned rewrite, keeping every step fully working usually means compatibility code you'll throw away later. Except it doesn't get thrown away. It sticks around and becomes debt. So aim at the end state and accept some breakage along the way, but only in the part you control.

## The line

A rewrite touches two kinds of things.

**Code in your branch.** Nobody else is running it. It can break between phases as long as the breakage is planned, scoped, and easy to reverse. Don't write a shim to keep phase three working on your way to phase five.

**Anything persisted or deployed.** Database rows, files on disk, queue messages, API responses other services read, config that agents mid-task are holding. Old and new code read this at the same time, during a rolling deploy, a rollback, or an agent that started before the change. This never breaks. Add first, migrate, then remove. Never a change where the code and the data have to flip at the same moment.

The test for which side something is on: can a version you didn't deploy read it? If yes, it's data. Treat it that way even if it lives in a code file.

## How to run the rewrite

- **Say where breakage is allowed before you start.** Name the phases and which ones leave things broken. Unplanned breakage is a bug. Planned breakage is a step.
- **Keep the checks running on what you're touching.** Tests and lint for the area you're in stay green as you go, even while the rest of the rewrite is mid-flight.
- **Verify everything at the end.** Full static and runtime checks when the plan is done, not just the last phase. Breakage you allowed in the middle has to be gone by the end.

## Don't go too far the other way

A rewrite isn't a license to break things because you can. If customers are on the thing and you deploy often, the data side of the line is most of the work. Plan the migration order before the code. And if a phase can stay working for free, let it. The rule is that you don't pay for intermediate stability with throwaway code, not that you avoid stability.
