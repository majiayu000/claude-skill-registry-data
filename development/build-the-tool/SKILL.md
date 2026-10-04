---
name: build-the-tool
description: "Use for any work that isn't trivial: edits across files, migrations, analysis, checks. Write the script, codemod, generator, or shared skill that does the work or proves it, instead of doing it by hand. The tool is what a reviewer reruns."
disable-model-invocation: true
kind: principle
---

# Build the tool

If the work isn't trivial, write the tool that does it instead of doing it by hand.

Two reasons. It's faster, since a script does the same thing every time and reruns for free. And it's checkable. A reviewer can read one script and run it. Work done by hand can only be checked by doing it again. A script turns "trust me" into "run this".

## How

- **Do the first one by hand.** That's how you learn the recipe. Then write the tool, run it on that same unit, and diff against your hand-done version. Now you trust the tool.
- **Make it safe to rerun.** A reviewer will run it. So will you, after a fix. Running it twice gives the same result.
- **Pick the right shape.** A codemod or script for edits. A generator for repetitive files. A dump to sqlite and a query for analysis. A rerunnable check for verification.
- **One script beats a fleet of subagents.** If a tool can process every unit in one pass, run it yourself. Don't fan out agents to hand-apply what a script could do.
- **When you do fan out, the tool is a skill.** Write the recipe, what counts as done, and what not to touch in one file every subagent reads. They all follow the same version instead of each drifting on its own prompt. Keep that file outside their write scope so none of them can quietly change the rules.
- **Commit it if the work outlives the session.** The next run reruns it instead of redoing it.

## The tool's output is the evidence

What the tool produces is what you attach as proof. A diff, a query result, a test log, a recording. Evidence is something the work actually produced, never something you wrote up afterward to describe it. Recordings especially: the test runner captures them as a side effect of running, you don't record them by hand. If the tool ran, the proof exists already. If you're assembling proof by hand, you skipped the tool.

## The bar

Triviality, not repetition. A couple of obvious edits you can see at a glance don't need a script. A one-off still does when the script is what makes it checkable.

Build the smallest script that does or proves the job. Never a framework.

## The test

If you applied this rule, there's a file in the diff. A script, a codemod, a generator, or a skill for subagents. No file, you didn't apply it.
