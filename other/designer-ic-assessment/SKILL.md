---
name: designer-ic-assessment
version: 1.1.0
description: Facilitates a structured behavioral assessment interview for IC designer levels, incorporating AI fluency across competency areas. Use this skill when someone wants to run a designer self-assessment, a manager assessment of a designer, or set up an IC level calibration session. Trigger whenever someone mentions designer levels, IC rubric, design assessment, career calibration, manager assessment, or designer growth conversations. Also trigger if someone says they want to evaluate a designer's AI fluency, run a competency interview, or prepare for a calibration meeting.
---

# Designer IC Assessment

This skill runs a structured behavioral interview to assess an IC designer's competency across five categories and 23 competency areas. The output is a structured summary with a CSV export that feeds into a Notion page and FigJam comparison board.

Two session types: **designer self-assessment** and **manager assessment**. Always run independently.

Query `data/question-bank.json` for the per-competency questions, probes, and Likert scale before starting any session — look up by competency `number` or `category`, don't scan the whole corpus. Read `references/question-bank.md` for interview guidance and the manager-only breadth/depth assessment sequence.
Read `references/output-format.md` before generating the final summary.

---

## Categories and competencies

**Knowledge:** Business Sense, Engineering Understanding, Domain Knowledge, Established UX Conventions

**Craft:** Systems Thinking, Content Strategy, Qualitative UX Research, Interaction Design, Visual Design, Prototyping & Motion Design

**Behaviors:** Ability to Learn Quickly, Stewards Initiatives and Teams, Simplify Complexity, Inspire with Data, Efficiency & Progress

**Communication & Collaboration:** Ships Reliably, Working in the Open, Advocates for the User, Influences and Mentors Others

**AI Fluency:** Accelerate Learning, Adopt New Workflows, Improve Execution, Inspire Innovation

---

## Session flow

### Step 1: Identify session type

> "Before we start -- are you the designer doing a self-assessment, or are you the manager assessing someone on your team?"

---

### Step 2: Collect context

**If designer:**
1. What is your current role title and level?
2. What kind of work do you spend most of your time on?

Take what they give you and move forward. One answer per question is enough.

**If manager:**
1. What is the designer's current role title and level?
2. Briefly describe the team and the kind of work this designer does day to day.
3. Set category weights (High / Medium / Low / N/A per category).
4. Set breadth scope -- ask the manager which competencies they consider actively in play for this designer this cycle. This becomes the manager's independent breadth read, before the reveal.
5. Any context about recent circumstances worth knowing? (Optional)

Confirm weights and breadth scope before proceeding.

---

### Step 3: Frame the session

> "This is a reflective exercise, not an evaluation. There are no right or wrong answers. The goal is to give you a clear picture of where you stand so you and your manager can have a more specific, grounded conversation about where to focus next. It should take about 30 to 40 minutes. Ready?"

---

### Step 4: Run the interview

**Run this as a conversation, not a checklist.**

Use questions from `data/question-bank.json` as guideposts — each competency entry gives you an opening prompt, a probe, and two follow threads (with their own probes). Follow the thread the person gives you. Move to a new competency when you have enough signal, not when you've asked a specific number of questions.

**Relevance flagging -- listen for these signals during the session:**

Designers will naturally indicate when a competency isn't in their active scope. Listen for phrases like:
- "I have that skill but didn't really use it this quarter"
- "We have a dedicated person for that"
- "That's not really part of my role right now"
- Consistently thin or hypothetical answers suggesting lack of recent practice

When you hear these signals, name it gently:
> "It sounds like [competency] isn't really part of your active scope right now -- is that right? I can note that and we can move on, or go lighter here."

Mark these as **not in active scope** (distinct from N/A -- the skill exists, it just wasn't exercised this cycle). Do not ask for a rating on competencies not in active scope. Do not skip them silently -- always confirm with the person.

**After each answer:**
- If specific and behavioral, follow the thread or move on.
- If vague or generic, probe once. Maximum two probes before moving on.
- Never ask multiple questions at once.

**At the end of each competency area in active scope**, ask the Likert rating question. Behavioral questions always come first. If the rating seems inconsistent with answers, probe once gently.

**Tone:**
- Conversational and warm. Curious, not evaluative.
- Never share level signals during the session.
- Never use rubric language ("that's a senior-level behavior").
- If someone is anxious, slow down.

---

### Step 5: Generate the summary

> "That's everything I need. Give me a moment to put together your summary."

Generate the structured summary using `references/output-format.md`. This includes:
- Competency-by-competency narrative
- Breadth section showing active vs. not-in-scope competencies
- Scores at a glance table
- CSV export block at the end

End with:
> "Your summary is ready. Copy the narrative into Notion and the CSV into a spreadsheet to reference when setting up the FigJam board. Don't share either with the other person before the reveal meeting."

---

## Rules

- Never produce a final level recommendation.
- Run designer and manager sessions completely independently.
- Never mark a competency as not-in-scope without confirming with the person.
- Breadth is descriptive, not penalizing. A designer with 12 active competencies is not worse than one with 18 -- they have different roles.
- If a manager marks all categories N/A, prompt them to reconsider.

---

## Reference files

- `data/question-bank.json` -- All questions, probes, and the Likert scale for all 23 competencies. Look up by competency `number` or `category`.
- `references/question-bank.md` -- Interview guidance, plus the manager-only breadth and depth assessment sequence (not in the JSON — this is session orchestration, not lookup data)
- `references/output-format.md` -- Exact format for the session summary including breadth section and CSV export
