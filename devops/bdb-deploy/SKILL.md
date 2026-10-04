---
name: bdb-deploy
description: Use when the user wants to build and deploy a project to a real server via rsync over SSH — "deploy this", "push the build live", "sync to production". Not for git push/PR workflows, and not a replacement for a real CI pipeline; this is the direct-deploy path.
category: bdb-core
risk: caution
---

# bdb-deploy

A thin wrapper around the real `bdb-deploy` CLI (`bin/bdb-deploy.mjs` in this package). **This skill does not construct rsync/ssh commands itself.** The CLI does that deterministically; the skill's job is knowing when and how to invoke it, and reading its output correctly.

## Why this exists

Freehand rsync/ssh commands written by an LLM in the moment are a real risk once they touch a production web root or hold an SSH key path: a wrong flag, a missing trailing slash on an rsync source (changes whether the *contents* or the *directory itself* gets copied), or a mistyped remote path can silently corrupt or wipe a live deployment. The CLI encodes the correct, tested behavior once; this skill just knows how to call it.

## Before running anything

1. Check for `bdb-deploy.json` in the project root. If it doesn't exist, this project isn't set up yet — see "First-time setup" below.
2. If it exists, read it to see what targets are configured (`bdb-deploy.json` has no secrets in it, safe to read directly). Note which targets are `"production": true`.

## First-time setup (no bdb-deploy.json yet)

Run `bdb-deploy init` **interactively** — it asks the user for host, SSH user, key path, remote directory, etc. Do not pre-fill these from guesses; if you don't know the real values (host, remote path, which SSH key), ask the user rather than inventing plausible-sounding ones. A wrong host or path here means the *next* command genuinely deploys somewhere unintended.

## Running a deploy

**Always dry-run first** unless the user explicitly says to skip it:

```
bdb-deploy --target <name> --dry-run
```

Read the dry-run output. It shows the exact build command, the exact rsync source/destination, and the exact remote restart command (if configured) — none of it executes in dry-run mode. Confirm this matches what the user actually wants before proceeding.

Then the real run:

```
bdb-deploy --target <name>
```

If the target is marked `"production": true`, the CLI itself will prompt for confirmation (typing the target name) unless `--yes` is passed. **Do not pass `--yes` on a production target on the user's behalf** unless they've explicitly said to skip confirmation for this specific run — that confirmation prompt exists precisely so a human is in the loop for the highest-consequence targets.

## Reading the result

- The CLI prints a SHA-256 hash + file count of the build output before rsyncing — this is what actually got deployed, useful for later verifying "did version X really go out."
- If a `healthcheckUrl` is configured, the CLI GETs it after deploy and fails loudly (non-zero exit) if it doesn't respond OK. Trust this over assuming the deploy worked just because rsync didn't error — a successful file copy to the wrong path still "succeeds" at the rsync level.
- If the CLI reports a config error (missing env var, missing required field), don't try to work around it by hand-running rsync instead. Fix the config or `.env`, then re-run through the CLI.

## What this is not

- Not a CI/CD pipeline. This is the direct, manual (or agent-triggered) deploy path for when no CI runner exists yet. If the project has real CI (a `.forgejo/workflows/` or `.github/workflows/` that already builds and deploys on push), prefer that — don't bypass it with a manual `bdb-deploy` run unless the user asks to.
- Not scoped to BDB infrastructure. `bdb-deploy.json` and `.env` are per-project and per-machine; this tool makes no assumption about which host, user, or path a project deploys to.
