---
name: vibecoding-resume-story
description: Turn a project built by vibecoding (user directs, AI tool writes the code) into a resume entry and interview story that is impressive yet impossible to expose as inflated. Use when writing resume bullets, portfolio descriptions, or interview talking points for AI-assisted projects where the user did not personally write the code. Not for projects the user actually wrote the code for, and never for inventing technical depth.
version: 1.0.1
---

# Vibecoding Resume Story

Vibecoding means the division of labor is: the user supplies requirements, prompts, rules, and acceptance decisions; the AI tool writes the code. A resume entry that implies "I wrote the code" collapses under two follow-up questions. One that presents "I designed and verified everything, the tool implemented it" is both honest and a stronger signal for AI-era roles.

## Non-negotiable Rules

1. **Every claim must reduce to a requirement the user actually issued.** Write each bullet as something the user said or decided, never as implementation work. "Defined the rule: at most 5 tasks per day, each with priority and estimated minutes" is defensible; "implemented a validation engine" is not.
2. **State the division of labor openly.** Name the tool (e.g. WorkBuddy) and the word vibecoding. Hiding it looks guilty; stating it reads as AI-toolchain fluency, which is the actual job skill.
3. **No implementation jargon the user cannot explain in plain words.** If the user cannot answer "what does L1/L2/LLM-as-Judge mean" in one sentence, the term does not go on the resume. Translate everything into requirement language.
4. **Metrics only from real runs, at real granularity.** One live test scoring 8/10 is written as "one end-to-end live run, scored 8/10" — never "stable 8-9 points". Inflated metrics are the first thing that gets probed.
5. **Pain point comes from the user's own experience.** "I hit this problem myself while doing X" beats "the whole industry has this problem" — it is unverifiable in the good way and shows user empathy.
6. **Acceptance is the user's job title.** The repeated verbs are: defined, required, directed, verified on a real device, rejected, iterated. Never: coded, implemented, developed the algorithm.

## Entry Structure (4-5 bullets, each at most 2 lines)

1. **Background & goal**: the user's own pain point in one line; division of labor in one line; shipped state (open-sourced, deployed, usable without a key).
2. **Rules & constraints**: the hard requirements issued as prompts, in plain numbers (counts, ranges, budgets).
3. **Evaluation & verification**: how output quality is checked (rule pass then model score, threshold, bounded retry, audit log); the deliberately-bad test path used to prove the check works; the live-run evidence with its real single-run score.
4. **Iterations & delivery**: the timeline as rounds of "requirement → verify → next requirement" (e.g. MVP overnight → live API → mobile polish → desktop → open-source launch), with the acceptance rule "rejected until it passed on a real device".
5. **Optional — reduced decision cost**: templates, one-tap adopt, one-tap export; the user's original "reduce decision cost" framing.

## Interview Prep Table (always deliver with the resume text)

For every bullet, provide the plain-language sentence the user can say out loud. Example mapping:

| Resume says | User says in interview |
|---|---|
| "daily tasks capped at 3-5, each with priority and estimated minutes, total within the day's budget" | "I told it: max five things a day, each needs a priority and rough minutes, and the total can't exceed the time I actually have" |
| "score below 7 retries, at most twice" | "first the hard rules block it, then the model grades it; under 7 it regenerates, twice at most, otherwise it keeps the best attempt" |
| "deliberately-bad sample path to verify interception" | "I made it generate a bad plan on purpose the first time, to watch the gate actually catch it — that's how I trusted the mechanism" |

## Red Flags To Scan For Before Sending

- Mixed-language accidents ("runtime 长问题") or terms the user did not write themselves.
- Contradictions between bullets (e.g. "independently completed" next to "AI-assisted").
- The same fact told twice in different bullets (assign each fact one home: mechanism in the rules bullet, evidence in the verification bullet, timeline in the iteration bullet).
- Any number that cannot be produced on demand (scores, counts, timings).
- Bolder claims in the resume than in the project's public README — interviewers do compare.

## Example

Bad, because it claims implementation work:

> 实现了电商脚本生成引擎，包含合规校验模块。

Good, because every clause reduces to something the user actually decided:

> 定义电商短视频脚本规则：单条不超过 60 秒，卖点不超过 3 个，合规词先过再写；
> 用 AI 工具实现后，我逐条验收输出并沉淀 27 类违禁表述词库，过审率从 70% 提到 80%。
