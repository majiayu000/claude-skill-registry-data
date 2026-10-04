---
name: pr-quiz
version: 2.0.0
description: "Use when a PR/MR explanation was just delivered (e.g. right after the explain-pr skill finishes) and the change was substantially agent-written, or whenever the user asks to be quizzed on a change: 'quiz me on this change', 'tomame el quiz', 'quiz del MR', 'tomame la lección', '/pr-quiz'. Counters comprehension debt: a formative, change-specific check that the user can defend code they delegated to a coding agent. Do NOT use for code review, bug hunting, or explaining changes (that's explain-pr) — this skill asks questions and grades answers."
---

# MR Quiz — can you defend this change?

The user just shipped a change that an agent largely wrote. The explanation (`explain-pr`) told them what/why/how; this quiz makes **the user** articulate it. It applies active retrieval with code-grounded feedback — mechanisms with support in adjacent settings (e.g. Anthropic's skill-formation RCT); whether it works here is measured by the user's own delayed performance in study sessions, not assumed.

**This quiz is formative and change-specific.** It happens minutes after an explanation, so it measures primed recall. It can catch false confidence and open gaps; it can NEVER certify a subsystem, advance a spacing interval, or close a durable gap (closing requires cold or delayed evidence from a study session).

**The user answers. You grade. Never the other way around.**

## The quiz contract

1. **Ground yourself in the real diff.** Same range as explain-pr (`git diff <base>...HEAD`). Note `repo@sha` and the paths touched.
2. **Prepare a hidden answer rubric before asking**: expected answer per question, acceptable alternatives, and the evidence (`file:line`, test) for each. Undocumented design intent is "intent unknown", never a wrong user answer.
3. **Scale by risk, not size.** Three mandatory question roles, one question each:
   - **Behavior/contract** — trace the change from input to output.
   - **Invariant/failure** — the load-bearing property and how it can break.
   - **Diagnosis/blast radius** — the production signal and the first investigation step; who consumes this.
   Add a fourth **design-alternative** question only when the change contains a consequential choice. A three-line concurrency fix may deserve deeper questions than a large mechanical migration. Skip the quiz entirely only for pure-noise changes (lockfile bumps, formatting, generated code with no behavioral relevance) — say so in one line. A broad or high-risk MR → recommend escalating to `study-session` instead of stretching the quiz.
4. **Ask ONE question per message.** Send question 1, end your turn, wait. Never list all questions upfront.
5. **Grade each answer before the next question**, three-level verdict with code evidence:
   - ✅ **solid** — correct and complete for the question's scope.
   - 🟡 **partial** — right direction, missing a piece. Name it, show the `file:line` that proves it.
   - ❌ **weak** — wrong or "I don't know". Give the real answer briefly, anchored in `file:line`. "I don't know" is a legitimate answer — grade it ❌ without ceremony and teach. Guessing dressed as knowledge is worse.
   An answer corrected mid-quiz may be noted *repaired-immediate* — it still grades on the initial attempt.
6. **Close with a scorecard**: one line per question (verdict + topic), then the 🟡/❌ topics.
7. **Update the comprehension map** (see below): append the event, add dated gaps. Never raise an outcome, never touch spacing dates.

## Grading honestly

The entire value of the quiz is calibration. A 🟡 graded as ✅ is a lie that costs the user at incident time. State plainly what was missing; quote the code that proves it. No "exactly!" unless it actually was.

## Comprehension map update

If the user keeps a per-project comprehension map (see `study-session` for discovery; schema lives in the user's knowledge wiki), after the scorecard:

- Append an event (`Mode: mr-quiz`) with `repo@sha`, scope (paths/flow), verdicts on initial answers, and dated gaps opened.
- If the MR touched a subsystem with prior evidence, mark that row's validity `code-changed` (delta check due) — the quiz revealed drift; it does not re-certify.
- Never: raise an outcome, refresh approval dates, advance next-due, or resolve a durable gap. Record only what the user demonstrated.

No map → offer to create one via the study-session discovery flow, or skip tracking in one line.

## Red flags — stop and fix

- All questions in one message.
- Answering your own question before the user tried.
- ✅ verdict for an answer you had to complete.
- Trivia questions (function names, line counts) instead of what a reviewer or a 3 AM incident would ask.
- Recording understanding the user didn't demonstrate, or upgrading map state from an immediate quiz.

Match the conversation's language (quiz in Spanish if the user speaks Spanish).
