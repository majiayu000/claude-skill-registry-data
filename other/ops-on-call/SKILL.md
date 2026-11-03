---
name: ops-on-call
description: Set up on-call for a service — the rotation, primary and secondary, the handoff checklist, severity levels, incident roles, the escalation path, and load limits on pages per shift with recovery after a heavy one. Use when a team is starting on-call or its current rotation is burning people out. Not for a security incident response plan; see /security-incident-response.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: ops
  phase: 5
  artifact: 05-on-call.md
---

# On-call

Set up on-call for "$ARGUMENTS" so pages get answered and people stay well.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"ops-on-call","workflow":"ops","phase":5,"project":"<project>","event":"skipped","artifact":"05-on-call.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 5 (On-call) of the Reliability Cycle workflow (`ops`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `ops` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ops-on-call","workflow":"ops","phase":5,"project":"<project>","event":"refused","artifact":"05-on-call.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"ops-on-call","workflow":"ops","phase":5,"project":"<project>","event":"started","artifact":"05-on-call.md","note":""}`.

Read `.singularskills/ops/<project>/03-alerting.md` for the pages and expected load and `.singularskills/ops/<project>/04-runbooks.md` for the runbooks.

## Process

1. **The rotation:** who is in it (roles or teams), shift length, hours covered, primary and secondary, and how swaps work. Ask once for team size and time zones.

2. **The handoff checklist** at every shift change: what is muted and why, and until when; risky changes in flight; open incidents and their state; anything the next person should watch.

3. **Severity levels** (SEV1 to SEV3 or P1 to P3): each with a test a responder can apply ("users cannot check out"), who is paged, and how fast.

4. **Incident roles:** incident commander, operations and communications, who takes each by default (the primary on call is incident commander until someone else is), and when to hand over.

5. **Escalation:** from primary to secondary to the owning team's lead, with times; the security contact when it may be a breach (`/security-incident-response`); customer communication with `/support-incident-update`.

6. **Load limits:** a target of no more than 2–3 actionable pages per 12-hour shift (`target`), what happens when a shift exceeds it (the alert gets reviewed), and recovery time after a heavy or overnight shift.

7. **Write the artifact** to `.singularskills/ops/<project>/05-on-call.md` with sections **Rotation**, **Handoff checklist**, **Severities**, **Roles**, **Escalation** and **Load limits**.

## Output

The on-call setup written to `.singularskills/ops/<project>/05-on-call.md`. Present a summary to the user highlighting:
- The rotation and who is in it
- The handoff checklist
- The load limit and what happens when it is exceeded

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"ops-on-call","workflow":"ops","phase":5,"project":"<project>","event":"finished","artifact":"05-on-call.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: ops-on-call
workflow: ops
phase: 5
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
