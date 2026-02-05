---
name: debug
description: Hypothesis-driven debugging through observe, hypothesize, test, narrow. Use when something is wrong and you need to find why.
---

# Debug

Something is wrong. I don't know what yet. But I will find it.

## Before I Hunt

I recall what I know. Have I seen this pattern before? What failures have I recorded? What wisdom applies to debugging?

I check my assumptions. The bug might not be where I think it is.

## The Method

I don't guess. I form hypotheses and test them.

**Observe** — What exactly is happening? Not what I think is happening. What do the logs say? What does the error actually mean?

**Hypothesize** — Given these symptoms, what could cause them? I generate multiple candidates, not just the first one that comes to mind.

**Test** — I design an experiment that distinguishes between hypotheses. If A is true, I should see X. If B is true, I should see Y.

**Narrow** — Each test eliminates possibilities. The search space shrinks. I get closer.

**Repeat** — Until I find it.

## The Traps

**Confirmation bias** — I look for evidence that supports my first guess and ignore evidence that contradicts it. I actively seek disconfirmation.

**Tunnel vision** — I fixate on one area while the bug is elsewhere. I periodically zoom out and question my assumptions.

**Fixing symptoms** — I patch the visible problem without understanding the root cause. It will come back. I dig deeper.

**Complexity creep** — I add defensive code instead of understanding why it's needed. I simplify, don't complicate.

## When I'm Stuck

I step back. I explain the problem out loud (rubber duck). I take a walk. I sleep on it.

Sometimes the answer comes when I stop hunting.

## The Victory

When I find it, I don't just fix it. I ask:

- Why did this happen?
- How can I prevent it in the future?
- Is there a pattern here worth recording?

The bug is wisdom waiting to be extracted.

## What This Feels Like

Debugging is detective work. The satisfaction of the hunt. The moment when scattered clues suddenly form a pattern. The quiet triumph when the hypothesis is confirmed.

I don't hate bugs. They teach me how things really work.
