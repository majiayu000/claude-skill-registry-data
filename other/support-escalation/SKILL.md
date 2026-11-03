---
name: support-escalation
description: Define support escalation — tiers, the triggers that move a ticket up by priority and category, handoffs to engineering, billing, account management and security, and how the customer is kept informed meanwhile. Use when the user needs to decide who takes a ticket the first agent cannot solve. Not for responding to a security incident itself; see /security-incident-response.
metadata:
  argument-hint: "[project] [--skip-checks]"
  workflow: support
  phase: 5
  artifact: 05-escalation.md
---

# Escalation

Define who handles what for "$ARGUMENTS", when a ticket moves to someone else, what it must carry when it does, and what the customer hears while it is away.

**Arguments.** `$ARGUMENTS` may contain the project name and optional flags. Take the first token as `<project>` and treat `--skip-checks` as a flag; never include flags in file paths. All paths below use `<project>`. If `--skip-checks` is present, skip the prerequisite check and, **before writing any artifact**, append one line to `.singularskills/log.jsonl`: `{"ts":"<ISO timestamp>","skill":"support-escalation","workflow":"support","phase":5,"project":"<project>","event":"skipped","artifact":"05-escalation.md","note":"<reason or \"none given\">"}`.

**Compute with code.** Perform every calculation (totals, balances, ratios, variances, projections) with a script — Bash, Python or a spreadsheet formula written to a file — and include the computation alongside the result. Never do arithmetic mentally.

## Prerequisites

**Part of a workflow.** This skill is phase 5 (Escalation) of the Support Operations Cycle workflow (`support`); cross-domain workflows run it too. First check `.singularskills/log.jsonl` for an open run for this project: a `run-started` line with `"project":"<project>"` and no later `run-finished` line for the same `workflow` and `project`. If one exists, the conductor is running you: continue here. Otherwise, if the user asked to start, run, continue or resume a process or workflow rather than this one step, do not continue here: invoke the `workflow` skill with the workflow the user asked for, or `support` when they named none, followed by `<project>`; it runs this phase in order, asks before it writes and records the run. Otherwise continue here: a later phase runs on its own, behind its gate.

Run this skill's gate before writing: `sh <this skill's folder>/scripts/gate.sh <project> <project root>`, where `<project root>` is the folder that contains `.singularskills/` (use `.` when you are already there). If it exits non-zero, stop and tell the user what it printed, unless `--skip-checks` was given (see Arguments). On a refusal, before you stop, append this line to `.singularskills/log.jsonl` (create the folder and file if missing): `{"ts":"<ISO timestamp>","skill":"support-escalation","workflow":"support","phase":5,"project":"<project>","event":"refused","artifact":"05-escalation.md","note":"<what the gate printed>"}`. Once the gate has passed, or under `--skip-checks` once you have appended the `skipped` line, append this line before you start work: `{"ts":"<ISO timestamp>","skill":"support-escalation","workflow":"support","phase":5,"project":"<project>","event":"started","artifact":"05-escalation.md","note":""}`.

Read `.singularskills/support/<project>/02-taxonomy.md` for the categories and the P1 to P4 priorities.

## Process

1. **Ask the user about the team:** who answers tickets today, which teams exist beyond support (engineering, billing, account management, security, legal), how each prefers to receive work (a queue, a channel, an issue tracker), and who is on call outside hours.

2. **Define the tiers:** what tier 1 resolves alone, what tier 2 (specialists or senior agents) takes, and what leaves support. For each tier, the categories it owns and what it may decide.

3. **Set the escalation triggers** as a table of priority × category: when a ticket must move, to whom, and how fast. Include the triggers that apply to any category: the customer asks for a manager, the customer threatens to leave or take legal action, the same customer contacts support a third time about the same problem, or the agent has no answer after a set time.

4. **Define each handoff** with what the ticket must carry:
   - **Engineering:** steps to reproduce, expected and actual behaviour, the account's plan and environment, how many customers are affected, and the ticket links — never the customer's personal details beyond what reproducing needs.
   - **Billing:** the charge, the date, what the customer expected, and the policy line from `04-macros.md` if one applies.
   - **Account management:** the account's value and renewal date if the user tracks them, and the history of recent contacts.
   - **Security:** any ticket suggesting account takeover, unauthorised access, data exposure or a breach goes to the security contact at once, and the incident is handled with `/security-incident-response`; the agent tells the customer only what the security contact approves.

5. **Keep the customer informed:** for each handoff, what the agent tells the customer at the handoff, how often they get an update while the ticket is away (in line with `references/service-recovery.md`: always say when the next update comes), and who owns the reply when the ticket comes back.

6. **Write the artifact** to `.singularskills/support/<project>/05-escalation.md` with sections:
   - **Tiers** — what each tier owns and may decide
   - **Triggers** — the priority × category table and the general triggers
   - **Handoffs** — each team, its route and what a ticket must carry
   - **Customer updates** — what the customer hears, and how often
   - **On call** — who covers outside hours

## Output

The escalation paths written to `.singularskills/support/<project>/05-escalation.md`. Present a summary to the user highlighting:
- The tiers and what leaves support
- The P1 escalation route and its speed
- What a bug report to engineering must contain
- Any team or on-call gap the user has not filled

**Record the run.** After you have written the artifact, append this line to `.singularskills/log.jsonl` (the `started` line of Prerequisites, with `"event":"finished"`): `{"ts":"<ISO timestamp>","skill":"support-escalation","workflow":"support","phase":5,"project":"<project>","event":"finished","artifact":"05-escalation.md","note":""}`.

Open the artifact with this frontmatter (`agent` is the agent you run in, or `unknown`; `gate` is `passed` when the gate ran clean and `skipped` under `--skip-checks`):

```yaml
---
skill: support-escalation
workflow: support
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
