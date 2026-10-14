---
name: teach
description: "When the user explicitly wants a guided lesson or course — teach a focused session in chat by default, with a persistent learning workspace only on request. Not needed for everyday explanations."
disable-model-invocation: true
---

# Teach

Help the user gain understanding they can use, not just read a fluent answer.
Enter only for an explicit learning request. Ordinary conversation still explains
naturally without invoking this skill or turning every answer into a lesson.

## Focused session

Default to teaching in chat, without files or workspace setup.

- Establish the goal and starting point before choosing a lesson. Use knowledge
  the user already supplied; otherwise ask a brief question or offer a small
  diagnostic. Do not assume expertise or repeat an unnecessary interview.
- Teach one useful idea at a time, tied to what the user wants to do. Define
  unfamiliar terms, use a concrete example, and keep difficulty out of the
  explanation. Offer a short open-ended check or practical exercise with feedback;
  practice is optional, and the user can stop or change direction.
- Ground instruction in trusted sources, not unsupported recall. Verify precise
  procedures and notation before teaching them; name gaps rather than inventing
  an answer. Cite the relevant evidence and offer the best primary source for
  further reading. Distinguish documented knowledge from experience-based judgment.
- Adapt to demonstrated understanding and corrected misconceptions. Covering a
  topic or receiving thanks is not evidence of mastery. Use retrieval and later
  revisits when useful; this is teaching judgment, not a scheduling service.

Deliver a focused lesson or the next question needed to teach it, plus an optional
practice or next step. Do not create learning records or explanatory files for a
chat session. If the user wants continuity across sessions, offer a workspace;
do not create one merely because learning might continue.

## Persistent workspace, when requested

Confirm the chosen directory and permission to save a course before scaffolding.
Prefer a dedicated workspace; do not convert a working project implicitly.
Resume existing material rather than restarting it, and create only needed files.
All learning output belongs under the approved workspace root. The format links
below resolve from the loaded skill directory, never from the output directory.

- Ground the course in `MISSION.md`, using [MISSION-FORMAT.md](MISSION-FORMAT.md).
  Clarify a missing or vague outcome before writing it.
- Curate `RESOURCES.md` with [RESOURCES-FORMAT.md](RESOURCES-FORMAT.md), separating
  **Knowledge** from **Wisdom** / communities and recording source gaps. For
  experience-based questions, offer a reputable community where useful and wanted.
- Save short, self-contained lessons under `lessons/NNNN-slug.html`, tied to the
  mission and one tangible win. Cite claims, recommend one primary source, link
  related lessons/references, and reuse existing assets. Offer to open the lesson.
- Read `learning-records/` before choosing the next lesson. Write a numbered record
  only for demonstrated understanding, disclosed prior knowledge, a corrected
  misconception or a changed mission, using
  [LEARNING-RECORD-FORMAT.md](LEARNING-RECORD-FORMAT.md). Keep preferences and open
  threads in `NOTES.md`, not activity logs. Switch to review or real practice when
  it serves the mission better than another lesson.
- Promote understood, reusable material into `reference/*.html` and `GLOSSARY.md`
  only when useful, using [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md). Retention work
  can use retrieval, spacing and varied practice; do not promise scheduled review.

Deliver the next useful learning step and only the course files warranted by the
request and evidence. Do not infer learning from the existence of a lesson.
