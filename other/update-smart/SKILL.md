---
name: update-smart
description: >-
  Use when Kosta invokes /update_smart or asks for a smart Hermes update.
  Performs the Mac Studio branch-first Hermes update workflow: audit local repos,
  create rollback branches, preserve and replay local git customizations, update
  Hermes/WebUI/non-Hermes sidecars carefully, run verification, and avoid
  restarting the live gateway from inside Telegram unless explicitly safe.
version: 0.1.2
author: Hermes Agent
license: MIT
targets: [hermes-default, hermes-gpt, claude-hermes]
metadata:
  hermes:
    command_priority: 450
    tags: [hermes, update, update-smart, local-git, maintenance]
---

# Smart Update

Use this skill for `/update_smart` or plain requests like “do a smart update,” “update Hermes smartly,” or “update using the local gits to put changes back.”

Important: this is **not** the built-in `/update` command. Built-in `/update` runs `hermes update --gateway`, which is useful for ordinary upstream updates but is too blunt for Kosta's local Mac Studio workflow. `/update_smart` means run an agent-led maintenance pass with local git preservation and verification.

## Scope

Default scope on Mac Studio:

- Hermes agent repo: `~/.hermes/hermes-agent`
- Hermes state repo: `~/.config/hermes-state`
- Skillshare canonical skills/allowlist: `~/.config/skillshare`
- hosted WebUI sidecar: `~/.hermes/hermes-webui`
- non-Hermes smart updater: `~/.hermes/profiles/gpt/scripts/non_hermes_update_audit.py`

Do not push remotes unless Kosta explicitly asks. Local commits are fine and preferred for preserving completed changes.

## Required workflow

1. Load `hermes-maintenance-and-distribution`, especially the smart local update reference.
2. Audit before touching anything:
   - current date/host/user
   - git branch, upstream, ahead/behind, status for the repos above
   - `hermes version` / `hermes update --check` when applicable
   - relevant LaunchAgent/LaunchDaemon status only if the update affects a service
3. Create rollback points before mutation:
   - timestamped backup branch in each touched git repo, e.g. `backup/pre-update-smart-YYYYMMDD-HHMMSS`
   - preserve meaningful uncommitted work by committing locally when it is real work, not by relying only on stash
4. Update Hermes using the branch-first local customization flow:
   - stay on the local customization branch, normally `local/studio-customizations`
   - fetch upstream/origin
   - merge upstream into the local branch deliberately; do not blindly reset local work to `origin/main`
   - resolve conflicts file-by-file, preserving intended local behavior
   - for large/risky merges, use the escalation gate below before finalizing conflict resolution
5. Reapply or preserve local behavior from git:
   - compare local branch changes against upstream with `git diff --name-status`, `git diff --stat`, and `git log --cherry-pick` / `git cherry -v`; do not rely on memory or a clean working tree as proof
   - classify every local-only commit or carried patch as `port`, `superseded`, `retire`, or `split`, with evidence from the diff or upstream replacement
   - keep carried local patches that are still needed
   - drop only patches that upstream clearly absorbed or made obsolete
   - run the smart merge gate scripts when a legacy/customization branch exists; if `commit-ledger.json`, `symbol-parity.json`, or `deleted-tests.json` contains unresolved items, do not finalize the update until each item is restored, explicitly retired, or documented as upstream-absorbed

## Large merge escalation gate

Trigger this gate before completing a merge when any condition is true: conflict files include `gateway/run.py`, `gateway/platforms/*`, `gateway/stream_consumer.py`, `agent/display.py`, `tools/approval.py`, `tools/terminal_tool.py`, profile config, Skillshare skills, or WebUI routing; a single file diff is >500 lines; total merge diff is >1500 lines; tests are deleted/rewritten; local commits touch the same files as upstream; or the merge changes Telegram/Discord visible behavior.

When triggered, split review into parallel subagents before committing:
- **Local-behavior preservation reviewer:** compare `git diff main...HEAD`, `git diff HEAD^..HEAD`, and the newest `backup/pre-*` branch for dropped local symbols/flows. Return exact file:function/line evidence and whether upstream absorbed, conflicted with, or lost each behavior.
- **Regression-test reviewer:** inspect changed surfaces and propose/add focused tests for user-visible local behavior, especially Telegram routing, compact HUD, context badges/buttons, update/restart safety, provider/media config, Mini App/API routes, and terminal/approval paths.
- **Runtime-verification reviewer:** identify the smallest commands, health probes, and live checks needed after the merge/restart. Include whether the live gateway is still running old code.

Verify subagent findings yourself before editing or claiming success. If a dropped behavior is real, either restore it with a test in the same update pass or explicitly report it as a deliberate removal with evidence. Do not let large merges finish with “tests pass” unless the sentinel tests cover the carried local behavior.

6. Install/rebuild/sync:
   - reinstall Hermes from the updated checkout as appropriate
   - sync skills through Skillshare, not manual profile copying, when skill distribution changed
   - update hosted WebUI via its sidecar path if needed
   - run the non-Hermes smart update audit if requested or relevant
7. Verify in layers:
   - syntax/compile checks for touched Python files
   - focused tests for changed behavior
   - `hermes version` and `hermes update --check` when safe; in Telegram, prefer direct `git fetch/status` for a pending-update check because the approval scanner may over-match harmless `hermes update --check` as gateway-disruptive. After a manual branch-first merge, clear stale profile update caches (`~/.hermes*/.update_check`, especially the active profile) before trusting `hermes version`; otherwise it may keep reporting the old behind count even when git is current.
   - service health endpoints for WebUI or other updated sidecars
   - after all tests/builds, run a final git cleanliness check for every touched repo; tests/builds can leave follow-up edits, so do not call the update clean from an earlier status check
   - if final validation produced legitimate durable fixes, commit them before the final report; otherwise explicitly report the dirty tree and why it is intentionally uncommitted
   - for “any updates pending?” reports, fetch first and include ahead/behind counts — a repo can be clean but still behind upstream again
   - when the update scope says “all,” include non-Hermes audit leftovers and PATH shadowing, not just Hermes repos; `xcodebuildmcp` may need both Homebrew and npm-global updates because the npm binary shadows the formula on Kosta’s PATH
   - `non_hermes_update_audit.py --help` is not a harmless help probe in the current sidecar; it runs the audit/update flow. If you need usage, inspect the script source instead of executing `--help`.
   - avoid claiming completion if the live process is still running old code and needs a safe restart
   - **post-restart miniapp/Telegram regression check** (catches dropped local customizations during clean-branch rebuild). Run after both gateways are back up:

     ```bash
     for ep in /api/model-info /api/session-usage /api/subscription-usage /api/subscription-providers \
               /api/processes /api/background-tasks /api/commands /miniapp/; do
       for port in 8642 8643; do
         code=$(curl -sS -m 3 -o /dev/null -w "%{http_code}" "http://127.0.0.1:$port$ep")
         [[ "$code" == "200" || "$code" == "401" ]] || echo "REGRESSION $port $ep -> $code"
       done
     done
     ```

     A 404 on any of those means a route was dropped during merge — re-port the handler and route registration from `backup/pre-*` to `gateway/platforms/api_server.py`. Historically dropped during clean-branch rebuilds: `_handle_subscription_providers`. Also verify `agent/display.py` still maps `"thinking": ("☁️", "Thinking")` in `render_compact_tool_progress` (the `("__compact__", "thinking")` event from `gateway/run.py:_emit_compact_thinking` renders that bucket as the thinking emoji in Telegram replies). Also confirm `~/.config/hermes-state/miniapp/index.html` still has the `savedSid` validation guard around `CS.getItem('hermes_sid')` so the Session ID field doesn't render as `[object Object]`.

     Telegram DM-topic post-update check: if `gateway/platforms/telegram.py` changed or conflicted, do not stop at API/miniapp checks. Run the focused Telegram topic suite and inspect that private/DM topic normal sends, stale-reply retries, and media retries keep `message_thread_id` rather than using `direct_messages_topic_id` or dropping topic kwargs. The failure mode is subtle: progress/tool HUD appears in the selected topic, but the final assistant output goes to `All` or disappears from the visible topic. See `references/telegram-dm-topic-regression-guard-2026-05-09.md` and `hermes__telegram-gateway/references/telegram-dm-topic-post-update-regression-2026-05-09.md`.
8. Gateway safety:
   - If the current conversation is arriving through Telegram/Discord/webhook, do not restart the gateway unless Kosta explicitly accepts the interruption.
   - It is okay to leave updated code on disk and say a safe restart is needed.
   - When Kosta has approved a restart from Telegram, schedule it with the terminal tool's native background mode plus a short `sleep`, not shell `&`; some tool environments reject foreground commands that self-background. Log the restart and run a follow-up health probe.

## Output style

Keep the report short. Say what changed, what was verified, and what still needs attention. Include backup branch names and exact failing check excerpts only if something failed.

End every successful or partially successful smart update with a compact change digest so Kosta can see the payoff without reading logs. Use plain-English buckets, 1-3 bullets each, and omit empty buckets:

- **New:** newly added commands, skills, features, sidecars, integrations, targets, or config surfaces.
- **Updated:** upstream versions pulled, dependency/tool versions changed, synced targets, refreshed prompts/skills/docs.
- **Fixed:** bugs, broken links/symlinks, stale configs, failing checks, drift, warnings resolved.
- **Still needs attention:** only real follow-ups, blockers, safe restarts, machines that could not be reached, or warnings intentionally left.

Keep the digest factual and evidence-backed. Do not pad it with every file touched; group related changes by user-visible effect. If nothing meaningful changed in a bucket, skip that bucket rather than saying “none.”

After the digest, always include a short **Claude hybrid restart prompt** when any Hermes surface is updated but not restarted. Keep it copy-pasteable, 1 short paragraph plus commands if useful, and tailor it to the exact surfaces touched. The prompt should ask Claude to restart all relevant Hermes surfaces safely, verify post-restart health, run the miniapp/API regression probe, and report live PIDs/ports. Do not include secrets. If no restart is needed, omit the prompt.

## Built-in `/update` comparison

If Kosta asks whether `/update` does this: answer no. `/update` currently spawns `hermes update --gateway`; it stashes local working tree changes, switches to `main`, pulls/resets from `origin/main`, then optionally restores the stash. That is not the same as Kosta's smart local-git workflow because it does not preserve the local customization branch as the primary branch, does not audit/replay local commits deliberately, and does not include WebUI/Skillshare/non-Hermes sidecar verification.

## Session references

- `references/post-smart-update-cleanliness-and-drift-check-2026-05-07.md` — final cleanliness/drift check lesson after a smart update: commit validation fallout before claiming clean, fetch before pending-update reports, and prefer direct git checks over `hermes update --check` inside Telegram when the approval scanner over-matches.
- `references/mac-studio-smart-update-all-2026-05-07.md` — all-scope Mac Studio update pass covering Hermes agent, Workspace, non-Hermes tools/apps, delayed gateway restart from Telegram, xcodebuildmcp dual-install shadowing, QLMarkdown direct app update, and final health checks.
