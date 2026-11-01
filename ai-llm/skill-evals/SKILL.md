---
name: skill-evals
description: Use when creating, editing, reviewing, or deciding whether to keep a Claude Code skill - builds a small eval harness (happy-path + negative trigger cases, regex/LLM asserts, ablation runs) so skill changes are measured instead of vibe-checked.
---

# Skill Evals

## Overview

A skill without evals is a vibe check. Agents are nondeterministic, so when a task
fails you cannot tell whether the skill is bad or the task was hard. Evals separate
those two.

**Core principle: don't ship a skill without evals.** Ten to twenty prompts and a
regex assert file catch most of what goes wrong.

Two things fail, and they fail differently:
- **Triggering** — the model never loads the skill (or loads it when it shouldn't). ~50% of failures.
- **Outcome** — the skill loads but the result is still wrong.

Test both.

## When to Use

- Writing a new skill, before calling it done
- Editing an existing skill (the eval is the regression gate)
- A skill "sometimes works" and you don't know why
- Deciding whether a skill still earns its tokens (ablation → retire)
- Auditing an AI-generated skill — these frequently degrade performance

Skip only for a throwaway one-off skill you will delete this week.

## The Loop

```
1. Classify the skill      capability (temporary) vs preference (durable)
2. Write 10-20 cases       ~5 should-trigger, ~5 should-NOT-trigger, rest outcome
3. Baseline (ablation)     run WITHOUT the skill -> this is the number to beat
4. Run WITH the skill      3-6 trials per case, isolated workspace each run
5. Read the failures       fix the description first, then the body
6. Gate every future edit  a change ships only if it improves or holds the score
```

## Classify First

| Kind | Teaches | Lifespan | Eval focus |
|---|---|---|---|
| **Capability** | Something the model can't do consistently yet (new API, unfamiliar tool) | Temporary — models catch up | Ablation, to detect when to retire |
| **Preference** | Your workflow, style, conventions, domain rules | Durable — models never learn your team | Regression, to protect against drift |

Capability skills get retired. Preference skills get defended. **Keep the eval either
way** — after retiring a skill, the eval keeps watching for regression, and tells you
when to bring the skill back.

## Writing Cases

A case is a user prompt plus what must be true afterward. Write prompts the way a
*user* writes them — vague, no skill name, no jargon from your SKILL.md. If every
test prompt happens to contain your trigger keywords, you have tested nothing.

**Five happy-path.** Realistic asks that should invoke the skill. Pull from real
transcripts where you can — real data beats synthetic.

**Five negative.** Adjacent asks that must NOT invoke it. This is the half everyone
skips, and it's where over-triggering (wasted tokens, confused agent) shows up. If
the skill is for React components, the negatives are Angular, Vue, plain CSS, backend.

**Test outcomes, not paths.** Assert the task got done. Do not assert the skill was
read on turn one — loading on turn five is fine, and not loading at all is fine if
the answer is right. The only path assertion that matters is on negative cases, where
*any* load is a failure.

See `references/eval-format.md` for the case-file schema and assertion types.

## Running

`scripts/run_evals.py` runs a case file against `claude -p` in an isolated config
directory and workspace, with and without the skill installed.

```bash
python scripts/run_evals.py evals.json --skill ~/.claude/skills/my-skill --trials 3
python scripts/run_evals.py evals.json --skill ~/.claude/skills/my-skill --ablation
```

Rules the runner enforces, and why:

- **Isolated runs.** Agents cheat. In your real workspace they'll read prior chats,
  neighboring files, or git history and produce the right answer without the skill.
  Fresh temp config dir + fresh cwd per run.
- **3-6 trials per case.** One green run proves nothing about a nondeterministic system.
  Report pass rate, not pass/fail.
- **Ablation always.** With-skill vs without-skill is the only number that says whether
  the skill does anything.

## Asserts: Regex First

Most skill evals are regex. Coding agents write good regex, they cost nothing, and you
can rerun them hundreds of times.

```
"expect":  ["from google import genai", "gemini-3"]     # must appear
"forbid":  ["google\.generativeai", "gemini-1\.5"]    # must not appear
```

Reach for an LLM judge only when correctness isn't lexical — multi-step traces,
prose quality, "did it follow the workflow". Give the judge a rubric and a
pass/fail verdict, not a 1-10 score.

## Reading Failures

| Symptom | Almost always | Fix |
|---|---|---|
| Never triggers | Description too vague or too abstract | Rewrite description: why + how + when, as a directive |
| Triggers on negatives | Description too broad ("web development") | Narrow to the specific artifact ("React components, Tailwind CSS") |
| Triggers, wrong output | Body is passive or over-specified | Directives over essays; goals and constraints over step-by-step |
| Works with skill, works without | Model caught up | Retire the skill, keep the eval |

The description is the highest-leverage text in the whole skill and the cheapest to
iterate on. Fix it before touching the body.

## Cost Audit

Two costs, two different fixes:

- **Description tokens** are paid on *every* model call, whether or not the skill fires.
  Keep it to a couple of sentences.
- **Body tokens** are paid whenever the skill loads. Keep SKILL.md under ~500 lines and
  push deep material into reference files the model opens only when it needs them
  (`references/aws.md`, `references/gcp.md` — not one file with everything).

**Strip no-ops.** Any instruction that doesn't change agent behavior is money burned:
"write clear code", "make it readable", "follow best practices". The model already does
that. Delete the line, rerun the evals; if the score holds, it was a no-op. AI-generated
skills are full of them.

**And if the workflow is genuinely fixed** — step 1, step 2, step 3, always identical —
it isn't a skill. Write a script and have the skill invoke it.

## Common Mistakes

- **No negative cases.** You'll ship an over-triggering skill and never see it.
- **Prompts written from the SKILL.md.** They leak trigger words; every case passes; nothing was tested.
- **One trial per case.** Noise reads as signal.
- **No baseline.** You can't claim improvement without a number to improve on.
- **Running in your real repo.** The agent finds the answer without the skill and you score a false pass.
- **Asserting the skill loaded on turn one.** Tests the path, not the outcome.
- **Deleting the eval with the skill.** The eval outlives the skill.
- **Testing one harness only.** Behavior differs across Claude Code / Cursor / Codex and across models. If your team is mixed, test mixed.

## Regression Gate

Once evals exist, they are the merge condition: **a skill edit ships only if the eval
score improves, or holds while adding new cases.** That is the whole point — you stop
guessing whether last week's tweak helped.

## Getting Started

Copy `assets/evals.template.json` next to the skill you're testing, fill in the ten
cases, then run the ablation. Start there even if the cases feel thin — ten prompts
beats zero, and you will be surprised what the first five surface.

## Reference

- `assets/evals.template.json` — starting case file, 5 positive + 5 negative
- `references/eval-format.md` — case-file schema, assertion types, LLM-judge rubric template
- `references/description-checklist.md` — how to write and audit a skill description
- `scripts/run_evals.py` — harness (stdlib only, no deps)
