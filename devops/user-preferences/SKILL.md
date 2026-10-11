---
name: user-preferences
description: User preferences — language and settings from preferences.json.
---

# User Preferences

## Read one file; never merge

```
.dev-team-agents/resolved/preferences.json      ← read THIS
```

It is the resolved view of three layers, written by `devteam bind` and `devteam sync`. Read it and
stop: no agent merges layers, and no agent reads a source layer to answer "what is the language?".

**Fallback, one level only:** if that file does not exist, the project is not bound (or predates
v3) — read `.dev-team-agents/user-data/preferences.json`, the v2 location. Nothing else.

The resolved file carries a `_generated_by` key naming the command that writes it. Editing it by
hand works until the next sync silently discards the edit, which is why writes go elsewhere.

## Write through a layer, never the projection

```
shipped defaults  ->  global user  ->  this project      (later layers win)
```

| Layer | Where | Set it with |
|-------|-------|-------------|
| Defaults | `<core version>/scripts/lib/preferences-defaults.json` | Not writable — it ships |
| Global user | `<data store>/preferences.json` | `devteam prefs set <key> <value>` |
| This project | `<data store>/projects/<project_id>/preferences.json` | `devteam prefs set <key> <value> --scope project` |

`devteam prefs list` shows every key with the layer it came from; `devteam prefs unset <key>` drops
it from a layer so the one below applies again. All three layers are **personal** and none is
committed — see `project.json` § `context_paths` in `skills/shared/project-context/SKILL.md` for the
topology that *is* committed, and why it is not a preference.

**Consent keys — `telemetry` and `auto_update` — resolve to `false` when no layer sets them.** The
shipped default is `true` because the installer prompts there; an absent value anywhere else means
the user never saw a prompt, and that reads as "no". `devteam prefs list` reports those as
`consent-withheld` rather than `defaults`, so the distinction is visible.

---

## Schema and Defaults

> **Canonical source:** `scripts/lib/preferences-defaults.json` is the single source of truth for the default schema. It is read by `install.sh` (on install/update) and by the `session-start.sh` health-check backfill, which fills any missing key on every session. The block below mirrors it — keep them in sync.

```json
{
  "language": "pt-BR",
  "context_window_percent_warning": 55,
  "context_window_percent_limit": 60,
  "suppress_notifications": false,
  "session_summary_max_days": 30,
  "session_summary_max_entries": 30,
  "docs_stale_after_days": 30,
  "auto_update": true,
  "update_check_interval_hours": 24,
  "model_max_tokens": 200000,
  "session_no_commit_turns": 8,
  "telemetry": true,
  "worktree_active": true,
  "worktree_base_branch": null,
  "worktree_commit_action": "ask",
  "auto_learn_before_commit": true,
  "worktree_path": ".worktrees",
  "worktree_docker_isolate": true,
  "qa_browser": null,
  "ci_cd_detected": null
}
```

**These defaults apply only to a preferences.json that does not exist yet.** An existing file is never rewritten: `install.sh` merges with existing values winning, and the `session-start.sh` backfill only adds absent keys.

**Consent keys — `telemetry` and `auto_update`.** Both default to `true` in a fresh file, where the installer prompts for them. They are **never** backfilled as `true` into a preferences.json that already exists: that file's owner never saw the prompt for a field added after they installed, so an absent key is read as "no". Both install and the session-start backfill write `false` in that case.

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `language` | string | `"pt-BR"` | Conversation language (BCP 47 tag). Docs remain English. |
| `context_window_percent_warning` | number | `55` | % at which agents emit a `warning` notification |
| `context_window_percent_limit` | number | `60` | % at which agents emit a `critical` notification |
| `suppress_notifications` | bool or array | `false` | `false` = none suppressed; `true` = all suppressed; `["info"]` = suppress by type |
| `session_summary_max_days` | number | `30` | Days before session-summary entries are trimmed |
| `session_summary_max_entries` | number | `30` | Maximum number of entries in session-summary.md |
| `docs_stale_after_days` | number | `30` | Days before project.md, session-summary.md, and the last health check are considered stale |
| `auto_update` | bool | `true` | Auto-update dev-team-agents when a new version is detected (consent key) |
| `update_check_interval_hours` | number | `24` | Hours between update checks |
| `model_max_tokens` | number | `200000` | Context window for the active model |
| `session_no_commit_turns` | number | `8` | Turns of work with a dirty tree and no commit before a one-time-per-session warning |
| `telemetry` | bool | `true` | Anonymous usage telemetry (opt out with `false`) (consent key) |
| `worktree_active` | bool | `true` | Default to a git worktree per task without asking |
| `worktree_base_branch` | string or null | `null` | Base branch for worktrees (`null` = auto-detect) |
| `worktree_commit_action` | string | `"ask"` | Default post-commit action in an active worktree: `ask`, `finalize`, `rebase`, or `commit-only` |
| `auto_learn_before_commit` | bool | `true` | Auto-run `/devteam:learn` before every commit (`false` = skip by default) |
| `worktree_path` | string | `".worktrees"` | Directory where worktrees are created |
| `worktree_docker_isolate` | bool | `true` | Isolated Docker Compose stack per worktree (when Docker present) |
| `qa_browser` | string or null | `null` | Browser the `qa-specialist` drives (`null` = ask on first use) |
| `ci_cd_detected` | bool or null | `null` | Cached GitHub Actions detection (`null` = unchecked) |

> For where each field is actually read and applied, see the "Consumed at" column in `CLAUDE-md/preferences.md` — the canonical consumer table, kept current whenever a field's wiring changes.

**Proposing a new value mid-session.** When the user repeatedly corrects the same behavior, `CLAUDE.md` § Correction Pattern Rule governs whether to propose persisting it here. That rule — not this file — owns the trigger (2+ corrections) and the confirmation step; this file only owns the schema the proposal must map to. Never write a field here without the `AskUserQuestion` confirmation that rule requires.

---

## Language Policy

Two distinct rules govern language in dev-team-agents:

| Output type | Language rule |
|-------------|--------------|
| Documents (ADRs, session-summary, plans, changelogs, code comments) | **Always English** — regardless of `preferences.json` |
| Conversation with the user (responses, questions, explanations, notifications) | **Use `language` from `preferences.json`** — fallback to English if absent or unreadable |

**How agents read the user's language:**

```bash
PREFS=".dev-team-agents/user-data/preferences.json"
USER_LANG="en"
if [ -f "$PREFS" ] && command -v python3 >/dev/null 2>&1; then
    USER_LANG=$(python3 -c \
        "import json; d=json.load(open('$PREFS')); print(d.get('language','en'))" \
        2>/dev/null || echo "en")
fi
```

For agents: read `.dev-team-agents/user-data/preferences.json` at the start of each session. Use the `language` value when writing any response directed at the user. If the file does not exist, use English.

---

## suppress_notifications Handling

| Value | Behavior |
|-------|---------|
| `false` | No suppression — all notifications shown |
| `true` | All notifications suppressed |
| `["info"]` | Only `info` type suppressed |
| `["warning", "critical"]` | `warning` and `critical` suppressed |

Any unrecognized value → treat as `false` (no suppression). Never fail — graceful degradation only.

---

## Missing File Behavior

If `preferences.json` does not exist:
- Use English as the conversation language
- Use all schema defaults for thresholds and intervals
- Emit a `warning` notification at session start prompting the user to run setup-assistant

If a specific field is missing from the file (partial schema), use its default value.

---

## Reading Individual Fields (shell)

```bash
_pref() {
    local field="$1" default="$2"
    python3 -c \
        "import json,sys; d=json.load(open('.dev-team-agents/user-data/preferences.json')); \
         print(d.get('$field', $default))" 2>/dev/null || echo "$default"
}

LANG=$(_pref language '"en"')
WARN_PCT=$(_pref context_window_percent_warning 55)
LIMIT_PCT=$(_pref context_window_percent_limit 60)
SUPPRESS=$(_pref suppress_notifications false)
STALE_DAYS=$(_pref docs_stale_after_days 30)
AUTO_UPDATE=$(_pref auto_update false)
CHECK_HOURS=$(_pref update_check_interval_hours 24)
```
