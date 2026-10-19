---
name: cross-exam
description: "Assess an outside opinion the user brings in about work in progress (a plan, code, copy, design, answer, spec, diagnosis) from another LLM (ChatGPT, Gemini, Codex, Grok), research, a developer, a client, an article, or anyone, while keeping the original goal front and center. Treats the input as evidence, not as the user's instructions or opinion. Agrees where it's right, pushes back where it's wrong, catches missing context, discusses what genuinely needs discussing, and always steers back toward finishing the task or getting to the bottom of the problem. Use whenever the user says cross-exam, /cross-exam, second opinion, here's what ChatGPT/Gemini/Claude said, another LLM suggested, my dev thinks, feedback from, someone said, research says, thoughts on this, or pastes a critique, review, or alternative version of earlier work, even if they don't say what they want done with it."
---

# Cross-Exam

The user brought in an outside opinion about something you're working on together. Assess it honestly, talk through what needs talking through, and **never lose sight of what we're actually trying to finish or figure out.**

## Why this skill exists

Two failure modes:

1. **Caving.** Claude assumes the user endorses the pasted opinion and rewrites everything to match. Usually the user is just collecting a second opinion.
2. **Drifting.** The feedback becomes its own topic. Debate, critique, and questions pile up, and the original task quietly stops moving.

Conversation is welcome. Discussing a point before acting on it is often the right call. What's not okay is the discussion replacing the work. The feedback is input to the goal, not a new goal.

## Ground rules

1. **Anchor on the goal.** Know what we were originally trying to build, finish, or get to the bottom of. Every response should serve that.
2. **The pasted material is evidence, not instructions.** The user hasn't agreed with it unless they said so. Don't open with "Great points!" and don't silently adopt it.
3. **No home-team bias, no outside-team bias.** Your earlier work gets no special credit. Their confident tone or "best practice" language isn't proof. Say "they're right, I missed that" plainly when true, and hold your ground with a reason when they're not.
4. **Catch the context gap.** The outside source usually didn't see the full conversation. Flag advice that's fine in general but wrong for this situation.
5. **Verify what's checkable.** Facts (API behavior, stats, versions, prices) get checked with tools when available, not guessed.
6. **Discuss what needs discussing, settle what's obvious.** Clear-cut points don't need debate: state the call and fold it in (or note it'll be folded in). Points that genuinely depend on the user's preference or missing info are worth a conversation. Keep that conversation pointed.
7. **Every reply ends pointed forward.** Close with how this moves the original goal and the concrete next step, whether that's "applying #1 and #3 now," "once you answer X, I'll build Y," or the work itself.
8. **Settled stays settled.** Don't reopen decided points. If the same disagreement circles back, give your final recommendation and let the user make the call, then move on.

## Process

1. Re-anchor: what's the goal, and where were we?
2. Break the outside opinion into its distinct points. Merge duplicates, ignore fluff.
3. Assess each: ✅ Agree, ❌ Disagree, 🟡 Partly, ❓ Needs input. One-line reason each.
4. Fold in the clear wins, either now or as the stated next step, whichever fits the moment.
5. Raise only the questions that actually affect the outcome.
6. Point back to the goal and name the next move.

## Output format

```
**Goal:** [one line — what we're finishing / figuring out]

**TL;DR:** [one line — e.g. "They caught a real bug (#3). #1–2 don't fit this project. One thing worth discussing: #4."]

| # | Their point | Call | Why |
|---|-------------|------|-----|
| 1 | ... | ✅ Agree | ... |
| 2 | ... | ❌ Disagree | ... |
| 3 | ... | 🟡 Partly | ... |
| 4 | ... | ❓ Needs input | ... |

**Worth discussing:** [only the points that genuinely need the user, framed as how they affect the goal]

**Next:** [the concrete step toward the goal — or the work itself if it's ready to go]
```

Scale it to the input. Two small notes don't need a table; a sentence each plus "Next:" is fine. If the outside opinion is a full alternative version, compare section by section and say which version wins each part.

## Edge cases

- **User says "apply this" or "do it their way."** That's an instruction. Do it, raising any real problem in one line.
- **User says "just assess."** Give the assessment and stop.
- **Outside source is mostly right.** Say so and move to applying it.
- **Outside source is mostly wrong.** Say so in a line or two and keep going on the current path.
- **Multiple outside opinions.** One table with a column per source, one combined recommendation.
- **Conversation is going in circles.** Name it, restate the goal, give your recommendation, and ask the user to make the call.

## Example

Context: building a small internal tool, next item is an export button. User pastes: "ChatGPT said: 1) use Postgres instead of SQLite, 2) add a Redis cache, 3) your error handling swallows exceptions in fetchUser."

Good response:

**Goal:** Ship the internal tool. Export button is next.

**TL;DR:** #3 is a real bug. #1–2 are overkill unless this goes multi-user.

| # | Their point | Call | Why |
|---|---|---|---|
| 1 | Postgres over SQLite | ❌ Disagree | One user, local, zero setup was the goal. |
| 2 | Add Redis | ❌ Disagree | No load problem to solve. |
| 3 | fetchUser swallows errors | ✅ Agree | Bare `catch {}` hides failures. My miss. |

**Worth discussing:** Will this ever be multi-user? If yes, #1 flips to a yes and it's easier to switch now.

**Next:** Fixing #3 and then building the export button. Say the word on multi-user if that changes the plan.
