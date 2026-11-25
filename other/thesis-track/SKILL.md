---
name: thesis-track
description: Takes a master's or doctoral thesis from proposal through plan, chapter cycles and whole-thesis revision to defence preparation, in gated steps with a supervisor checkpoint at each.
license: CC0-1.0
metadata:
  version: 1.0.1
  kind: workflow
  category: scientific-writing
  source: https://hermes-ide.com/prompts/thesis-track
  catalog: 2026.1014.1
---

# Thesis track

## Inputs

- [TOPIC] (required): Your thesis topic or question as it stands, the field, what you have done so far (reading, data, drafts) and what your supervisor has said.
- [DEGREE] (required): The degree and format, for example "MSc dissertation, 15,000 words", "PhD by monograph", "PhD by publication (3 papers)", plus your institution's rules if you have them.
- [DEADLINE] (optional): The submission deadline and any earlier milestones such as a proposal defence, confirmation review or ethics deadline.
- [SLUG] (optional; default: thesis): Short kebab-case name for the thesis, used for the folder the step artifacts are saved in.

Take each value from the invocation or the user’s message. If a required value is missing, ask for it once.

Guides a thesis the way an experienced supervisor would: a defensible question and contribution, a structure and timeline worked back from the deadline, chapter cycles, a whole-thesis revision read as an examiner would, then defence or viva preparation. Each step writes one artifact, ends with a supervisor checkpoint (what to bring, questions to ask, what to record) and stops for approval: the supervisor and the institution, not this workflow, approve the thesis.

<topic>
[TOPIC]
</topic>

Degree and format: [DEGREE]
Only if [DEADLINE] was provided: Deadline and milestones: [DEADLINE]

Rules for every step:
- The thesis is the student's own work. Help by questioning, planning, outlining, reviewing drafts and modelling a short example; never write chapters or sections for submission, and never invent sources, data, results or quotations. Mark gaps as [MISSING: ...].
- Ask before assuming institutional rules (word limits, format, publication rules, examination process); list unknown ones as questions for the supervisor or graduate school.
- Keep scope realistic: a master's thesis shows competence and a modest contribution; a PhD makes an original contribution. Prefer a smaller finished thesis to a larger unfinished one.
- Remind the student once, at the start, to follow the institution's policy on AI assistance and disclosure.
- Carry decisions from approved artifacts forward instead of re-asking; record changes the supervisor requests.

## Steps

Work through these steps in order. Do not skip a gate.

1. proposal (plan)
2. plan (plan)
3. chapters (build)
4. revision (review)
5. defence (review)

### Step 1: Question, contribution and proposal

Fix what the thesis answers and why it matters before planning chapters.

1. Get the student to state the question and the claim they hope to defend in one or two sentences each. If they cannot yet, ask about the problem, the gap and the evidence they can get, and offer two or three candidate questions to react to.
2. Test the question: answerable with the time, data, skills and access available; narrow enough to finish; important beyond the student; more than a summary. Name the weakest point.
3. State the intended contribution in the form examiners recognise (new finding, method, dataset, theory, application or synthesis) and for whom.
4. Outline the proposal: background and gap, aims or questions, methods and feasibility, ethics and data access, expected contribution, risks and an initial timeline, under the institution's headings if given.
5. List dependencies that could sink the timeline (ethics, data access, recruitment, equipment, partners), each with action and owner.

Supervisor checkpoint: the outline to discuss, three questions to ask, space to record decisions.

Stop and wait for approval of the question, contribution and proposal outline.

Save this step's result to `theses/[SLUG]/01-proposal.md`.

**Gate:** stop here and wait for the user's approval before step 2 (plan).

### Step 2: Structure and timeline

Turn the approved proposal into a thesis structure and a plan that fits the deadline.

1. Propose the structure that fits the degree and format: chapters for a monograph, or introduction, papers and integrating chapters for a thesis by publication. For each chapter: its job in the argument, the aim it serves, the main content and a target word count.
2. Show the argument thread: one line per chapter on how it moves the claim forward, so gaps and redundancies show.
3. Build the timeline backwards from the deadline: submission, proofreading, whole-thesis revision, supervisor reading time per draft, drafting, analysis, data collection and ethics approval, with buffers. Mark milestones and the next deliverable's date.
4. Mark the critical path and the two or three likeliest slippage risks, each with a fallback (what to cut or defer).
5. Set a writing routine that fits the student's real week, drafting early rather than after all data are in.

Supervisor checkpoint: agree the structure, timeline and turnaround times; confirm institutional deadlines.

Stop and wait for approval of the structure and timeline.

Save this step's result to `theses/[SLUG]/02-structure-and-timeline.md`.

**Gate:** stop here and wait for the user's approval before step 3 (chapters).

### Step 3: Chapter cycles

Work through the chapters one at a time in a repeatable cycle, keeping a log. Start with the chapter the student can write most easily now (often methods), not necessarily chapter one.

For each chapter:
1. Outline with the student: the chapter's question and claim, the sections, each paragraph's point in one line, and the figures or tables. Check it against the step 2 argument thread.
2. The student drafts, not you. If they are stuck, talk through the point, suggest freewriting, or model a short paragraph clearly marked as an example to replace.
3. Review the draft from big to small: it serves the thesis question, the claim is clear at start and end, literature is synthesised rather than listed, results come before interpretation, claims are proportionate and cited where needed. Give the three most important changes first.
4. Log chapter, version, date sent to the supervisor, feedback, decisions and remaining actions.

Keep the step 2 timeline updated; flag slippage early with what to cut or defer.

Supervisor checkpoint per chapter: the draft plus the specific questions the student wants feedback on.

Stop and wait for approval when every chapter has a complete draft or the student wants to move on.

Save this step's result to `theses/[SLUG]/03-chapter-log.md`.

**Gate:** stop here and wait for the user's approval before step 4 (revision).

### Step 4: Whole-thesis revision

Read the full draft as an examiner would and plan the revision.

1. Check the whole: the introduction's question and contribution match the conclusion's claims; every chapter serves the question; the argument thread shows in chapter openings and closings; terms and numbers are consistent; contribution and limitations are explicit.
2. For a thesis by publication, check the integrating chapters show how the papers form a whole and state the student's contribution to co-authored papers.
3. List revisions in priority order (structural, chapter, sentence and formatting), each with location and effort.
4. Final checks: formatting and word limits, front matter, references, figure and table numbering, appendices, permissions for reproduced material, ethics and data statements, AI-use disclosure if required, and the institution's similarity check.
5. Plan the last weeks: revisions, the supervisor's final read, proofreading and submission.

Supervisor checkpoint: the revision plan and final draft for sign-off; confirm examination arrangements.

Stop and wait for approval of the revision plan.

Save this step's result to `theses/[SLUG]/04-revision-plan.md`.

**Gate:** stop here and wait for the user's approval before step 5 (defence).

### Step 5: Defence or viva preparation

Prepare the student to explain and defend the thesis.

1. Help the student write three-minute and ten-minute summaries in their own words: question, why it matters, what they did and found, contribution and main limitation.
2. Draft likely questions in groups: motivation and contribution, literature, methodology and alternatives, results and interpretation, limitations and what they would change, future work, and questions on the weakest points found in step 4.
3. For each group, give one example of a strong answer structure (acknowledge, answer, evidence, limit), not scripted answers.
4. Plan a mock defence: who runs it, how long, what to practise, including a question they cannot answer.
5. List known errors and corrections to bring, and arrangements to confirm (format, length, examiners, any presentation).

Supervisor checkpoint: arrange the mock defence and confirm the examination format.

This is the last step. End with a checklist of what to do in the final week.

Save this step's result to `theses/[SLUG]/05-defence-prep.md`.
