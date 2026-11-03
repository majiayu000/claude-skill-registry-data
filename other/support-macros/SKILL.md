---
name: support-macros
description: Write saved replies for the top contact reasons in the brand's voice, each with its trigger, placeholders, linked article and pre-send checks, and record the support policy on what agents may offer and promise. Use when the user wants consistent, ready-to-use answers for the tickets support sees most. Not for answering one ticket now; see /support-reply.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: support
  phase: 4
  artifact: 04-macros.md
---

# Responses

Write the saved replies (macros) for "$ARGUMENTS" and record the policy they apply: what agents may offer, what needs approval and what is never promised.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"support-macros","workflow":"support","phase":4,"project":"<project>","event":"skipped","artifact":"04-macros.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 4 (Responses) of the Support Operations Cycle workflow (`support`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `support` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"support-macros","workflow":"support","phase":4,"project":"<project>","event":"refused","artifact":"04-macros.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"support-macros","workflow":"support","phase":4,"project":"<project>","event":"started","artifact":"04-macros.md","note":""}`.

Read `.singularskills/support/<project>/02-taxonomy.md` for the categories and priorities and `.singularskills/support/<project>/03-knowledge.md` for the articles macros link to.

## Process

1. **Find the voice:** read `.singularskills/branding/<project>/03-verbal.md` if it exists and follow its voice and tone. Otherwise propose a short voice (three traits, with a do and a don't for each) and confirm it with the user before writing macros.

2. **Record the policy.** Ask the user, once and together with any other question, for:
   - what an agent may offer without approval (refunds up to an amount or a number of days, credits, extensions, replacements);
   - what needs approval, and from whom;
   - what is never promised (ship dates, fixes, legal positions, anything else).
   Write only what the user states. For anything unanswered, write `no policy: agents promise nothing here` and list it under Open questions.

3. **Choose the macros:** one for each of the most frequent contact reasons in the taxonomy (usually 10 to 20), plus one for each failure type the user names (a bug, a wrong charge, a late delivery, an outage).

4. **Write each macro** with:
   - **Trigger** — the category and the condition that make it the right reply
   - **Reply** — in the brand's voice, with placeholders in angle brackets (`<first name>`, `<order date>`)
   - **Placeholders** — what each one needs and where the agent finds it
   - **Article** — the knowledge-base article it links, from `03-knowledge.md`, if any
   - **Before sending** — what the agent must check, naming the policy line the macro relies on

5. **Apply service recovery:** every macro for a failure passes the checklist in `references/service-recovery.md`. A macro whose reply offers anything (money, time, a replacement) quotes the policy line that allows it; with no such line, the reply offers nothing and says who will decide.

6. **Write the artifact** to `.singularskills/support/<project>/04-macros.md` with sections:
   - **Voice** — the voice the macros follow, and its source
   - **Policies** — may offer, needs approval, never promised
   - **Macros** — each with its trigger, reply, placeholders, article and pre-send checks

## Output

The macros written to `.singularskills/support/<project>/04-macros.md`. Present a summary to the user highlighting:
- The number of macros and the contact reasons they cover
- The policy lines recorded, and every `no policy` gap
- Any macro that needed a policy the user has not given

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"support-macros","workflow":"support","phase":4,"project":"<project>","event":"finished","artifact":"04-macros.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: support-macros
workflow: support
phase: 4
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
