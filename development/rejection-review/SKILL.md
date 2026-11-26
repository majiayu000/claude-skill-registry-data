---
name: rejection-review
description: A structured, honest post-mortem after an interview or OA, whether rejected, ghosted, or unsure. It reconstructs what happened round by round, finds the real root causes (knowledge gap, problem-solving process, communication, time, nerves, or fit), cross-checks them against past cracked sessions for repeating patterns, and turns them into three targeted drills and an updated plan. Use when the user got rejected, failed an interview or OA, wants to debrief an interview, or asks "why do I keep failing interviews".
---

# Rejection review

Rejection hurts, and most candidates respond by grinding more random problems. The fix is almost never "more of everything". It's one or two specific failure modes, repeating. Find them.

## 0. Open with care, briefly

One line of acknowledgement, no therapy speak: "That's frustrating. Let's make it count: a 10-minute debrief now beats 100 random problems." 

Call the Skill tool with "cracked-profile", then read `$CRACKED_DIR/journal.md`.

## 1. Reconstruct, while it's fresh

Ask in **one round** (numbered; they can answer briefly):

1. Company, role, and which round(s): OA, technical (how many), system design, HR/managerial.
2. For each round: the questions asked, as close to verbatim as they remember.
3. What they did: approach, how far they got, whether the code ran, how much time was left.
4. Interviewer signals: hints given, follow-ups, tone, the moment it felt like it went wrong.
5. Their own gut feeling: where do *they* think it went wrong?

Then ask follow-ups on the round that most likely decided it. Up to 3 questions, one at a time.

## 2. Diagnose

Classify the evidence against these failure modes. A rejection usually has one primary cause and maybe a secondary one:

| Failure mode | Typical evidence |
|---|---|
| **Knowledge gap** | Didn't know the pattern, concept, or theory at all |
| **Problem-solving process** | Knew the topic but jumped to code, no brute force first, no examples, got lost |
| **Implementation** | Right approach, but buggy code, edge cases missed, couldn't debug |
| **Communication** | Silent for long stretches, unclear explanations, didn't ask clarifying questions |
| **Time management** | Stuck too long on part 1, never reached the follow-up |
| **Nerves / performance** | Knew it at home, blanked in the room; this often shows as a big home-vs-interview gap |
| **Fit / external** | Role or level mismatch, a strong competing pool, headcount, or no clear performance failure |

Be honest. If the evidence says "you didn't know Dijkstra", say that. If it genuinely looks external, say *that* too, so they don't over-correct. Some rejections aren't about performance.

**Cross-check the journal**: normalise its tags onto the canonical list in `cracked-profile`, then check whether these failure modes or weak-spot tags appear in past mocks. A repeat is the headline finding: "This is the third time edge cases sank you: twice in mocks, now in a real round."

## 3. Prescribe

1. **Root cause**, in 1–2 sentences.
2. **Three drills**, each specific, time-boxed, and mapped to a cracked skill where possible. For example:
   - "Edge cases: for the next 10 problems, write 5 edge-case inputs *before* coding. Then run `/mock-interview`. Target: Correctness ≥ 8."
   - "Graph shortest paths: `/pattern-coach shortest path`, then 6 problems from its ladder over 4 days."
   - "Nerves: three `/mock-interview` sessions this week, timed and out loud. Exposure is the fix."
3. **What went right**: at least one real positive from the evidence (not filler).
4. **Re-attempt**: give the key question(s) from the interview back as a practice problem now, or schedule it, so they close the loop.

## 4. Log and re-plan

1. Log a scorecard via the Skill tool with "cracked-profile", titled `<Company> · <round>`. Dimensions: **Knowledge, Problem-Solving Process, Implementation, Communication, Composure**, scored from the reconstruction. Tag weak spots precisely; this is where `prep-plan` gets its data.
2. If `$CRACKED_DIR/plan.md` exists, offer to run `/prep-plan` to fold the drills into the plan.
3. Close with one line of perspective that's true and not saccharine, e.g. "Most people who get offers have a pile of rejections behind them. The difference is that they debriefed."

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
