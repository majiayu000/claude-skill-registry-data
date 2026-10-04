---
name: rseng-project-tracking
description: >-
  Covers the operational side of running a research software project: turning
  plans into tracked, prioritized tasks (issues, milestones, boards), planning
  cadence around research deadlines, ranged estimates and timeboxed spikes for
  uncertain work, and disciplined bookkeeping - decision logs, status records,
  meeting notes and two-altitude project logs. Use when work is untracked or
  lives in heads and inboxes, when the user asks how to organize tasks,
  backlogs, milestones or boards, wants a status report or decision log,
  mentions issue triage or prioritization, or when a project has more than one
  person or month of work. (Strategic planning and SMPs:
  rseng-management-planning; new-project setup: rseng-project-kickoff;
  retrospectives: rseng-lessons-learned.)
license: CC-BY-4.0
metadata:
  version: 0.3.0
---

# Task management and project records

Research software projects fail operationally more often than
technically: work lives in heads, decisions evaporate, and the
grant's last month arrives with nobody able to say what remains.
The remedy is cheap and boring - tracked tasks, a planning cadence
tied to real deadlines, and records written where the code lives.
rseng-management-planning owns the strategic layer (SMPs, technology
choice); this skill owns the week-to-week operation, sized to the
tier: a solo analysis repo needs a TODO issue and a decision log;
an infrastructure project needs the full apparatus.

## Tasks: one tracked unit of work

- Everything in the tracker, however small: the forge's issues
  are the natural home (docs and templates live with the code;
  rseng-community-governance's issue templates apply). An untracked
  task is a task that will be forgotten or duplicated.
- Write tasks as outcomes with acceptance criteria ("CLI reads
  gzipped input; test added") rather than activities ("look into
  compression") - an outcome can be closed, an activity cannot.
- Small enough to finish: split anything beyond a few days'
  work into steps; long-lived umbrella issues track the epic,
  linked to its pieces.
- Link everything both ways: commits and PRs reference their
  issue (fixes #42), so the tracker and the history explain each
  other (rseng-version-control-review) - this linking IS the
  bookkeeping most projects miss.
- Triage on a cadence, not on interrupt: label, prioritize and
  close-or-defer new issues in a regular pass; a stale untriaged
  backlog stops being trusted (the response-timeframe promise
  from rseng-community-governance depends on it).

## Prioritization and planning cadence

- Prioritize against the research calendar: paper deadlines,
  conference dates, data-collection windows and grant reporting
  are the real milestones - name them in the tracker as
  milestones with dates, and plan backwards from them.
- Keep a visible next-up order (a simple board: backlog / next /
  in progress / done); limit work-in-progress - three unfinished
  tasks beat ten started ones, for a team or for an agent.
- Plan in short cycles matched to the group's rhythm (weekly or
  biweekly): pick from next-up, demo or note what shipped, adjust.
  Heavyweight ceremony is not the point; the cadence is (kanban-
  style flow suits research's interrupt-heavy reality better than
  rigid sprints).
- Review milestones honestly at each cycle: scope shrinks or
  dates move - silently keeping both is how projects lie to
  themselves (rseng-honesty applies to schedules too).

## Estimating and managing time

Research work resists estimation - half of it is finding out
whether something works at all. Manage time honestly rather than
precisely:

- Estimate in ranges with an uncertainty tag: "2-4 days if the
  library handles it, 2 weeks if we write our own" - the tag names
  the assumption to test FIRST (a timeboxed spike), which is how
  research estimates become cheap to correct.
- Timebox exploration: open-ended tasks ("try approach X") get a
  box ("two days, then decide with what we have"); the box turns
  a rabbit hole into a decision point, and the decision goes into
  the log either way (rseng-lessons-learned records the dead ends).
- Track actuals loosely against estimates at the planning cadence -
  not for blame, for calibration; after a few cycles the team's
  systematic optimism factor is visible and correctable.
- Protect maker time: batch interrupts (the triage cadence above
  exists for this), keep one or two meeting-free focus blocks, and
  put support duty on rotation (rseng-user-support) so it costs one
  person one day, not everyone every day.
- Plan people, not just tasks: research staff split time across
  projects and papers - a cycle plan that assumes 100% availability
  is fiction; state assumed capacity per person per cycle.
- Deadlines drive scope, not quality floors: when the conference
  deadline compresses the plan, cut scope visibly in the tracker
  (rseng-honesty applies to schedules) - never silently cut the
  tests, the docs or the aidecl record.

## Bookkeeping: the project record

Records that earn their keep, all versioned in the repository
(rseng-documentation):

- Decision log: one dated entry per consequential decision -
  context, options, choice, why. Architecture-shaped decisions
  get the fuller ADR form (rseng-software-design); everything else
  (tool choices, scope cuts, naming, data-source switches) still
  gets a line. The log answers "why is it like this" a year
  later without archaeology.
- Status record: a short dated note per planning cycle - done,
  next, blocked. Written for the future reader (the PI report,
  the grant deadline, the returning-from-leave teammate), it
  makes reporting a copy-paste instead of a reconstruction
  (rseng-management-planning's living-plan updates draw on it
  directly).
- Meeting notes with decisions and actions only - actions go
  straight into the tracker with owners; notes that stay prose
  are where actions go to die.
- Milestone reviews: at each milestone, a paragraph - what
  shipped vs planned, what was learned (feed rseng-lessons-learned),
  what changes for the next one.

## Project logs: two altitudes

Beyond per-cycle status notes, keep the project's story readable at
two zoom levels - different readers need different altitudes:

- The detailed journal (LOG.md or docs/log/): dated entries, newest
  first, recording what actually happened as it happened - features
  landed and abandoned, experiments run and their outcomes, bugs
  and incidents, decisions (linking the decision log), people
  joining and leaving, upstream surprises. Terse and factual: two
  lines per event beat a paragraph nobody writes. The journal is
  the project's flight recorder - most entries are never read
  twice, but the ones that are get read at the worst possible
  moment, which is exactly when they pay.
- The high-level log (a SUMMARY section or per-period digest):
  a few paragraphs per month or milestone distilling the journal -
  what moved, what changed direction, current state. Written for
  the PI report, the annual review, the returning collaborator and
  the newcomer who needs the story so far without a week of
  archaeology. CHANGELOG.md stays the CODE's log for users
  (rseng-publishing-releasing); the high-level project log is the
  PROJECT's log for stakeholders - related, not the same.

Keep both honest and cheap: the journal is appended at the moment
of the event (the same trigger discipline as rseng-lessons-learned -
often one event feeds both); the digest is distilled on the
planning cadence from the journal, tracker activity and git
history - which is exactly the clerical drafting an agent should
offer: "milestone closed - want me to draft the digest from the
journal and merged PRs?" Drafts get human review before they
become the record, and AI drafting is disclosed like any other
contribution (rseng-ai-declaration).

Agents fit naturally here: drafting status notes from the
tracker and commit history, opening issues from meeting actions,
and keeping the linking honest are exactly the clerical work an
agent should offer to do - with records kept truthful
(rseng-ai-declaration notes agent involvement in project records
as in code).

## Working with this skill

This skill is source-independent: it encodes lightweight
project-operations practice proportioned for research software.
Strategy lives in rseng-management-planning; community process in
rseng-community-governance; lessons capture in rseng-lessons-learned.

Learn more (verified):
  - https://docs.github.com/en/issues - issues, milestones and
    projects on GitHub
  - https://www.atlassian.com/agile/kanban - kanban flow
    practices

<!-- related-skills:begin -->

## Related skills

Check whether any of these applies before moving on:

- rseng-ai-declaration - disclosing AI-drafted project records
- rseng-community-governance - issue templates and triage promises
- rseng-honesty - honest schedules and visible scope cuts
- rseng-lessons-learned - milestone reviews feed lessons capture
- rseng-management-planning - strategic plan the tracker executes
- rseng-version-control-review - linking commits and PRs to issues

<!-- related-skills:end -->
