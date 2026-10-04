---
name: ship
description: End-to-end ship workflow — commit, push, deploy to Vercel, and save a project note. Runs after a build session to handle all the boring stuff.
argument-hint: [optional commit message]
user-invocable: true
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
---

# Ship It

Post-build skill that handles commit → push → deploy → notes in one shot. No more asking for each step.

## When to use

After finishing a build session — new feature, bug fix, new tool, client deliverable. Replaces the manual "ok commit this, push it, deploy it, remember it" sequence.

## Process

### Step 1: Assess what changed

Run `git status` and `git diff --stat` in the current project directory. Identify:
- Which files changed
- Whether this is a new project or update to existing
- Whether there are sensitive files (.env, credentials) — exclude those

If there are no changes, say so and stop.

### Step 2: Commit

- Stage relevant files (NOT node_modules, .env, .DS_Store, credentials)
- If the user provided a commit message in the argument, use it
- If not, write a concise commit message based on the diff (1-2 sentences, focus on "why")
- Append the commit attribution trailer the harness supplies (do not hardcode a model name)
- Commit. If pre-commit hook fails, fix and retry.

### Step 3: Push

- Check if branch tracks a remote. If not, push with `-u origin <branch>`
- Push to remote

### Step 4: Deploy to Vercel

Check if this is a Vercel project:
```bash
ls vercel.json .vercel/project.json 2>/dev/null
```

If yes:
- Run `vercel --prod` for production deploy (default)
- Wait for deploy to complete
- Report the URL

If no Vercel config exists, skip this step and mention it.

### Step 5: Save a project note

Keep a short record so the next session (yours or Claude's) knows what shipped. Use whichever the project already has, in this order:
- Claude Code auto-memory, if it is enabled in this session (the harness tells you the memory directory): update or create a `project_<name>.md` entry
- Otherwise `CLAUDE.md` in the project root: add or update a "Deployed" line with the URL and date
- Otherwise a `SHIPLOG.md` in the project root: append one line — date, commit hash, one-sentence summary, deploy URL

Record: what the project does (1-2 sentences), tech stack, deploy URL, date shipped.

### Step 6: Summary

Report:
```
Shipped:
- Commit: <hash> — <message>
- Push: <branch> → origin
- Deploy: <url> (or "skipped — no Vercel config")
- Note: <created/updated> <filename>
```

## Important

- Never commit .env files, API keys, or node_modules
- If `git status` shows nothing to commit, just say "nothing to ship" and stop
- Don't amend previous commits — always create new ones
- If deploy fails, still complete the other steps and report the error
- Keep commit messages concise — the diff tells the story
