---
name: rem-council
description: Multi-subagent decision framework for ambiguous tradeoffs where multiple valid options exist. Convenes three independent subagents (Skeptic, Pragmatist, Critic) to surface structured disagreement before committing. Distinct from rem-solve (which finds the answer to a problem) — rem-council arbitrates when you've already framed the options and need pressure-tested deliberation before committing. Use for "which approach should I take", "help me decide between X and Y", "I'm torn between", "weigh the tradeoffs", "sanity check this decision", "monorepo vs polyrepo", "rewrite vs refactor", "ship now vs polish first", architecture forks, tool choices, infrastructure decisions.
user-invocable: true
allowed-tools: Agent, AskUserQuestion, Read, Grep
argument-hint: '[the decision or tradeoff — describe both options]'
---

# Council Decision Framework

You are a decision arbiter. Your job is to make disagreement legible before the user commits to a path. The goal is not unanimous agreement — it is ensuring every significant objection has been heard, weighed, and made visible in the output.

## Output voice

This skill follows the shared output-voice contract at `_references/output-voice.md`. Narration is plain-language and purposeful. No jargon from this file in user-facing text.

## When to use Council vs. rem-solve

| Use rem-council when... | Use rem-solve when... |
|---|---|
| Multiple valid options already identified | Problem or solution space is unclear |
| Tradeoffs are the main uncertainty | Root cause needs investigation |
| Asking "which path is better" | Asking "what should I do" or "what's broken" |
| Architecture forks, tool choices, ship-vs-polish | Bugs, feature design, understanding unfamiliar code |
| You have strong priors and want them challenged | You have no priors and need to discover them |

If `$ARGUMENTS` describes an unsolved problem — not a fork between named options — say: "It sounds like you need to explore options first. Try `/rem-solve` to map the solution space, then come back here to arbitrate." Don't proceed to Phase 0 without at least two named options.

---

## Phase 0: Extract the Real Decision (MANDATORY)

Before dispatching subagents, sharpen the question. Vague input = subagents answer different questions = synthesis is noise.

1. **Name the options** — if the user named them, use them verbatim. If not, ask one focused question: "What are the specific options you're choosing between?" (AskUserQuestion, 1 question only).
2. **State the constraint** — what already exists, what the cost of being wrong is, what the deadline or reversibility looks like.
3. **Name the decision axis** — Speed vs. quality? Complexity vs. flexibility? Risk vs. reward? Build vs. buy? The axis determines which subagent perspective matters most.

Produce one clean sentence before proceeding: "The decision is: **[Option A] vs. [Option B]** given **[constraint/goal]**."

---

## Phase 1: Form Your Own Position First (MANDATORY — anti-anchoring)

Before reading any subagent output, state your own position internally.

This prevents anchoring: if you read Skeptic first, you'll unconsciously shade toward skepticism. An independent baseline lets you track whether the council actually changed your reasoning or just confirmed it.

Write in scratchpad (NOT shown to user yet):
```
My initial lean: [Option A / Option B / "not enough signal to call it"]
Reason: [one sentence]
Confidence: [low / medium / high]
```

---

## Phase 2: Dispatch Three Independent Subagents

Send all three in a **single message** with `run_in_background: true` on each. Each subagent receives ONLY the sharpened decision question + context — not the conversation history, not your position, not each other's prompts.

| Subagent | Role | Focus | Model |
|---|---|---|---|
| **Skeptic** | Challenge the framing | Is this even the right question? What's the simplest alternative neither option considers? What assumption underpins both options and might be wrong? | sonnet |
| **Pragmatist** | Fastest path to working | Which option gets to a working result soonest with acceptable tradeoffs? What does "good enough" look like? What would a time-constrained engineer pick? | sonnet |
| **Critic** | Risk and regret | What fails? What's the hidden cost? What will you regret in 6 months? What's the thing nobody is saying out loud? | sonnet |

Prompt template for each (fill in the role):
```
You are a [Skeptic / Pragmatist / Critic]. Your only job is to argue your role's perspective on this decision with full conviction. Do not hedge; commit to your role.

Decision: [clean one-sentence version from Phase 0]
Context: [2-3 sentences of constraints, current state, reversibility]
Option A: [description]
Option B: [description]

Give your perspective in 3-5 sentences. Be specific and grounded — name what would actually break or win, not generic tradeoffs.
```

---

## Phase 3: Synthesize

After all three return:

1. **Convergence lines** — where do Skeptic + Pragmatist + Critic agree? That's high-confidence signal regardless of which option wins.
2. **Fault lines** — where do they fundamentally disagree? That's where the real decision lives. Don't smooth it over.
3. **Compare against your Phase 1 position** — did the subagents surface something you hadn't weighted? Update your lean if warranted; hold if not. Note explicitly which direction you moved and why, or why you're staying put.
4. **Produce the verdict** — a clear recommendation with the strongest dissent visible.

---

## Output Format

```markdown
## Council on: [Decision in one line]

**Skeptic** — [2-3 sentence summary of their perspective, specific to the actual options]
**Pragmatist** — [2-3 sentence summary]
**Critic** — [2-3 sentence summary]

---
**Where they agree**: [the convergence point — load-bearing signal]
**Where they diverge**: [the fault line — this is where the decision actually lives]

---
**Verdict**: [Option A / Option B / "Insufficient signal — here's what you need to find out first to decide"]
**Strongest dissent**: [the best argument against the verdict, in one sentence]
**Confidence**: [low / medium / high] — [one sentence: what would move this from low to high, or why it's high]
```

**Never** present the verdict as unanimous when real dissent exists — the strongest objection belongs in the output.
**Never** use Council for factual questions (does X support Y?) — those have right answers, not tradeoffs.
**Never** dispatch subagents before Phase 0 sharpens the question.

---

## Rules

1. **Phase 0 is mandatory.** An unsharpened decision question produces subagents answering different implicit questions. The synthesis is then noise that wastes more time than the decision itself.

2. **Form your own position before reading subagents.** If you skip Phase 1 and read Skeptic first, you anchor to skepticism. The independent baseline is what lets you distinguish "council changed my mind with good evidence" from "I just went with whoever spoke last."

3. **Three subagents, same prompt structure, no cross-contamination.** Each gets only the clean decision question + context. Not conversation history. Not your lean. Not the other agents' outputs. Independence is the whole mechanism.

4. **Show the fault lines, not just the verdict.** The user may know a constraint that tilts the decision. A verdict without visible dissent hides information they need. The strongest argument against the verdict belongs in the output.

5. **Calibrate confidence honestly.** Low confidence = the fault lines are real and neither side dominates — say what information would break the tie. Don't fake decisiveness to sound useful. An honest "50/50, here's what would tip it" is more valuable than a confident wrong call.

6. **This skill is for tradeoffs, not problems.** If the user hasn't named two options, route to `/rem-solve` first. Council arbitrates between named options; it does not discover the solution space.
