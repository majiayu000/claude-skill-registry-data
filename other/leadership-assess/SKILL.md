---
name: leadership-assess
description: Assess your leadership style, each team member's maturity and the team's current challenges, and recommend what to tackle first. Use when the user is new to leading a team or has inherited one and wants to know where to start as its leader. Not for a health check of a delivery team; see /project-management-team-health.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: leadership
  phase: 1
  artifact: 01-assess.md
---

# Assess

Assess the leadership landscape for "$ARGUMENTS". Understand your leadership style, evaluate team maturity, and identify the key challenges to address.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"leadership-assess","workflow":"leadership","phase":1,"project":"<project>","event":"skipped","artifact":"01-assess.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Assess) of the Leadership Development workflow (`leadership`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `leadership` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise, unless the user named this skill, ask one question, since this is the first phase of its workflow: "Just this step, or the whole Leadership Development workflow?" End your turn and wait; on the whole workflow, hand off the same way; on just this step, continue here.

**Recall.** Before you ask the user anything, look for what this repository already holds about `<project>`: if a tool is available whose description says it searches or maps this repository (a memory or repo-map server such as `repo_map` or `entities`), query it for `<project>` and this phase's subject and read what it returns, keeping only results from this repository; in every case also list `.singularskills/*/<project>/` and read the **Decisions** and **Open questions** of any artifact there, and the lines of `.singularskills/log.jsonl` whose `project` is `<project>`. After the frontmatter and title, add a `## Recalled` section of at most ten lines naming what you found and where (path or tool), or the single line `Nothing recalled: no earlier artifacts, log lines or memory results for <project>.` Ask the user only what this did not answer. The trail's shape is described in `references/memory/trail.md`, bundled with this skill.

Before you start work, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"leadership-assess","workflow":"leadership","phase":1,"project":"<project>","event":"started","artifact":"01-assess.md","note":""}`.

None — this is the first phase.

## Process

1. **Ask leadership assessment questions:**
   - What is your role? (team lead, manager, director, founder)
   - How large is your team? What are their experience levels?
   - What's your current leadership challenge? (new team, scaling, conflict, performance, culture)
   - How do you currently communicate with your team? (1:1s, standups, async)
   - What's working well? What's not?

2. **Assess team maturity:**
   - For each team member: how experienced are they in their role?
   - Who needs more direction vs. more autonomy? (Situational Leadership)
   - Where are the skill gaps?
   - What's the team's morale and engagement level?

3. **Identify leadership style:**
   - Based on answers, identify the user's natural leadership tendencies
   - Recommend style adjustments based on team maturity
   - Flag potential blind spots

4. **Write the artifact** to `.singularskills/leadership/<project>/01-assess.md` with sections:
   - **Leadership Profile** — role, style, strengths, blind spots
   - **Team Assessment** — each member's maturity level and needs
   - **Current Challenges** — prioritized list of issues to address
   - **Recommended Focus** — what to tackle first in the Vision phase

## Output

The assessment written to `.singularskills/leadership/<project>/01-assess.md`. Present a summary highlighting:
- Leadership style identified
- Team maturity overview
- Top 3 challenges to address

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"leadership-assess","workflow":"leadership","phase":1,"project":"<project>","event":"finished","artifact":"01-assess.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `none`, as this phase has no gate):

```yaml
---
skill: leadership-assess
workflow: leadership
phase: 1
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: none
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
