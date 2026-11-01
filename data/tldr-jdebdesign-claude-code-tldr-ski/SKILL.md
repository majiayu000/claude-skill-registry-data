---
name: tldr
description: Boil a Claude Code plan down to a short, beginner-friendly bullet list. Use when the user types /tldr, or asks for a TL;DR, summary, or plain-English version of a plan Claude just made (in plan mode or otherwise). Anything typed after /tldr is treated as a hint for how to write it.
argument-hint: "[optional hint: anything to keep in mind, e.g. 'focus on risks', 'explain like I am new to React', or a path to a plan file]"
---

# /tldr

Turn a plan into a short bullet version that a beginner developer can read in under a minute.

## The user's hint

Whatever the user typed after `/tldr` is a hint for this run:

> $ARGUMENTS

If the hint above is empty, ignore this section and use the defaults.

Treat the hint as guidance on how to write the TL;DR, not as part of the plan. Examples of what it might ask for:

- A focus: "just the risks", "only the steps", "files that change".
- An audience or tone: "explain it like I'm new to React", "for a non-technical manager".
- A specific concern: "will this touch the database?", "anything that could break login?". Make sure the TL;DR answers it using only what the plan says. If the plan does not say, state that plainly.
- Length or language: "3 bullets total", "in Spanish".
- A path to a plan file: use that file as the plan (see step 1).

Apply the hint by changing emphasis, depth, wording, and which sections you include. A hint never overrides the Rules below: stay read-only, stay faithful to the plan, and never use em dashes. If a hint asks for something the rules forbid (for example "add a step for tests"), do the rest of the TL;DR and say in one line why you left that part out.

## 1. Find the plan

Use the first of these that applies:

1. A path to an existing file in the hint: read that file.
2. The most recent plan in this conversation (a plan-mode proposal, a "Plan:" section, or a numbered implementation outline).
3. The newest file in `~/.claude/plans/` (check with `ls -t ~/.claude/plans | head -1`), but only if the conversation has no plan. Say which file you used.

If none exist, say so in one line and stop. Do not invent a plan.

## 2. Write the TL;DR

Unless the hint says otherwise, output exactly this structure, nothing before or after it except an optional one-line question at the end (see rules):

**Goal**
- One bullet: what we are trying to achieve, in plain words.

**What will change**
- 3 to 6 bullets. Each names a thing that will be added, edited, or removed, and why in a few words.

**Steps, in order**
1. Short imperative step.
2. Keep it to 3 to 7 steps. Merge small steps; drop obvious ones.

**Watch out for**
- 1 to 3 bullets: risks, things that could break, or decisions still open. Omit this section if there are none.

## Rules

- Concise: each bullet is one line, ideally under 15 words. The whole thing should fit on one screen.
- Beginner-friendly: no unexplained jargon. When a technical term is unavoidable, add a few words in parentheses, e.g. "migration (a script that updates the database shape)".
- Name real files, functions, and commands from the plan, but wrap them in backticks and say what they do.
- Faithful: only summarize what the plan says. Do not add steps, change scope, or editorialize. If the plan is ambiguous, say so under "Watch out for".
- Never use em dashes. Use commas, colons, or parentheses instead.
- Read-only: do not edit files, run the plan, or exit plan mode. This skill only explains.
- If the hint asks for a single focus (e.g. "risks only", "just the steps"), return only that section.
- If the plan has an open question the user must answer before work can start, end with one line: "Question: ..."
