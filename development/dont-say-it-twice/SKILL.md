---
name: dont-say-it-twice
description: "Use when you catch yourself writing the same instruction a second time, or the human corrects the same thing again. Turn the rule into a lint, a type, a hook, a check, or a script instead of more text. Text asks for cooperation. Structure doesn't."
disable-model-invocation: true
kind: principle
---

# Don't say it twice

The second time you write the same instruction, stop writing it and build something that enforces it. Every correction from a human, every test failure, every "oh, again" is a signal. Catch it, put it somewhere that holds, and close the loop.

An instruction in a prompt or a doc only works if the reader notices it, remembers it, and follows it. A lint rule, a type, a hook, or a script works whether anyone cooperates or not.

## How

When you notice you're writing a rule for the second time:

1. Ask whether it could be a lint rule, a type that won't compile, a hook, a runtime check, or a script.
2. If yes, build that and delete the text.
3. If no, because it needs judgment, make the text more visible and add an example of what going wrong looks like.

## Pick the strongest option available

Agents copy whatever the surrounding code already does, so a weak guard becomes the next template. When more than one would work, go strongest first:

1. A state that can't be represented, so the wrong version doesn't compile.
2. A lint rule or banned API that fails CI.
3. A hook that runs on its own, before or after the tool call, without the agent choosing to.
4. One shared helper that does it right, so nobody writes their own.
5. A runtime check.
6. Text, as the last resort.

If the fix is structural, only do the structural fix. The instruction was the symptom.

## Where lessons go

- **A one-off.** Write it down where the project keeps decisions, so the next agent doesn't relearn it.
- **A recurring correction.** Becomes a skill, a lint rule, or a hook.
- **A pattern across projects.** Becomes a principle in the stack.

Two copies of the same rule drift. If a rule has to appear in two places, generate one from the other. The one-line index of principles in the mode is built from each skill's description line by a script. Nobody types it twice.

## Close the loop

Don't just record. Apply it now, or leave a concrete todo with a file path.

Three ways this goes wrong:

- Saying "I'll keep that in mind". Nothing was recorded, so nothing persists.
- Recording without building. A note that says "there should be a lint rule for this" is a lint rule that doesn't exist.
- Fixing the one instance and leaving the pattern. Grep for the rest.

## The test

Could the next agent break this rule without anything stopping them? If yes, it's still text.
