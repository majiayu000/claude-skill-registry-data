---
name: research-deliver
description: Validate the leading solution concept against evidence and success criteria and turn it into a final recommendation with action items and risks. Use when a preferred solution has emerged and the user wants to know whether it holds up and what to do next.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: research
  phase: 4
  artifact: 04-deliver.md
---

# Deliver

Converge on the final recommendation for "$ARGUMENTS". Validate the top solution concept(s) with evidence, refine the approach, and produce actionable recommendations.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"research-deliver","workflow":"research","phase":4,"project":"<project>","event":"skipped","artifact":"04-deliver.md","note":"<reason or \"none given\">"}`.

## Prerequisites

**Part of a workflow.** This skill is phase 4 (Deliver) of the Double Diamond workflow (`research`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `research` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"research-deliver","workflow":"research","phase":4,"project":"<project>","event":"refused","artifact":"04-deliver.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"research-deliver","workflow":"research","phase":4,"project":"<project>","event":"started","artifact":"04-deliver.md","note":""}`.

Read `.singularskills/research/<project>/01-discover.md`, `.singularskills/research/<project>/02-define.md`, and `.singularskills/research/<project>/03-design.md`.

If `03-design.md` does not exist, tell the user:

> Phase 3 (Design) has not been completed for "<project>". Run `/research-design <project>` first, or use `--skip-checks` to bypass.

## Process

1. **Read all prior artifacts:**
   - Read `.singularskills/research/<project>/01-discover.md` for original research
   - Read `.singularskills/research/<project>/02-define.md` for problem statement and success criteria
   - Read `.singularskills/research/<project>/03-design.md` for recommended solutions and validation plan

2. **Validate the top solution(s):**
   - Use WebSearch to find evidence supporting or contradicting the recommended approach
   - Use WebFetch to read detailed case studies of similar implementations
   - Look for: success stories, failure modes, edge cases, unintended consequences
   - Test each assumption identified in the Design phase

3. **Assess against success criteria:**
   - Review each success criterion from the Define phase
   - For each criterion, document evidence that the solution meets it (or doesn't)
   - Flag any criteria that can't be validated with desk research alone

4. **Refine recommendations:**
   - Adjust the solution based on validation findings
   - Add implementation considerations discovered during validation
   - Identify quick wins vs. long-term investments
   - Note dependencies and prerequisites

5. **Write the artifact** to `.singularskills/research/<project>/04-deliver.md` with sections:
   - **Executive Summary** — one-paragraph recommendation
   - **Validation Findings** — evidence for/against the solution, organized by assumption
   - **Success Criteria Assessment** — each criterion with evidence status
   - **Final Recommendation** — refined solution with implementation approach
   - **Action Items** — prioritized next steps with owners/timelines if applicable
   - **Risks & Mitigations** — remaining risks and how to handle them
   - **Research Journey** — brief timeline of what was discovered across all 4 phases

## Output

The final deliverable written to `.singularskills/research/<project>/04-deliver.md`. Present a summary to the user highlighting:
- The final recommendation (1-2 sentences)
- Confidence level based on evidence strength
- Top 3 action items
- Key risks to watch

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"research-deliver","workflow":"research","phase":4,"project":"<project>","event":"finished","artifact":"04-deliver.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: research-deliver
workflow: research
phase: 4
project: <project>
started: <ISO timestamp>
finished: <ISO timestamp>
agent: <the agent you run in, or "unknown">
gate: <passed|skipped>
---
```

End the artifact with `## Decisions` and `## Open questions`, in this shape:

```markdown
## Decisions
- <what was chosen> — <why> — <what was rejected>

## Open questions
- <what the next phase or a reviewer must settle>
```
