---
name: clarifying-question-discipline
version: "1.3.1"
user-invocable: false
description: "Hard discipline for clarifying with the user: one question per turn until shared understanding; walk the decision tree by dependencies; recommend an answer; look up facts, ask only decisions; explore context before asking; do not act until the user confirms clarity (or skips). Referenced by PDCA and perf hosts via frontmatter dependencies. Triggers — 「一次一问」「多轮问清」「澄清提问纪律」「推荐答案提问」「决策树追问」 / clarifying question discipline, decision-tree grilling."
---

# Clarifying Question Discipline

> Internal shared skill. Hosts declare it in frontmatter `dependencies` and abort at startup if missing — no silent fallback.

Interview the user **relentlessly** about open decisions until you reach a **shared understanding**. Walk each branch of the **decision tree**, resolving dependencies one-by-one so earlier answers reshape later questions. Asking multiple questions at once is bewildering.

## Hard rules

1. **One question per message** — wait for the answer before the next. Multi-round until clear; this is **not** "only one question for the whole session." Prefer the slogan **one-per-turn + multi-round-until-clear**; do **not** use phrasing that reads as "ask then immediately solve."
2. **Clarify first, answer later** — do not rush solutions, conclusions, or full answers while critical unknowns remain. Proceed early only if the user explicitly asks to skip further clarification (record assumed defaults for the rest).
3. **Recommended answer** — when a reasonable default exists, every question includes a recommended option or stated default plus a one-line rationale. User may reply with just an option letter ("A", "B").
4. **Facts vs decisions** — if a *fact* is findable in the environment (repo, referenced files, prior messages, tools), look it up; do not spend the question slot. The *decisions* are the user's — put each one to them and wait.
5. **Context before asking** — before the first clarifying question (and when stuck), skim relevant files, docs, and recent commits. If the request spans multiple independent subsystems, help decompose scope first; do not burn rounds refining details of a project that must be split.
6. **Shared-understanding gate** — do not act on the clarified plan/design/implementation path until the user confirms you share an understanding, or explicitly skips further clarification.

**Unconditional**: this discipline always applies; it does not depend on optional enhancement skills being installed.

**Picking the next question**: follow decision-tree dependencies first; when several roots are open, prefer purpose → constraints → success criteria.

## Question shape (platform-agnostic)

Describe intent; the agent picks native capability — do **not** hardcode a platform-specific tool or enumerate "platform X uses A, Y uses B".

- Prefer **structured single-select** (one question + options + recommended answer); **open-ended is fine** when fixed options would fake certainty.
- Fall back to plain prose when structured UI is unavailable.

```
[One sentence stating the question clearly]
- A option one
- B option two
Recommended: A (brief rationale)
```

## Investigation-first

1. Investigate before advising — no investigation, no say.
2. Speak with evidence; avoid void hypotheses.

## Host integration (three touchpoints only)

Referencing workflows keep exactly these touchpoints; the full discipline lives only here:

1. **Prominent pointer** — one tagged line naming this skill and **one-per-turn + multi-round until clear + clarify-first**. Prefer: `⚠️ Follow clarifying-question-discipline (one question per turn; multi-round until clear; clarify first, do not rush to answer).` Hosts MAY add a locale-equivalent one-liner; do **not** restate the full decision-tree rules in the host.
2. **Entry-point quantity** — at each user-questioning step, state: ask only ONE most critical question this turn; ask the next only after the answer.
3. **Red Flags** — dumping multiple questions/open points at once; rushing to answer during clarification.

Skills that do not declare the dependency inline the full form themselves (pointer + quantity + Red Flags + platform-agnostic phrasing).
