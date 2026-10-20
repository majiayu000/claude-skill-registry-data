---
name: rca
owner: baseline
description: Draft a Root Cause Analysis for an incident, outage, or repeated test failure. Unlike intake/spec/brd, RCA is not a workflow phase — it's a standalone postmortem artifact that often precedes a bugfix intake. Output lives at `docs/rca/<slug>.md`.
---

# RCA — Root Cause Analysis

You are drafting an **RCA**. It is a narrative of what went wrong, why, and what will change so it doesn't recur. Unlike the other artifact skills in this workflow, RCA is **not** part of the linear phase chain — it's a separate document that often feeds into a bugfix intake (`/triage` → `/intake` → …).

**Use an RCA when:**
- A production incident occurred (outage, data corruption, security breach).
- A test that previously passed now fails intermittently and the cause is non-obvious.
- A `verify` skill verdict has been `FAIL` across multiple attempts and the team needs a blameless record.
- The user explicitly says "postmortem", "RCA", "incident review", or equivalent.

**Don't use an RCA for:** a bug reported in a ticket, a missing feature, or a normal TDD failure. Those belong in intake/spec/tdd.

## Inputs

- The incident's observable facts: timeline, alerts, logs, user reports, metrics screenshots (paths or URLs).
- The commits, deploys, or config changes in the suspect window.
- `template.md` in this skill directory.

## Steps

1. Read `template.md`. Every heading must appear in the output.
2. Assemble the **Timeline** from raw evidence (logs, alert history, chat transcripts, deploy log). Wall-clock times in a single timezone. Do NOT paraphrase events — record what happened.
3. State the **Root cause** as a single sentence. If you have multiple candidate causes and cannot distinguish them from the evidence, list them under **Contributing factors** and put "not conclusively identified" as the Root cause. Do not guess.
4. **Impact must be quantified.** Users affected: count or estimate with method. Duration: precise. Business impact: dollars, SLA minutes, or "none measurable" — never a vague "significant".
5. **Action items have owners and due dates.** Unassigned action items are placeholder; delete them or assign.
6. Write to `docs/rca/<slug>.md`. Slug: `YYYY-MM-DD-<short-name>` so the file sorts chronologically in the directory.
7. Tell the user: "RCA drafted at `docs/rca/<slug>.md`. Action items: N, owners assigned: M. If this warrants a fix, run `/triage` with a bugfix description referencing this RCA."

## Drafting rules

- **Blameless.** Describe what a system or process allowed, not who is at fault. "The deploy ran without a staging rehearsal" — not "Alice deployed without testing".
- **Evidence links trump prose.** Where possible, cite the log line, the commit SHA, the dashboard URL. Prose that isn't traceable is speculation.
- **What went well matters.** Most RCAs omit this. Include it — it reinforces practices that should persist.
- **Action items are specific.** "Improve monitoring" is not an action item; "Add alarm on upstream 5xx rate > 1% for 2m, paging to #oncall-payments, owner: Priya, due 2026-05-15" is.
- **Do not self-commit to a timeline you can't honor.** If action item ETAs are uncertain, mark them "tentative".
- **Don't mix RCA and spec.** The RCA says what broke and why. The fix spec (separate, via `/spec`) says how to repair it.
