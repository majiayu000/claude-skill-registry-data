---
name: user-research
description: "Evidence about people before any design decision."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, research]
    category: web
    related_skills: [web-design, user-journeys, usability-testing]
    web_designer_stages: [intake, research, brief]
---

# User Research and Personas Skill

Gather evidence about people before any design decision, and turn it into research-grounded personas and problem statements. This skill covers interviews, surveys, analytics and competitor analysis, and what may and may not be claimed from them. It does not cover user journeys, which have their own skill, and it does not cover usability testing of a built page. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- At the start of a project, and whenever Hermes does not know who the user is or what task they are trying to do.
- Before IA, copy and priorities are decided, so those decisions trace to evidence.
- When the user supplies audience, tasks or evidence that must be recorded rather than assumed.
- When a design decision is disputed and the dispute must be settled by evidence, not taste.
- When a gap in knowledge must be named as a question instead of filled by assumption.
- Not to invent a persona to justify a design already chosen: personas come from what was heard, never the other way round.
- Not as a substitute for testing with real users later: research grounds the design, testing checks it.

## Prerequisites

- The run is active and the coordinator loaded this skill for its stage or stages.
- The user has been asked for audience, tasks and evidence; the answers, or their absence, are on the run record.
- Any evidence supplied — interviews, surveys, analytics, competitor analysis — is recorded with its source.
- The coordinator is the only router to the user: the skill never asks the user anything directly.

## How to Run

1. Ask the user for audience, tasks and evidence: who the site is for, what they are trying to do, and what is already known.
   - Record the answers in the user's own words where they matter.
   - Record an unanswered question as an open question, not as a blank.
2. Record what was heard, with sources; record gaps as open questions, not as silent assumptions.
   - Each finding names its source: an interview, a survey, analytics, or a competitor.
   - A finding with no source is labelled as an assumption.
3. Where evidence is missing, state the assumptions explicitly, labelled as assumptions.
   - An assumption is a statement that may be wrong, and it stays labelled until evidence replaces it.
4. Build personas and audience profiles only from what was heard — research-grounded, not invented demographics.
   - A persona carries tasks, needs and evidence, not just age and location.
   - No persona claims a trait no source supports.
5. Write the problem statement from the evidence, and let the personas drive IA, copy and priorities.
   - The problem statement names the people, their task, and what stands in their way.
6. Record the note, sources, personas and problem statement in the stage record.
   - The brief then carries the same audience, problem and primary action, with no drift.
7. Re-check after any fix, and record what changed.
   - A changed persona, finding or assumption is re-checked against its source before the stage closes.
   - The evidence recorded is the evidence the brief rests on, not an earlier draft.

## Quick Reference

- Methods: interviews, surveys, analytics, competitor analysis.
- Output: research-grounded personas and audience profiles, plus problem statements.
- Rule: personas are cited, not asserted; every major decision traces to a named user task or a named finding.
- Gaps: flagged as questions, never filled silently.
- Assumptions: stated explicitly when evidence is missing.
- Personas drive: IA, copy and priorities.
- Findings: each names its source — interview, survey, analytics, or competitor.
- Problem statement: names the people, their task, and what stands in their way.
- Personas: tasks, needs and evidence, not demographics alone.
- Labels: assumptions stay labelled until evidence replaces them.
- Gaps: open questions on the record, never silent assumptions.

## Procedure

### 1. What it is

Research before design: interviews, surveys, analytics and competitor analysis, turned into research-grounded personas/audience profiles and problem statements — not invented demographics.

### 2. How Hermes applies it

Hermes asks the user for audience, tasks and evidence, states its assumptions explicitly when evidence is missing, builds personas only from what was heard, and lets personas drive IA, copy and priorities — it does not invent a persona to justify a design.

### 3. What it returns to the stage

- `intake` stage record: `purpose`, `audience` and `primary_action` carry what the user said the site is for, who it is for, and the one action that matters.
- `research` stage record: `note` carries the research summary, the personas, the problem statement and the labelled assumptions; `sources` lists every source the note rests on.
- `brief` stage record: `problem`, `audience`, `primary_action`, `success_measure`, `tone`, `non_goals` and `intent` carry the evidence into the frozen brief.

### 4. Good looks like

Every major decision traces to a named user task or finding; personas are cited, not asserted; gaps are flagged as questions, not filled silently.

## Pitfalls

- Inventing a persona to justify a design: a made-up audience that conveniently wants exactly what was already planned.
- Filling a gap silently: an unanswered question answered by assumption, with no label, so the assumption hardens into a decision.
- Personas as demographics only: age and location with no task, no need and no evidence behind them.
- Research gathered after the design: evidence collected to confirm choices already made, rather than to shape them.
- A persona never cited again: IA, copy and priorities decided without reference to the people the research described.
- Competitor analysis copied as design: what rivals do is evidence about the market, not a decision about this site.
- One interview treated as the whole audience: a single voice standing in for every visitor, with no note of how narrow the sample is.
- Analytics read without a question: numbers collected with no task in mind, so they answer nothing the design needs.
- An assumption that loses its label: copied from the research note into the brief as if it were evidence.

## Verification

- Every major decision traces to a named user task or a named finding in the research note.
- Personas are cited with their sources; no persona rests on invented demographics.
- Gaps are flagged as open questions in the record, and assumptions are labelled as assumptions.
- The brief carries the same audience, problem and primary action as the research, with no drift.
- IA, copy and priorities each cite the personas or findings they follow.
- No assumption appears in the brief without its label.
- Each finding names its source: an interview, a survey, analytics, or a competitor.
- No persona claims a trait no source supports.
- A single interview is not treated as the whole audience; the sample's narrowness is noted.
- Competitor analysis is recorded as evidence about the market, not copied as design.
- The research note, sources, personas and problem statement are all on the stage record.
- The stage record carries the final evidence, not earlier drafts.
- The content judger checks that copy and priorities match the recorded audience and tasks. The skill does the work and the judger checks it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: intake, research, brief. Returns: `intake.purpose`, `intake.audience`, `intake.primary_action`; `research.note` (summary, personas, problem statement, labelled assumptions); `research.sources`; `brief.problem`, `brief.audience`, `brief.primary_action`, `brief.success_measure`, `brief.tone`, `brief.non_goals`, `brief.intent`. Judger boundary: content judger checks copy and priorities against the recorded audience and tasks.
