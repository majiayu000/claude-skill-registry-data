---
name: prove-it
description: "Use after finishing a task, before saying it's done. Check the real thing, run the feature, read the actual value, inspect the diff, and attach the evidence to the tracker. Not a proxy, not a self-report, not 'it compiles'."
disable-model-invocation: true
kind: principle
---

# Prove it

"It should work" is a guess. Every task ships with evidence that it works, and the evidence is something the work actually produced. No evidence, no turn-in.

Checking indirectly feels cheaper. File timestamps, a subagent's summary, a cached screenshot, a green build. It isn't. Acting on a wrong guess costs more than looking at the real thing.

## Check the real thing

After any task, ask "how do I prove this actually works?" Then do that.

- Read the actual value, not a cached or derived copy of it.
- Check the process directly, not some state that implies it's running.
- Build it, run it, then walk the feature path from input to output. Building is necessary, not sufficient.
- For integrations, test the full round trip end to end.
- When a check fails, suspect how you're looking before you suspect the system.

## Use it like a person would

Passing tests are the floor. Use what you built the way a user would. Click through the flow in a real browser with agent-browser. Run the CLI with real arguments. Hit the endpoint with a real request.

For web UIs, walk the flow a second time keyboard-only. Tab reaches every control in a sensible order, focus is always visible, Enter and Space activate, Escape dismisses, nothing traps focus. If a keyboard user can't finish, the flow isn't done.

## What evidence looks like

- **Anything a user can see.** Screenshots of the finished states, including empty, loading, and error states when they exist. Terminal UIs too, an image or a text capture of the rendered frame.
- **Anything that changes state.** Receipts, not assurances. The actual request or mutation you ran, and the stored record afterward with its fields. State before, the action, state after. Same for jobs, webhooks, and migrations.
- **Bugs.** Capture the broken state before touching code. Fix. Capture the same thing again. Every fix ships with a before and an after. If you can't reproduce it, stop and say so.
- **Anything a still can't prove.** Animations, drag, keyboard traversal, multi-step journeys. A `.webm`, recorded by the test runner as a side effect of running, not by hand. A GIF only when the tooling can't emit webm. If recording becomes more work than the change, say so and attach stills.

Every file carries its real extension. `.png`, `.webm`, `.json`, `.html`. That's how the viewer knows what opens it.

## Script the check when you can

The strongest proof is a script that reruns the same comparison. Write it, run it, keep its output. A reviewer runs the script instead of trusting your word.

## Delegated work

Trust artifacts, not summaries. When a subagent says it's done, read the diff, open the files, run the thing. Agents report what they meant to do, which isn't always what happened.

## Where evidence goes

Evidence lives in the work tracker, attached to the task when you turn it in, with the task id in the PR description. Whichever tracker the project uses, the contract is the same: real files, attached at turn-in, a human completes after the merge. `tracker` says where each backend takes them. Never in git. History carries every committed byte forever, in every clone.

Never fabricate proof. If the evidence doesn't exist, the work isn't done.
