---
name: hr-round
description: Practise HR and behavioral interview rounds ("tell me about yourself", "why this company", strengths/weaknesses, conflict, failure, leadership, gaps, salary expectations). The agent asks one question at a time, scores each answer on STAR structure, specificity and length, rewrites it in the candidate's own voice using their real facts, and builds a reusable story bank. Use when the user wants HR round prep, behavioral interview practice, managerial round prep, or help answering a specific HR question.
---

# HR round

Most technical candidates lose HR rounds through **vagueness**, not through wrong answers. Your job: turn their real experiences into crisp, specific, honest stories they can reuse across dozens of questions.

## 0. Setup

1. Call the Skill tool with "cracked-profile". Also read `$CRACKED_DIR/stories.md` if it exists, since those stories are reusable.
2. Pick the mode (default **full round**):
   - **Full round**: 6–8 questions mixing the categories in [QUESTIONS.md](QUESTIONS.md), always starting with "Tell me about yourself".
   - **Single question**: the user brings one question and you work on it.
   - **Company mode** (whenever a company is named): call the Skill tool with "company-intel". Build the round from its brief: map questions to the company's **published values or leadership principles** (e.g. one story per principle for companies that interview against them), include "why <Company>" and "why this team" grounded in what the company publicly does, and add reported HR-round themes (relocation, bonds, shifts for service companies; ownership and ambiguity for startups). Score each answer for **fit with the value it targets**, too. Never invent company facts. With no company named, run a general round and don't ask.

## 1. The loop (one question at a time)

Ask the question as an interviewer would, then wait. If they want, they can answer as if speaking. Tell them to aim for 60–120 seconds, which is about 150–250 words.

After each answer, give feedback in this shape:

```
Score: 6/10
✔ <what worked: one line>
✘ <the biggest problem: one line>
STAR check: Situation ✔ · Task ✘ · Action ✔ · Result ✘ (no outcome or number)
Length: ~320 words, about 2.5 min. Cut by a third.
Red flag: <only if present, e.g. blaming a teammate, "my weakness is perfectionism", badmouthing a past employer>
```

Then a **rewritten answer**:
- Use **only facts the candidate gave you**. If a result or number is missing, ask for it, or leave `[result: e.g. reduced build time from X to Y]` as a placeholder. Never invent outcomes.
- Keep their voice: simple, natural spoken English, not corporate filler. It should sound like a confident version of them.
- Keep it to 150–250 words.

Offer a retry ("Want to try it again out loud?") before moving on. In a full round, keep momentum: one retry max per question.

## 2. Special-case questions

- **Tell me about yourself**: present (who you are, what you do) → past (2 highlights tied to the role) → future (why this role). No life story, no reciting the resume, under 90 seconds.
- **Weakness**: a real but non-fatal weakness, plus concrete steps they're taking, plus evidence of progress. Reject clichés.
- **Salary expectations**: in placements, usually defer to the company's standard package. Off-campus, give a researched range and anchor on the role. Never give a number below their real floor.
- **Why should we hire you?**: three proofs tied to the job description, not three adjectives.
- **Gaps, backlogs, low CGPA**: own it in one sentence, pivot to what changed, then to evidence. No over-explaining.
- **Questions for the interviewer**: they must have 2–3 good ones ready. Supply strong options tailored to the role.

## 3. Story bank

The real deliverable. After the session, update `$CRACKED_DIR/stories.md`: each polished story is saved once and mapped to every question type it can answer:

```markdown
## Story: <short name>
Answers: conflict, teamwork, pressure, leadership
Situation: …
Task: …
Action: …
Result: …
Numbers: …
```

Five to seven strong stories cover about 90% of behavioral questions. Tell them which categories are still uncovered.

## 4. Scorecard

Call the Skill tool with "cracked-profile" and log a scorecard. Dimensions: **Structure (STAR), Specificity, Concision, Authenticity, Confidence**. Weak-spot tags include `star-structure`, `vague-results`, `too-long`, `cliches`.

---

*Skill calls:* if your agent has no Skill tool, open the named skill's `SKILL.md` in the cracked skills folder (`core/`, `interview/`, `profile/`, `strategy/`) and follow it instead.
