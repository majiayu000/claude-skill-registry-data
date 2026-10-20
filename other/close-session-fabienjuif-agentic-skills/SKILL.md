---
name: close-session
description: Wrap up a work session in one pass — find the issue-tracker tickets the session touched (Linear) and update them, or propose a new one when the work has none; mark the Slack threads that announced the session's merged PRs with a reaction (default :pr-merged:); run capture-docs on a fresh branch and open a docs PR; and clean up the scratch data the session left behind (temp clones, extra git worktrees, merged local branches, background processes), then fast-forward each touched repo's main checkout. Gathers everything first, shows one plan, waits for a single go, then executes. Use when the user runs "/close-session", or says "close the session", "wrap up", "we're done, clean up", "end of session", "close this out".
---

# /close-session — wrap up a session

Four jobs, one confirmation:

1. **Tickets** — update the tickets this session worked on, or propose one when the work has none.
2. **Slack** — react on the thread that announced each merged PR.
3. **Docs** — run `capture-docs` on a fresh branch and open a docs PR.
4. **Cleanup** — remove the scratch data this session created.

The conversation is the primary source. Same rule as `capture-docs`: do not re-research the
codebase. Use cheap signals (`gh`, `git`, the MCP tools) to confirm state, never to rediscover the
session's work.

## Step 0 — Load config

Config file: `.claude/.config/close-session.json`. Walk up from the cwd to `$HOME` (inclusive),
first match wins; `$CLOSE_SESSION_CONFIG` overrides the walk. Every key is optional.

A job runs only when it is set up: **Tickets** needs a `linear` section and a tracker tool
connected, **Slack** needs a `slack` section and a Slack tool connected. **Docs** and **Cleanup**
always run. A job that does not run is silent: not gathered, not in the plan, not in the report,
no "skipped" or "not configured" line. Inside a running job, a missing key falls back to its
default (no `linear.team`: ask for a team only when a ticket is actually created).

```jsonc
{
  "linear": {
    "team": "ENG",                 // team key for new tickets
    "labels": ["platform"],        // labels every new ticket carries
    "doneState": "Done"            // state to propose when the work is finished
  },
  "slack": {
    "reaction": "pr-merged",       // emoji name, no colons
    "channels": ["#team-prs"]      // where PRs get announced; [] = search everywhere
  },
  "docs": {
    "prDraft": false,              // open the docs PR as draft
    "assignee": "@me"
  },
  "cleanup": {
    "tmpRoots": ["/tmp", "$TMPDIR"] // where session scratch clones live
  }
}
```

If a project's agent docs (CLAUDE.md / AGENTS.md / memory) define ticket, PR, or commit rules, those
rules win over this skill's defaults. Load any skill they name for ticket writing before a ticket
write.

## Step 1 — Gather (read-only)

Run the gathers of the jobs that run, in parallel. Nothing is written in this step.

**a) PRs of the session.** From the conversation: every PR opened, pushed to, reviewed-and-merged,
or merged this session. Confirm each with
`gh pr view <url> --json number,url,title,state,mergedAt,body,headRefName`. Keep the URL — every
later step keys on it.

**b) Tickets.** Collect ticket ids (`[A-Z][A-Z0-9]+-\d+`) from the conversation, the PR titles,
bodies, and branch names from (a). Fetch each (`get_issue`) for its state, assignee, and labels.
Map each ticket to the PRs and outcomes that concern it. Work with no ticket: search the tracker
first (`list_issues`, two or three keyword queries — feature name, component, error string). A
match becomes an update, not a new ticket. Only unmatched work becomes a creation proposal.

**c) Slack threads.** For each **merged** PR: search Slack for its URL (and `<repo>#<number>`
form), scoped to `slack.channels` when set. For each hit take the thread root (the message
itself if it has no parent). Read its reactions; drop roots that already carry the reaction. Open
or closed-unmerged PRs get no reaction.

**d) Scratch data.** Only what the transcript shows this session created:

- temp clones and worktrees under `cleanup.tmpRoots` (`git worktree list` in each repo touched)
- local branches whose PR merged (never the current branch, never the default branch)
- background processes the session started (port-forwards, dev servers, watchers) still running
- scratch files the session wrote outside the repo
- for each repo with a merged PR: its main checkout (first line of `git worktree list`), if it
  sits on the default branch, gets a `git pull --ff-only -p`

Before listing a path, check it: `git -C <path> status --short` — uncommitted changes or unpushed
commits (`git log @{u}..` or no upstream) mark it **dirty**. Dirty items are listed but never
deleted without an explicit per-item go. Never list the current working directory, the main
checkout, or anything the session did not create.

**e) Docs worth capturing.** Decide whether the session produced doc-worthy knowledge, using
`capture-docs` Step 1 rules. If not, the docs job is skipped.

## Step 2 — Plan and wait

Show one plan, grouped by job, every write spelled out:

```
Tickets
  ENG-123  comment: "Shipped in <PR link>: <one line outcome>"   state: In Progress → Done
  ENG-130  comment only (work continues: <what is left>)
  new      "<title>" — <~250-char body> — team ENG, labels [platform]   (searched: q1, q2 → no match)
Slack (:pr-merged:)
  #team-prs  <permalink>  → <PR link>
  skipped    <PR link> — no announcement found
Docs
  branch docs/<topic> from origin/<default> → capture-docs → PR "<title>"
Cleanup
  /tmp/repo-topic-1a2b  worktree, clean          remove
  feat/foo              local branch, PR merged  delete
  kubectl port-forward  pid 4242                 kill
  /tmp/repo-x-9f9f      DIRTY (2 unpushed)       keep unless you say so
  ~/repos/repo          main, 3 behind           pull --ff-only -p
```

Give a recommendation for each judgment call (state moves, new ticket vs comment) in one line.
Then **stop and wait for the user's go**. The user can drop or edit items ("go, skip the new
ticket"). A job with nothing to do is left out of the plan; if every job is empty, say so in one
line and stop.

## Step 3 — Execute

Run in this order. One failure does not stop the rest — record it and continue.

1. **Tickets.** Comments first, then state moves, then creations. On an update that sets labels,
   pass the existing labels too (many trackers replace the set). Link each PR to its ticket
   (attachment or link field) when the tracker supports it.
2. **Slack.** `slack_add_reaction` on each thread root. `already_reacted` counts as success.
3. **Docs.** Never in the current working tree — other sessions may share it.
   ```bash
   git fetch origin
   dir=$(mktemp -d "${TMPDIR:-/tmp}/<repo>-docs-XXXXXX")
   git worktree add "$dir" -b docs/<topic> origin/<default-branch>
   ```
   Run `capture-docs` with `$dir` as the repo root; it draws from this conversation, so the fresh
   branch is fine. If it reports "Nothing new to capture", remove the worktree and branch and
   mark the job skipped. Else commit (project's commit convention), push, and
   `gh pr create --assignee <docs.assignee>` (add `--draft` when `docs.prDraft`), with the
   project's PR template when one exists. Add the new docs worktree to the cleanup list.
4. **Cleanup.** `git worktree remove <path>` (no `--force` on a dirty one), `git branch -d`
   (lowercase `-d`: it refuses an unmerged branch — report it, do not escalate to `-D` without a
   go; squash-merged branches need `-D`, which the plan already showed), `kill <pid>`, `rm -r`
   only on paths in the approved list. Run `git worktree prune` once per repo touched.
5. **Main checkouts.** `git -C <main checkout> pull --ff-only -p` on each listed one, so `main`
   has every PR merged this session and deleted remote branches are pruned. It keeps the user's
   uncommitted edits; if it refuses (diverged, conflicting local edit), report it: never stash,
   reset or merge.

## Step 4 — Report

Outcome first, a few lines, only for jobs that ran and did something:

- tickets updated / created, as links
- threads reacted, as permalinks; PRs with no announcement found
- docs PR link, or "no docs to capture"
- what was removed, what was kept and why (dirty, refused `-d`)
- main checkouts fast-forwarded (old..new), or why one refused
- every failure with its error

## Rules

- **One gate.** Nothing writes before the go in Step 2. Reads are free.
- **Quiet when not set up.** An unconfigured job is never mentioned, in the plan or the report.
- **Only this session's footprint.** Tickets, threads, and scratch data trace back to the
  conversation. Never sweep "all my PRs" or "everything in /tmp".
- **Search before create.** No ticket creation without a recorded search that found no match.
- **Reaction on merged PRs only**, on the thread root, once.
- **Docs on a fresh branch** in its own worktree, never on the session's branch.
- **Dirty means keep.** Uncommitted or unpushed work survives unless the user names it.
- **Never force-push, never merge a PR** as part of closing.
