---
name: brainstorm
description: Find an approach for a goal that has none yet; stops once you pick one.
disable-model-invocation: true
argument-hint: "[goal]"
---

The arguments name the goal to find an approach for; none means what the conversation is about. This skill finds the approach and starts nothing else: no detailed design, no code.

1. **Facts first.** Read what the goal touches: the code, config and docs, and how similar things are already done here. Never ask the user what you can look up.
2. **Clarify.** Ask only what would change which approaches are on the table: the goal behind the ask, hard constraints, what's already ruled out. Aim for one or two rounds, more only when the answers leave the options unclear, and none when the context already answers them. Ask about the goal and motive openly, without a recommendation, so your guess doesn't steer the answer. Phrase the other questions as your recommendation so "yes" accepts it, with a `> **Recommended:**` blockquote under each; number every question (`**1. <question>**`) and give a fork's alternatives as `- **A.** <option>` lines. Use the harness's question tool (pi `ask_user_question`, Claude `AskUserQuestion`) only when every question in the round is a short pick (at most four, 2–4 options each, recommended first and labelled "(Recommended)"); otherwise the whole round is markdown.
3. **Propose approaches.** Two or three that differ in structure or trade-off, not variations of one idea, each checked against the code it would touch. Include a smaller-scope or don't-build-it option when it's real. If only one approach is reasonable, say so and present it alone in markdown rather than padding with straw men.

   Present several through the question tool: one option per approach, its name as the label, its main trade-off as the description, and a preview of at most about 12 lines with the sketch, pros and cons, plus a snippet or layout where it helps. Put the recommended approach first, labelled "(Recommended)"; the tool's free-text row is how the user combines or rejects them. Without a question tool, write a markdown section per approach followed by your recommendation.

4. **Stop.** Restate the chosen approach in a few lines, then one line naming the next steps: `/grill-me`, `/annotate-plan`, `/handoff`, or just build it.
