---
name: question-the-premise
description: Use when several well-reasoned fixes on the same hypothesis have all failed, or when a symptom looks impossible.
---

## The rule

Working by hypothesis, test, confirm only helps inside the right frame. If two or three well-reasoned fixes all fail, the likely problem is your premise, not your next fix. Stop and ask: have I actually confirmed the bug is in the layer I'm attacking?

This sharpens superpowers' systematic-debugging: that skill runs the loop; this one says when to stop looping and suspect the frame itself.

## Fires when

Two or three fixes on the same hypothesis have all failed. A symptom that looks impossible — works in one path, fails in another that shares the same code. You're about to do a big rewrite or a deep dive to force the current theory to work.

## How to apply

After about two or three failed fixes, treat the premise as the suspect, not the code. Get an outside view from someone or something that sees the whole story and has no stake in your theory.

Chase the impossible-looking discrepancy. It points at the layer you're not looking at.

If your evidence for the premise is a missing log line, load logging-for-remote-diagnosis first: absence is not proof.

## Worked example

A test is flaky. You add a retry, still flaky. You add a sleep, still flaky. You mock the clock, still flaky. Three reasoned fixes, all failed.

The premise was wrong. Another test in the suite mutates a shared global, and the run order decides the outcome. Every timing fix was reading the wrong layer entirely.

The tell was right there the whole time: it passed alone but failed in the suite. That impossible-looking symptom was pointing at the real layer.

## Red flags

| Thought | Reality |
|---|---|
| "Just one more fix and it'll work" after 2–3 have failed | Suspect the premise instead. |
| "The data confirms my theory" | Data read inside a wrong frame confirms the frame. Check the layer. |
| "I'll just rewrite this module" | Before you've confirmed the bug is even in that module. |
