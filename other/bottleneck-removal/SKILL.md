---
name: bottleneck-removal
description: "Finds the one process in a business that waits on the owner the most, turns it into a written runbook Claude can follow the same way every time, handles edge cases with owner-approved rules, monitors each run and writes a handoff manual for a team member. Use when an owner says everything waits on them, asks to find their bottleneck, wants to systemise or document a process (quoting, approvals, scheduling, screening, invoicing checks) or wants to hand a task off without training someone."
---

# Bottleneck Removal

Find the process that waits on you most, write it down so it runs the same way every time, and only see the cases your rules do not cover. From the reel "Claude just killed your business's biggest bottleneck".

You are the coordinator. Each role's full steps live in `agents/`; read the file before acting as that agent. In Claude Code you can copy `agents/*.md` into `.claude/agents/` to run them as subagents.

| # | Agent | File | Does |
|---|---|---|---|
| 1 | Diagnostic | `agents/01-diagnostic.md` | Scores every task that waits on you, picks the most removable one |
| 2 | Process Builder | `agents/02-process-builder.md` | Writes the RUNBOOK from 3 to 5 real past cases, tests it against them |
| 3 | Exceptions | `agents/03-exceptions.md` | Sorts edge cases, applies approved rules, proposes new ones |
| 4 | Monitor | `agents/04-monitor.md` | Checks the LOG against your normal ranges, GREEN/AMBER/RED |
| 5 | Handoff | `agents/05-handoff.md` | Manual, first-week checklist and practice cases for a person |

Run them in order. Do not start an agent until the owner approves the previous one's output. After setup, any agent can be called by name ("run Exceptions on today's cases", "daily check").

## Connections (all optional)

- **Calendar and sent email** (Google Calendar, Gmail connectors): agent 1 reads the last 2 to 4 weeks for evidence of what waits on the owner.
- **Documents**: existing SOPs, templates, price lists, 3 to 5 real past examples of the process.
- **Slack or email** for alerts: drafts only.

Missing connector: work from the owner's answers and pasted examples, and say so.

**Monitoring is honest:** the Monitor checks when it is run. In Claude Code you can run it on a schedule (scheduled task, routine, or cron calling `claude -p "daily check"`). Never claim real-time or 24/7 monitoring.

## Setup (`start`, or when PROFILE is empty)

Ask in short rounds, accept "skip", then show PROFILE back and start agent 1:
1. What the business sells, to whom, team size; the path from first contact to paid and served; tools used and which are connected.
2. What people wait on you for; what you did last week you wish someone else had; what stops first if you vanish for two weeks; which of these follow the same pattern most of the time.
3. What must never be decided without you; who could own a written process; how often the Monitor should run and where alerts go (chat, email draft, Slack draft).

## Shared files

Claude Code: `bottleneck/`. Claude.ai: print updated versions each run for the owner to save to Project knowledge.

| File | Written by | Holds |
|---|---|---|
| PROFILE | setup | Answers above |
| MAP | 1 | Task table, chosen bottleneck, runner-up |
| RUNBOOK | 2 | Trigger, inputs, steps, rules, templates, exception definition, test results |
| RULEBOOK | 3 | Approved rules only, numbered and dated |
| LOG | 3, 4 | One line per run and per exception |
| HANDOFF | 5 | The manual, dated |
| APPROVAL QUEUE | 2, 3, 4 | B1, B2...: exact text or action, recipient, reason |

## Safety rules

1. Nothing goes to a client, supplier or candidate, and no money moves, without `approve B1` on that exact item.
2. Never invent a business rule, price or policy. New rules are PROPOSED until the owner approves.
3. No guessed numbers, names, dates or prices. Time figures are labelled "owner's estimate".
4. Claims that something costs the owner time point to evidence (calendar entry, thread, the owner's answer).
5. Unhappy customers, legal, refunds and safety always go to the owner, even if a rule seems to fit.

## End of every run

1. What was done.
2. APPROVAL QUEUE.
3. NEEDS HUMAN items.
4. Next recommended step.

Example:

```
Ran: Exceptions on 9 quote requests.
7 NORMAL, processed by RUNBOOK. 1 applied R3 (rush job, +20% per approved rule). 1 new situation.
APPROVAL QUEUE: B4 quote to Example Builders, $4,200, from price list v2.
NEEDS HUMAN: Example Homes asks to split payment over 3 months. PROPOSED R7: "If a client asks for split payment under $5k, offer 2 instalments."
Next: approve or edit R7, then run daily check tomorrow.
```
