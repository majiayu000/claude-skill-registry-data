---
name: hw-doctor-prep
version: 1.0.0
description: Organize symptoms, history, and questions into a clear summary to bring to a clinician — no diagnosis.
author: matrixx0070
tags: [health, doctor-visit, symptoms, preparation, communication]
capabilities: []
---

This is general wellness information, not medical diagnosis or treatment. This skill does NOT diagnose, interpret symptoms, name conditions, or suggest treatments — it only helps you organize information to discuss with a licensed healthcare professional. For emergencies (chest pain, trouble breathing, stroke signs, severe bleeding), call emergency services now.

## When to use

Use this when someone has an upcoming medical appointment and wants to arrive organized — a clear timeline of symptoms, relevant history, current medications, and prioritized questions.

**Not for:** figuring out "what's wrong," estimating how serious something is, suggesting diagnoses/tests/treatments, or triaging urgency. Do not speculate about causes — capture facts and hand them to the clinician.

## Method

1. Capture the main concern in the person's own words, plus the single most important thing they want from the visit.
2. Build a symptom timeline: when it started, frequency, duration, severity (their own 0-10), what makes it better/worse, and how it affects daily life. Record only what they observed — no interpretation.
3. List relevant history: past conditions, surgeries, family history, allergies.
4. List current medications and supplements with doses (and anything recently stopped).
5. Decision point: if any red-flag symptom is mentioned (severe/sudden pain, breathing difficulty, fainting, etc.), advise seeking urgent care rather than waiting for the appointment — do not assess likelihood or cause.
6. Draft prioritized questions, most important first, so the top concerns get covered if time runs short.
7. Note logistics: what to bring (records, device data, insurance), and who is coming along.

## Example

Concern: "Recurring headaches, want to know what to do next." Timeline: started ~6 weeks ago, 3-4x/week, ~2h each, 6/10, worse in the afternoon, better with rest. History: none noted. Meds: occasional ibuprofen. Questions (top first): 1) What could be worth checking? 2) Should I track anything? 3) Any warning signs to watch for? (Facts only — no cause suggested.)

## Pitfalls

- Slipping into diagnosis or reassurance ("it's probably just stress") — stay descriptive; that is the clinician's job.
- Vague timelines ("a while ago") that waste appointment time.
- Forgetting the medication/supplement list, a common source of interactions.
- Burying the most important question at the bottom where it may be skipped.

## Output format

```
MAIN CONCERN: <in their words> | TOP GOAL FOR VISIT: <one line>

SYMPTOM TIMELINE
- Onset: <when> | Frequency: <how often> | Duration: <how long>
- Severity (self-rated 0-10): <n> | Better with: <x> | Worse with: <y>
- Daily impact: <note>   (facts only, no interpretation)

HISTORY: <conditions/surgeries/family/allergies>
MEDICATIONS & SUPPLEMENTS: <name — dose>

QUESTIONS (most important first)
1. <q>
2. <q>

BRING: <records/data/insurance> | WITH ME: <person>
NOTE: Organizational aid only — not a diagnosis. Discuss all of this with a licensed clinician; seek urgent care for red-flag symptoms.
```
