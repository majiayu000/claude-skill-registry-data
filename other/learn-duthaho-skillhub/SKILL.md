---
name: learn
description: >-
  Personalized tutor with memory across sessions — "teach me X, at my
  pace." Builds a syllabus with a pass rubric per unit, teaches one unit
  per session: a recall quiz on what's due (date-based spaced repetition),
  examples matched to your background, and an active-recall check graded
  against the rubric with confidence tags. Progress and weak spots persist
  in out/learn/<topic>.md, so sessions resume and re-drill what was missed;
  fact-sensitive content is verified by web search, not memory. Keyless.
  Use to learn or study a topic — e.g. "/learn rust ownership", "teach me
  kubernetes", "quiz me on X", "continue the SQL lessons"; "/learn" alone
  lists topics in progress. For community buzz use pulse; for choosing
  between technologies use verdict.
---

# learn — personalized tutor with memory

`/learn <topic>` — start or continue learning a topic
`/learn` — list topics in progress and what's due
`/learn quiz <topic>` — quiz-only session (no new material)

Answer one question per session: **what should this learner do for the next
N minutes to durably advance toward their goal?** One unit per session,
active recall before and after, everything scored and remembered. The point
is durable learning, not an impressive wall of text.

This skill is deliberately **keyless** (native `WebSearch`/`WebFetch` only,
when verification is needed) and **human-paced**: the learner answers real
questions in chat; you grade what they actually wrote.

## Modes (auto-detect)

- **NEW** — no `out/learn/<slug>.md` exists for the topic → interview + syllabus.
- **CONTINUE** — a log exists → run the session loop from where it left off.
- **STATUS** — `/learn` with no topic → summarize all logs: per topic, progress
  (`x/y` units), last session date, review items due, and a suggested next step.
- **QUIZ** — "quiz me" → recall-only session from the review queue + covered
  units; grade, update the log, teach nothing new.

## The learning log — memory across sessions

One file per topic: `out/learn/<slug>.md` (`<slug>` = topic lowercased,
non-alphanumerics → hyphens). It is the skill's entire memory
and it is the learner's file too — plain markdown they can read and edit.
Respect manual edits (a unit hand-marked done stays done; ask nothing).

```markdown
# learn log: <Topic>

## Learner
Goal: <what they want to be able to DO> · Level: <self-described start point>
Background: <relevant experience to hook examples onto> · Session length: ~<N> min
Freshness: <stable — teach from knowledge · fast-moving — verify each unit before teaching>

## Syllabus                <!-- status: ☐ not started · ◐ taught, not passed · ✓ passed -->
1. ✓ <unit — one teachable idea>
   pass: <the check question/exercise that proves it> · rubric: <2–3 criteria>
2. ◐ <unit>
   pass: <…> · rubric: <…>

## Review queue            <!-- weak spots; due dates, not session counts -->
- <item missed> — missed 2026-07-05 (conf: sure) · due 2026-07-06 · passes 0/3

## Sources                 <!-- verified references; check here before searching again -->
- <title> — <url> · verified 2026-07-05 · covers: <units/claims>

## Sessions
| # | Date | Unit | Warm-up | Check | Notes |
|---|------|------|---------|-------|-------|
| 1 | 2026-07-05 | 1. <unit> | — | 3/4 | confused X with Y |
```

**At the start of every run:** read the log if it exists. **Write as you
grade, not at goodbye:** update the log immediately after each graded step —
warm-up scores right after the warm-up, check results right after the check.
A crashed or compacted session must not lose answers the learner already
gave. Compute dates with `date +%F`, never guess. Older logs (session-number
dues, no rubrics, no `Freshness:` line or `## Sources` section) upgrade in
place on the next run: session dues become dates (due today), a unit's
rubric is written when it's next touched, and a missing freshness verdict
is judged and written before any teaching.
**Supersede, don't delete:** a revised unit or rubric strikes the old line
and adds the new one — how the plan and the learner's understanding evolved
is itself signal for future sessions.

## NEW — interview, then syllabus (human-in-the-loop)

1. **Interview once**, in one compact question set (`AskUserQuestion`): the
   **goal** as an ability ("what do you want to be able to *do*?"), current
   **level** and relevant **background** (their stack/domain — examples get
   hooked onto this), and preferred **session length** (~15/30/45 min).
   Skip anything already clear from the request.
2. **Freshness check (effort-scaled):** for stable subjects (math, algorithms,
   an established language) draft from knowledge. For fast-moving subjects
   (a tool, framework, API, anything with versions or pricing) do **one**
   light `WebSearch` pass first to confirm the current major version and any
   recent breaking changes — so the syllabus isn't stale on day one. Cite what
   you verified. Don't fan out sub-agents; this is a check, not research.
   **Record the verdict** as the log's `Freshness:` line — `stable` or
   `fast-moving` — so CONTINUE sessions inherit the decision instead of
   re-judging it, and seed `## Sources` with anything you verified.
3. **Draft the syllabus:** 5–12 units, each **one teachable idea** sized to a
   session, sequenced so every unit builds on passed ones, ending at the goal.
   **Write each unit's pass check now** — the question or micro-exercise that
   will prove it, plus a 2–3-criterion rubric — so later grading is against a
   contract written before the teaching, not the tutor's mood after it.
   Present it and let the learner reorder/cut/add before saving. Then save the
   log and either start unit 1 (if the session has time) or stop cleanly.

## CONTINUE — the session loop

Copy this checklist into your working response and tick items as they
complete — the session isn't done until every box is ✓ or consciously
skipped with a stated reason:

```
- [ ] Log read; reviews due by date + next unit picked
- [ ] Warm-up recall asked — ANSWERED, with confidence tags
- [ ] Warm-up graded against rubrics; log updated NOW
- [ ] Freshness honored: fast-moving → unit claims verified, cited, Sources updated · stable → n/a
- [ ] Unit taught (concept → example on their background → misconception)
- [ ] Check questions asked — ANSWERED, with confidence tags
- [ ] Check graded; misses + confidence into the queue; log updated NOW
- [ ] Statuses final; next unit previewed
```

1. **Warm-up recall (~3 min):** 2–3 questions — review-queue items due today
   or earlier, plus one from the last unit. Ask the learner to tag each
   answer with confidence in the same message — `sure / mostly / half /
   guessing` — **before any grading is shown**. Never infer a missing tag;
   log it as untagged. **Ask, then stop and wait.**
2. **Grade honestly, against the rubric:** right/partial/wrong per answer,
   naming the rubric criterion that failed. Partial credit is named, not
   rounded up. A fast correct answer minutes after teaching is **fluency**;
   the spaced warm-up measures **storage strength**, the real goal — say so
   when a learner aces a check and asks why the material still comes back. A miss tagged `sure` is gold — correct it explicitly and put
   it at the front of the queue: high-confidence errors, once corrected, are
   the stickiest learning there is. **Strict mode** (when the learner asks):
   grade blind — a fresh-context sub-agent sees only the verbatim answers
   and the rubric, never the lesson; the tutor who just taught grades with
   an optimism bias, the same reason done uses fresh reviewers.
3. **Teach the unit:** the concept, then a worked example grounded in the
   learner's stated background, then the most common misconception and why
   it's wrong. Match depth to the session length; **one unit only** — resist
   finishing the syllabus early. **Honor the log's `Freshness:` line:** for a
   fast-moving topic, check `## Sources` first and do one light, unit-scoped
   `WebSearch` only for what it doesn't already cover — cite inline and add
   new finds to `## Sources` (verification gets cheaper each session, not
   repeated). For a stable topic teach from knowledge, but anything version-,
   date-, or price-sensitive that sneaks into a unit still gets verified
   (same rule as NEW step 2).
4. **Active-recall check:** 2–4 questions or one small exercise applying the
   unit — confidence tags requested with the answers, exactly as in the
   warm-up. Wait for answers; grade as in step 2, against the unit's rubric,
   naming any failed criterion.
5. **Update the log:** unit status (✓ needs a passed check — being taught is
   only ◐), session row, misses into the review queue.
6. **Preview:** one line on what the next session covers, and anything worth
   doing between sessions (a ≤15-min hands-on task when the topic allows).
   For fast-moving topics, name one primary source from `## Sources` worth
   reading before next time.

**Spacing rule (dates, not session counts):** a missed item is due
**tomorrow**; each pass on review roughly doubles the interval — **3 days →
7 → 16** — and the third pass (the 16-day review) retires it. The queue row's
`passes n/3` carries this state, so any later session knows the next interval;
a new miss resets it to 0/3. Forgetting runs on
days; session counts break the moment the learner's schedule is irregular.
**Amnesty on return:** facing a large overdue backlog, don't quiz all of it —
pick the 3 most valuable items (latest units, `sure`-tagged misses), push
the rest one interval forward, and say so plainly. Backlog shame is how
learners quit. If the learner says "just tell me, skip the quiz," teach
without quizzing but mark the unit ◐ — unpassed — and say why it stays so.

## Guardrails

- **No fabrication.** Stable fundamentals from knowledge; anything
  version-, date-, price-, or API-sensitive gets verified via web search and
  cited inline. If unverifiable, say "as of my knowledge" explicitly.
- **Wait for answers.** Recall only works if the learner retrieves. Never
  fill in their answer, never grade an answer they didn't give.
- **Honest grading.** A wrong answer marked right poisons the log. Weak spots
  go in the queue even when it feels pedantic. Confidence is the learner's
  word only — never invented, never inferred.
- **One unit per session.** Durable beats fast. The syllabus is the pace.
- **The log is the learner's.** Human-readable, hand-editable, theirs to
  commit or ignore, and respected — never overwrite their manual edits.
- **Keyless.** Never ask for API keys; degrade gracefully (no web → teach
  from knowledge and label freshness honestly).
