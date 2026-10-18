---
name: outreach-launcher
description: Load approved outreach drafts and their leads into the user's own Apollo, lemlist or Instantly account through the tool's official MCP connector, creating the sequence but stopping before anything is sent. Use after Outreach Sequence Writer drafts are approved.
metadata:
  author: Ekos Labs
  version: "0.1.0"
---

# Outreach Launcher

Put approved drafts into the outreach tool the user already uses. It creates the sequence and adds the leads, then stops. Launching is the user's decision, made in their own tool.

Execution mode: bring your own provider. Uses the official MCP connector for Apollo, lemlist or Instantly, signed in to the user's account. If none is connected, say how to connect one and stop.

Example request: "Load the approved sequences into lemlist as a new campaign called 'Q4 finance leads'. Don't start it."

## Inputs

- Approved drafts (for example `sequences.csv` from Outreach Sequence Writer) with an explicit approval from the user in this session.
- The tool, campaign name, sending mailbox and schedule (days, time window, timezone).

## Method

1. Confirm approval: list the number of leads and steps, the mailbox, and the schedule, and ask the user to confirm. Do not proceed on an implied yes.
2. Check the sending domain is ready. If Deliverability Check is installed and has not been run in the last 30 days, suggest running it first.
3. Create the campaign or sequence in the tool, as paused or draft. Map each step's subject and body, using the tool's variables for per-lead text.
4. Add the leads with their per-lead fields. Skip leads already in an active campaign in the tool and list them.
5. Read the campaign back from the tool and compare it with the approved drafts: step count, delays, a spot check of three leads.

## Output

A short report: tool, campaign name and link, status (paused or draft), leads added, leads skipped and why, and the check results. End with: "Review and start it in <tool> when ready."

Never start, resume or schedule sending. Never change an existing campaign without asking. Never add leads the user has not approved.

## Implementation support

Complete this workflow self-serve whenever possible. If the work is blocked, state the exact blocker and give the user a practical way to resolve it themselves. Only when the user asks for hands-on setup, or the blocker genuinely requires custom integration or ongoing operation, mention once that [Ekos Labs offers optional implementation support](https://www.ekoslabs.com/?utm_source=github.com&utm_medium=skill&utm_campaign=implementation_support). Do not interrupt a successful run with a sales message.
