---
name: notifier
description: Dev Team Agents notifications — hooks queue them, the desktop app shows them.
---

# Dev Team Agents Notifier

## How a notification reaches the user

```
hook ──devteam_notify──▶ <state-dir>/notifications.jsonl ──devteam notifications watch──▶ desktop app ──▶ native notification + bell
```

- **Hooks raise them; agents do not.** A hook appends one record through `scripts/hooks/lib/notify.sh`. The desktop app streams the queue and shows each record as an OS notification titled with the project's name (ADR-0017).
- **Never print a `DEV TEAM AGENTS` box.** Hook stdout never reached the user — `SessionStart` stdout is model context, `Stop` stdout is not shown — and a box in an agent's reply is noise the hook already covers. The format is retired.
- The `[DEVTEAM:*]` markers a hook prints (`FIRST_TIME_SETUP`, `SESSION_BANNER`, `SYMLINK_BROKEN`, `TEST_SCOPE_RULE`) are **instructions to you**, not notifications. Act on them as their own rules say.

## Levels

| Level | Use for |
|-------|---------|
| `info` | Tips, suggestions, an update available or applied, a pending `devteam upgrade`, work without a commit |
| `warning` | Context approaching its limit, stale docs or health check |
| `critical` | Context at or past its limit, broken links (the dev-team is not loaded) |

`critical` stays on screen until dismissed where the OS allows it. The banner's title is the project's name alone — no level prefix; a backlog summary that holds a `critical` record leads its body with that record's message. Every message is rendered in the user's `language` (`en`, `pt-BR`, `es`; others fall back to English).

## What raises what

| Code | Level | Raised by | Once per |
|------|-------|-----------|----------|
| `update.available` / `update.applied` | info | `session-start.sh` (update check) | version pair |
| `symlinks.broken` | critical | `session-start.sh` | day |
| `docs.project_stale`, `docs.session_summary_stale` | warning | `session-start.sh` | day |
| `health_check.stale`, `health_check.never` | warning | `session-start.sh` | day |
| `layout.upgrade_available` | info | `session-start.sh` | day |
| `context.warning`, `context.critical` | warning / critical | `stop/04-notifier.sh` | session (expires after 2 h) |
| `session.uncommitted` | info | `stop/04-notifier.sh` | session |
| `tip.daily` | info | `stop/04-notifier.sh` | day |
| `tasks.session_done` | info | `post-tool-use/01-task-board.sh`, `pre-tool-use/04-task-board.sh`, `stop/04b-task-board.sh` (a review pass releasing the last task) | session |
| `tasks.review_findings` | warning | `post-tool-use/01-task-board.sh` (agent result), `stop/04b-task-board.sh` (command/prompt review) | review window |
| `tasks.pr_created` | info | `stop/04b-task-board.sh` | PR/MR |
| `tasks.session_abandoned` | warning | `session-end.sh` | session |

The four `tasks.*` messages name the session by its provider title, quoted and cut to 15 characters (`Sessão "Notificações do…": …`), or by the first 8 characters of its id when it has no title. `tasks.pr_created` also names the PR/MR number (e.g. `#123` for GitHub, `!456` for GitLab). Where each provider keeps the title: `docs/providers.md`.

Thresholds come from preferences: `context_window_percent_warning`, `context_window_percent_limit`, `model_max_tokens`, `session_no_commit_turns`, `docs_stale_after_days`. Messages are rendered by the hook in `language`.

## Suppression

`suppress_notifications` in the resolved preferences, applied by `notify.sh` before anything is queued:

| Value | Behavior |
|-------|---------|
| `false` | Queue all |
| `true` | Queue none |
| `["info"]` | Skip only the listed levels |

One exception: `update.available` ignores the level list and is skipped only by `true` — with `auto_update` off it is the one way a user learns a fix shipped.

The app's own **Pause** only silences banners for that app session; paused notices still land in the bell.

## Raising a new one (hook authors)

```bash
. "${SCRIPT_DIR}/lib/notify.sh"
devteam_notify_init "$MAIN_REPO_ROOT" "$STATE_DIR" "$SUPPRESS" "$SESSION_ID"
devteam_notify warning my.code "$(devteam_msg "$USER_LANG" "English text." "Texto em português." "Texto en español.")" 86400 "my.code:$(date +%Y-%m-%d)"
```

- Render every message with `devteam_msg <lang> <en> <pt-BR> <es>` from `notify.sh` — the one language switch; never write a local copy.

- Pick a stable `code` — clients switch on it; the message may change.
- Always pass a dedupe key: a notice raised on every turn is a notification per turn.
- Pass a TTL for anything tied to a moment (context, a session); `0` only for what stays true until acted on.
- Keep the Stop path python-free unless the check cannot be done without it.

Full reference: `CLAUDE-md/notifications.md`.

## Context window — what an agent does

Nothing to emit: `stop/04-notifier.sh` measures the real context size from the transcript every turn. If the user asks, or you judge the conversation is degrading, say so plainly in your reply and suggest `/compact` or a new session.
