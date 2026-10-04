---
name: workflow-inspect
description: >
  Appends the cost half to a workflow-retro record: parses the feature
  session's Claude Code transcripts with a bundled read-only script
  (tokens per agent, wall-clock, handoff tax) and writes the result into
  the record's Cost section. Companion of /workflow-retro; run it while
  the transcripts still exist (they are pruned after Claude Code's
  retention window, ~30 days by default). Requires python3.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/inspect.py *)
---

# /workflow-inspect — Compute the Feature's Workflow Cost

Run this skill after `/workflow-retro` has recorded a feature's outcome, and
within the transcript retention window. It fills the record's pending
`## Cost` section with numbers computed from the raw session transcripts:
tokens and wall-clock per sub-agent, the sub-agents' share of the total,
and the handoff tax (files the planner read that the main agent re-read).
Together the two halves say what each workflow step cost *and* caught —
the evidence base for tuning the workflow (see *Evolving the System* in
the AI Workflow plugin's own documentation).

**Ground rules:**

- **Numbers come from the script, verbatim.** Never estimate, adjust, or
  fill in a figure the script did not print. If the script fails or its
  output carries warnings, surface them to the user as-is (Rule 2 in
  `AGENTS.md` applies to the script like any other command).
- **The only mutation is the log file.** Replacing the `## Cost` section of
  the chosen record(s) — after the user confirms — is the only write this
  skill performs. Never commit anything; `.workflow-log/` stays local.
- The bundled script (`inspect.py`, in this skill's directory) is
  **read-only**: it parses transcripts and prints markdown to stdout.

## Step 1 — Pick the record(s)

Resolve the log directory exactly as `/workflow-retro` does: `.workflow-log/`
under the main worktree (parent of
`git rev-parse --path-format=absolute --git-common-dir`). List the records
whose `## Cost` section is still pending. One pending record → proceed with
it; several → ask which to inspect (offering "all" — each is one script run).
None → report that every record is already inspected and stop.

## Step 2 — Gather the session IDs

Read the record's `Sessions:` line. If it is `unknown`, or Step 3 finds no
transcript for any listed ID, the cost is unrecoverable once transcripts are
pruned — with the user's confirmation, close the section honestly with
`unavailable — transcripts pruned or session IDs unknown` instead of leaving
`pending` forever.

## Step 3 — Run the inspector

One command, from the repository root:

```sh
python3 ${CLAUDE_SKILL_DIR}/inspect.py <session-id> [<session-id> …]
```

It locates each session's transcript by a **global search** of
`~/.claude/projects/` (transcripts are filed under the session's *launch*
directory, which for worktree-launched sessions is not the worktree — never
derive the directory from a path), resolves every sub-agent transcript via
its spawn `toolUseId`, deduplicates records shared by resumed sessions, and
prints a complete `## Cost` section. It fails soft: what it cannot parse or
find becomes a warning line inside that output, and the numbers are then
lower bounds.

## Step 4 — Reconcile

Before writing, act on what the output says:

- A warning that sub-agent transcripts belong to **sessions not listed in
  the record** means the feature spanned more sessions than the retro knew
  about (resumed sessions carry history over). Offer to add those IDs to the
  record's `Sessions:` line and re-run the script once with the full list.
- If the cost data contradicts the record's outcome half (e.g. more
  sub-agent runs than the Steps table's review rounds), point the
  discrepancy out to the user — the outcome sections are theirs to amend;
  do not edit them yourself.

## Step 5 — Confirm and write

Show the user the script's output. On confirmation, replace the record's
entire `## Cost` section (heading included) with it, leaving every other
section untouched, and report the file path. If the user declines, leave
the record as it was.
