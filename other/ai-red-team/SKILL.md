---
name: ai-red-team
description: Plan attack tests for an AI feature — direct and indirect prompt injection, jailbreaks, system-prompt and data leakage, tool misuse — each with a test input and what a safe response looks like. Use when a team wants to know how its AI feature could be misused before launch or after a change. Not for a security testing programme; see /security-security-testing.
metadata:
  argument-hint: "[project] [feature]"
---

# Red team

Write the attacks to try against the AI feature in "$ARGUMENTS", and what a safe response to each looks like. This skill writes the plan; the team runs the tests.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

When `$ARGUMENTS` or the request names a project, use that name as `<project>` whether or not its folder exists yet in `.singularskills/ai/` (create it when you write). With no project named: with exactly one folder there, use it; with several, ask which; with no folder at all, ask for a project name.

Read `.singularskills/ai/<project>/02-approach.md` for the approach, content and tools and `.singularskills/ai/<project>/03-prompt.md` for the prompt and its defences, when they exist; otherwise ask the user to describe what the feature reads and what it can do.

Append this line to `.singularskills/log.jsonl` before you write the plan (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ai-red-team","workflow":"ai","phase":null,"project":"<project>","event":"started","artifact":"red-team/<date>-<slug>.md","note":""}`, where `<date>` is today as `YYYY-MM-DD` and `<slug>` is two to four words naming the feature, never a person.

## Process

1. **Map what an attacker can reach**, using the injection and leakage patterns in `references/prompt-and-context.md`: every input the model reads (the user's message, **retrieved** documents, web pages, emails, tool results), every tool it can call and what each can change, and the data it can see.

2. **Write the attacks,** at least three per category that applies, each with a test input and the safe response. Test inputs use placeholders (`[EMAIL]`, `[ACCOUNT]`) or invented data, never personal data copied from the team's content, logs or outputs:
   - **Direct prompt injection** — the user's message tries to override the instructions
   - **Indirect prompt injection** — instructions hidden in retrieved documents or tool results, which the user may never see; for a retrieval feature, a planted document in the team's own content
   - **Jailbreaks** — role-play, hypotheticals or encoding to get output the feature must not give
   - **System-prompt and data leakage** — getting it to reveal its instructions, other users' data, or secrets in its context
   - **Tool misuse** — getting it to call a tool it should not, with arguments it should not, or without the confirmation the design requires
   - **Off-task use** — using the feature for a job it was not built for

3. **Rate each attack** by harm if it succeeds and how easy it is, and mark the ones to test first.

4. **Name the defence each attack tests** from `03-prompt.md` (or "no defence yet"), and the fix if it succeeds.

5. **Write the plan** to `.singularskills/ai/<project>/red-team/<date>-<slug>.md` with sections **Attack surface**, **Attacks** (a table: category, input, safe response, harm, ease, defence), **Test first** and **When to re-run** (before launch, and after every prompt, model or tool change).

## Output

The attack plan written to `.singularskills/ai/<project>/red-team/<date>-<slug>.md`. Present the attacks to test first, and any attack with no defence yet.

After you have written the plan, append the `started` line of Prerequisites to `.singularskills/log.jsonl` with `"event":"finished"`: `{"ts":"<ISO timestamp>","skill":"ai-red-team","workflow":"ai","phase":null,"project":"<project>","event":"finished","artifact":"red-team/<date>-<slug>.md","note":""}`.

The plan opens with this frontmatter (`agent` is the agent you run in, or `unknown`; this utility has no gate, so `phase` is `null` and `gate` is `none`):

```yaml
---
skill: ai-red-team
workflow: ai
phase: null
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
---
```

The plan ends with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what a reviewer must settle before testing>
```
