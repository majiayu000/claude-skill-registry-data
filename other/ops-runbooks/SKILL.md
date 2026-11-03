---
name: ops-runbooks
description: Write runbooks for a service — one per paging alert plus the common incident types — each a checklist of is-this-real checks, mitigations as commands with expected output, impact and rollback, and when to escalate, with every step that changes production marked. Use when the people on call need steps they can follow at 3am. Not for a security incident playbook; see /security-incident-response.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: ops
  phase: 4
  artifact: 04-runbooks.md
  stack-aware: true
---

# Runbooks

Write what the person paged for "$ARGUMENTS" follows, as `references/incidents.md` describes: a checklist, not a manual.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"ops-runbooks","workflow":"ops","phase":4,"project":"<project>","event":"skipped","artifact":"04-runbooks.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 4 (Runbooks) of the Reliability Cycle workflow (`ops`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `ops` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

**Stack.** Before you build, test, lint, run or generate code, read the `Stack` section of the project's `AGENTS.md`, or of `CLAUDE.md` when `AGENTS.md` has none. Use its commands exactly as written, its `layout` for where files go and its `rules` as requirements. If it names a `profile`, also read the file `<profile>.md` in the `stacks` folder of this skill's bundled references for the full commands, layout and rules; the project's own keys win where both speak. If there is no `Stack` section, run the `singular-detect` skill, state what you inferred in one line, and offer to write the section with `singular-init`. Never assume a package manager, test runner or formatter the project did not declare.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"ops-runbooks","workflow":"ops","phase":4,"project":"<project>","event":"refused","artifact":"04-runbooks.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"ops-runbooks","workflow":"ops","phase":4,"project":"<project>","event":"started","artifact":"04-runbooks.md","note":""}`.

Read `.singularskills/ops/<project>/03-alerting.md` for the paging alerts and their runbook names. Read `.singularskills/ops/<project>/01-inventory.md` for the **Tooling** section and the services, when it exists.

## Process

1. **Choose the runbooks:** one per paging alert in `03-alerting.md`, plus the five most common incident types the user names (ask once).

2. **Write each as three sections, in order:**
   - **Is this real?** How to confirm users are affected: the dashboard, the query, the expected and the alarming values.
   - **Mitigations.** Each step a copy-paste command in the tooling recorded under **Tooling**, with its **expected output**, its **impact** ("expect 30 seconds of 503s") and its **rollback**. Stabilise first: roll back the last deploy, fail over, shed load or disable a feature before diagnosing. Mark every step that **changes production**.
   - **Escalate.** When to stop and call someone, and who (a role or team).

3. **With the tooling unknown,** write the step in plain language and mark it **command to fill in**; never invent a command or a flag.

4. **Put architecture background last,** short, for the person who needs to understand before acting.

5. **Mark every runbook a draft** until the team has run it in an exercise, and say when it was last exercised; never claim a command was tested.

6. **Never touch live systems.** Do not run any command against a live system, and never say a command, alert or runbook was tested or verified; you write them for people to apply.

7. **Write the artifact** to `.singularskills/ops/<project>/04-runbooks.md` with one section per runbook, named as the alert names it.


## References

- `references/stacks/bun-react-ts.md` and `references/stacks/rust-gpui.md`: the shipped stack profiles

## Output

The runbooks written to `.singularskills/ops/<project>/04-runbooks.md`. Present a summary to the user highlighting:
- The runbooks written, and the paging alerts they serve
- Every step marked changes production
- Every command to fill in

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"ops-runbooks","workflow":"ops","phase":4,"project":"<project>","event":"finished","artifact":"04-runbooks.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: ops-runbooks
workflow: ops
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
