---
name: lab-notes
description: >-
  Use when starting experiments, planning features with hypothesis-first
  approach, checking experiment status, logging observations, or wrapping
  up trials. Triggers: start an experiment, new trial, begin experiment,
  what experiments are running, check experiment status, wrap up the
  experiment, log observation, experiment verdict, plan a feature,
  explore an idea, /lab-notes.
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: "1.1.1"
---

# Lab Notes

Structured experiment management with append-only running logs, optional hypotheses, and formal verdicts. Two modes: **Rigorous** (full scientific method) and **Freeform** (exploratory, structure grows organically). Works for any hypothesis-first exploration — technical experiments, feature planning, product ideas, infrastructure changes.

## Workflow: FRAME -> SETUP -> RUN -> ANALYZE -> VERDICT

```
FRAME  ->  SETUP  ->  RUN  ->  ANALYZE  ->  VERDICT
  |                    |                       |
  |  (freeform: skip to)   |   (freeform: skip to)     |
  +--------------------+                       |
                                               v
                                    GRADUATE / ARCHIVE / ITERATE / PIVOT
```

## Mode Selection

Ask at experiment start: **"Is this a structured experiment or are you just trying something out?"**

| Answer | Mode | Behavior |
|--------|------|----------|
| "Structured" / "rigorous" / "I have a hypothesis" | **Rigorous** | All REQUIRED sections enforced via phase gates |
| "Just trying" / "exploring" / vague / casual | **Freeform** | Title + motivation required; everything else optional, asked but skippable |

Set `mode: rigorous` or `mode: freeform` in LOG frontmatter. Mode can be upgraded (freeform -> rigorous) at any time.

In Freeform mode, still ASK for hypothesis, success criteria, and fail condition — but accept "skip", casual one-liners, or "I'll figure that out later." A casual hypothesis is fine: "I bet we can do X with Y and it'd be really cool."

## Dispatcher: `/lab-notes`

Analyzes current state and suggests next action:

1. Scan `experiments/*/LOG-*.md` for YAML frontmatter
2. Check timebox deadlines against today (if set)
3. Detect if user is in an experiment directory
4. Report status table:

```
## Active Experiments

| Experiment | Phase | Mode | Started | Timebox | Status |
|------------|-------|------|---------|---------|--------|
| local-llm  | RUN   | freeform | 2026-03-11 | open-ended | 3 log entries |
| ev-charging | FRAME | rigorous | 2026-03-12 | 2026-04-01 | OVERDUE |
```

5. Suggest next action based on context

### Timebox Handling

- **Past deadline:** Prominent warning, suggest ANALYZE or VERDICT
- **Within 1 day:** Gentle reminder
- **Open-ended:** No nag — valid choice for hobby experiments
- **No timebox field:** Ask once if they want one, then leave it

The skill does NOT auto-close experiments. It informs. The human decides.

## Spoke Commands

| Command | Transition | What It Does |
|---------|-----------|--------------|
| `/lab-notes new <slug>: <title>` | -> FRAME | Create experiment from template |
| `/lab-notes setup [slug]` | FRAME -> SETUP | Validate framing, update phase |
| `/lab-notes run [slug]` | SETUP -> RUN | Validate setup, update phase |
| `/lab-notes log <observation>` | (stays in RUN) | Append dated entry to Running Log |
| `/lab-notes analyze [slug]` | RUN -> ANALYZE | Validate observations exist, update phase |
| `/lab-notes verdict [slug]` | ANALYZE -> VERDICT | Validate findings, prompt for verdict + next action |

### `/lab-notes new`

1. Ask mode question (rigorous or freeform?)
2. Create `experiments/YYYY-MM-DD-slug/LOG-slug.md` from `${CLAUDE_SKILL_DIR}/templates/log.md`
3. Fill frontmatter: phase, mode, started, slug
4. In **Rigorous** mode: prompt for hypothesis, success criteria, fail condition, motivation, time-box, pre-committed decisions
5. In **Freeform** mode: prompt for motivation (required), then ask for hypothesis (accept skip), ask about time-box (accept "open-ended")
6. Commit: `D: Start lab-notes <slug> — <title>`

### `/lab-notes log`

The most-used command. Must be frictionless:

```
/lab-notes log Tested model X — 84% accuracy, 990ms avg. Better than baseline.
```

Appends to the active experiment's Running Log:
```markdown
### 2026-04-05 14:30 — Tested model X
84% accuracy, 990ms avg. Better than baseline.
```

If multiple experiments are active, ask which one (or detect from current directory).

## Phase Gates

Phase gates are **requirements in Rigorous mode** and **suggestions in Freeform mode**.

### Rigorous Mode Gates

| Gate | Required Before Advancing |
|------|--------------------------|
| FRAME -> SETUP | Hypothesis non-empty, >=1 success criterion, fail condition stated |
| SETUP -> RUN | Environment section non-empty |
| RUN -> ANALYZE | >=1 dated entry in Running Log |
| ANALYZE -> VERDICT | Findings section non-empty |

Blocked transitions produce a clear message: "Cannot advance to SETUP — hypothesis is empty. Write your hypothesis first."

### Freeform Mode Gates

| Gate | Required Before Advancing |
|------|--------------------------|
| FRAME -> RUN | Motivation non-empty (can skip SETUP entirely) |
| RUN -> VERDICT | >=1 dated entry in Running Log (can skip ANALYZE) |

Freeform mode allows jumping: FRAME -> RUN -> VERDICT. The skill suggests intermediate steps but does not block.

## Reference

For lab notebook conventions (do's and don'ts, electronic record-keeping), consult `${CLAUDE_SKILL_DIR}/references/nci-lab-records-guide.md` — the NCI's official guide (public domain).

## Context Loss Prevention

- Every skill invocation that touches the LOG MUST append, never overwrite
- Running Log uses append-only semantics: new entries at bottom
- When entering a new session with an active experiment: prompt "Read LOG-slug.md to re-establish context"
- Failed Attempts section captures what did NOT work (often more valuable than successes)

## Verdict and Graduation

### Verdict Structure

Two independent axes (completeness is phase; confidence is judgment):

```markdown
**Outcome:** CONFIRMED | REFUTED | INCONCLUSIVE | ABANDONED
**Confidence:** certain | high | moderate | low
```

An experiment can be INCONCLUSIVE with high confidence ("we definitely don't have enough data") or CONFIRMED with low confidence ("it worked once but...").

### Next Actions

| Action | When | How |
|--------|------|-----|
| **GRADUATE** | Confirmed AND needs ongoing work | `git mv experiments/YYYY-MM-DD-slug/ projects/slug/` — add README.md, update TODO.md |
| **ARCHIVE** | Any verdict, no ongoing work needed | Write verdict, set phase to VERDICT. No file moves. |
| **ITERATE** | New questions raised | Write verdict with pointer to new experiment. Create new experiment. |
| **PIVOT** | Reframe hypothesis | Reset phase to FRAME, append new hypothesis to same LOG. |

Commit conventions:
- `D: Archive lab-notes <slug> — <one-line verdict>`
- `R: Graduate lab-notes <slug> to projects/<slug>`
- `D: Iterate from lab-notes <slug> -> <new-slug>`

## Integration

| System | How |
|--------|-----|
| **Sessionlogs** | Complementary: sessionlogs = session narrative; LOG = experiment observations. A session touches multiple experiments; an experiment spans multiple sessions. |
| **TODO.md** | Active experiments don't need TODO entries — `/lab-notes` is the tracker. VERDICT outcomes requiring follow-up (graduation, iteration) create TODO items. |
| **Delegate-agents** | Tell the delegate: "Append all observations to experiments/YYYY-MM-DD-slug/LOG-slug.md". The LOG protects against context loss across compact/restart cycles. |
| **Dossier skill** | Complementary: dossier = one-shot research deliverable; lab-notes = multi-session exploration. A dossier may feed into an experiment; an experiment may produce a dossier. |
| **commit-notation** | `D:` for experiment docs, `R:` for graduation moves, `E:` for experiment work (code, scripts, eval harnesses). |
| **system-maintenance** | Overdue timeboxes flagged as health check items. |
| **tracer-bullets** (in [plot-pm/plot](https://github.com/plot-pm/plot)) | Different purpose: tracer-bullets proves architecture works (vertical slice); lab-notes documents what was learned exploring. An experiment might USE a tracer bullet as its method. |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Rewriting LOG entries | Always append. Cross out with ~~strikethrough~~ if correcting. |
| Skipping motivation in Freeform mode | Motivation is required even in Freeform — it's the minimum "why" |
| Forcing deadlines on exploratory work | Time-box is optional. Ask, don't require. |
| Starting Rigorous when Freeform fits | Ask the mode question. Most hobby experiments are Freeform. |
| Forgetting to log during execution | `/lab-notes log` should be called frequently during RUN phase |
| Drawing verdict without evidence | Findings/observations must support the verdict — even in Freeform mode |

## Migration for Existing Experiments

Existing experiments (pre-skill) are NOT retroactively restructured. When revisiting an old experiment, the skill can offer to add frontmatter and a Verdict section. All new experiments via `/lab-notes new` follow the full convention.
