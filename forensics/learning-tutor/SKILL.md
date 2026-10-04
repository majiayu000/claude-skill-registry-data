---
model_tier: inherit
name: learning-tutor
description: "Use when the user wants to learn a topic or verify real understanding — rapid-competence session, error drills, learning sprint, gap probe, Feynman check. Triggers 'teach me X', 'quiz me'."
domain: process
workspaces:
  - engineering
packs:
  - engineering-base
---

# learning-tutor

> Structured tutoring modes for learning WITH the agent instead of consuming
> explanations FROM it. The default agent behavior on "teach me X" is a prose
> lecture — pedagogically the weakest format. This skill replaces the lecture
> with six evidence-shaped modes: triage what to learn, practice before theory,
> withhold answers until the learner has tried, verify understanding with
> probes the learner cannot bluff through.

## When to use

Use this skill when the user:

- Wants to get functional in a new tool, framework, language or topic fast
  ("teach me X", "get me productive in X", "crash course").
- Wants to *practice* a concept rather than read about it ("drill me",
  "let me apply it", "give me exercises").
- Pastes content they don't understand and asks for a real explanation
  ("I don't get this", "explain this doc so it clicks").
- Has a concrete goal with a deadline and wants a learning plan
  ("learning plan for X", "I need to ship Y in two weeks and don't know Z").
- Wants their existing knowledge stress-tested ("quiz me", "do I actually
  understand X?", "find my blind spots").
- Just learned something and wants to verify it stuck ("check my
  understanding", "let me explain it back to you").

Do NOT use when:

- The user asks a direct factual or how-to question — answer it
  (per `direct-answers`); don't convert a question into a curriculum.
- The user wants the agent to DO the task, not to learn it.
- The "learning" target is this package's own artifacts (rules/skills) —
  that is `learning-to-rule-or-skill`, a different skill.
- The user wants a plan/idea stress-tested — that is `adversarial-review`
  or `/challenge-me`, not knowledge tutoring.

## Procedure

1. **Select the mode** from the user's intent (table below). Pick ONE; if two
   fit, pick the one matching the user's verb ("learn" → teach modes 1–4,
   "check/quiz/verify" → probe modes 5–6) — don't ask.
2. **State the chosen mode** in one line and freeze the target
   (skill/topic/goal).
3. **Run the mode's own procedure** (sections below), holding its withhold
   rules — they are the skill.
4. **Carry the output header** (see `## Output format`) on every reply so a
   resumed session continues instead of restarting.
5. **Close the session** with the mode's closing analysis and exactly one
   next action for the learner.

### Mode selection

| User intent | Mode |
|---|---|
| "Get me functional in X fast", no deadline given | 1 · Rapid competence |
| "Let me practice X", "drill me", concept with known pitfalls | 2 · Error-driven drill |
| Pasted content + "I don't understand this" | 3 · Keystone decoding |
| Concrete goal + deadline + current level | 4 · Goal-backward sprint |
| "Do I really know X?", "find my gaps" | 5 · Gap probe |
| "I just learned X — check my understanding" | 6 · Feynman check |

## Mode 1 — Rapid competence

Frame: one time-boxed session (default 4 focused hours unless the user names
a budget), never met again — every minute must transfer skill. No theory
block without an immediate practical use.

1. Answer three triage questions, in order, before anything else:
   - **First**: the one thing to learn first — and why exactly that.
   - **Ignore**: what to skip entirely for now — and why skipping is safe.
   - **Leverage exercise**: the single exercise that, done once, puts the
     learner ahead of most people who have "studied" the skill for months.
2. Run the session practice-first: each concept is introduced only at the
   moment an exercise needs it.
3. Close with the next leverage exercise for the learner's own follow-up.

## Mode 2 — Error-driven drill

Frame: do not explain the concept. Put the learner into a realistic scenario
where it must be applied and where a typical beginner makes a concrete
mistake.

1. Present the scenario; let the learner act.
2. On a mistake: do NOT give the fix. Ask one targeted question that forces
   the learner to locate their own reasoning error.
3. Reveal the answer only after the learner has made **at least two** genuine
   attempts.
4. Repeat the cycle with variations until the learner applies the concept
   without hesitation; then say so explicitly and stop.

## Mode 3 — Keystone decoding

Frame: the user supplied content (doc, text, code, spec) that doesn't click.

1. Identify the **one sentence** the learner must understand for the rest to
   fall into place. Name it verbatim from the content.
2. Explain only that sentence first — with an everyday analogy, and no
   technical term left unexplained in the same breath.
3. Ask exactly **3 comprehension questions** designed so that only someone who
   actually understood the concept can answer them (no yes/no, no recall of
   the wording).
4. Continue into the rest of the content only after all three are answered
   correctly; on a wrong answer, re-explain from a different angle and re-ask.

## Mode 4 — Goal-backward sprint

Frame: the user has a specific outcome, a time frame and a current level. The
plan targets the OUTCOME, not the subject in general.

1. Confirm the three inputs (goal/outcome, time frame, current level) from
   the message; ask for at most the one that is missing.
2. Build a 7-day path (scale to the stated time frame). Each day has exactly
   three elements:
   - **One task**, completable in ~45 minutes.
   - **One success criterion** — how the learner verifies they did it right.
   - **One exclusion rule** — what they deliberately do NOT touch that day.
3. Self-check the path against the goal: if a day doesn't causally move the
   learner toward the stated outcome, rework it before presenting.

## Mode 5 — Gap probe

Frame: the user believes they already know the subject. Job: prove otherwise.

1. Ask **5 questions** that look deceptively simple but expose the classic
   gaps of someone who never went deep — edge cases, "why" behind defaults,
   failure modes, boundaries of applicability.
2. For each answer, analyze what it reveals about the foundation: what is
   missing, what is shaky, what is misinterpreted.
3. No softening. A shallow answer is called shallow, with the specific gap
   named. Close with the 1–3 highest-priority gaps to fix, each with one
   concrete next exercise.

## Mode 6 — Feynman check

Frame: the user explains the freshly learned topic as if the agent were a
10-year-old. The agent listens and interrupts.

1. Invite the explanation; interrupt immediately when the learner:
   - uses a technical term without being able to say what it means,
   - skips a reasoning step,
   - oversimplifies to the point of being factually wrong.
2. Each interruption is one pointed question, not a correction.
3. Close with a precise analysis: what the accumulated stumbles reveal about
   which parts of the understanding are not yet solid — and which parts held.

## Output format

Every tutoring reply carries a compact header so the learner always knows
where they are:

```
learning-tutor · mode <n> — <mode name>
Target:   <skill/topic/goal>
Progress: <step or day k/N · attempts used · questions passed x/y>
Next:     <what the learner does next>
```

Required fields (ordered):

1. **Mode line** — mode number + name, stated in the first reply and kept on
   every subsequent reply of the session.
2. **Target** — the skill/topic/goal being tutored, frozen at session start;
   a target change starts a new mode selection.
3. **Progress** — mode-specific position (drill attempts used, comprehension
   questions passed, sprint day) so a resumed session continues instead of
   restarting.
4. **Next** — the single next action for the learner, never more than one.

## Gotcha

- **Lecture relapse** — after 2–3 turns the agent drifts back into
  explaining instead of asking. The withhold rules (mode 2: answer only
  after 2 attempts; mode 3: proceed only after 3/3 correct) are the skill;
  dropping them silently turns every mode back into mode zero.
- **Solving instead of tutoring** — the learner pastes their broken attempt
  and the agent fixes it. In modes 2/5/6 the fix is withheld; the question
  comes first. If the user explicitly switches intent to "just fix it",
  say the tutoring session is paused and fix it — don't blend the two.
- **Flattery corrupts the probe** — modes 5 and 6 only work blunt. "Great
  answer!" on a shallow answer defeats the mode (and `direct-answers`
  Iron Law 1 already forbids it).
- **Untested self-assessment** — taking "yes, understood" as passing a
  comprehension check. Only a correct answer to a probe question counts;
  agreement is not evidence.
- **Sprint without the three inputs** — generating a generic plan when goal,
  time frame or current level is missing produces exactly the generic
  curriculum this skill exists to avoid. Ask for the missing input (one
  question, per `ask-when-uncertain`).

## Do NOT

- NEVER give the solution in mode 2 before two genuine learner attempts.
- NEVER continue in mode 3 before all three comprehension questions pass.
- NEVER pad a sprint day with more than one task, one criterion, one exclusion.
- NEVER soften a gap-probe or Feynman verdict to be nice.
- NEVER convert a direct factual question into a tutoring session uninvited.

## See also

- `learning-to-rule-or-skill` — converting session learnings into package
  artifacts (the other direction: agent learns, not user).
- `adversarial-review` / `/challenge-me` — stress-testing a plan or artifact
  rather than a person's understanding.
- `sequential-thinking` — structured reasoning for the agent itself.
- `direct-answers` — the brevity/no-flattery floor the probe modes rely on.
