---
name: research-discover
description: Research a topic or problem broadly from desk sources — articles, studies, existing solutions, stakeholder groups — into a discovery brief of themes and open questions. Use when the user is starting to explore a problem space or product idea and wants to know what is already known. Not for buyer personas and pain points to drive a campaign; see /marketing-customer-research.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: research
  phase: 1
  artifact: 01-discover.md
---

# Discover

Cast a wide net on the research topic "$ARGUMENTS". Gather data, insights, existing research, competitive landscape, and stakeholder perspectives without filtering or narrowing.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"research-discover","workflow":"research","phase":1,"project":"<project>","event":"skipped","artifact":"01-discover.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 1 (Discover) of the Double Diamond workflow (`research`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `research` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise, unless the user named this skill, ask one question, since this is the first phase of its workflow: "Just this step, or the whole Double Diamond workflow?" End your turn and wait; on the whole workflow, hand off the same way; on just this step, continue here.

**Recall.** Before you ask the user anything, look for what this repository already holds about `<project>`: if a tool is available whose description says it searches or maps this repository (a memory or repo-map server such as `repo_map` or `entities`), query it for `<project>` and this phase's subject and read what it returns, keeping only results from this repository; in every case also list `.singularskills/*/<project>/` and read the **Decisions** and **Open questions** of any artifact there, and the lines of `.singularskills/log.jsonl` whose `project` is `<project>`. After the frontmatter and title, add a `## Recalled` section of at most ten lines naming what you found and where (path or tool), or the single line `Nothing recalled: no earlier artifacts, log lines or memory results for <project>.` Ask the user only what this did not answer. The trail's shape is described in `references/memory/trail.md`, bundled with this skill.

Before you start work, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"research-discover","workflow":"research","phase":1,"project":"<project>","event":"started","artifact":"01-discover.md","note":""}`.

None — this is the first phase.

## Process

1. **Web research** to gather broad context:
   - Use WebSearch to find recent articles, studies, reports, and discussions about "<project>"
   - Use WebFetch to read the most relevant sources in depth (aim for 5-8 quality sources)
   - Look for: academic research, industry reports, case studies, expert opinions, user forums

2. **Competitive and market analysis:**
   - Use WebSearch to find how others have approached this problem
   - Identify existing solutions, products, or methodologies
   - Note what works well and what gaps exist

3. **Stakeholder perspective mapping:**
   - Identify the key stakeholder groups affected by "<project>"
   - Document each group's likely needs, pain points, and motivations
   - Note conflicts or tensions between stakeholder groups

4. **Pattern identification:**
   - Group findings into themes
   - Identify recurring patterns across sources
   - Flag surprising or contradictory findings
   - Note data gaps — what's unknown or under-researched

5. **Write the artifact** to `.singularskills/research/<project>/01-discover.md` with sections:
   - **Sources** — list of sources consulted with key takeaways
   - **User & Stakeholder Insights** — needs, pain points, motivations by group
   - **Market & Competitive Landscape** — existing solutions, gaps, trends
   - **Key Themes** — recurring patterns across all research
   - **Surprises & Contradictions** — unexpected findings
   - **Open Questions** — what remains unknown

## Output

The discovery brief written to `.singularskills/research/<project>/01-discover.md`. Present a summary to the user highlighting:
- Top 3-5 key themes discovered
- Most surprising finding
- Biggest open questions for the Define phase

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"research-discover","workflow":"research","phase":1,"project":"<project>","event":"finished","artifact":"01-discover.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `none`, as this phase has no gate):

```yaml
---
skill: research-discover
workflow: research
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
