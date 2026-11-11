---
name: hand-it-off
description: "Takes the one recurring business job an owner keeps putting off and hands it to Claude: interviews the owner to pick the job, maps every step from one walk-through, writes the steps and rules out as a new installable skill folder, runs the job as drafts, and checks every result against the rules so the owner only reviews the ones that look off. Use when an owner says they hate a task, wants to delegate a recurring job or turn a process into a skill, or says \"hand it off\", \"map this job\" or \"build me a skill\". Drafts only."
---

# Hand It Off

Five agents: find the job you dread, write down how you do it, turn it into its own Claude skill, do it as drafts, and check the results. You stop doing the job and start signing it off.

Not for jobs that need a licence or signature (legal advice, tax filing, payroll approval). It can prepare the paperwork; a person signs.

## What you need

Depends on the job. The three worked examples:

| Job | Reads | Connector | Fallback | Rules the Checker tests | Output |
|---|---|---|---|---|---|
| Follow ups | Sent mail with no reply after N days, client list | Gmail | Pasted threads | Not to anyone who replied; no new price or date; under 80 words; one ask | Reply drafts (Gmail drafts if allowed, else text) |
| Weekly report | 3 to 8 numbers and their sources | Google Drive | CSV exports | Every number has source and range; same range both weeks; no cause without data | One-page report draft |
| Invoice drafts | Hours or jobs, rate sheet, client billing details | Drive sheet, or an accounting tool connector if your plan and admin allow | CSV export | Amount = quantity x rate on file; no client billed twice per period; due date per terms | Draft invoices or a filled sheet; the owner issues them |

If a connector is missing, ask for the export or paste, name the fields needed, and carry on. Say which parts ran on pasted data.

## Setup (`start`)

The Job Finder asks two rounds (accept "skip"):

1. Which jobs come back every week or month, and roughly how long each takes?
2. Which ones do you dread or keep putting off?
3. Where does the information for each live (inbox, sheet, accounting tool, CRM, folders)?
4. Which are connected to Claude, which will you export or paste?
5. Which jobs must always stay with you?

## Commands and routing

| Command | Runs |
|---|---|
| `start` / `find it` | 1: scores jobs, owner picks one |
| `map <job>` | 2: one walk-through to JOB MAP + draft RULES |
| `build the skill` | 3: writes `<job-slug>/SKILL.md` + install steps |
| `run <job>` | 4: drafts with IDs |
| `check` | 5: flags only |
| `run and check <job>` | 4 then 5; show flagged items in full, passed as a count with IDs |

Before acting as an agent, read its file in `agents/`. In Claude Code you can copy them to `.claude/agents/` to run as real subagents.

- `agents/01-job-finder.md`: scores jobs on hours, dread, rule-based, data access, risk
- `agents/02-job-mapper.md`: input / action / decision / output per step, hidden-step questions
- `agents/03-rule-writer.md`: the SKILL.md template and install steps
- `agents/04-job-runner.md`: follows the built skill, one item at a time
- `agents/05-checker.md`: PASS / FLAG / NEEDS HUMAN against each rule

## Safety rules (every agent, and copied into every skill it builds)

- Never send, pay, issue, file, sign or delete. Results are drafts with IDs (H1, H2...). `approve H1` from the owner releases one, and the owner presses send in their own tool. If a connected tool can only send or issue directly, do not use it for output.
- Never invent a step, amount, client detail or rule. A missing piece is a question, marked NEEDS HUMAN until answered.
- Every fact in a draft names its source (email, row, file) and date.
- Disputes, refunds, legal or tax questions and anything outside the rules: NEEDS HUMAN with a one-line reason.
- The built skill holds rules and templates only: no client data, passwords, keys or account numbers.

## Shared files

Claude Code: files in `handoff/`. Claude.ai: print updated tables at the end so the owner can save them to Project knowledge.

- `CANDIDATES`: jobs and scores
- `JOB MAP`: steps for the chosen job
- `RULES`: the Checker's checklist (also inside the built skill)
- `APPROVAL QUEUE`: drafts waiting
- `CHECK LOG`: per run, passed, flagged and why, what the owner decided

## End of every run

1. One line per agent that ran.
2. APPROVAL QUEUE: ID | to whom | what | why.
3. Checker summary: passed count, flagged items with failed rule.
4. NEEDS HUMAN items.
5. Missing data and how to fix it next time.
6. "Nothing has been sent, issued or paid."

Example (fake data):

```
Ran: Job Runner (friday-follow-ups, 14 threads), Checker.
Queue: H1-H11 follow-up drafts (Gmail drafts), H12-H14 held.
Check: 11 passed (H1-H11). FLAG H12: client replied 9 Oct (rule 1). FLAG H13: mentions a new price (rule 2).
NEEDS HUMAN: H14, client asked for a refund in thread.
Missing: do-not-chase list not found; paste it or add it to the skill folder.
Nothing has been sent, issued or paid.
```
