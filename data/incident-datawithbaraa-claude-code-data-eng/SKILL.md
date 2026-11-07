---
name: incident
description: Use when a job run failed with an error, to walk the incident from the error to the root cause, the workaround, two solutions, the future risks, the email drafts and the log entry.
argument-hint: "[date or run]"
---

# Incident

The job: from the first error to the log entry. It proposes and drafts. It never fixes and never sends.

Input: the date of the failed run, or the job and its run.

## Steps

1. Where it failed: the job, the task, the file and line, and the error message.
2. Status: the severity, the impact on the consumers, and the next step.
3. What happened: the run layer by layer, with each check and its result.
4. Root cause: what changed, with the rows before and after.
5. Seen before: check the incident log for the same kind of failure and its known fix.
6. Workaround: how the consumers get fresh data today.
7. Solutions: 2 options with the effort of each, and which one to recommend.
8. Future risks: every table with the same weakness, and which ones are safe.
9. Email drafts: one to the consumers and one to the source owner.
10. Log entry: draft it for the incident log, and write it after the yes.
11. Give the result as one web page.

## Output

One HTML file, like [references/incident.html](references/incident.html): the title with the severity, the layers with the failed task, where, when and the status, the error message, then one section per step. Read it for the layout before you write the page.

## Reads

- the run records, the check results, the quarantine, the delivered files, the pipeline code, the incident log

## Writes

- the web page, and one entry in the incident log after the yes

## Never

- Never fixes anything, never reruns a job, never sends an email.
