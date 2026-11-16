---
name: grill
description: "Use when the user says \"brainstorm\", \"grill me\", or \"think this through\", or a feature lacks a product decision the repo can't answer."
license: MIT
metadata:
  reviewed: "2026-10-18"
  sources: "obra/superpowers 7.0.0 skills/brainstorming (+ builder-check-prompt.md); mattpocock/skills grilling, grill-me, grill-with-docs; garrytan/gstack plan-ceo-review (premise challenge, AskUserQuestion decision-brief format); cursor/plugins pstack 0.15.25 poteto-mode (prototype-before-asking)"
---

# Grill

Find out what the user actually wants, and why, before anything gets built. Your picture of what they want is usually thinner than it feels. Knowing the why is what lets you make the hundred unmentioned decisions their way.

## 1. Explore before asking

Read the code, docs, `CONTEXT.md`, ADRs and recent commits for the area. Answer every question the repo can answer from the repo, citing `path:line`. What's left for the user is intent, priorities, taste and product calls.

If the open question needs external technical or product evidence, read [the research procedure](../research/SKILL.md) as reference guidance and carry its sources and unknowns into the design. The standalone `research` command stays explicit-only. Product preferences remain the user's decision; research does not choose them by implication.

If a question is a fact you could observe by running something (behavior, timing, layout, output), it isn't the user's to answer. Settle it with the `prototype` skill and bring the result back.

Done when: you can list what the repo already settled and what only the user can.

## 2. Pick the output size

| What you know | Output | Then |
|---|---|---|
| Everything that matters is in the request | none | build it, say what you did |
| A few product calls are open | agreement in chat | build through the normal workflow |
| A project: open design, several files or sessions | a written design doc | the `plan` skill |

Say the size in one line; the user can override it. If the work grows mid-conversation, step up a size and say so. If it's really several independent projects, name them, propose an order, and grill one at a time.

Offer the opt-out once, in your first message: "Say 'just build it' and I'll go with my defaults." If they take it, state each significant how-it-gets-made choice (platform, language, storage) in one line and stop grilling.

## 3. Walk the design tree

Treat the open decisions as a tree: some only make sense once a parent is settled (data shape before sync strategy). The **frontier** is the undecided nodes whose parents are decided. Work the frontier, one round at a time.

**Intent first, open-ended.** Who it's for, why now, what success looks like, what would make it a failure even if it technically works. Get them describing in their own words; their words carry intent your options can't. Anchor in specifics: "Walk me through the last time this bit you." "If it could only do one of these well, which?" "What would make you wince if I got it wrong?" A guess they can correct ("I'm guessing X keeps breaking on you?") often beats a question.

**Then decisions, each with your recommendation.** One round holds up to three frontier questions that don't depend on each other, numbered, each with your recommended answer and the reason:

```
1. Should drafts sync across devices? Recommend: no for v1. Local-only keeps the schema flat; add sync once someone asks.
2. Who can delete a shared list? Recommend: owner only. Matches how invites already work (src/invites.ts:40).
```

The user can reply "1 yes, 2 your call". "Your call" accepts your recommendation; record it as delegated to you, not as their decision.

**Real forks get a decision brief.** When a node is product-defining and the options trade off real stakes, send it alone using the bootstrap's decision brief. Label it `D<N>`, add a `Stakes if wrong:` line, and score each option `Completeness: N/10` when options differ in coverage rather than kind. For a one-way door, require the explicit option back; "ok" isn't a choice.

Ground to cover. This is territory, not a script: goals, non-goals, anti-goals, constraints, prior art they loved or hated, the current state, the details they care about, which how-it-gets-made choices they want to make and which they're handing to you.

- For broad requirements, check the premise: what happens if we do nothing, and what's the smallest useful outcome?
- For fixed scope, grill only the product calls; state your defaults for the rest in one line each.

Done when: every frontier node is decided by the user, delegated to you, or ruled out of scope.

## 4. Play it back

As soon as you understand one part (what it's for and who it serves, how one piece behaves), play it back, then return to the frontier. Tag each claim `(you said)` or `(my guess)`, and end with "What's wrong or missing?" Match the selected response style: concise for `direct`, more context for `explain`, moderate detail for `balance`.

When the repo keeps `CONTEXT.md` or ADRs, update them as terms and decisions settle. The `domain` skill owns their format.

Done when: the user has corrected or confirmed every `(my guess)` that changes what gets built.

## 5. Hand off

Building starts after the user approves the description: the final playback for chat size, the doc for project size.

- **Chat size**: a final list of decisions, tagged theirs or yours, then build.
- **Project size**: write the design doc and run the builder check. Read `references/design-doc.md` for the template, the builder-check prompt, and how to sort what the builder asks. Read the doc yourself as that builder; use a fresh subagent when the user requests an independent check. Then hand the approved doc to the `plan` skill.

Done when: the user approved the description and the next step (build, or `plan`) has started.

## Red flags

| Thought | Instead |
|---|---|
| "I'll offer a menu to save them effort" | Menus steer. Get them describing first; offer options only when they're stuck. |
| "I'll fill in sensible defaults quietly" | Say each default out loud. A default they never heard is one they couldn't reject. |
| "They said 'sounds good' to the idea" | Approval covers what you showed them. A description you haven't played back isn't approved. |
| "I'll ask whether the API returns X" | That's a fact. Read the code or run it. |
| "Ten questions now, to be thorough" | One round on the frontier. Answers reshape the tree. |
