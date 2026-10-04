---
name: setup-channel-routine
description: "Create or update the daily CLOUD routine (scheduled Claude Code agent) that runs a content-factory channel's growth agent on a cron schedule. Reusable across channels — LinkedIn, X, Instagram Reels, and any future channel. Bakes in the canonical config (environment, the FORK repo the routine clones, allowed tools, no MCP connectors, push notifications, commit+PR after the run) and the per-channel prompt template, so every channel's routine is set up identically. Use when the user says /setup-channel-routine, 'set up the routine for X', 'schedule the <channel> agent', 'create a daily runner for <channel>', or 'make a routine like LinkedIn for <channel>'. Always trigger this skill for channel routine setup."
trigger: /setup-channel-routine
---

# /setup-channel-routine

Stands up (or updates) the **daily cloud routine** for a content-factory channel — a scheduled Claude Code agent that runs in Anthropic's cloud, clones the repo, runs the channel's growth-agent skill, commits, and opens a PR. One reusable recipe so every channel's routine matches the LinkedIn original.

**Argument:** the channel — `linkedin` | `x` | `instagram` (default: ask if missing).

---

## Critical context: the fork the routine clones

Cloud routines do **not** read your local working copy. They clone **`altaf-shaikh-cs/content-factory`** — the FORK, which is the single integration point and the source of truth. A routine runs whatever is on the **fork's `main`**. The personal repo `altafshaikh/content-factory` (your local `origin`) is just a downstream mirror.

So before creating a routine, the channel's skill files MUST already be on the fork:
1. Commit the channel skill + folder locally.
2. Deploy to the fork: `bash scripts/deploy-code.sh`.

If the channel skill isn't on the fork, the routine will fail or run stale. **Always verify deployment** (see Step 4).

---

## Canonical routine config (identical for every channel)

| Field | Value |
|-------|-------|
| `environment_id` | `env_01Vofgnx2PoR7qURGVMb4HcN` (personal) |
| source repo (cloned) | `https://github.com/altaf-shaikh-cs/content-factory` (the FORK) |
| `allowed_tools` | `["Bash","Read","Write","Edit","Glob","Grep","WebFetch","WebSearch"]` |
| `mcp_connections` | **none** — clear them after create (the API auto-attaches all connected ones) |
| notifications | push on (the API default) |
| `enabled` | `true` |
| schedule | per-channel cron below, in **UTC** (user TZ is Asia/Calcutta = UTC+5:30) |

---

## Channel registry (agent + default schedule)

Schedules are staggered so the daily runs don't collide.

| Channel | Growth-agent invocation | Default time (IST) | Cron (UTC) |
|---------|-------------------------|--------------------|------------|
| `linkedin` | `/linkedin-growth-agent with N=3` | 8:30 PM | `0 15 * * *` |
| `instagram` | `/instagram-reels-agent` | 9:00 PM | `30 15 * * *` |
| `x` | `/x-growth-agent` | 10:00 AM | `30 4 * * *` |

If the user names a different time, convert IST → UTC (subtract 5:30) and **confirm the conversion** before creating.

### Non-channel routine: Factory Health

Not a channel and it produces no content, but it uses the same config block, so it is set up here.

| Routine | Invocation | Default time (IST) | Cron (UTC) |
|---------|-----------|--------------------|------------|
| `health` | `/factory-health` | Mondays 9:00 AM | `30 3 * * 1` |

Its prompt is **not** the channel template above. Use this instead:

```
Run /factory-health.

You are the weekly health check for a multi-channel content factory. Follow .claude/skills/factory-health/SKILL.md exactly. You are READ-ONLY: do not generate content, do not write to raw-ideas/ or any channel folder, do not create a branch, do not open a PR, do not push anything.

Read the run logs in ./runs/, the open PR list on this fork (gh pr list --state open), and the LinkedIn unshipped register, then report which channels are dark, starved, or gated, which PRs are stuck in review, and the single highest-leverage next action. Your report is delivered as a push notification, so the first two lines have to carry the verdict on their own.
```

Because it is read-only and pushes nothing, this routine is safe to run as often as the user wants. Weekly is the default so it stays a signal rather than noise.

---

## Prompt template (per run)

The cloud agent starts with zero context, so the prompt must be self-contained. The routine clones the fork (which is current — it's the source of truth), so no self-sync step is needed. The final block opens a **within-fork PR** for review, which works because the cloud's `gh` owns the fork.

```
Run <AGENT INVOCATION>.

<one-paragraph channel summary: what this channel does and where it writes — pull it from the channel's CLAUDE.md so the cloud agent has context>. Follow .claude/skills/<channel-skill>/SKILL.md and ./<channel-folder>/CLAUDE.md exactly. ./raw-ideas/ is immutable — never move, rename, or delete files there. Only write inside ./<channel-folder>/; cross-channel reads are read-only. Update the channel's TODO.md.

This repo IS the fork and the integration point. Before generating, run `gh pr list --state open --json headRefName` to see which ideas already have content in flight. Use the skill to select the single best next item to produce, and derive a STABLE kebab slug for it from its source raw-idea (NOT today's date), so the same idea always maps to the same branch: claude/<channel>-<slug>.

If that branch already has an open PR, or the skill determines there is nothing new worth producing, or a gate in the skill blocks the run, then STOP — do not create a branch or PR. Write the run-log row (see below) and report that there was nothing new. Otherwise:
1. git checkout -b claude/<channel>-<slug>
2. Stage and commit only the new/changed files with a clear message. Include the run-log row for this run (see below) in this same commit.
3. Push the branch to origin (the fork): git push -u origin claude/<channel>-<slug>
4. Open a pull request into the fork's own main for review:
     gh pr create --base main --head claude/<channel>-<slug> \
       --title "content: <channel> — <slug>" \
       --body "Routine-generated <channel> content. Review and merge into the fork's main; the personal mirror syncs automatically."
This is a same-repo PR on the fork, which your gh account owns, so it succeeds. Do NOT touch the personal upstream.

HEARTBEAT — do this on EVERY run, including runs that produce nothing. It is the last thing you do. Append exactly one row to ./runs/<channel>.md following the contract in runs/README.md:
  | <YYYY-MM-DD UTC> | <produced|skipped|blocked|error> | <one short line why> | <link to output or —> |
If you opened a PR, that row is already in the branch (step 2) and there is nothing more to do. If you did NOT open a PR, commit that single file on its own and push it straight to main:
  git add runs/<channel>.md
  git commit -m "runs: <channel> <YYYY-MM-DD> <outcome>"
  git pull --rebase origin main && git push origin main
This single-line append is the ONLY thing you may ever push to main directly, and the commit must contain no other file. If that push fails, say so and finish anyway.
A quiet exit and a routine that never fired look identical from outside; two channels went dark for seven weeks under exactly that cover. A `skipped` row is a healthy result. A missing row is not.
```

## Sync model (fork `main` = single source of truth)

The **fork** is the integration point; the personal repo is a downstream mirror. Three parts:

- **Content (routine → fork PR):** the routine picks the next item, derives a stable idea slug, and — only if no open PR already covers it and there's something new worth producing — pushes `claude/<channel>-<slug>` to the fork and opens a **within-fork PR** into the fork's own `main`. Idempotent across days: an in-flight idea won't be duplicated. The cloud's `gh` owns the fork, so this same-repo PR succeeds (a cross-repo PR to the personal upstream would NOT — the work account isn't a collaborator there).
- **Code (local → fork):** `bash scripts/deploy-code.sh` pushes committed local changes to the fork's `main`. Never `git push origin main` (diverges the mirror).
- **Mirror (fork → personal):** `bash scripts/mirror-personal.sh` fast-forwards personal `main` from the fork. Runs daily at 11:00 AM via launchd; safe to run by hand.

Because personal `main` is only ever a fast-forward of the fork, the mirror never conflicts. The routine always clones current code because the fork is the source of truth.

---

## Procedure

1. **Resolve the channel** from the argument. If absent, ask which channel. Look it up in the registry for the agent invocation, default cron, and folder.
2. **Load the API tool:** `ToolSearch` with `select:RemoteTrigger`. (Auth is in-process — never use curl.)
3. **Check for an existing routine:** `RemoteTrigger {action:"list"}`. If one already exists for this channel (match by name, e.g. "Daily X Post Creator"), ask whether to **update** it (`action:"update"`, partial body) instead of creating a duplicate.
4. **Verify the channel skill is deployed to the fork** (so the routine won't run stale):
   - Confirm the channel's `SKILL.md` + folder are committed locally.
   - `gh api repos/altaf-shaikh-cs/content-factory/contents --jq '.[].name'` and check the channel folder is present on the fork. If not, run `bash scripts/deploy-code.sh` first.
5. **Build the create body** (generate a fresh lowercase v4 UUID for `events[].data.uuid`):
   ```json
   {
     "name": "Daily <Channel> <Post|Reel> Creator",
     "cron_expression": "<cron from registry or user>",
     "enabled": true,
     "job_config": { "ccr": {
       "environment_id": "env_01Vofgnx2PoR7qURGVMb4HcN",
       "session_context": {
         "sources": [{"git_repository": {"url": "https://github.com/altaf-shaikh-cs/content-factory"}}],
         "allowed_tools": ["Bash","Read","Write","Edit","Glob","Grep","WebFetch","WebSearch"]
       },
       "events": [{"data": {
         "uuid": "<fresh uuid>", "session_id": "", "type": "user", "parent_tool_use_id": null,
         "message": {"role": "user", "content": "<filled prompt template>"}
       }}]
     }}
   }
   ```
6. **Create:** `RemoteTrigger {action:"create", body:<above>}`.
7. **Strip auto-attached connectors:** the create response usually lists every connected MCP connector. Immediately `RemoteTrigger {action:"update", trigger_id:"<id>", body:{"clear_mcp_connections": true}}` so the routine matches the others (no connectors).
8. **Report:** print the routine id, the human-readable schedule (IST + UTC), `next_run_at`, and the management URL `https://claude.ai/code/routines/<id>`.
9. **Offer a test run:** ask whether to `RemoteTrigger {action:"run", trigger_id:"<id>"}` now to validate end-to-end before the first scheduled fire.

---

## Notes

- Routines can be listed/updated/run but **not deleted** here — to delete, direct the user to https://claude.ai/code/routines.
- Min cron interval is 1 hour.
- Keep schedules staggered; check the existing routines' times before picking a new one.
- This skill only configures the cloud routine. The channel's generation logic lives in its own growth-agent skill — this skill just schedules it.
- After ANY repo change that the routine depends on, re-deploy: commit locally, then `bash scripts/deploy-code.sh` (pushes to the fork). The personal mirror follows via `scripts/mirror-personal.sh`.
