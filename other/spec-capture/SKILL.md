---
name: spec-capture
description: >
  Save what this chat session found out into the project's memory (specs/CONTEXT.md and
  context/AREA.md) when the work happened outside a spec, then refresh GitRisk. Use when the
  user says "capture this", "save what we learned", "update the context from this chat",
  "remember this for the project", "/spec-capture", or at the end of an ad-hoc investigation or
  bug hunt done in plain chat. Only confirmed findings about the repos or packages configured in
  .spec-driven.yml are saved, and only after the user says yes. Does not commit (use
  spec-checkpoint) and does not create the context (use spec-setup).
license: MIT
---

# Capture

Chat investigations ("why does this fail?", "where is X computed?") hold verified findings, but
checkpoint only saves context for spec work. This skill saves them to the project's memory with
the same rules, only after the person says yes.

## Project config (read first)

Load `.spec-driven.yml`: walk up from the current directory to the home folder, and the first one
found wins (a `multi-repo` config only applies inside the repos it lists). If none is found, check
`~/.spec-driven/workspaces.json`, which maps each multi-repo config to its repo paths. Use the
config whose repos contain the current directory. Its values beat anything you would detect or
assume. If `{specs_dir}/team.yml` exists, it holds the team's shared rules: read it first, and let
`.spec-driven.yml` override it. This skill uses `layout`, `repos`, `specs_dir` and `risk.enabled`.

**No config?** Stop. Say: "This project has no .spec-driven.yml; say 'run spec-setup' first."

The context rules are in references/context-template.md inside the installed `spec-setup` skill
folder. Read it before writing anything.

## Step 1: Gather candidates from this session only

1. Go back through this conversation: files read and what they showed, commands run and their
   output, tests, the conclusion reached, conventions or pitfalls found, where things live, and
   decisions the person stated.
2. Run `git status --short` and `git diff --stat` in each configured repo, so you know which
   areas changed.
3. Never read other sessions' transcripts, `~/.claude/projects`, or any other chat history.

## Step 2: Keep only confirmed, lasting findings

1. For each candidate, write down its evidence: a `path:line` you read, output you saw, a test
   result, or "you told me".
2. Drop routine progress, guesses, hypotheses never checked, anything contradicted later in the
   session, one-off data values, and anything secret or personal (customer names, emails, keys).
3. Keep what a future change in the same area needs: the cause of a bug and where the real fix
   belongs, conventions, off-limits areas, pitfalls, "X is computed in Y".
4. List the tempting ones you dropped as **Not saved (unconfirmed)**, each with the reason.

## Step 3: Check scope

1. Collect every path each finding names. Run `spec-driven-dev scope <paths...> --json` once.
2. A finding with any path that is not `in` is not written. List it under **Not saved (outside
   configured repos)** with the path and the reason. Paths inside `{specs_dir}` are out.
3. A finding with no path is kept only if it is about an area already in CONTEXT.md's **Areas**
   table.
4. If the CLI is not installed, apply the same rule by hand from `.spec-driven.yml` and say
   "scope checked by hand".

## Step 4: Place each finding

1. Read CONTEXT.md and only the `context/<area>.md` files the findings touch.
2. Pick the area by its **Where** paths. Add a new area only for a folder inside scope that holds
   a real area (not a single helper), and add its row to **Areas**.
3. Skip anything already recorded.
4. If a finding contradicts an existing entry, show both under **Conflicts**. Do not rewrite. The
   person decides.
5. Tag each line `(YYYY-MM-DD, chat)`, or `(YYYY-MM-DD, you told me)` for the person's own
   statements. Add a short subject so it can be traced, for example
   `(2026-11-20, chat: login 500 for stale client)`.
6. Keep the size limits (index 60 lines, area 150): merge duplicates and move superseded lines to
   `context/archive.md`.

## Step 5: Show and confirm

1. Print a table: file, section, new line.
2. Print the three lists: **Not saved (unconfirmed)**, **Not saved (outside configured repos)**,
   **Conflicts**.
3. Ask "Save these? (yes / drop N / edit N)". Write nothing until the answer is yes.
4. No CONTEXT.md? Print what would be saved, suggest `spec-setup` to create the context, and stop.
   Do not create CONTEXT.md yourself.

## Step 6: Write

Append each line at the end of its section exactly as shown. Do not reorder or reformat existing
lines. Never touch the block between `<!-- risk:start -->` and `<!-- risk:end -->`.

## Step 7: Refresh GitRisk

1. If `risk.enabled` is on or absent, and `spec-driven-dev` is on PATH, run `spec-driven-dev risk`
   (it scores only the configured repos) and quote its hotspot summary line.
2. Do this even when nothing was saved, if code changed in this session.
3. Never stage `context/risk.md`.
4. If risk is off or the CLI is missing, say so in one line.

## Step 8: Report

Say what was saved (count per file), what was not and why, and the GitRisk line. End with:
"Next: spec-checkpoint to commit (the context lives in {specs_dir}, which may be its own repo)."
Never stage, commit or push.

## Rules

- Use this session only.
- Save confirmed findings only.
- Write about configured repos and packages only.
- Write nothing before a yes.
- Never stage, commit or push.
- Never edit the risk block.
- No secrets or personal data.
- The code wins: report conflicts, never rewrite to match a guess.
