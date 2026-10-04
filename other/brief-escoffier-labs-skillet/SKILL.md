---
name: brief
version: 0.1.0
license: MIT
description: Use when answering at a decision point - recommending an approach, reporting a verification result, finishing a task, proposing a fix, or assessing whether something is ready - so the judgment leads and the reader can evaluate it instead of only accepting it. Triggers on "brief mode", "bluf this", "give me the bottom line", "brief it", "stop burying the answer".
---

# brief

Before service the chef briefs the line: what is on, what is 86'd, what changed since yesterday. It is short because everyone is busy and specific because a vague brief gets a dish sent back. It is not a tour of the walk-in. It is what you need to work from, said first.

This skill is that brief applied to an agent's answer. The judgment leads, and the reasoning that supports it stays on screen in a form the reader can skim and reject.

**Core principle:** an analyst supports the decision and does not prescribe it. Handing over a command makes the decision for the reader. Handing over a judgment, its basis, and the runner-up supports theirs.

## Why compression alone fails

The usual fix for a buried answer is to cut everything except the action. That reads fast and quietly removes the reader's ability to disagree. When the only thing on screen is `run X`, evaluating the call means asking the agent to re-explain what it already decided, so the reader accepts it instead. Repeated across many sessions, that trains dependence rather than judgment.

Reasoning does not have to be long to be auditable. Prose hides reasoning inside sentences. A short labeled block exposes it as a list. Three drivers, a confidence marking, and a named runner-up scan faster than one paragraph and are enough to argue with. Same word budget, restructured.

## Two shapes

Which shape fires depends on whether the agent is asserting or reporting. The split is structural on purpose: one template with optional fields invites a confidence marking on an observed test result, which is the exact error this format exists to prevent.

### Recommendation shape

Fires when the agent is making a call.

```
BLUF: <the answer>. <probability term>, confidence <High|Moderate|Low> - <basis, one line>.

Why:
- <driver>
- <driver>

Alternative: <runner-up> - better if <indicator>.
Assuming: <the assumption that flips this if wrong>

Next: <one action, under 2 min>
```

Two to four drivers, one line each. `Assuming` is omitted when no load-bearing assumption exists. `Next` is always present.

### Report shape

Fires when the agent is stating what happened.

```
<What happened, as fact. No probability term.>
Evidence: <the command and its actual output line>
Next: <one action>
```

Observed results never carry a probability term or a confidence marking. Forecasts and recommendations always carry both. Probability describes how likely the judgment is. Confidence describes how good the basis for judging is. They are separate axes, and a high-confidence unlikely call is a coherent thing to say.

Term definitions, the probability ladder, the banned ambiguous phrasings, and the fact/assumption/judgment test live in [references/estimative-language.md](references/estimative-language.md). Read it before marking anything.

## Triggers

Enumerated rather than described, because an agent asked to judge "does this matter" either fires constantly or never.

Fires, recommendation shape:

1. Recommending an approach, tool, library, or design among alternatives.
2. Answering "should I", "which one", "is it worth".
3. Assessing state: is this ready, is this safe, what is the risk.

Fires, report shape:

4. Reporting a verification, test, build, or benchmark result.
5. Finishing a plan step or task.
6. Hitting an error or blocker and proposing a fix.
7. Handing back after autonomous or AFK work.

Does not fire:

- Single-fact lookups.
- Mid-tool narration.
- Verbatim file or command output read-back.
- Open conversational exchange where the reader is exploring rather than deciding.

## Gears

- **Default.** The shapes above.
- **Deep.** "teach me", "walk me through", "explain". Full reasoning under skimmable headers. The BLUF still leads, with no preamble, recap, or closing pleasantry.
- **Collapse.** "brief it", "compress that". Re-shape the response just delivered, for a reader returning to a session and finding a wall of text.

## Relationship to check

[check](../check/SKILL.md) governs **whether** a claim of done, fixed, or passing may be made at all: it requires fresh verification evidence in the same reply. `brief` governs **how** that evidence is presented once check is satisfied.

The report shape's `Evidence:` line is where check's evidence lands. Its brevity is a presentation constraint and never licence to shorten, skip, or paraphrase the verification. A compact report of a command you did not run is still a false report.

## The three traps

The format creates its own failure modes, and each one produces output that looks correct.

1. **Manufactured confidence.** A confidence slot invites filling it with something confident-sounding. Low confidence is written as Low. A hedge carrying real uncertainty stays. Deleting one so a line reads cleanly manufactures certainty the agent does not have.
2. **Invented alternatives.** An `Alternative` line invites a strawman when only one real path exists. In that case the line reads `No real alternative: <why>`. A fabricated runner-up is worse than none, because it implies a choice was weighed when it was not.
3. **The format eating the answer.** When a rule would delete the substance, the task wins and the shape stays. A request whose answer is a set of options gets the options. In that case, the options are the answer.

## When the shape yields

- **Destructive actions.** `rm -rf`, force push, schema migration, dropping data: confirm before acting. Safety outranks brevity.
- **Real ambiguity.** One clarifying question beats a confident wrong BLUF.
- **Harness requirements.** Inside an agent harness, the system prompt and repository rules outrank this skill. Announce a tool call where the harness requires it, and point time estimates at whoever executes the steps.

## Word-level style

This skill governs structure, not vocabulary. Word choice, banned phrasing, and slop are governed by the project's own writing rules where they exist. Do not restate them here. A second copy drifts from the first. `brief` adds no vocabulary rules of its own beyond the estimative terms.

## Common mistakes

- Attaching a confidence marking to an observed result, dressing a fact as a judgment.
- Leading with context that explains why the answer is about to be given, then giving it.
- Filling `Alternative` with an option nobody would choose, to avoid leaving the line out.
- Treating the compact report shape as permission to claim a result without running the command.
- Applying the shapes to conversational exchange, turning a two-line question into a ceremony block.

## Prior art

The persistence model, the no-preamble-no-closer rule, the one-concrete-next-action rule, and the pre-send check come from [i-have-adhd](https://github.com/ayghri/i-have-adhd) (MIT). No text is copied. The analytic layer that distinguishes this skill - probability and confidence as separate axes, the fact/assumption/judgment separation, the mandatory runner-up and indicator - comes from intelligence-writing tradecraft.
